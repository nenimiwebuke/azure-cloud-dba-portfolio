"""
Accepted-value rules for Northstar Benefits datasets.

Used by notebooks/config/northstar/validation_rules.py to build
data-quality checks.
"""

from __future__ import annotations

VALID_EMPLOYMENT_STATUSES = ("Active", "Terminated")

VALID_DEPENDENT_RELATIONSHIPS = (
    "Spouse",
    "Child",
    "Domestic Partner",
)

VALID_DEPENDENT_STATUSES = ("Active", "Terminated")

VALID_ENROLLMENT_STATUSES = (
    "Active",
    "Pending",
    "Cancelled",
)

VALID_ELIGIBILITY_STATUSES = (
    "Active",
    "Pending",
    "Terminated",
)

VALID_GENDERS = ("M", "F")

VALID_US_STATE_CODES = (
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC",
)
