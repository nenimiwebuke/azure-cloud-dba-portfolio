import sys
from pathlib import Path

import joblib
import pandas as pd

for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "ml" / "common").exists():
        repository_root = str(candidate)
        if repository_root not in sys.path:
            sys.path.insert(0, repository_root)
        break

from ml.common.paths import MLPaths

PATHS = MLPaths(business_case="northstar")

DATA_FILE = PATHS.output_file("eligibility_exception_training.csv")
MODEL_FILE = PATHS.output_file("eligibility_exception_model.joblib")
OUTPUT_FILE = PATHS.output_file("eligibility_exception_scored_queue.csv")

df = pd.read_csv(DATA_FILE)

print("Scoring dataset shape:", df.shape)

model = joblib.load(MODEL_FILE)

print("Trained model loaded successfully.")

feature_columns = [
    "employer_id",
    "plan_id",
    "department",
    "state",
    "tenure_days_at_coverage",
    "coverage_month",
]

X_score = df[feature_columns]

exception_probability = model.predict_proba(X_score)[:, 1]

scored = df[
    [
        "enrollment_id",
        "employee_id",
        "employer_id",
        "plan_id",
        "department",
        "state",
    ]
].copy()

scored["exception_probability"] = exception_probability
scored["risk_score"] = (scored["exception_probability"] * 100).round(2)

print("\nScoring complete.")
print("Records scored:", len(scored))
print("\nProbability summary:")
print(scored["exception_probability"].describe().round(4))

high_threshold = scored["exception_probability"].quantile(0.90)
medium_threshold = scored["exception_probability"].quantile(0.70)

scored["risk_tier"] = "LOW"
scored.loc[scored["exception_probability"] >= medium_threshold, "risk_tier"] = "MEDIUM"
scored.loc[scored["exception_probability"] >= high_threshold, "risk_tier"] = "HIGH"

scored = scored.sort_values("exception_probability", ascending=False).reset_index(
    drop=True
)
scored["priority_rank"] = range(1, len(scored) + 1)

print("\nOperational risk thresholds:")
print(f"HIGH threshold: {high_threshold:.4f}")
print(f"MEDIUM threshold: {medium_threshold:.4f}")
print("\nOperational risk tier distribution:")
print(scored["risk_tier"].value_counts())
print("\nTop 10 records for operational review:")
print(
    scored[
        ["priority_rank", "enrollment_id", "employee_id", "risk_score", "risk_tier"]
    ]
    .head(10)
    .to_string(index=False)
)

PATHS.ensure_outputs_dir()

scored.to_csv(OUTPUT_FILE, index=False)

print("\nOperational scoring queue written to:")
print(OUTPUT_FILE)
