#!/usr/bin/env python3
"""
Generate deterministic synthetic benefits-administration data for the
Northstar Benefits Group portfolio.

The generator produces interconnected employee, dependent, enrollment,
and eligibility datasets. It also injects controlled business exceptions
that later pipelines must detect through reconciliation and data-quality
processing.

No production, customer, employer, patient, or personally identifiable
data is used.
"""

from __future__ import annotations

import csv
import json
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


SEED = 20260728
EMPLOYEE_COUNT = 10_000

AS_OF_DATE = date(2026, 7, 1)
FILE_RECEIVED_TIMESTAMP = "2026-07-01T06:30:00Z"
ELIGIBILITY_APPROVAL_TIMESTAMP = "2026-07-02T02:15:00Z"

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "data" / "northstar" / "reference"
ENROLLMENT_DIR = ROOT / "data" / "northstar" / "inbound" / "enrollment"
ELIGIBILITY_DIR = ROOT / "data" / "northstar" / "inbound" / "eligibility"
EXPECTED_DIR = ROOT / "data" / "northstar" / "expected-results"

EMPLOYEES_FILE = ENROLLMENT_DIR / "employees_20260701.csv"
DEPENDENTS_FILE = ENROLLMENT_DIR / "dependents_20260701.csv"
ENROLLMENTS_FILE = ENROLLMENT_DIR / "enrollments_20260701.csv"
ELIGIBILITY_FILE = ELIGIBILITY_DIR / "eligibility_20260702.csv"
EXCEPTIONS_FILE = EXPECTED_DIR / "eligibility_reconciliation_expected.csv"
SUMMARY_FILE = EXPECTED_DIR / "generation_summary.json"


FIRST_NAMES = [
    "Aaliyah", "Amara", "Andre", "Angela", "Carlos", "Chiamaka", "Daniel",
    "David", "Elena", "Ethan", "Fatima", "Grace", "Isaiah", "Jasmine",
    "Jordan", "Kevin", "Leah", "Luis", "Malik", "Maya", "Michael", "Naomi",
    "Nia", "Noah", "Olivia", "Omar", "Priya", "Samuel", "Sophia", "Victor",
    "Zoe",
]

LAST_NAMES = [
    "Adams", "Adeyemi", "Bennett", "Brown", "Campbell", "Chen", "Davis",
    "Garcia", "Hernandez", "Ibrahim", "Johnson", "Kim", "Lewis", "Martinez",
    "Mensah", "Miller", "Moore", "Nguyen", "Okafor", "Patel", "Robinson",
    "Smith", "Taylor", "Thomas", "Walker", "Williams", "Wilson",
]

DEPARTMENTS = [
    "Administration",
    "Customer Operations",
    "Finance",
    "Human Resources",
    "Information Technology",
    "Legal and Compliance",
    "Operations",
    "Sales",
    "Supply Chain",
]

EMPLOYEE_STATES = ["DC", "FL", "MD", "NC", "NY", "OH", "TX", "VA"]

MEDICAL_PLANS = [
    "PLN-MED-001",
    "PLN-MED-002",
    "PLN-MED-003",
    "PLN-MED-004",
    "PLN-MED-005",
    "PLN-MED-006",
    "PLN-MED-007",
    "PLN-MED-008",
]

DENTAL_PLANS = [
    "PLN-DEN-001",
    "PLN-DEN-002",
    "PLN-DEN-003",
    "PLN-DEN-004",
]

VISION_PLANS = [
    "PLN-VIS-001",
    "PLN-VIS-002",
    "PLN-VIS-003",
    "PLN-VIS-004",
]

LIFE_PLAN = "PLN-LIF-001"
DISABILITY_PLAN = "PLN-DIS-001"


@dataclass(frozen=True)
class Employer:
    employer_id: str
    employer_name: str
    state: str
    source_system: str


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Required source file not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def random_date(start: date, end: date) -> date:
    if end < start:
        raise ValueError(f"Invalid date range: {start} to {end}")

    day_count = (end - start).days
    return start + timedelta(days=random.randint(0, day_count))


def iso(value: date | None) -> str:
    return value.isoformat() if value else ""


def choose_coverage_tier(dependents: list[dict[str, str]]) -> str:
    if not dependents:
        return "Employee"

    relationships = {row["relationship"] for row in dependents}

    has_spouse = bool({"Spouse", "Domestic Partner"} & relationships)
    has_child = "Child" in relationships

    if has_spouse and has_child:
        return "Family"
    if has_spouse:
        return "Employee+Spouse"
    return "Employee+Children"


def choose_plan(plan_type: str, coverage_tier: str) -> str:
    tier_index = {
        "Employee": 0,
        "Employee+Spouse": 1,
        "Employee+Children": 2,
        "Family": 3,
    }[coverage_tier]

    if plan_type == "Medical":
        plan_family_offset = random.choice([0, 4])
        return MEDICAL_PLANS[plan_family_offset + tier_index]

    if plan_type == "Dental":
        return DENTAL_PLANS[tier_index]

    if plan_type == "Vision":
        return VISION_PLANS[tier_index]

    raise ValueError(f"Unsupported plan type: {plan_type}")


def alternate_medical_plan(current_plan: str) -> str:
    alternatives = [plan for plan in MEDICAL_PLANS if plan != current_plan]
    return random.choice(alternatives)


def build_employees(
    employers: list[Employer],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    employees: list[dict[str, Any]] = []
    dependents_by_employee: dict[str, list[dict[str, Any]]] = {}

    for employee_number in range(1, EMPLOYEE_COUNT + 1):
        employee_id = f"EE{employee_number:07d}"
        employer = random.choice(employers)

        birth_date = random_date(date(1961, 1, 1), date(2007, 6, 30))
        hire_date = random_date(date(2014, 1, 1), date(2026, 6, 15))

        is_terminated = random.random() < 0.18
        termination_date: date | None = None

        if is_terminated:
            earliest_termination = max(hire_date + timedelta(days=30), date(2024, 1, 1))
            if earliest_termination <= AS_OF_DATE:
                termination_date = random_date(earliest_termination, AS_OF_DATE)
            else:
                is_terminated = False

        employment_status = "Terminated" if is_terminated else "Active"

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        employees.append(
            {
                "employee_id": employee_id,
                "employer_id": employer.employer_id,
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": iso(birth_date),
                "hire_date": iso(hire_date),
                "termination_date": iso(termination_date),
                "employment_status": employment_status,
                "department": random.choice(DEPARTMENTS),
                "state": random.choice([employer.state, random.choice(EMPLOYEE_STATES)]),
            }
        )

        employee_dependents: list[dict[str, Any]] = []

        if not is_terminated and random.random() < 0.58:
            dependent_count = random.choices(
                population=[1, 2, 3],
                weights=[0.48, 0.38, 0.14],
                k=1,
            )[0]

            include_partner = random.random() < 0.58

            for dependent_index in range(1, dependent_count + 1):
                dependent_id = f"DP{employee_number:07d}{dependent_index:02d}"

                if dependent_index == 1 and include_partner:
                    relationship = random.choice(["Spouse", "Domestic Partner"])
                    dependent_birth_date = random_date(
                        max(date(1961, 1, 1), birth_date - timedelta(days=365 * 8)),
                        min(date(2007, 6, 30), birth_date + timedelta(days=365 * 8)),
                    )
                else:
                    relationship = "Child"
                    oldest_child_date = max(
                        birth_date + timedelta(days=365 * 16),
                        date(2000, 1, 1),
                    )
                    dependent_birth_date = random_date(
                        oldest_child_date,
                        date(2026, 6, 30),
                    )

                employee_dependents.append(
                    {
                        "dependent_id": dependent_id,
                        "employee_id": employee_id,
                        "first_name": random.choice(FIRST_NAMES),
                        "last_name": last_name,
                        "relationship": relationship,
                        "date_of_birth": iso(dependent_birth_date),
                        "gender": random.choice(["M", "F"]),
                        "dependent_status": "Active",
                    }
                )

        dependents_by_employee[employee_id] = employee_dependents

    return employees, dependents_by_employee


def build_enrollments(
    employees: list[dict[str, Any]],
    dependents_by_employee: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    enrollments: list[dict[str, Any]] = []
    sequence = 1

    for employee in employees:
        if employee["employment_status"] != "Active":
            continue

        employee_id = employee["employee_id"]
        employer_id = employee["employer_id"]
        dependents = dependents_by_employee[employee_id]
        coverage_tier = choose_coverage_tier(dependents)

        hire_date = date.fromisoformat(employee["hire_date"])
        coverage_start = max(date(2026, 1, 1), hire_date)

        selected_plans = [
            choose_plan("Medical", coverage_tier),
            choose_plan("Dental", coverage_tier),
            choose_plan("Vision", coverage_tier),
            LIFE_PLAN,
        ]

        if random.random() < 0.42:
            selected_plans.append(DISABILITY_PLAN)

        for plan_id in selected_plans:
            enrollment_id = f"ENR{sequence:09d}"
            sequence += 1

            enrollments.append(
                {
                    "enrollment_id": enrollment_id,
                    "employer_id": employer_id,
                    "employee_id": employee_id,
                    "dependent_id": "",
                    "plan_id": plan_id,
                    "coverage_start_date": iso(coverage_start),
                    "coverage_end_date": "",
                    "enrollment_status": "Active",
                    "source_file_name": "northstar_enrollment_20260701.csv",
                    "source_received_timestamp": FILE_RECEIVED_TIMESTAMP,
                }
            )

    return enrollments


def build_eligibility(
    enrollments: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    eligibility_rows: list[dict[str, Any]] = []
    expected_exceptions: list[dict[str, Any]] = []

    eligibility_sequence = 1

    for enrollment in enrollments:
        roll = random.random()

        # Intentionally omit approximately 2 percent of enrollment records.
        if roll < 0.02:
            expected_exceptions.append(
                {
                    "enrollment_id": enrollment["enrollment_id"],
                    "employee_id": enrollment["employee_id"],
                    "expected_exception_type": "MISSING_ELIGIBILITY",
                    "expected_severity": "High",
                    "expected_business_impact": "Requested coverage was not established.",
                }
            )
            continue

        plan_id = enrollment["plan_id"]
        eligibility_start = date.fromisoformat(enrollment["coverage_start_date"])
        anomaly_type = ""

        # Wrong-plan mismatches are limited to medical enrollments.
        if 0.02 <= roll < 0.035 and plan_id.startswith("PLN-MED"):
            plan_id = alternate_medical_plan(plan_id)
            anomaly_type = "PLAN_MISMATCH"

        # Delayed eligibility creates a coverage gap.
        elif 0.035 <= roll < 0.055:
            eligibility_start += timedelta(days=random.choice([7, 14, 30]))
            anomaly_type = "DELAYED_ELIGIBILITY_START"

        eligibility_id = f"ELG{eligibility_sequence:09d}"
        eligibility_sequence += 1

        eligibility_rows.append(
            {
                "eligibility_id": eligibility_id,
                "employee_id": enrollment["employee_id"],
                "dependent_id": enrollment["dependent_id"],
                "plan_id": plan_id,
                "eligibility_start_date": iso(eligibility_start),
                "eligibility_end_date": "",
                "eligibility_status": "Active",
                "approval_timestamp": ELIGIBILITY_APPROVAL_TIMESTAMP,
                "source_system": "Northstar Benefits Administration",
            }
        )

        if anomaly_type:
            business_impact = {
                "PLAN_MISMATCH": "Approved plan differs from the employer election.",
                "DELAYED_ELIGIBILITY_START": (
                    "Eligibility begins after the requested coverage date."
                ),
            }[anomaly_type]

            expected_exceptions.append(
                {
                    "enrollment_id": enrollment["enrollment_id"],
                    "employee_id": enrollment["employee_id"],
                    "expected_exception_type": anomaly_type,
                    "expected_severity": "High",
                    "expected_business_impact": business_impact,
                }
            )

        # Seed duplicate active eligibility records for about 0.5 percent.
        if random.random() < 0.005:
            duplicate_id = f"ELG{eligibility_sequence:09d}"
            eligibility_sequence += 1

            duplicate_row = dict(eligibility_rows[-1])
            duplicate_row["eligibility_id"] = duplicate_id
            eligibility_rows.append(duplicate_row)

            expected_exceptions.append(
                {
                    "enrollment_id": enrollment["enrollment_id"],
                    "employee_id": enrollment["employee_id"],
                    "expected_exception_type": "DUPLICATE_ACTIVE_ELIGIBILITY",
                    "expected_severity": "Medium",
                    "expected_business_impact": (
                        "Multiple active eligibility rows may cause billing "
                        "or claims-processing errors."
                    ),
                }
            )

    # Seed records referencing employees that do not exist.
    invalid_reference_count = max(1, int(len(enrollments) * 0.002))

    for invalid_number in range(1, invalid_reference_count + 1):
        eligibility_id = f"ELG{eligibility_sequence:09d}"
        eligibility_sequence += 1
        invalid_employee_id = f"UNKNOWN{invalid_number:06d}"

        eligibility_rows.append(
            {
                "eligibility_id": eligibility_id,
                "employee_id": invalid_employee_id,
                "dependent_id": "",
                "plan_id": "PLN-MED-001",
                "eligibility_start_date": "2026-01-01",
                "eligibility_end_date": "",
                "eligibility_status": "Active",
                "approval_timestamp": ELIGIBILITY_APPROVAL_TIMESTAMP,
                "source_system": "Northstar Benefits Administration",
            }
        )

        expected_exceptions.append(
            {
                "enrollment_id": "",
                "employee_id": invalid_employee_id,
                "expected_exception_type": "UNKNOWN_EMPLOYEE",
                "expected_severity": "Critical",
                "expected_business_impact": (
                    "Eligibility exists for a member absent from the employee population."
                ),
            }
        )

    return eligibility_rows, expected_exceptions


def main() -> None:
    random.seed(SEED)

    employers_source = read_csv(REFERENCE_DIR / "employers.csv")
    plan_source = read_csv(REFERENCE_DIR / "plans.csv")

    if not employers_source:
        raise ValueError("Employers reference data is empty.")

    if not plan_source:
        raise ValueError("Plans reference data is empty.")

    employers = [
        Employer(
            employer_id=row["employer_id"],
            employer_name=row["employer_name"],
            state=row["state"],
            source_system=row["source_system"],
        )
        for row in employers_source
        if row["account_status"] == "Active"
    ]

    employees, dependents_by_employee = build_employees(employers)

    dependents = [
        dependent
        for employee_dependents in dependents_by_employee.values()
        for dependent in employee_dependents
    ]

    enrollments = build_enrollments(employees, dependents_by_employee)
    eligibility, expected_exceptions = build_eligibility(enrollments)

    write_csv(
        EMPLOYEES_FILE,
        employees,
        [
            "employee_id",
            "employer_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "hire_date",
            "termination_date",
            "employment_status",
            "department",
            "state",
        ],
    )

    write_csv(
        DEPENDENTS_FILE,
        dependents,
        [
            "dependent_id",
            "employee_id",
            "first_name",
            "last_name",
            "relationship",
            "date_of_birth",
            "gender",
            "dependent_status",
        ],
    )

    write_csv(
        ENROLLMENTS_FILE,
        enrollments,
        [
            "enrollment_id",
            "employer_id",
            "employee_id",
            "dependent_id",
            "plan_id",
            "coverage_start_date",
            "coverage_end_date",
            "enrollment_status",
            "source_file_name",
            "source_received_timestamp",
        ],
    )

    write_csv(
        ELIGIBILITY_FILE,
        eligibility,
        [
            "eligibility_id",
            "employee_id",
            "dependent_id",
            "plan_id",
            "eligibility_start_date",
            "eligibility_end_date",
            "eligibility_status",
            "approval_timestamp",
            "source_system",
        ],
    )

    write_csv(
        EXCEPTIONS_FILE,
        expected_exceptions,
        [
            "enrollment_id",
            "employee_id",
            "expected_exception_type",
            "expected_severity",
            "expected_business_impact",
        ],
    )

    summary = {
        "generator_seed": SEED,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "as_of_date": AS_OF_DATE.isoformat(),
        "source_employers": len(employers),
        "employees": len(employees),
        "dependents": len(dependents),
        "enrollments": len(enrollments),
        "eligibility_records": len(eligibility),
        "expected_reconciliation_exceptions": len(expected_exceptions),
        "expected_exception_counts": {},
    }

    for row in expected_exceptions:
        exception_type = row["expected_exception_type"]
        summary["expected_exception_counts"][exception_type] = (
            summary["expected_exception_counts"].get(exception_type, 0) + 1
        )

    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_FILE.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("Northstar synthetic enterprise data generated successfully.")
    print(f"Employees:              {len(employees):,}")
    print(f"Dependents:             {len(dependents):,}")
    print(f"Enrollments:            {len(enrollments):,}")
    print(f"Eligibility records:    {len(eligibility):,}")
    print(f"Expected exceptions:    {len(expected_exceptions):,}")
    print(f"Summary:                {SUMMARY_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()