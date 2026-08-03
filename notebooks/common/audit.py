"""
Audit utilities for Northstar data engineering notebooks.

Provides reusable audit columns that are appended to every curated dataset.
"""

from pyspark.sql.functions import (
    current_timestamp,
    lit,
    sha2,
    concat_ws,
    col,
)


def add_audit_columns(df, batch_id: str, source_system: str):
    """
    Add standard enterprise audit metadata.
    """

    business_columns = [
        column_name
        for column_name in df.columns
        if column_name != "_source_file_path"
    ]

    return (
        df
        .withColumn("batch_id", lit(batch_id))
        .withColumn("source_system", lit(source_system))
        .withColumn("source_file", col("_source_file_path"))
        .withColumn("processing_timestamp", current_timestamp())
        .withColumn(
            "record_hash",
            sha2(
                concat_ws(
                    "||",
                    *[
                        col(column_name).cast("string")
                        for column_name in business_columns
                    ],
                ),
                256,
            ),
        )
        .drop("_source_file_path")
    )