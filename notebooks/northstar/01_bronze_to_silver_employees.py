# Databricks notebook source
"""
Northstar Benefits Group
Bronze-to-Silver Employee Processing

Purpose
-------
Read the raw employee CSV deposited by Azure Data Factory in ADLS Bronze,
enforce the Employee Data Contract, preserve rejected records in quarantine,
and write valid employee records to a governed Silver Delta dataset.

The notebook is intentionally deterministic and parameterized so the same
batch can be replayed safely.
"""

# COMMAND ----------

from __future__ import annotations

import sys
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# Databricks Repos normally adds the repository root to sys.path. This fallback
# also supports execution from other working directories.
for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "notebooks" / "common").exists():
        repository_root = str(candidate)
        if repository_root not in sys.path:
            sys.path.insert(0, repository_root)
        break

from notebooks.common.audit import add_audit_columns
from notebooks.common.contracts import EMPLOYEE_SCHEMA
from notebooks.common.metrics import print_summary
from notebooks.common.paths import PATHS
from notebooks.common.validation import (
    add_employee_validation_errors,
    split_valid_and_quarantine,
)

# COMMAND ----------

# Runtime parameters make the notebook reusable for later business dates.

dbutils.widgets.text("business_date", "2026-07-01")
dbutils.widgets.text("batch_id", "northstar-employees-20260701")
dbutils.widgets.text("source_system", "Employer HR Systems")
dbutils.widgets.dropdown("write_mode", "overwrite", ["overwrite", "append"])

BUSINESS_DATE = dbutils.widgets.get("business_date")
BATCH_ID = dbutils.widgets.get("batch_id")
SOURCE_SYSTEM = dbutils.widgets.get("source_system")
WRITE_MODE = dbutils.widgets.get("write_mode")

SOURCE_PATH = PATHS.employees_bronze
SILVER_PATH = PATHS.employees_silver
QUARANTINE_PATH = PATHS.employees_quarantine

print(f"Business date:     {BUSINESS_DATE}")
print(f"Batch ID:          {BATCH_ID}")
print(f"Source path:       {SOURCE_PATH}")
print(f"Silver path:       {SILVER_PATH}")
print(f"Quarantine path:   {QUARANTINE_PATH}")
print(f"Write mode:        {WRITE_MODE}")

# COMMAND ----------

def read_bronze_employees(path: str) -> DataFrame:
    """
    Read the immutable Bronze employee file using an explicit schema.

    PERMISSIVE mode preserves malformed rows rather than silently discarding
    them. The corrupt-record column can be routed to quarantine.
    """

    return (
        spark.read.format("csv")
        .schema(EMPLOYEE_SCHEMA)
        .option("header", "true")
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .option("dateFormat", "yyyy-MM-dd")
        .load(path)
    )


bronze_df = read_bronze_employees(SOURCE_PATH)

records_read = bronze_df.count()

print(f"Bronze employee records read: {records_read:,}")

# COMMAND ----------

# Normalize text without changing the raw Bronze source.

normalized_df = (
    bronze_df
    .withColumn("employee_id", F.upper(F.trim(F.col("employee_id"))))
    .withColumn("employer_id", F.upper(F.trim(F.col("employer_id"))))
    .withColumn("first_name", F.initcap(F.trim(F.col("first_name"))))
    .withColumn("last_name", F.initcap(F.trim(F.col("last_name"))))
    .withColumn(
        "employment_status",
        F.initcap(F.trim(F.col("employment_status"))),
    )
    .withColumn("department", F.trim(F.col("department")))
    .withColumn("state", F.upper(F.trim(F.col("state"))))
)

# COMMAND ----------

validated_df = add_employee_validation_errors(
    normalized_df,
    as_of_date=BUSINESS_DATE,
)

valid_df, quarantine_df = split_valid_and_quarantine(validated_df)

# Cache because both DataFrames are counted and written.
valid_df = valid_df.cache()
quarantine_df = quarantine_df.cache()

valid_count = valid_df.count()
quarantine_count = quarantine_df.count()

if records_read != valid_count + quarantine_count:
    raise RuntimeError(
        "Record reconciliation failed: "
        f"read={records_read:,}, "
        f"valid={valid_count:,}, "
        f"quarantine={quarantine_count:,}"
    )

# COMMAND ----------

silver_df = (
    add_audit_columns(
        valid_df,
        batch_id=BATCH_ID,
        source_system=SOURCE_SYSTEM,
    )
    .withColumn(
        "employee_age",
        F.floor(
            F.months_between(
                F.to_date(F.lit(BUSINESS_DATE)),
                F.col("date_of_birth"),
            )
            / 12
        ),
    )
    .withColumn(
        "years_of_service",
        F.round(
            F.months_between(
                F.to_date(F.lit(BUSINESS_DATE)),
                F.col("hire_date"),
            )
            / 12,
            2,
        ),
    )
    .withColumn(
        "coverage_eligible_as_of_date",
        (
            (F.col("employment_status") == "Active")
            & (F.col("hire_date") <= F.to_date(F.lit(BUSINESS_DATE)))
        ),
    )
)

quarantine_output_df = (
    add_audit_columns(
        quarantine_df,
        batch_id=BATCH_ID,
        source_system=SOURCE_SYSTEM,
    )
    .withColumn("quarantine_timestamp", F.current_timestamp())
    .withColumn("quarantine_domain", F.lit("employees"))
)

# COMMAND ----------

# Valid employee data is stored as Delta in Silver.

(
    silver_df.write.format("delta")
    .mode(WRITE_MODE)
    .option("overwriteSchema", "true")
    .partitionBy("employer_id")
    .save(SILVER_PATH)
)

# Rejected records are preserved separately for investigation and remediation.

(
    quarantine_output_df.write.format("delta")
    .mode(WRITE_MODE)
    .option("overwriteSchema", "true")
    .save(QUARANTINE_PATH)
)

# COMMAND ----------

print_summary(
    records_read=records_read,
    records_written=valid_count,
    rejected_records=quarantine_count,
)

print("\nVALIDATION FAILURE COUNTS")

(
    quarantine_output_df
    .select(F.explode("validation_errors").alias("validation_error"))
    .groupBy("validation_error")
    .count()
    .orderBy(F.desc("count"), "validation_error")
    .show(truncate=False)
)

# COMMAND ----------

# Final assertions make failures visible to orchestration and CI/CD.

silver_written_count = spark.read.format("delta").load(SILVER_PATH).count()
quarantine_written_count = (
    spark.read.format("delta").load(QUARANTINE_PATH).count()
)

if silver_written_count != valid_count:
    raise RuntimeError(
        "Silver write validation failed: "
        f"expected={valid_count:,}, actual={silver_written_count:,}"
    )

if quarantine_written_count != quarantine_count:
    raise RuntimeError(
        "Quarantine write validation failed: "
        f"expected={quarantine_count:,}, "
        f"actual={quarantine_written_count:,}"
    )

print("\nEmployee Bronze-to-Silver processing completed successfully.")
print(f"Silver rows:      {silver_written_count:,}")
print(f"Quarantine rows:  {quarantine_written_count:,}")

valid_df.unpersist()
quarantine_df.unpersist()
