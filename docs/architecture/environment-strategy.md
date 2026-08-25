# Environment Strategy

## Document Control

| Attribute | Value |
|------------|-------|
| Document | Environment Strategy |
| Platform | Enterprise Azure Data Platform |
| Repository | azure-data-engineering-portfolio |
| Status | Active |
| Owner | Data Platform Engineering |
| Last Reviewed | 2026-07-20 |

---

# Purpose

This document defines how the Enterprise Azure Data Platform is deployed, managed, promoted, and isolated across environments.

The strategy is designed to balance enterprise engineering practices with the practical constraints of a personal Azure subscription.

Rather than maintaining three permanently deployed environments, the repository separates **logical architecture** from **physical deployment**. This allows the project to demonstrate production-grade engineering while remaining cost-effective.

---

# Environment Objectives

The environment strategy is designed to achieve the following objectives:

- Isolate workloads across environments.
- Prevent unintended changes from reaching production.
- Support repeatable deployments through Terraform.
- Minimize Azure costs during portfolio development.
- Enable future CI/CD automation.
- Provide a realistic enterprise deployment model.

---

# Environment Model

The platform supports three logical environments.

```text
Development
        │
        ▼
Test
        │
        ▼
Production
```

Each environment represents an independent deployment boundary.

---

# Development Environment

Purpose:

Active engineering and experimentation.

Typical activities:

- Terraform development
- Module validation
- Azure resource deployment
- Databricks notebook development
- Azure Data Factory pipeline development
- Integration testing
- Documentation updates

Characteristics:

- Lowest operational risk
- Fast iteration
- Frequent changes
- Primary persistent Azure deployment

---

# Test Environment

Purpose:

Validate infrastructure and data engineering changes before production.

Typical activities:

- Integration testing
- Pipeline validation
- Infrastructure verification
- Release candidate testing
- Performance validation

Characteristics:

- Mirrors production architecture
- May be deployed temporarily
- Short-lived to reduce Azure cost
- Used during release validation

---

# Production Environment

Purpose:

Represents the production deployment model.

Characteristics:

- Stable
- Controlled
- Approved deployments only
- Infrastructure deployed from version-controlled code
- No direct manual modifications

Within this portfolio, Production initially exists as **deployable code** and documented architecture.

This distinction is intentional. The repository will not claim that Production resources exist unless they have actually been deployed and validated.

---

# Environment Isolation

Each environment maintains complete logical separation.

This includes:

- Resource Groups
- Terraform state
- Storage
- Key Vault
- Azure SQL
- Data Factory
- Databricks
- Monitoring
- Diagnostic settings

Environment boundaries prevent accidental cross-environment changes.

---

# Terraform Layout

Each environment is represented by an independent root module.

```text
terraform/
└── environments/
    ├── dev/
    ├── test/
    └── prod/
```

Each environment contains:

- providers.tf
- versions.tf
- backend.tf
- variables.tf
- outputs.tf
- locals.tf
- main.tf

Reusable infrastructure is stored separately under:

```text
terraform/modules/
```

Root modules compose reusable modules rather than duplicating infrastructure definitions.

---

# Terraform State Strategy

Each environment uses independent remote state.

```text
Development
    ↓
dev.tfstate

Test
    ↓
test.tfstate

Production
    ↓
prod.tfstate
```

Separating state files reduces operational risk and prevents one environment from affecting another.

Terraform state is treated as sensitive operational data and is never committed to Git.

---

# Naming Convention

Environment identifiers are standardized.

| Environment | Code |
|-------------|------|
| Development | dev |
| Test | tst |
| Production | prd |

Example resource names:

```text
rg-edp-dev-eus2-001
rg-edp-tst-eus2-001
rg-edp-prd-eus2-001
```

Only stable attributes are included in resource names.

Metadata such as owners and cost centers are stored as Azure tags.

---

# Deployment Strategy

Infrastructure changes follow a promotion model.

```text
Feature Branch
        │
        ▼
Pull Request
        │
        ▼
Validation
        │
        ▼
Development
        │
        ▼
Test
        │
        ▼
Production
```

Each promotion requires successful validation before advancing.

---

# CI/CD Strategy

Future GitHub Actions workflows will include:

- Terraform formatting
- Terraform validation
- Static analysis
- Security scanning
- Terraform plan generation
- Pull request review
- Environment approval
- Terraform apply

Production deployments require explicit approval.

---

# Cost Management Strategy

To control Azure spending:

Development remains deployed.

Test is deployed only when required.

Production initially exists as validated Terraform configuration.

Resources not actively required for development should be destroyed after validation where practical.

This approach demonstrates enterprise architecture while avoiding unnecessary ongoing Azure costs.

---

# Branch Strategy

Git follows a simplified trunk-based workflow.

```text
main
│
├── feature/networking
├── feature/databricks
├── feature/adf
├── feature/monitoring
└── feature/documentation
```

Feature branches are merged through Pull Requests.

Direct commits to production infrastructure should be avoided.

---

# Operational Principles

Environment design follows these principles:

- Infrastructure is immutable where practical.
- Terraform is the source of truth.
- Manual Azure Portal changes are temporary.
- Secrets remain outside source control.
- Production changes require review.
- Deployments are repeatable.
- Environments remain independently recoverable.

---

# Current Portfolio Implementation

Current state:

| Environment | Status |
|------------|--------|
| Development | Active |
| Test | Planned |
| Production | Planned |

The repository intentionally documents environments beyond those currently deployed.

Documentation clearly distinguishes between:

- Designed
- Implemented
- Deployed
- Validated
- Future

This prevents overstating the maturity of the platform while preserving a realistic enterprise roadmap.

---

# Future Enhancements

Future iterations may include:

- Ephemeral test environments
- Automated environment teardown
- Blue/green deployments
- Canary deployments
- Policy as Code
- Azure Policy integration
- Cost budgets
- Environment drift detection

These capabilities will be added only when they support the overall platform architecture.

---

# Related Documentation

- Platform Overview
- Logical Architecture
- Naming Standards
- ADR-0001 Platform Scope
- ADR-0002 Terraform Standard
- ADR-0003 Environment Strategy