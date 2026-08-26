"""
Reusable data-quality validation engine.

Business-case-specific rule sets (a list of F.when(...) column
expressions) are defined per dataset in notebooks/config/<business_case>/
validation_rules.py and passed into apply_validation_rules. This module
knows nothing about employee IDs, dependents, or any other domain schema.
"""

from __future__ import annotations

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F


def apply_validation_rules(df: DataFrame, rules: list[Column]) -> DataFrame:
    """
    Attach data-contract violations to each row using a supplied rule set.

    Parameters
    ----------
    df:
        DataFrame after applying its explicit schema.
    rules:
        A list of F.when(condition, F.lit("ERROR_CODE")) expressions.
        Rules that don't match a given row evaluate to null and are
        compacted out.

    Returns
    -------
    DataFrame
        Original columns plus ``validation_errors`` and ``is_valid``.
    """

    return (
        df.withColumn(
            "validation_errors",
            F.array_compact(F.array(*rules)),
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