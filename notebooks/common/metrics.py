"""
Operational metric utilities for Northstar Databricks workloads.

These helpers provide both readable notebook output and structured metric
records that can be persisted for monitoring, reconciliation, and reporting.
"""

from __future__ import annotations

from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


PIPELINE_METRIC_SCHEMA = StructType(
    [
        StructField("pipeline_name", StringType(), nullable=False),
        StructField("notebook_version", StringType(), nullable=False),
        StructField("batch_id", StringType(), nullable=False),
        StructField("business_date", StringType(), nullable=False),
        StructField("source_system", StringType(), nullable=False),
        StructField("source_path", StringType(), nullable=False),
        StructField("target_path", StringType(), nullable=False),
        StructField("records_read", LongType(), nullable=False),
        StructField("records_written", LongType(), nullable=False),
        StructField("records_rejected", LongType(), nullable=False),
        StructField("data_quality_score", StringType(), nullable=False),
        StructField("run_status", StringType(), nullable=False),
        StructField("run_timestamp", TimestampType(), nullable=False),
    ]
)


def print_metric(name: str, value: Any) -> None:
    """Print one consistently formatted metric."""

    print(f"{name:.<45} {value}")


def calculate_data_quality_score(
    records_read: int,
    records_rejected: int,
) -> float:
    """
    Calculate the percentage of source records accepted by validation.

    A zero-row input returns 100 because no source records failed.
    """

    if records_read == 0:
        return 100.0

    accepted = records_read - records_rejected
    return round((accepted / records_read) * 100, 2)


def print_summary(
    records_read: int,
    records_written: int,
    rejected_records: int,
    data_quality_score: float | None = None,
) -> None:
    """Print a standard pipeline execution summary."""

    score = (
        data_quality_score
        if data_quality_score is not None
        else calculate_data_quality_score(records_read, rejected_records)
    )

    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)

    print_metric("Records Read", f"{records_read:,}")
    print_metric("Records Written", f"{records_written:,}")
    print_metric("Rejected Records", f"{rejected_records:,}")
    print_metric("Data Quality Score", f"{score:.2f}%")

    print("=" * 60)


def create_pipeline_metric_df(
    spark: SparkSession,
    *,
    pipeline_name: str,
    notebook_version: str,
    batch_id: str,
    business_date: str,
    source_system: str,
    source_path: str,
    target_path: str,
    records_read: int,
    records_written: int,
    records_rejected: int,
    run_status: str,
) -> DataFrame:
    """Create a one-row DataFrame representing a pipeline execution."""

    quality_score = calculate_data_quality_score(
        records_read,
        records_rejected,
    )

    metric_row = [
        {
            "pipeline_name": pipeline_name,
            "notebook_version": notebook_version,
            "batch_id": batch_id,
            "business_date": business_date,
            "source_system": source_system,
            "source_path": source_path,
            "target_path": target_path,
            "records_read": records_read,
            "records_written": records_written,
            "records_rejected": records_rejected,
            "data_quality_score": f"{quality_score:.2f}",
            "run_status": run_status,
        }
    ]

    return (
        spark.createDataFrame(metric_row)
        .withColumn("run_timestamp", F.current_timestamp())
        .select(
            "pipeline_name",
            "notebook_version",
            "batch_id",
            "business_date",
            "source_system",
            "source_path",
            "target_path",
            F.col("records_read").cast("long"),
            F.col("records_written").cast("long"),
            F.col("records_rejected").cast("long"),
            "data_quality_score",
            "run_status",
            "run_timestamp",
        )
    )
