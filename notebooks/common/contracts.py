"""
PySpark schemas and data-contract constants for Northstar datasets.

These definitions translate the documented Markdown data contracts into
machine-enforceable schemas and accepted-value rules.
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


VALID_EMPLOYMENT_STATUSES = ("Active", "Terminated")

VALID_DEPENDENT_RELATIONSHIPS = (
    "Spouse",
    "Child",
    "Domestic Partner",
)

VALID_DEPENDENT_STATUSES = ("Active", "Terminated")

VALID_ENROLLMENT_STATUSES = (
    "Active",
    "Pending",
    "Cancelled",
)

VALID_ELIGIBILITY_STATUSES = (
    "Active",
    "Pending",
    "Terminated",
)

VALID_GENDERS = ("M", "F")

VALID_US_STATE_CODES = (
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC",
)
