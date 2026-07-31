"""
Audit utilities for Northstar data engineering notebooks.

Provides reusable audit columns that are appended to every curated dataset.
"""

from pyspark.sql.functions import (
    current_timestamp,
    input_file_name,
    lit,
    sha2,
    concat_ws,
    col,
)


def add_audit_columns(df, batch_id: str, source_system: str):
    """
    Adds standard enterprise audit metadata.
    """

    business_columns = df.columns

    return (
        df
        .withColumn("batch_id", lit(batch_id))
        .withColumn("source_system", lit(source_system))
        .withColumn("source_file", input_file_name())
        .withColumn("processing_timestamp", current_timestamp())
        .withColumn(
            "record_hash",
            sha2(
                concat_ws(
                    "||",
                    *[col(c).cast("string") for c in business_columns]
                ),
                256,
            ),
        )
    )
