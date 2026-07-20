# Enterprise Azure Data Platform — Platform Overview

## Document Control

| Attribute | Value |
|---|---|
| Document | Platform Overview |
| Platform | Enterprise Azure Data Platform |
| Repository | `azure-cloud-dba-portfolio` |
| Status | Active |
| Owner | Data Platform Engineering |
| Infrastructure Standard | Terraform |
| Primary Cloud | Microsoft Azure |
| Last Reviewed | 2026-07-19 |

---

## 1. Executive Summary

This repository implements a production-oriented enterprise data platform on Microsoft Azure.

The platform demonstrates how an organization can securely ingest operational data, store it in Azure Data Lake Storage Gen2, transform it through a governed lakehouse architecture, and publish trusted data products for analytics, reporting, and future artificial intelligence workloads.

The solution is designed as an **application landing zone** that would operate within a broader enterprise Azure environment. It does not attempt to reproduce an entire organization-wide cloud landing zone inside a personal subscription. Instead, it focuses on the workload responsibilities normally owned by a data platform engineering team:

- Infrastructure provisioning
- Workload networking
- Identity and access management
- Secrets management
- Data ingestion
- Data transformation
- Data quality
- Data storage
- Analytics enablement
- Monitoring and operational support
- Continuous integration and deployment

All Azure infrastructure is managed through Terraform. Manual portal deployment is used only for investigation, troubleshooting, or validation—not as the authoritative deployment method.

The platform is intentionally designed beyond tutorial-level implementation. Every resource must have a documented responsibility, defined security boundary, operational purpose, and lifecycle strategy.

---

## 2. Business Context

The reference implementation represents a fictional enterprise organization named **Northstar Benefits Group**.

Northstar administers employee benefits and processes data from several operational and external systems, including:

- SQL Server membership databases
- Azure SQL operational applications
- Employee and eligibility records
- Claims and provider data
- Employer enrollment files
- Partner-delivered CSV and JSON files
- Reference and configuration data
- Future REST API integrations

The organization requires a centralized platform that can:

1. Ingest data from heterogeneous sources.
2. Preserve source data for traceability and replay.
3. Validate and standardize incoming records.
4. Quarantine invalid or nonconforming data.
5. Transform operational data into analytical models.
6. provide trusted datasets for business reporting.
7. Record operational and data-quality metrics.
8. Enforce least-privilege access.
9. support repeatable deployment across environments.
10. Establish a governed foundation for future machine learning and AI workloads.

All data used by this repository is synthetic. No proprietary, employer-owned, customer, patient, member, or personally identifiable production data is stored in the project.

---

## 3. Platform Objectives

The platform is designed to satisfy the following objectives.

### 3.1 Repeatable infrastructure

Azure resources must be provisioned consistently through version-controlled Terraform configurations.

Infrastructure changes must be:

- Reviewable
- Testable
- Repeatable
- Auditable
- Environment-aware
- Recoverable

### 3.2 Secure-by-default design

The architecture prioritizes:

- Microsoft Entra ID authentication
- Managed identities
- Least-privilege role-based access control
- Azure Key Vault
- Controlled network access
- Private connectivity where justified
- Encryption in transit and at rest
- Removal of long-lived credentials from source code and CI/CD systems

### 3.3 Reliable data ingestion

Azure Data Factory provides orchestration for batch and hybrid ingestion patterns.

Pipelines will support:

- Parameterized execution
- Metadata-driven ingestion
- Full and incremental loads
- Retry handling
- Audit logging
- Row-count reconciliation
- Failure capture
- Quarantine processing
- Operational correlation identifiers

### 3.4 Governed lakehouse processing

Azure Databricks, Apache Spark, Delta Lake, and Unity Catalog provide the data-processing and governance foundation.

Data is progressively refined through the Medallion Architecture:

- **Landing** — immutable source deliveries and ingestion artifacts
- **Bronze** — source-aligned records with ingestion metadata
- **Silver** — validated, standardized, deduplicated, and conformed data
- **Gold** — business-ready data products and analytical models
- **Quarantine** — rejected records requiring investigation or remediation

### 3.5 Operational visibility

The platform must expose sufficient telemetry to support production operations.

Observability will include:

- Azure resource diagnostic logs
- Azure Data Factory pipeline metrics
- Databricks workflow execution status
- Data-ingestion volumes
- Data-quality measurements
- Data-freshness indicators
- Failure alerts
- Cost visibility
- Log Analytics queries
- Operational runbooks

### 3.6 Controlled delivery

GitHub Actions will provide CI/CD capabilities for infrastructure, application code, data-engineering code, and documentation.

The delivery model will include:

- Pull-request validation
- Terraform formatting and validation
- Static analysis
- Security scanning
- Terraform plan review
- Python linting and unit testing
- Environment approvals
- OpenID Connect authentication to Azure
- Controlled deployment promotion

---

## 4. Architecture Overview

The platform follows a layered architecture.

```text
┌──────────────────────────────────────────────────────────────┐
│                       Source Systems                         │
│                                                              │
│  SQL Server │ Azure SQL │ CSV/JSON │ Partner Files │ APIs   │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Ingestion and Orchestration               │
│                                                              │
│                    Azure Data Factory                        │
│                                                              │
│  Metadata-driven pipelines │ Incremental loads │ Auditing   │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                      Data Lake Storage                       │
│                                                              │
│                    Azure Data Lake Gen2                      │
│                                                              │
│  Landing │ Quarantine │ Bronze │ Silver │ Gold              │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     Processing and Governance                │
│                                                              │
│  Azure Databricks │ Apache Spark │ Delta Lake               │
│  Unity Catalog │ Data Quality │ Schema Enforcement          │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                   Consumption and Data Products              │
│                                                              │
│  Databricks SQL │ Azure SQL Marts │ Power BI                │
│  Machine Learning │ Azure AI Services — future phases       │
└──────────────────────────────────────────────────────────────┘