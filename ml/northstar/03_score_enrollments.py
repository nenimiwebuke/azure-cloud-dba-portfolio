import joblib
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DATA_FILE = (
    "ml/northstar/outputs/"
    "eligibility_exception_training.csv"
)

MODEL_FILE = (
    "ml/northstar/outputs/"
    "eligibility_exception_model.joblib"
)

OUTPUT_FILE = (
    "ml/northstar/outputs/"
    "eligibility_exception_scored_queue.csv"
)


# ---------------------------------------------------------
# Load scoring dataset
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("Scoring dataset shape:", df.shape)


# ---------------------------------------------------------
# Load trained model
# ---------------------------------------------------------

model = joblib.load(MODEL_FILE)

print("Trained model loaded successfully.")

# ---------------------------------------------------------
# Prepare model features
# ---------------------------------------------------------

feature_columns = [
    "employer_id",
    "plan_id",
    "department",
    "state",
    "tenure_days_at_coverage",
    "coverage_month",
]

X_score = df[feature_columns]


# ---------------------------------------------------------
# Generate exception-risk probabilities
# ---------------------------------------------------------

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

scored["risk_score"] = (
    scored["exception_probability"] * 100
).round(2)

print("\nScoring complete.")
print("Records scored:", len(scored))

print("\nProbability summary:")
print(
    scored["exception_probability"]
    .describe()
    .round(4)
)

# ---------------------------------------------------------
# Assign relative operational risk tiers
# HIGH   = top 10%
# MEDIUM = next 20%
# LOW    = remaining 70%
# ---------------------------------------------------------

high_threshold = scored["exception_probability"].quantile(0.90)
medium_threshold = scored["exception_probability"].quantile(0.70)

scored["risk_tier"] = "LOW"

scored.loc[
    scored["exception_probability"] >= medium_threshold,
    "risk_tier",
] = "MEDIUM"

scored.loc[
    scored["exception_probability"] >= high_threshold,
    "risk_tier",
] = "HIGH"


# ---------------------------------------------------------
# Create prioritized operational queue
# ---------------------------------------------------------

scored = scored.sort_values(
    "exception_probability",
    ascending=False,
).reset_index(drop=True)

scored["priority_rank"] = range(
    1,
    len(scored) + 1,
)

print("\nOperational risk thresholds:")
print(f"HIGH threshold: {high_threshold:.4f}")
print(f"MEDIUM threshold: {medium_threshold:.4f}")

print("\nOperational risk tier distribution:")
print(scored["risk_tier"].value_counts())

print("\nTop 10 records for operational review:")
print(
    scored[
        [
            "priority_rank",
            "enrollment_id",
            "employee_id",
            "risk_score",
            "risk_tier",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ---------------------------------------------------------
# Write operational scoring queue
# ---------------------------------------------------------

scored.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("\nOperational scoring queue written to:")
print(OUTPUT_FILE)