# Logical Architecture

## Document Control

| Attribute | Value |
|------------|-------|
| Document | Logical Architecture |
| Platform | Enterprise Azure Data Platform |
| Repository | azure-data-engineering-portfolio |
| Status | Active |
| Owner | Data Platform Engineering |
| Last Reviewed | 2026-07-20 |

---

# Purpose

This document describes the logical architecture of the Enterprise Azure Data Platform.

It explains how data moves through the platform, how Azure services interact, and how the platform supports secure, scalable, and repeatable data engineering workloads.

Unlike a physical architecture document, this document focuses on **functional responsibilities** rather than Azure resource deployment details.

---

# Architectural Principles

The platform follows the following engineering principles.

## Infrastructure as Code

All Azure infrastructure is provisioned using Terraform.

Manual Azure Portal changes are avoided except for:

- troubleshooting
- validation
- investigation

Terraform remains the source of truth.

---

## Security by Default

The platform prioritizes:

- Microsoft Entra ID authentication
- Managed Identities
- Azure Key Vault
- Least Privilege RBAC
- Private connectivity where justified
- No secrets committed to Git

---

## Layered Architecture

Each platform responsibility belongs to a specific layer.

This separation improves:

- maintainability
- scalability
- testing
- operational ownership

---

# High-Level Data Flow

```
                 Source Systems
                        │
                        ▼
              Azure Data Factory
                        │
                        ▼
             Azure Data Lake Gen2
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    Landing          Quarantine      Bronze
                                          │
                                          ▼
                                      Silver
                                          │
                                          ▼
                                        Gold
                                          │
                                          ▼
                            Analytics / Data Products
```

---

# Source Systems

The platform is designed to ingest data from multiple enterprise systems.

Supported source categories include:

- SQL Server
- Azure SQL Database
- CSV files
- JSON files
- REST APIs (future)
- Third-party partner feeds

Each source is treated as an independent producer.

No assumptions are made regarding source quality.

---

# Ingestion Layer

## Azure Data Factory

Azure Data Factory is responsible for orchestrating data movement.

Responsibilities include:

- scheduling
- metadata-driven pipelines
- incremental loading
- retry handling
- audit logging
- parameterization
- source validation

ADF is intentionally kept focused on orchestration rather than complex transformations.

Business transformations occur inside Databricks.

---

# Storage Layer

## Azure Data Lake Storage Gen2

ADLS Gen2 is the central storage platform.

Logical containers include:

```
Landing
Quarantine
Bronze
Silver
Gold
```

### Landing

Stores raw incoming files.

### Quarantine

Stores rejected records.

### Bronze

Stores source-aligned records.

### Silver

Stores cleaned and validated datasets.

### Gold

Stores business-ready datasets.

---

# Processing Layer

## Azure Databricks

Azure Databricks performs distributed data engineering workloads.

Responsibilities include:

- Spark transformations
- Delta Lake processing
- schema enforcement
- data validation
- deduplication
- business rule implementation
- aggregation

Databricks is the primary transformation engine.

---

# Delta Lake

Delta Lake provides:

- ACID transactions
- schema evolution
- time travel
- scalable storage
- reliable updates

Delta tables represent the authoritative analytical datasets.

---

# Serving Layer

Business users consume Gold datasets through:

- Databricks SQL
- Azure SQL analytical marts
- Power BI
- future AI workloads

Serving datasets are optimized for business consumption rather than operational storage.

---

# Cross-Cutting Services

The following services support every architectural layer.

## Azure Key Vault

Stores secrets and certificates.

---

## Azure Monitor

Collects metrics and alerts.

---

## Log Analytics

Centralizes operational logs.

---

## Managed Identities

Provides passwordless authentication between Azure services.

---

## GitHub Actions

Automates:

- validation
- testing
- deployment
- documentation checks

---

# Security Architecture

Security is identity-first.

Preferred authentication order:

1. Managed Identity
2. Microsoft Entra ID
3. Azure Key Vault
4. Service Principal (only when required)

Storage account keys are not used for application authentication.

---

# Monitoring Strategy

The platform captures telemetry from:

- Azure Data Factory
- Databricks
- Azure SQL
- Storage
- Terraform deployments

Operational metrics include:

- pipeline duration
- failed executions
- record counts
- data freshness
- cost
- storage growth

---

# Network Architecture

Logical network segmentation includes:

```
Virtual Network

├── Data Subnet
├── Databricks Subnet
├── Private Endpoint Subnet
```

Private networking will be introduced where it adds architectural value without creating unnecessary portfolio cost.

---

# Technology Responsibilities

| Technology | Responsibility |
|------------|----------------|
| Terraform | Infrastructure provisioning |
| Azure Data Factory | Pipeline orchestration |
| ADLS Gen2 | Enterprise data lake |
| Azure Databricks | Data engineering |
| Spark | Distributed processing |
| Delta Lake | Reliable storage layer |
| Azure SQL | Operational and serving database |
| Azure Monitor | Metrics |
| Log Analytics | Centralized logging |
| GitHub Actions | CI/CD |
| Key Vault | Secrets management |

---

# Future Architecture

Future phases include:

- Unity Catalog
- CI/CD promotion
- Private Endpoints
- Feature Engineering
- MLflow
- Azure AI
- Retrieval-Augmented Generation (RAG)
- AI-powered data assistant

These capabilities will be added only after the core data platform is complete.

---

# Related Documentation

- Platform Overview
- Environment Strategy
- Naming Standards
- ADR-0001 Platform Scope