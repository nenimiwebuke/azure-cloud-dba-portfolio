# Northstar Machine Learning Layer

This folder contains the machine learning extension of the Northstar data platform.

The goal is to evaluate whether pre-reconciliation enrollment and employee attributes can help prioritize records that are more likely to produce eligibility reconciliation exceptions.

## Workflow

1. `01_build_training_dataset.py`
   - Loads enrollment, employee, eligibility, and expected reconciliation data.
   - Validates joins and exception mappings.
   - Engineers leakage-safe pre-reconciliation features.
   - Creates the binary `exception_flag` target.
   - Produces a model-ready training dataset.

2. `02_train_exception_model.py`
   - Splits the data into stratified training and test sets.
   - Encodes categorical features and scales numeric features.
   - Trains Logistic Regression and Random Forest classifiers.
   - Evaluates precision, recall, F1 score, confusion matrices, and ROC-AUC.
   - Measures operational prioritization lift.
   - Persists the selected Logistic Regression pipeline with `joblib`.

3. `03_score_enrollments.py`
   - Loads the persisted model.
   - Scores enrollment records independently of model training.
   - Produces a relative risk score and priority rank.
   - Assigns:
     - HIGH = top 10%
     - MEDIUM = next 20%
     - LOW = remaining 70%
   - Writes a prioritized operational review queue.

## Training Dataset

The enrollment-level dataset contains:

- 36,397 enrollment records
- 1,735 enrollment records with known reconciliation exceptions
- 4.77% positive exception rate

The 72 `UNKNOWN_EMPLOYEE` reconciliation exceptions were excluded from the enrollment-level ML target because they do not have an enrollment record and are better handled through deterministic data-quality rules.

## Leakage Prevention

Post-reconciliation indicators were deliberately excluded from model training.

Examples include:

- Missing eligibility records
- Eligibility start delays
- Duplicate active eligibility matches
- Expected exception type
- Expected severity
- Expected business impact

These fields would reveal or closely encode the reconciliation outcome and would artificially inflate model performance.

## Model Comparison

### Logistic Regression

- ROC-AUC: 0.5376
- Exception recall: 45.82%
- Exception precision: 5.33%
- Exception F1: 9.54%

### Random Forest

- ROC-AUC: 0.5191
- Exception recall: 29.68%
- Exception precision: 5.55%
- Exception F1: 9.35%

Logistic Regression was retained for the scoring proof-of-concept because it provided better exception recall, F1 score, and ROC-AUC on the same leakage-safe test set.

## Operational Prioritization

Rather than treating the model output as a calibrated probability, scores are used as relative prioritization rankings.

On the held-out test set:

- Overall exception rate: 4.77%
- HIGH-tier exception rate: 6.73%
- HIGH tier captured 14.12% of exceptions while representing 10% of records
- HIGH-tier lift versus baseline: 1.41x
- HIGH + MEDIUM tiers captured 35.45% of exceptions while representing 30% of records
- Top-30% lift versus baseline: 1.18x

## Interpretation

The available pre-reconciliation features provide modest prioritization lift but limited overall predictive strength.

This model should therefore be interpreted as a proof-of-concept rather than a production-ready prediction system.

A production implementation would benefit from richer historical and operational features such as prior reconciliation history, employer submission behavior, plan-change history, file-quality metrics, processing latency, and historical exception frequency.

## Generated Artifacts

Generated datasets and trained model artifacts are intentionally excluded from Git using `.gitignore`.

Examples include:

- `eligibility_exception_training.csv`
- `eligibility_exception_model.joblib`
- `eligibility_exception_scored_queue.csv`

These artifacts are reproducible by running the Python scripts in sequence.