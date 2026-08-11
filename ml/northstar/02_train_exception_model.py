import pandas as pd

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
