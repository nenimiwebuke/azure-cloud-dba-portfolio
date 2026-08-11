import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ---------------------------------------------------------
# Load ML training dataset
# ---------------------------------------------------------

DATA_FILE = (
    "ml/northstar/outputs/"
    "eligibility_exception_training.csv"
)

df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)

print("\nTarget distribution:")
print(df["exception_flag"].value_counts())

print("\nTarget percentage:")
print(
    df["exception_flag"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# ---------------------------------------------------------
# Define features and target
# ---------------------------------------------------------

feature_columns = [
    "employer_id",
    "plan_id",
    "department",
    "state",
    "tenure_days_at_coverage",
    "coverage_month",
]

X = df[feature_columns]
y = df["exception_flag"]


# ---------------------------------------------------------
# Train / test split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))

print(
    "Training exception rate:",
    f"{y_train.mean() * 100:.2f}%"
)

print(
    "Testing exception rate:",
    f"{y_test.mean() * 100:.2f}%"
)


# ---------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------

categorical_features = [
    "employer_id",
    "plan_id",
    "department",
    "state",
]

numeric_features = [
    "tenure_days_at_coverage",
    "coverage_month",
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
        (
            "numeric",
            StandardScaler(),
            numeric_features,
        ),
    ]
)


# ---------------------------------------------------------
# Baseline classifier
# ---------------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42,
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# ---------------------------------------------------------
# Train model
# ---------------------------------------------------------

pipeline.fit(X_train, y_train)

print("\nModel training complete.")


# ---------------------------------------------------------
# Evaluate model
# ---------------------------------------------------------

y_pred = pipeline.predict(X_test)

y_prob = pipeline.predict_proba(X_test)[:, 1]

print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        digits=4,
    )
)

print(
    "ROC-AUC:",
    round(
        roc_auc_score(
            y_test,
            y_prob,
        ),
        4,
    ),
)

# ---------------------------------------------------------
# Random Forest classifier
# ---------------------------------------------------------

rf_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)

rf_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", rf_model),
    ]
)

rf_pipeline.fit(X_train, y_train)

print("\nRandom Forest training complete.")


# ---------------------------------------------------------
# Evaluate Random Forest
# ---------------------------------------------------------

rf_pred = rf_pipeline.predict(X_test)

rf_prob = rf_pipeline.predict_proba(X_test)[:, 1]

print("\nRandom Forest confusion matrix:")
print(confusion_matrix(y_test, rf_pred))

print("\nRandom Forest classification report:")
print(
    classification_report(
        y_test,
        rf_pred,
        digits=4,
    )
)

print(
    "Random Forest ROC-AUC:",
    round(
        roc_auc_score(
            y_test,
            rf_prob,
        ),
        4,
    ),
)

# ---------------------------------------------------------
# Create operational risk-scoring output
# ---------------------------------------------------------

risk_results = df.loc[X_test.index, [
    "enrollment_id",
    "employee_id",
    "employer_id",
    "plan_id",
    "department",
    "state",
    "exception_flag",
]].copy()

risk_results["exception_probability"] = y_prob

risk_results["risk_score"] = (
    risk_results["exception_probability"] * 100
).round(2)


# ---------------------------------------------------------
# Assign relative risk tiers
# HIGH   = top 10%
# MEDIUM = next 20%
# LOW    = remaining 70%
# ---------------------------------------------------------

high_threshold = risk_results["exception_probability"].quantile(0.90)
medium_threshold = risk_results["exception_probability"].quantile(0.70)

risk_results["risk_tier"] = "LOW"

risk_results.loc[
    risk_results["exception_probability"] >= medium_threshold,
    "risk_tier",
] = "MEDIUM"

risk_results.loc[
    risk_results["exception_probability"] >= high_threshold,
    "risk_tier",
] = "HIGH"

print("\nRisk tier thresholds:")
print(f"HIGH threshold: {high_threshold:.4f}")
print(f"MEDIUM threshold: {medium_threshold:.4f}")


# ---------------------------------------------------------
# Prioritize highest-risk records
# ---------------------------------------------------------

risk_results = risk_results.sort_values(
    "exception_probability",
    ascending=False,
)

print("\nRisk tier distribution:")
print(risk_results["risk_tier"].value_counts())

print("\nTop 10 highest-risk enrollments:")
print(
    risk_results[
        [
            "enrollment_id",
            "employee_id",
            "exception_probability",
            "risk_score",
            "risk_tier",
            "exception_flag",
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ---------------------------------------------------------
# Write scored records
# ---------------------------------------------------------

OUTPUT_FILE = (
    "ml/northstar/outputs/"
    "eligibility_exception_risk_scores.csv"
)

risk_results.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("\nRisk scores written to:")
print(OUTPUT_FILE)

# ---------------------------------------------------------
# Evaluate operational prioritization
# ---------------------------------------------------------

total_exceptions = int(risk_results["exception_flag"].sum())

high_risk = risk_results[
    risk_results["risk_tier"] == "HIGH"
]

top_30 = risk_results[
    risk_results["risk_tier"].isin(["HIGH", "MEDIUM"])
]

high_exceptions = int(
    high_risk["exception_flag"].sum()
)

top_30_exceptions = int(
    top_30["exception_flag"].sum()
)

high_capture_rate = (
    high_exceptions / total_exceptions
)

top_30_capture_rate = (
    top_30_exceptions / total_exceptions
)

overall_exception_rate = (
    risk_results["exception_flag"].mean()
)

high_exception_rate = (
    high_risk["exception_flag"].mean()
)

top_30_exception_rate = (
    top_30["exception_flag"].mean()
)


print("\nOperational prioritization evaluation:")

print(
    f"Total test-set exceptions: "
    f"{total_exceptions}"
)

print(
    f"Exceptions captured in HIGH tier: "
    f"{high_exceptions} / {total_exceptions} "
    f"({high_capture_rate:.2%})"
)

print(
    f"Exceptions captured in HIGH + MEDIUM tiers: "
    f"{top_30_exceptions} / {total_exceptions} "
    f"({top_30_capture_rate:.2%})"
)

print(
    f"Overall exception rate: "
    f"{overall_exception_rate:.2%}"
)

print(
    f"HIGH-tier exception rate: "
    f"{high_exception_rate:.2%}"
)

print(
    f"Top-30% exception rate: "
    f"{top_30_exception_rate:.2%}"
)

# ---------------------------------------------------------
# Calculate prioritization lift
# ---------------------------------------------------------

high_lift = (
    high_exception_rate
    / overall_exception_rate
)

top_30_lift = (
    top_30_exception_rate
    / overall_exception_rate
)

print("\nPrioritization lift:")

print(
    f"HIGH-tier lift vs baseline: "
    f"{high_lift:.2f}x"
)

print(
    f"Top-30% lift vs baseline: "
    f"{top_30_lift:.2f}x"
)