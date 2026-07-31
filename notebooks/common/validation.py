"""
Reusable data-quality validation functions for Northstar datasets.

Validation functions attach an array of rule failures to each record.
Rows with no failures are valid; rows with one or more failures are
preserved for quarantine and investigation.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from notebooks.common.contracts import (
    VALID_EMPLOYMENT_STATUSES,
    VALID_US_STATE_CODES,
)


def add_employee_validation_errors(
    df: DataFrame,
    as_of_date: str,
) -> DataFrame:
    """
    Attach employee data-contract violations to each row.

    Parameters
    ----------
    df:
        Employee DataFrame after applying the explicit employee schema.
    as_of_date:
        Business date in ISO format, for example ``2026-07-01``.

    Returns
    -------
    DataFrame
        Original columns plus ``validation_errors`` and ``is_valid``.
    """

    business_date = F.to_date(F.lit(as_of_date))

    employee_window = Window.partitionBy("employee_id")

    validation_rules = [
        F.when(
            F.col("employee_id").isNull()
            | (F.trim(F.col("employee_id")) == ""),
            F.lit("MISSING_EMPLOYEE_ID"),
        ),
        F.when(
            F.col("employer_id").isNull()
            | (F.trim(F.col("employer_id")) == ""),
            F.lit("MISSING_EMPLOYER_ID"),
        ),
        F.when(
            F.col("first_name").isNull()
            | (F.trim(F.col("first_name")) == ""),
            F.lit("MISSING_FIRST_NAME"),
        ),
        F.when(
            F.col("last_name").isNull()
            | (F.trim(F.col("last_name")) == ""),
            F.lit("MISSING_LAST_NAME"),
        ),
        F.when(
            F.col("date_of_birth").isNull(),
            F.lit("INVALID_OR_MISSING_DATE_OF_BIRTH"),
        ),
        F.when(
            F.col("hire_date").isNull(),
            F.lit("INVALID_OR_MISSING_HIRE_DATE"),
        ),
        F.when(
            ~F.col("employment_status").isin(*VALID_EMPLOYMENT_STATUSES),
            F.lit("INVALID_EMPLOYMENT_STATUS"),
        ),
        F.when(
            ~F.col("state").isin(*VALID_US_STATE_CODES),
            F.lit("INVALID_STATE_CODE"),
        ),
        F.when(
            F.col("date_of_birth") > business_date,
            F.lit("FUTURE_DATE_OF_BIRTH"),
        ),
        F.when(
            F.col("hire_date") > business_date,
            F.lit("FUTURE_HIRE_DATE"),
        ),
        F.when(
            F.months_between(business_date, F.col("date_of_birth")) / 12 < 16,
            F.lit("EMPLOYEE_UNDER_MINIMUM_AGE"),
        ),
        F.when(
            (F.col("employment_status") == "Active")
            & F.col("termination_date").isNotNull(),
            F.lit("ACTIVE_EMPLOYEE_HAS_TERMINATION_DATE"),
        ),
        F.when(
            (F.col("employment_status") == "Terminated")
            & F.col("termination_date").isNull(),
            F.lit("TERMINATED_EMPLOYEE_MISSING_TERMINATION_DATE"),
        ),
        F.when(
            F.col("termination_date").isNotNull()
            & F.col("hire_date").isNotNull()
            & (F.col("termination_date") < F.col("hire_date")),
            F.lit("TERMINATION_BEFORE_HIRE_DATE"),
        ),
        F.when(
            F.col("employee_id").isNotNull()
            & (F.count(F.lit(1)).over(employee_window) > 1),
            F.lit("DUPLICATE_EMPLOYEE_ID"),
        ),
    ]

    return (
        df.withColumn(
            "validation_errors",
            F.array_compact(F.array(*validation_rules)),
        )
        .withColumn(
            "is_valid",
            F.size(F.col("validation_errors")) == 0,
        )
    )


def split_valid_and_quarantine(
    df: DataFrame,
) -> tuple[DataFrame, DataFrame]:
    """Split validated records into valid and quarantine DataFrames."""

    valid_df = df.filter(F.col("is_valid")).drop(
        "validation_errors",
        "is_valid",
    )

    quarantine_df = df.filter(~F.col("is_valid"))

    return valid_df, quarantine_df
