"""
Northstar-specific data-quality rule definitions.

Each build_*_validation_rules function returns a list of F.when(...)
expressions consumed by notebooks.common.validation.apply_validation_rules.
Keeping the rule lists here (rather than in common/) means a new
business case defines its own rule sets without touching shared code.
"""

from __future__ import annotations

from pyspark.sql import Column, Window
from pyspark.sql import functions as F

from notebooks.config.northstar.valid_values import (
    VALID_EMPLOYMENT_STATUSES,
    VALID_US_STATE_CODES,
)


def build_employee_validation_rules(as_of_date: str) -> list[Column]:
    """
    Build employee data-contract violation rules.

    Parameters
    ----------
    as_of_date:
        Business date in ISO format, for example ``2026-07-01``.
    """

    business_date = F.to_date(F.lit(as_of_date))
    employee_window = Window.partitionBy("employee_id")

    return [
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
