"""
Centralized, business-case-agnostic storage path builder.

A BusinessCasePaths instance encapsulates the bronze/silver/gold
root conventions for one business case (e.g. "northstar"). Dataset-
level path helpers take the dataset name explicitly rather than
being hardcoded per-column, so this class works unchanged for any
future business case.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BusinessCasePaths:
    """Storage paths used by a business case's Databricks workloads."""

    storage_account: str
    business_case: str

    @property
    def bronze_root(self) -> str:
        return f"abfss://bronze@{self.storage_account}.dfs.core.windows.net/{self.business_case}"

    @property
    def silver_root(self) -> str:
        return f"abfss://silver@{self.storage_account}.dfs.core.windows.net/{self.business_case}"

    @property
    def gold_root(self) -> str:
        return f"abfss://gold@{self.storage_account}.dfs.core.windows.net/{self.business_case}"

    def bronze_dataset_root(self, dataset: str) -> str:
        """Directory containing a dataset's raw bronze file drops."""
        return f"{self.bronze_root}/{dataset}"

    def bronze_file(self, dataset: str, filename: str) -> str:
        """Path to a specific bronze file drop for a dataset."""
        return f"{self.bronze_dataset_root(dataset)}/{filename}"

    def silver_path(self, dataset: str) -> str:
        return f"{self.silver_root}/{dataset}"

    def quarantine_path(self, dataset: str) -> str:
        return f"{self.silver_root}/quarantine/{dataset}"

    def gold_path(self, table_name: str) -> str:
        return f"{self.gold_root}/{table_name}"