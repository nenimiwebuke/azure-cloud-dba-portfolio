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
batch can be replayed safely. It draws its schema, validation rules, and
paths from notebooks/config/northstar/, so the same shape of notebook can
be reused for a future business case by swapping the config import.
"""

# COMMAND ----------

from __future__ import annotations

import sys
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructField, StructType

# Databricks Repos normally adds the repository root to sys.path. This fallback
# also supports execution from other working directories.
for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "notebooks" / "common").exists():
        repository_root = str(candidate)
        if repository_root not in sys.path:
            sys.path.insert(0, repository_root)
        break

from notebooks.common.audit import add_audit_columns
from notebooks.common.metrics import (
    calculate_data_quality_score,
    create_pipeline_metric_df,
    print_summary,
)
from notebooks.common.validation import (
    apply_validation_rules,
    split_valid_and_quarantine,
)
from notebooks.config.northstar.paths import PATHS
from notebooks.config.northstar.schemas import EMPLOYEE_SCHEMA
from notebooks.config.northstar.validation_rules import (
    build_employee_validation_rules,
)

# COMMAND ----------

# Runtime parameters make the notebook reusable for later business dates
# and later bronze file drops.

dbutils.widgets.text("business_date", "2026-07-01")
dbutils.widgets.text("batch_id", "northstar-employees-20260701")
dbutils.widgets.text("source_system", "Employer HR Systems")
dbutils.widgets.text("bronze_filename", "employees_20260701.csv")
dbutils.widgets.dropdown("write_mode", "overwrite", ["overwrite", "append"])

BUSINESS_DATE = dbutils.widgets.get("business_date")
BATCH_ID = dbutils.widgets.get("batch_id")
SOURCE_SYSTEM = dbutils.widgets.get("source_system")
BRONZE_FILENAME = dbutils.widgets.get("bronze_filename")
WRITE_MODE = dbutils.widgets.get("write_mode")

PIPELINE_NAME = "northstar_bronze_to_silver_employees"
NOTEBOOK_VERSION = "1.1.0"

SOURCE_PATH = PATHS.bronze_file("employees", BRONZE_FILENAME)
SILVER_PATH = PATHS.silver_path("employees")
QUARANTINE_PATH = PATHS.quarantine_path("employees")
METRICS_PATH = PATHS.gold_path("data_quality_metrics")

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

    bronze_schema = StructType(
        [
            field
            for field in EMPLOYEE_SCHEMA.fields
            if field.name != "_corrupt_record"
        ]
        + [
            StructField("_corrupt_record", StringType(), nullable=True)
        ]
    )

    return (
        spark.read.format("csv")
        .schema(bronze_schema)
        .option("header", "true")
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .option("dateFormat", "yyyy-MM-dd")
        .load(path)
        .select(
            "*",
            F.col("_metadata.file_path").alias("_source_file_path"),
        )
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

# DBTITLE 1,Cell 6
validated_df = (
    apply_validation_rules(
        normalized_df,
        build_employee_validation_rules(as_of_date=BUSINESS_DATE),
    )
    .withColumn(
        "validation_errors",
        F.when(
            F.col("_corrupt_record").isNotNull(),
            F.array_union(
                F.col("validation_errors"),
                F.array(F.lit("MALFORMED_SOURCE_RECORD")),
            ),
        ).otherwise(F.col("validation_errors")),
    )
    .withColumn(
        "is_valid",
        F.size(F.col("validation_errors")) == 0,
    )
)

valid_df, quarantine_df = split_valid_and_quarantine(validated_df)

# Cache because both DataFrames are counted and written.
#valid_df = valid_df.cache()
#quarantine_df = quarantine_df.cache()

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

data_quality_score = calculate_data_quality_score(
    records_read,
    quarantine_count,
)

print_summary(
    records_read=records_read,
    records_written=valid_count,
    rejected_records=quarantine_count,
    data_quality_score=data_quality_score,
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

metric_df = create_pipeline_metric_df(
    spark,
    pipeline_name=PIPELINE_NAME,
    notebook_version=NOTEBOOK_VERSION,
    batch_id=BATCH_ID,
    business_date=BUSINESS_DATE,
    source_system=SOURCE_SYSTEM,
    source_path=SOURCE_PATH,
    target_path=SILVER_PATH,
    records_read=records_read,
    records_written=silver_written_count,
    records_rejected=quarantine_written_count,
    run_status="SUCCEEDED",
)

(
    metric_df.write.format("delta")
    .mode("append")
    .save(METRICS_PATH)
)

print("\nEmployee Bronze-to-Silver processing completed successfully.")
print(f"Notebook version: {NOTEBOOK_VERSION}")
print(f"Silver rows:      {silver_written_count:,}")
print(f"Quarantine rows:  {quarantine_written_count:,}")
print(f"Quality score:    {data_quality_score:.2f}%")
print(f"Metrics path:     {METRICS_PATH}")

# DataFrames are not cached on Serverless compute, so no unpersist is required.
