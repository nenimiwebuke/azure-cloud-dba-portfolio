"""
PySpark schemas for Northstar Benefits datasets.

These definitions translate the documented Markdown data contracts in
docs/data-contracts/ into machine-enforceable schemas.
"""

from __future__ import annotations

from pyspark.sql.types import (
    DateType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


EMPLOYEE_SCHEMA = StructType(
    [
        StructField("employee_id", StringType(), nullable=True),
        StructField("employer_id", StringType(), nullable=True),
        StructField("first_name", StringType(), nullable=True),
        StructField("last_name", StringType(), nullable=True),
        StructField("date_of_birth", DateType(), nullable=True),
        StructField("hire_date", DateType(), nullable=True),
        StructField("termination_date", DateType(), nullable=True),
        StructField("employment_status", StringType(), nullable=True),
        StructField("department", StringType(), nullable=True),
        StructField("state", StringType(), nullable=True),
    ]
)

DEPENDENT_SCHEMA = StructType(
    [
        StructField("dependent_id", StringType(), nullable=True),
        StructField("employee_id", StringType(), nullable=True),
        StructField("first_name", StringType(), nullable=True),
        StructField("last_name", StringType(), nullable=True),
        StructField("relationship", StringType(), nullable=True),
        StructField("date_of_birth", DateType(), nullable=True),
        StructField("gender", StringType(), nullable=True),
        StructField("dependent_status", StringType(), nullable=True),
    ]
)

ENROLLMENT_SCHEMA = StructType(
    [
        StructField("enrollment_id", StringType(), nullable=True),
        StructField("employer_id", StringType(), nullable=True),
        StructField("employee_id", StringType(), nullable=True),
        StructField("dependent_id", StringType(), nullable=True),
        StructField("plan_id", StringType(), nullable=True),
        StructField("coverage_start_date", DateType(), nullable=True),
        StructField("coverage_end_date", DateType(), nullable=True),
        StructField("enrollment_status", StringType(), nullable=True),
        StructField("source_file_name", StringType(), nullable=True),
        StructField("source_received_timestamp", TimestampType(), nullable=True),
    ]
)

ELIGIBILITY_SCHEMA = StructType(
    [
        StructField("eligibility_id", StringType(), nullable=True),
        StructField("employee_id", StringType(), nullable=True),
        StructField("dependent_id", StringType(), nullable=True),
        StructField("plan_id", StringType(), nullable=True),
        StructField("eligibility_start_date", DateType(), nullable=True),
        StructField("eligibility_end_date", DateType(), nullable=True),
        StructField("eligibility_status", StringType(), nullable=True),
        StructField("approval_timestamp", TimestampType(), nullable=True),
        StructField("source_system", StringType(), nullable=True),
    ]
)
