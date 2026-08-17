import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DATA_DIR = Path("data/northstar")

EMPLOYEES_FILE = DATA_DIR / "inbound/enrollment/employees_20260701.csv"
ENROLLMENTS_FILE = DATA_DIR / "inbound/enrollment/enrollments_20260701.csv"
ELIGIBILITY_FILE = DATA_DIR / "inbound/eligibility/eligibility_20260702.csv"

EXPECTED_FILE = (
    DATA_DIR
    / "expected-results"
    / "eligibility_reconciliation_expected.csv"
)


# ---------------------------------------------------------
# Load source datasets
# ---------------------------------------------------------

employees = pd.read_csv(EMPLOYEES_FILE)
enrollments = pd.read_csv(ENROLLMENTS_FILE)
eligibility = pd.read_csv(ELIGIBILITY_FILE)
expected = pd.read_csv(EXPECTED_FILE)


# ---------------------------------------------------------
# Verify datasets
# ---------------------------------------------------------

print("Employees:", employees.shape)
print("Enrollments:", enrollments.shape)
print("Eligibility:", eligibility.shape)
print("Expected exceptions:", expected.shape)

# ---------------------------------------------------------
# Join employee attributes to enrollment records
# ---------------------------------------------------------

training = enrollments.merge(
    employees[
        [
            "employee_id",
            "employer_id",
            "employment_status",
            "department",
            "state",
            "hire_date",
            "termination_date",
        ]
    ],
    on="employee_id",
    how="left",
    suffixes=("_enrollment", "_employee"),
)

print("\nAfter employee join:", training.shape)

missing_employee_attributes = training["department"].isna().sum()

print(
    "Enrollments missing employee attributes:",
    missing_employee_attributes,
)

# ---------------------------------------------------------
# Join eligibility records
# ---------------------------------------------------------

training = training.merge(
    eligibility[
        [
            "employee_id",
            "dependent_id",
            "plan_id",
            "eligibility_start_date",
            "eligibility_end_date",
            "eligibility_status",
        ]
    ],
    on=[
        "employee_id",
        "dependent_id",
        "plan_id",
    ],
    how="left",
)

print("\nAfter eligibility join:", training.shape)

missing_eligibility = training["eligibility_status"].isna().sum()

print(
    "Enrollments with no matching eligibility:",
    missing_eligibility,
)

# ---------------------------------------------------------
# Diagnose duplicate eligibility matches
# ---------------------------------------------------------

eligibility_key_counts = (
    eligibility
    .groupby(
        [
            "employee_id",
            "dependent_id",
            "plan_id",
        ],
        dropna=False,
    )
    .size()
    .reset_index(name="eligibility_match_count")
)

duplicate_eligibility_keys = eligibility_key_counts[
    eligibility_key_counts["eligibility_match_count"] > 1
]

print(
    "\nEligibility keys with multiple matches:",
    len(duplicate_eligibility_keys),
)

print(
    "Extra eligibility rows caused by duplicate matches:",
    (
        duplicate_eligibility_keys["eligibility_match_count"] - 1
    ).sum(),
)

# ---------------------------------------------------------
# Aggregate eligibility features to one row per enrollment key
# ---------------------------------------------------------

eligibility_features = (
    eligibility
    .groupby(
        [
            "employee_id",
            "dependent_id",
            "plan_id",
        ],
        dropna=False,
    )
    .agg(
        eligibility_match_count=("eligibility_status", "size"),
        eligibility_start_date=("eligibility_start_date", "min"),
        eligibility_end_date=("eligibility_end_date", "max"),
        eligibility_status=("eligibility_status", "first"),
    )
    .reset_index()
)

training = enrollments.merge(
    employees[
        [
            "employee_id",
            "employer_id",
            "employment_status",
            "department",
            "state",
            "hire_date",
            "termination_date",
        ]
    ],
    on="employee_id",
    how="left",
    suffixes=("_enrollment", "_employee"),
)

training = training.merge(
    eligibility_features,
    on=[
        "employee_id",
        "dependent_id",
        "plan_id",
    ],
    how="left",
)

print("\nTraining rows after aggregated eligibility join:", training.shape)

print(
    "Rows with multiple eligibility matches:",
    (training["eligibility_match_count"] > 1).sum(),
)

print(
    "Rows with no eligibility match:",
    training["eligibility_match_count"].isna().sum(),
)

# ---------------------------------------------------------
# Create binary target from known reconciliation exceptions
# ---------------------------------------------------------

exception_enrollment_ids = set(
    expected["enrollment_id"].dropna().astype(str)
)

training["exception_flag"] = (
    training["enrollment_id"]
    .astype(str)
    .isin(exception_enrollment_ids)
    .astype(int)
)

print("\nTarget distribution:")
print(training["exception_flag"].value_counts())

print("\nException rate:")
print(
    f"{training['exception_flag'].mean() * 100:.2f}%"
)

# ---------------------------------------------------------
# Diagnose expected exceptions not mapped to enrollments
# ---------------------------------------------------------

enrollment_ids = set(
    enrollments["enrollment_id"].dropna().astype(str)
)

expected_ids = expected["enrollment_id"].dropna().astype(str)

unmapped_expected = expected[
    ~expected["enrollment_id"].astype(str).isin(enrollment_ids)
]

print("\nExpected exceptions not mapped to enrollment rows:")
print(len(unmapped_expected))

print("\nUnmapped exception types:")
print(
    unmapped_expected["expected_exception_type"]
    .value_counts(dropna=False)
)

print("\nSample unmapped exceptions:")
print(
    unmapped_expected.head(10).to_string(index=False)
)

# ---------------------------------------------------------
# Diagnose multiple exceptions per enrollment
# ---------------------------------------------------------

mapped_expected = expected[
    expected["enrollment_id"].notna()
].copy()

exception_counts = (
    mapped_expected
    .groupby("enrollment_id")
    .size()
    .reset_index(name="exception_count")
)

multiple_exception_enrollments = exception_counts[
    exception_counts["exception_count"] > 1
]

print("\nMapped exception records:", len(mapped_expected))

print(
    "Unique enrollment IDs with exceptions:",
    mapped_expected["enrollment_id"].nunique(),
)

print(
    "Enrollments with multiple exception records:",
    len(multiple_exception_enrollments),
)

print(
    "Extra exception records from multi-exception enrollments:",
    (
        multiple_exception_enrollments["exception_count"] - 1
    ).sum(),
)

# ---------------------------------------------------------
# Feature engineering - dates
# ---------------------------------------------------------

date_columns = [
    "coverage_start_date",
    "coverage_end_date",
    "hire_date",
    "termination_date",
    "eligibility_start_date",
    "eligibility_end_date",
]

for column in date_columns:
    training[column] = pd.to_datetime(
        training[column],
        errors="coerce",
    )


# Employee tenure when coverage begins
training["tenure_days_at_coverage"] = (
    training["coverage_start_date"]
    - training["hire_date"]
).dt.days


# Days between requested coverage and eligibility start
training["eligibility_start_delay_days"] = (
    training["eligibility_start_date"]
    - training["coverage_start_date"]
).dt.days


print("\nFeature engineering checks:")

print(
    "Median tenure days at coverage:",
    training["tenure_days_at_coverage"].median(),
)

print(
    "Enrollments with delayed eligibility start:",
    (training["eligibility_start_delay_days"] > 0).sum(),
)

# ---------------------------------------------------------
# Feature engineering - pre-reconciliation features
# ---------------------------------------------------------

# Employee tenure at requested coverage date
training["tenure_days_at_coverage"] = (
    training["coverage_start_date"]
    - training["hire_date"]
).dt.days


# Whether employee was already terminated
# when requested coverage begins
training["terminated_before_coverage"] = (
    training["termination_date"].notna()
    & (
        training["termination_date"]
        < training["coverage_start_date"]
    )
).astype(int)


# Coverage year/month can capture temporal patterns
training["coverage_year"] = (
    training["coverage_start_date"].dt.year
)

training["coverage_month"] = (
    training["coverage_start_date"].dt.month
)


# Flag whether enrollment is for employee or dependent
training["is_dependent"] = (
    training["dependent_id"].notna()
).astype(int)


print("\nPre-reconciliation feature checks:")

print(
    "Terminated before coverage:",
    training["terminated_before_coverage"].sum(),
)

print(
    "Dependent enrollments:",
    training["is_dependent"].sum(),
)

print(
    "Coverage months:",
    sorted(
        training["coverage_month"]
        .dropna()
        .unique()
        .tolist()
    ),
)

# ---------------------------------------------------------
# Select final ML training columns
# ---------------------------------------------------------

training_dataset = training[
    [
        "enrollment_id",
        "employee_id",
        "employer_id_enrollment",
        "plan_id",
        "department",
        "state",
        "tenure_days_at_coverage",
        "coverage_month",
        "exception_flag",
    ]
].copy()

training_dataset = training_dataset.rename(
    columns={
        "employer_id_enrollment": "employer_id",
    }
)


# ---------------------------------------------------------
# Validate final training dataset
# ---------------------------------------------------------

print("\nFinal training dataset shape:")
print(training_dataset.shape)

print("\nFinal training columns:")
print(training_dataset.columns.tolist())

print("\nMissing values:")
print(training_dataset.isna().sum())


# ---------------------------------------------------------
# Save training dataset
# ---------------------------------------------------------

OUTPUT_FILE = (
    Path("ml/northstar/outputs")
    / "eligibility_exception_training.csv"
)

training_dataset.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("\nTraining dataset written to:")
print(OUTPUT_FILE)