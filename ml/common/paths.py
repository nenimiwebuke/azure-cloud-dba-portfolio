"""
Centralized, business-case-agnostic local filesystem paths for the ML layer.

Mirrors notebooks/common/paths.py's BusinessCasePaths, but for local
pandas/scikit-learn scripts reading and writing plain files rather than
ADLS Gen2. A future business case instantiates MLPaths with its own
business_case name and gets the same inbound/outputs directory structure
without touching this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MLPaths:
    """Local filesystem paths used by a business case's ML scripts."""

    business_case: str
    data_root: str = "data"
    ml_root: str = "ml"

    @property
    def data_dir(self) -> Path:
        return Path(self.data_root) / self.business_case

    @property
    def inbound_dir(self) -> Path:
        return self.data_dir / "inbound"

    def inbound_file(self, relative_path: str) -> Path:
        """Path to a source file under data/<business_case>/inbound/."""
        return self.inbound_dir / relative_path

    @property
    def expected_results_dir(self) -> Path:
        return self.data_dir / "expected-results"

    def expected_results_file(self, filename: str) -> Path:
        return self.expected_results_dir / filename

    @property
    def outputs_dir(self) -> Path:
        return Path(self.ml_root) / self.business_case / "outputs"

    def output_file(self, filename: str) -> Path:
        """Path to a generated file under ml/<business_case>/outputs/."""
        return self.outputs_dir / filename

    def ensure_outputs_dir(self) -> Path:
        """Create the outputs directory if it doesn't already exist."""
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        return self.outputs_dir
