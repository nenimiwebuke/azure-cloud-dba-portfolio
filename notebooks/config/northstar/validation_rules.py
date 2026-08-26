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


def build_dependent_validation_rules(as_of_date: str) -> list[Column]:
    """
    Build dependent data-contract violation rules.

    Note: this currently checks required-field presence only, matching
    the notebook's original "basic dependent validation." The full
    Dependent Data Contract also specifies referential checks (employee_id
    must exist in Employees) and cross-field checks (child cannot be
    older than the subscriber) that are not yet implemented here.
    ``as_of_date`` is accepted for interface consistency with the other
    build_* functions and for future use once those checks are added.
    """

    return [
        F.when(
            F.col("dependent_id").isNull(),
            F.lit("MISSING_DEPENDENT_ID"),
        ),
        F.when(
            F.col("employee_id").isNull(),
            F.lit("MISSING_EMPLOYEE_ID"),
        ),
        F.when(
            F.col("relationship").isNull(),
            F.lit("MISSING_RELATIONSHIP"),
        ),
        F.when(
            F.col("date_of_birth").isNull(),
            F.lit("MISSING_DATE_OF_BIRTH"),
        ),
        F.when(
            F.col("_corrupt_record").isNotNull(),
            F.lit("MALFORMED_SOURCE_RECORD"),
        ),
    ]


def build_enrollment_validation_rules(as_of_date: str) -> list[Column]:
    """
    Build enrollment data-contract violation rules.

    Note: required-field presence only, matching the notebook's
    original checks. ``as_of_date`` is accepted for interface
    consistency and future use (e.g. coverage_start_date vs. hire_date).
    """

    return [
        F.when(
            F.col("enrollment_id").isNull(),
            F.lit("MISSING_ENROLLMENT_ID"),
        ),
        F.when(
            F.col("employee_id").isNull(),
            F.lit("MISSING_EMPLOYEE_ID"),
        ),
        F.when(
            F.col("employer_id").isNull(),
            F.lit("MISSING_EMPLOYER_ID"),
        ),
        F.when(
            F.col("plan_id").isNull(),
            F.lit("MISSING_PLAN_ID"),
        ),
        F.when(
            F.col("coverage_start_date").isNull(),
            F.lit("MISSING_COVERAGE_START_DATE"),
        ),
        F.when(
            F.col("enrollment_status").isNull(),
            F.lit("MISSING_ENROLLMENT_STATUS"),
        ),
        F.when(
            F.col("_corrupt_record").isNotNull(),
            F.lit("MALFORMED_SOURCE_RECORD"),
        ),
    ]


def build_eligibility_validation_rules(as_of_date: str) -> list[Column]:
    """
    Build eligibility data-contract violation rules.

    Note: required-field presence only, matching the notebook's
    original checks. ``as_of_date`` is accepted for interface
    consistency and future use.
    """

    return [
        F.when(
            F.col("eligibility_id").isNull(),
            F.lit("MISSING_ELIGIBILITY_ID"),
        ),
        F.when(
            F.col("employee_id").isNull(),
            F.lit("MISSING_EMPLOYEE_ID"),
        ),
        F.when(
            F.col("plan_id").isNull(),
            F.lit("MISSING_PLAN_ID"),
        ),
        F.when(
            F.col("eligibility_start_date").isNull(),
            F.lit("MISSING_ELIGIBILITY_START_DATE"),
        ),
        F.when(
            F.col("eligibility_status").isNull(),
            F.lit("MISSING_ELIGIBILITY_STATUS"),
        ),
        F.when(
            F.col("approval_timestamp").isNull(),
            F.lit("MISSING_APPROVAL_TIMESTAMP"),
        ),
        F.when(
            F.col("_corrupt_record").isNotNull(),
            F.lit("MALFORMED_SOURCE_RECORD"),
        ),
    ]
