# Azure Data Engineering & Cloud Data Platform Portfolio

A production-oriented Azure data engineering portfolio demonstrating end-to-end ingestion, PySpark transformation, Delta Lake Medallion processing, incremental data pipelines, analytical data products, machine learning, and cloud infrastructure automation.

The implementation combines Azure Databricks, Azure Data Lake Storage Gen2, Azure Data Factory, Azure SQL, Power BI, Terraform, GitHub Actions, Key Vault, and Azure identity services to demonstrate how reliable enterprise data workloads can be engineered and operated in the cloud.

The project also incorporates database engineering, Infrastructure as Code (IaC), security, observability, and CI/CD practices to demonstrate the operational depth required to run data platforms reliably beyond the notebook layer.

The reference implementation uses a fictional organization, **Northstar Benefits Group**, and synthetic data only. No employer-owned, customer, patient, member, or other production data is stored in this repository.

---

## Business Problem

Northstar Benefits Group represents an enterprise benefits organization that processes data from operational databases, employee and eligibility systems, claims and provider systems, enrollment files, partner-delivered files, and other sources.

The organization requires a centralized Azure data platform capable of supporting:

- Batch data ingestion and orchestration
- Bronze, Silver, and Gold Medallion transformations
- Incremental data processing using persisted watermarks and Delta Lake `MERGE`
- Governed analytical data products
- Data-quality and reconciliation workflows
- Power BI analytical consumption
- Machine learning and predictive risk scoring
- Secure operational and analytical data storage
- Cloud database workloads
- Secrets and identity management
- Monitoring and operational visibility
- Repeatable infrastructure deployment
- CI/CD and a foundation for controlled environment promotion

The Northstar implementation models an enterprise data-engineering workload in which operational and file-based source data is ingested into Azure, transformed through Medallion layers, incrementally maintained, and exposed to analytical and machine-learning consumers.

The supporting Azure infrastructure is managed as code and incorporates database engineering, security, identity, monitoring, and deployment practices required to operate the workload reliably.

---

## Architecture

The Northstar implementation follows an end-to-end Azure data-engineering architecture spanning source ingestion, Medallion processing, incremental data maintenance, analytics, machine learning, governance, and cloud infrastructure automation.

![Northstar Data Engineering Platform on Azure](docs/diagrams/northstar-data-engineering-architecture.png)

The architecture highlights the implemented data flow from operational and file-based source systems through Azure Data Factory, Azure Data Lake Storage Gen2, and Azure Databricks into curated analytical and machine-learning outputs.

The diagram also distinguishes implemented capabilities from target-state enhancements. Current delivery automation stops at a validated Terraform `plan`; approval-gated `terraform apply` and automated infrastructure promotion remain future-state capabilities.

Cross-cutting platform services include Azure SQL Database, Key Vault, Microsoft Entra ID, Unity Catalog, Log Analytics, Azure Storage, Terraform, and GitHub Actions.

Northstar Benefits Group is fictional, and all data represented in the architecture is synthetic and generated for portfolio and demonstration purposes.

Detailed architecture documentation is available under [`docs/architecture`](docs/architecture), with editable source diagrams maintained under [`docs/diagrams`](docs/diagrams).

---

## Medallion Architecture

The data-engineering design progressively refines data through logical processing layers.

### Landing

Immutable source deliveries and ingestion artifacts.

### Bronze

Raw or source-aligned records retained for traceability and replay.

### Silver

Validated, standardized, cleaned, deduplicated, and conformed data.

### Gold

Business-ready datasets, aggregations, and analytical models.

### Quarantine

Invalid or nonconforming records requiring investigation or remediation.

Bronze, Silver, and Gold storage are currently represented in the Azure Data Lake implementation. Landing and Quarantine are part of the target architecture and planned expansion.

---

## Northstar Data Engineering Implementation

**Northstar Benefits Group** is the primary end-to-end data-engineering workload implemented in this repository.

The synthetic workload models enterprise workforce, enrollment, dependent, and eligibility data moving through Azure Data Lake Storage and Databricks using a Medallion architecture.

The implementation demonstrates:

- Bronze ingestion of source-aligned enterprise datasets
- PySpark-based validation, standardization, and transformation
- Silver conformed datasets for employees, dependents, enrollments, and eligibility
- Data-quality validation and reconciliation patterns
- Gold analytical datasets for downstream consumption
- Delta Lake persistence and table management
- Unity Catalog registration of curated Gold datasets
- Incremental employee processing using a persisted watermark and Delta Lake `MERGE`
- Idempotent processing that prevents duplicate inserts during reruns
- Analytical consumption through Power BI
- Machine-learning feature engineering and operational risk prioritization

Northstar operates on synthetic datasets at a scale intended to demonstrate more realistic data-engineering behavior, including a 10,000-row employee population and more than 36,000 enrollment records.

Implementation notebooks are maintained under:

```text
notebooks/northstar/
```

The repository also retains earlier foundational examples covering ADLS Medallion processing, retail transformations, and Spark SQL analytics. These examples document the progression of the project but are secondary to the Northstar enterprise workload.

---

## Northstar Incremental Processing

The Northstar employee pipeline implements an incremental processing pattern using a persisted watermark and Delta Lake `MERGE`.

![Northstar Incremental Processing Pattern](docs/diagrams/northstar-incremental-processing-pattern.png)

The implementation demonstrates:

- Watermark-based filtering of newly arrived employee records
- Incremental processing without rebuilding the full Silver dataset
- Delta Lake `MERGE` semantics for inserts and updates
- Persistent watermark advancement after successful processing
- Idempotent reruns that prevent duplicate inserts
- Validation of updated and newly inserted employee records

The implementation is available in [`08_incremental_employee_merge.ipynb`](notebooks/northstar/08_incremental_employee_merge.ipynb).

During validation, a 10,000-row Silver employee dataset received an incremental batch containing two updates and two new employees. The resulting Silver dataset contained 10,002 rows, and the persisted watermark advanced to the latest successfully processed source timestamp.

---

## Power BI Executive Analytics

The **Northstar Workforce & Eligibility Executive Dashboard** provides an executive-level view of workforce distribution, employee activity, and eligibility reconciliation across the synthetic Northstar Benefits Group dataset.

The dashboard highlights:

- 10,000 total employees and 8,227 active employees
- 82.27% workforce coverage eligibility
- 17.73% termination rate
- Employee distribution by department and state
- Eligibility reconciliation with a 97.09% match rate
- Executive-level workforce insights for operational decision-making

![Northstar Workforce & Eligibility Executive Dashboard](powerbi/screenshots/northstar-workforce-executive-dashboard.png)

The Power BI report demonstrates the analytical consumption layer of the platform, transforming curated enterprise data into business-facing KPIs and visual insights.

---

## Machine Learning & Predictive Risk Scoring

The Northstar workload extends the enterprise data platform beyond descriptive analytics by introducing a machine-learning layer for eligibility reconciliation risk prioritization.

The objective is to determine whether information available before reconciliation can help operations teams prioritize enrollment records that are more likely to produce downstream eligibility exceptions.

### End-to-End Flow

```text
Northstar Source Data
        │
        ▼
ADLS Bronze
Raw enrollment, employee, dependent,
and eligibility data
        │
        ▼
Databricks Silver
Validated, standardized, deduplicated,
and conformed records
        │
        ▼
Gold Reconciliation
Business-ready eligibility reconciliation
and analytical datasets
        │
        ▼
ML Feature Engineering
Leakage-safe pre-reconciliation features
        │
        ▼
Model Training & Evaluation
Logistic Regression + Random Forest
        │
        ▼
Persisted Model
Reusable scikit-learn pipeline
        │
        ▼
Operational Scoring
Relative exception-risk ranking
        │
        ▼
Prioritized Review Queue
HIGH / MEDIUM / LOW
        │
        ▼
Power BI / Operations

```

### ML Pipeline

The implementation is separated into three stages:

- [`01_build_training_dataset.py`](ml/northstar/01_build_training_dataset.py) — constructs the enrollment-level training dataset and engineers leakage-safe features.
- [`02_train_exception_model.py`](ml/northstar/02_train_exception_model.py) — trains and compares classifiers, evaluates model performance, measures prioritization lift, and persists the selected model.
- [`03_score_enrollments.py`](ml/northstar/03_score_enrollments.py) — independently loads the trained model and produces a ranked operational review queue.

Detailed implementation notes are available in the [`Northstar ML README`](ml/northstar/README.md).

### Model Evaluation

The training dataset contains 36,397 enrollment records with a 4.77% exception rate.

Two classifiers were evaluated using the same leakage-safe train/test split:

| Model | ROC-AUC | Exception Recall | Exception Precision | Exception F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.5376 | 45.82% | 5.33% | 9.54% |
| Random Forest | 0.5191 | 29.68% | 5.55% | 9.35% |

Logistic Regression was retained for the scoring proof-of-concept because it provided stronger recall, F1, and ROC-AUC for the exception class.

### Operational Prioritization

Model output is treated as a **relative risk ranking**, not as a calibrated probability of failure.

The operational queue assigns:

- **HIGH** — top 10% of scored records
- **MEDIUM** — next 20%
- **LOW** — remaining 70%

On the held-out test set, the HIGH tier captured **14.12% of known exceptions while representing only 10% of records**, producing a **1.41x lift over the baseline exception rate**.

The HIGH + MEDIUM population captured **35.45% of exceptions within 30% of records**, producing a **1.18x lift**.

### Engineering Interpretation

The experiment demonstrates modest prioritization value but limited overall predictive strength from the currently available pre-reconciliation features.

The ML component is therefore presented as a **proof-of-concept**, not a production-ready prediction system.

A production implementation would require richer historical and operational signals such as prior reconciliation history, employer submission behavior, plan-change history, processing latency, file-quality metrics, and historical exception frequency.

---

## Infrastructure as Code

Azure infrastructure is managed using **Terraform**.

The project originally contained Azure resources directly in the root Terraform configuration. The infrastructure is being progressively refactored into reusable child modules while preserving the existing deployed Azure resources.

Terraform `moved` blocks are used during refactoring to change resource addresses without destroying and recreating the underlying Azure resources.

For example, a resource originally managed at a root address such as:

```text
azurerm_virtual_network.portfolio_vnet
```

can be moved to:

```text
module.networking.azurerm_virtual_network.this
```

while Terraform continues managing the same Azure resource.

This allows structural improvements to the codebase to be separated from functional infrastructure changes.

### Current Terraform Modules

```text
terraform/modules/
├── azure-sql/
├── data-factory/
├── data-lake/
├── key-vault/
├── log-analytics/
├── networking/
├── resource-group/
└── storage-account/
```

Each module follows a consistent structure:

```text
module/
├── main.tf
├── variables.tf
├── outputs.tf
└── versions.tf
```

The modules provide defined inputs and outputs, isolate infrastructure responsibilities, and prepare the platform for reusable environment deployments.

---

## Terraform Remote State

Terraform state is stored remotely in Azure Storage rather than relying on a workstation-local state file.

The remote backend provides a centralized source of truth for Terraform-managed infrastructure and allows the same environment to be administered from different workstations or Azure Cloud Shell.

The backend uses a dedicated Terraform state resource group, storage account, container, and state object separate from the workload resources being managed.

Sensitive values are not intended to be committed to source control.

---

## Azure Services

| Service | Responsibility |
|---|---|
| Azure Resource Group | Workload resource boundary |
| Azure Virtual Network | Network foundation |
| Azure Subnet | Workload network segmentation |
| Network Security Group | Network traffic controls |
| Azure Public IP | Public network endpoint for applicable lab resources |
| Azure Network Interface | Network interface for applicable compute workloads |
| Azure Storage | General-purpose object storage |
| Azure Data Lake Storage Gen2 | Medallion data lake |
| Azure Data Factory | Data ingestion and orchestration |
| Azure Databricks | Distributed data processing |
| Azure SQL Database | Relational database workload |
| Azure Key Vault | Secrets-management foundation |
| Azure Log Analytics | Centralized monitoring foundation |

---

## CI/CD

Continuous integration is implemented with GitHub Actions through `.github/workflows/ci.yml`.

The workflow runs automatically on pushes and pull requests targeting `main`.

Current CI validation includes:

- Python 3.12 environment setup
- Dependency installation for Northstar ML workloads
- Python syntax compilation checks for the Northstar ML scripts
- Terraform formatting validation with `terraform fmt -check -recursive`
- Terraform initialization with the remote backend disabled
- Terraform configuration validation with `terraform validate`

A continuous-delivery foundation is implemented through `.github/workflows/cd.yml` as a manually triggered Terraform planning workflow.

The CD workflow uses Azure OpenID Connect federation with a user-assigned managed identity, retrieves the SQL administrator password from Azure Key Vault, initializes the remote Terraform backend, refreshes Azure resource state, and executes a real Terraform plan against the deployed environment.

The validated CD workflow currently stops at `terraform plan`. Automatic `terraform apply` is intentionally not enabled. A future controlled promotion stage can introduce GitHub Environment approvals and an explicitly approved apply step.

---

## Architecture Decision Records

Important platform decisions are documented explicitly through Architecture Decision Records (ADRs):

```text
docs/adr/
├── ADR-0001-platform-scope.md
├── ADR-0002-terraform-standard.md
└── ADR-0003-environment-strategy.md
```

Current ADRs document decisions concerning:

- Platform scope and workload boundaries
- Terraform as the Infrastructure as Code standard
- Environment strategy

This provides a record of not only **what** was implemented, but **why** architectural decisions were made.

---

## Architecture Documentation

Detailed platform documentation is maintained alongside the implementation:

```text
docs/architecture/
├── environment-strategy.md
├── logical-architecture.md
├── naming-standards.md
└── platform-overview.md
```

Architecture diagram source files are maintained under:

```text
docs/diagrams/
├── enterprise-data-platform.drawio
└── enterprise-data-platform-enhanced.drawio
```

The documentation describes platform scope, logical architecture, naming conventions, environment strategy, security direction, data architecture, and target-state capabilities.

---

## Repository Structure

```text
azure-cloud-dba-portfolio/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── docs/
│   ├── adr/
│   ├── architecture/
│   ├── data-contracts/
│   └── diagrams/
│       ├── enterprise-data-platform.drawio
│       ├── enterprise-data-platform-enhanced.drawio
│       ├── northstar-data-engineering-architecture.png
│       └── northstar-incremental-processing-pattern.png
│
├── notebooks/
│   ├── common/
│   │   ├── audit.py
│   │   ├── contracts.py
│   │   ├── metrics.py
│   │   ├── paths.py
│   │   └── validation.py
│   │
│   ├── northstar/
│   │   ├── 01_bronze_to_silver_employees.py
│   │   ├── 02_bronze_to_silver_dependents.ipynb
│   │   ├── 03_bronze_to_silver_enrollments.ipynb
│   │   ├── 04_bronze_to_silver_eligibility.ipynb
│   │   ├── 05_silver_to_gold_employees.ipynb
│   │   ├── 06_gold_eligibility_reconciliation.ipynb
│   │   ├── 07_register_gold_tables.ipynb
│   │   └── 08_incremental_employee_merge.ipynb
│   │
│   └── archive/
│       ├── 01_ADLS_Bronze_Silver_Gold_Pipeline.py
│       ├── 02_Retail_Sales_Bronze_Silver_Gold.py
│       └── 03_SQL_Analytics_Gold_Data.sql
│
├── ml/
│   └── northstar/
│       ├── README.md
│       ├── 01_build_training_dataset.py
│       ├── 02_train_exception_model.py
│       └── 03_score_enrollments.py
│
├── powerbi/
│   ├── Northstar_Executive_Analytics.pbix
│   └── screenshots/
│       └── northstar-workforce-executive-dashboard.png
│
├── scripts/
│   └── generate_northstar_data.py
│
├── terraform/
│   ├── modules/
│   │   ├── azure-sql/
│   │   ├── databricks/
│   │   ├── data-factory/
│   │   ├── data-lake/
│   │   ├── key-vault/
│   │   ├── log-analytics/
│   │   ├── networking/
│   │   ├── resource-group/
│   │   └── storage-account/
│   ├── databricks-storage-access.tf
│   ├── main.tf
│   ├── outputs.tf
│   └── variables.tf
│
├── data/
│   ├── employees.csv
│   └── sales.csv
│
├── .gitignore
├── LICENSE
└── README.md
```

The repository is organized around the Northstar data-engineering workload, with reusable notebook utilities, documented data contracts, analytical and machine-learning consumers, and the supporting Azure infrastructure maintained alongside the workload code.

The original retail and introductory Medallion examples are retained under `notebooks/archive/` to preserve the project evolution while keeping the Northstar implementation as the primary engineering reference.

---

## Engineering Principles

The platform is being developed around several core engineering principles:

- Infrastructure as Code instead of portal-driven deployment
- Version-controlled infrastructure and data-engineering code
- Modular and reusable Terraform
- Remote infrastructure state
- Separation of infrastructure responsibilities
- State-safe infrastructure refactoring
- Separation of structural refactoring from functional changes
- Secure handling of credentials and secrets
- Least-privilege access as a target security model
- Repeatable environment deployment
- Medallion data architecture
- Architecture decisions documented alongside code
- Monitoring and operational support as platform concerns
- Synthetic data for portfolio workloads

---

## Current Implementation Status

### Implemented

- Azure workload resource group
- Azure networking foundation
- Virtual network and subnet
- Network Security Group and subnet association
- Public IP and network interface
- General-purpose Azure Storage
- Azure Data Lake Storage Gen2
- Bronze, Silver, and Gold storage layers
- Azure SQL logical server
- Azure SQL Database
- Azure SQL firewall configuration
- Azure Data Factory
- Azure Databricks workspace
- Azure Key Vault
- Azure Log Analytics workspace
- Terraform remote state in Azure Storage
- Modular Terraform for major platform components, including Azure Databricks
- State-preserving Terraform refactoring using `moved` blocks
- Common resource tagging structure
- PySpark Medallion transformations and Spark SQL analytics
- Delta Lake processing
- Gold table registration in Unity Catalog
- Northstar Bronze-to-Silver-to-Gold data engineering workflows
- Watermark-based incremental employee processing with Delta Lake `MERGE`
- Persisted incremental-processing watermark and idempotent rerun behavior
- Northstar machine-learning risk-prioritization proof of concept
- Power BI executive analytics dashboard
- Architecture documentation
- Architecture Decision Records
- Naming and tagging standards
- GitHub Actions continuous integration
- GitHub Actions continuous-delivery planning workflow
- Azure OpenID Connect authentication for GitHub Actions
- User-assigned managed identity for deployment authentication
- Azure Key Vault secret retrieval during CD execution
- Remote Terraform plan execution against Azure
- Automated Python syntax validation for Northstar ML workloads
- Automated Terraform formatting validation
- Automated Terraform initialization without remote backend access in CI
- Automated Terraform configuration validation

### In Progress

- Data-quality controls
- Security hardening
- Monitoring and diagnostic integration
- Environment separation
- Controlled Terraform apply and environment approval workflow

### Planned

- Landing and Quarantine layers
- Metadata-driven ingestion
- Retry and failure handling
- Audit logging and row-count reconciliation
- Expanded Azure RBAC
- Private connectivity where appropriate
- Azure resource diagnostic settings
- Data-quality and freshness monitoring
- Terraform security scanning in CI
- Python linting and automated testing
- Operational alerts and runbooks
- Expanded machine learning and Azure AI workloads

---

## Terraform Workflow

A typical Terraform workflow for the project is:

```bash
terraform -chdir=terraform fmt -recursive
terraform -chdir=terraform init
terraform -chdir=terraform validate
terraform -chdir=terraform plan
terraform -chdir=terraform apply
```

Before applying infrastructure changes, Terraform plans are reviewed to understand whether resources will be created, modified, destroyed, or simply moved to new Terraform addresses.

During module refactoring, a successful migration should ideally produce:

```text
Plan: 0 to add, 0 to change, 0 to destroy.
```

This confirms that Terraform's configuration structure changed without modifying the underlying Azure infrastructure.

---

## Git Workflow

Infrastructure and documentation changes are version controlled in Git.

A typical workflow includes:

```bash
git status
git add <files>
git commit -m "descriptive commit message"
git pull --rebase origin main
git push origin main
```

The repository history intentionally records the platform's evolution, including architecture documentation, Terraform modularization, state-safe refactoring, and infrastructure improvements.

---

## Project Evolution

This repository began as a practical Azure data-engineering workload demonstrating a retail sales Medallion pipeline.

It has since evolved into a broader **Azure cloud database and enterprise data platform engineering portfolio**.

The project now demonstrates not only how individual Azure services are deployed, but how an existing cloud environment can be progressively improved through:

- Infrastructure as Code
- Terraform modularization
- Remote state management
- State-safe refactoring
- Cloud database engineering
- Data engineering
- Architecture documentation
- Security design
- Environment strategy
- Operational thinking
- Version control

The evolution is intentionally visible in the Git history and documentation.

---

## Roadmap

Future expansion of the project can focus on:

1. Expand Azure Data Factory orchestration and metadata-driven ingestion.
2. Add Landing and Quarantine processing patterns.
3. Add data-quality, freshness, row-count, and reconciliation controls.
4. Strengthen RBAC, private connectivity, and network security.
5. Expand Azure resource diagnostics, Log Analytics, and operational alerting.
6. Add retry, failure-handling, and operational runbook patterns.
7. Add Terraform security scanning, Python linting, and automated testing.
8. Introduce approval-gated Terraform apply and controlled environment promotion.
9. Expand Unity Catalog governance and environment separation.
10. Extend the analytical and machine-learning workloads toward future Azure AI use cases.

---

## Disclaimer

This repository is an independent portfolio and learning project.

**Northstar Benefits Group is fictional.** All organizations, business scenarios, datasets, credentials, and workloads represented in this project are fictional or synthetic.

The repository does not contain proprietary employer information, customer information, production credentials, personally identifiable production data, or production workloads.
