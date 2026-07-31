"""
Centralized storage paths for the Northstar Benefits data platform.

Keeping paths in one module prevents notebooks from duplicating hard-coded
storage locations and makes future environment changes easier to manage.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NorthstarPaths:
    """Storage paths used by the Northstar Databricks workloads."""

    storage_account: str = "stnenimadlsdev01"

    @property
    def bronze_root(self) -> str:
        return f"abfss://bronze@{self.storage_account}.dfs.core.windows.net/northstar"

    @property
    def silver_root(self) -> str:
        return f"abfss://silver@{self.storage_account}.dfs.core.windows.net/northstar"

    @property
    def gold_root(self) -> str:
        return f"abfss://gold@{self.storage_account}.dfs.core.windows.net/northstar"

    @property
    def employees_bronze(self) -> str:
        return f"{self.bronze_root}/employees/employees_20260701.csv"

    @property
    def dependents_bronze(self) -> str:
        return f"{self.bronze_root}/dependents/dependents_20260701.csv"

    @property
    def enrollments_bronze(self) -> str:
        return f"{self.bronze_root}/enrollments/enrollments_20260701.csv"

    @property
    def eligibility_bronze(self) -> str:
        return f"{self.bronze_root}/eligibility/eligibility_20260702.csv"

    @property
    def employees_silver(self) -> str:
        return f"{self.silver_root}/employees"

    @property
    def dependents_silver(self) -> str:
        return f"{self.silver_root}/dependents"

    @property
    def enrollments_silver(self) -> str:
        return f"{self.silver_root}/enrollments"

    @property
    def eligibility_silver(self) -> str:
        return f"{self.silver_root}/eligibility"

    @property
    def employees_quarantine(self) -> str:
        return f"{self.silver_root}/quarantine/employees"

    @property
    def dependents_quarantine(self) -> str:
        return f"{self.silver_root}/quarantine/dependents"

    @property
    def enrollments_quarantine(self) -> str:
        return f"{self.silver_root}/quarantine/enrollments"

    @property
    def eligibility_quarantine(self) -> str:
        return f"{self.silver_root}/quarantine/eligibility"

    @property
    def eligibility_reconciliation_gold(self) -> str:
        return f"{self.gold_root}/eligibility_reconciliation"

    @property
    def data_quality_metrics_gold(self) -> str:
        return f"{self.gold_root}/data_quality_metrics"


PATHS = NorthstarPaths()
