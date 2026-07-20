# ADR-0001: Define the Enterprise Data Platform Scope

## Status

Accepted

## Date

2026-07-20

## Decision Owners

Data Platform Engineering

## Context

This repository is intended to demonstrate the design and implementation of a production-oriented enterprise data platform on Microsoft Azure.

The platform must be credible to senior data engineers, cloud architects, database engineers, and technical hiring managers. It must therefore include more than isolated Azure resources or tutorial-style service demonstrations.

At the same time, the repository is maintained in a personal Azure subscription and cannot realistically reproduce every organizational capability normally present in a large enterprise environment.

A complete enterprise Azure estate may include:

- Management groups
- Multiple subscriptions
- Centralized identity governance
- Enterprise network connectivity
- Shared security services
- Centralized policy enforcement
- Organization-wide cost management
- Security operations
- Regulatory compliance controls
- Shared DNS and connectivity services
- Central platform operations
- Enterprise support agreements

Attempting to reproduce all of these capabilities inside this repository would introduce unnecessary cost, complexity, and architectural noise.

The project therefore requires a clearly defined scope that is both technically ambitious and operationally honest.

---

## Decision

This repository will implement an **Enterprise Data Platform Application Landing Zone**.

The platform will be designed as a workload that operates within an assumed broader enterprise Azure environment.

The repository will own the architecture, infrastructure, data engineering, security controls, monitoring, deployment processes, and documentation required for the data platform workload itself.

The repository will not claim to implement an entire organization-wide Azure landing zone.

---

## Scope Included

The following responsibilities are included within the platform scope.

### Infrastructure as Code

- Terraform-based infrastructure provisioning
- Reusable Terraform modules
- Environment-specific root configurations
- Remote Terraform state
- Provider and version constraints
- Infrastructure validation
- Security scanning
- Controlled deployment workflows

### Azure workload architecture

- Resource groups
- Virtual networks
- Subnets
- Network Security Groups
- Private endpoints where justified
- Private DNS integration where required
- Storage accounts
- Azure Data Lake Storage Gen2
- Azure Key Vault
- Azure SQL Database
- Azure Data Factory
- Azure Databricks
- Log Analytics
- Azure Monitor
- Diagnostic settings
- Managed identities
- Role-based access control

### Data engineering

- Batch ingestion
- Metadata-driven pipelines
- Full and incremental loading
- Data validation
- Data-quality rules
- Quarantine processing
- Bronze, Silver, and Gold data layers
- Delta Lake
- Apache Spark
- PySpark
- Enterprise data modeling
- Slowly changing dimensions
- Fact and dimension models
- Reconciliation
- Audit logging

### Platform security

- Microsoft Entra ID authentication
- Managed identities
- Least-privilege RBAC
- Secret elimination where possible
- Azure Key Vault where secrets remain necessary
- Environment isolation
- Controlled network exposure
- Secure CI/CD authentication
- Protection of Terraform state
- Protection of sensitive operational metadata

### DevOps and delivery

- Git-based version control
- Pull-request workflows
- Conventional commit standards
- GitHub Actions
- Terraform validation and planning
- Security and static-analysis checks
- Environment approvals
- Deployment evidence
- Documentation validation
- Release traceability

### Monitoring and operations

- Azure diagnostic logging
- Pipeline execution monitoring
- Databricks workflow monitoring
- Data-freshness measurements
- Data-quality metrics
- Failure alerts
- Cost visibility
- Log Analytics queries
- Operational runbooks
- Recovery guidance
- Troubleshooting procedures

### Documentation

- Platform overview
- Logical and physical architecture
- Environment strategy
- Naming and tagging standards
- Architecture Decision Records
- Security documentation
- Operational documentation
- Data-engineering standards
- Architecture diagrams
- Interview-ready technical narratives

---

## Scope Excluded

The following capabilities are intentionally outside the implementation scope of this repository.

### Organization-wide Azure governance

The repository will not implement:

- Enterprise management-group hierarchies
- Organization-wide subscription vending
- Enterprise-scale Azure Policy assignments
- Centralized tenant governance
- Enterprise identity lifecycle management
- Organization-wide privileged identity management
- Central cloud security operations
- Shared enterprise network hubs
- ExpressRoute
- Corporate VPN connectivity
- Enterprise DNS administration

These capabilities may be referenced as assumed upstream controls.

### Full production business operations

The repository will not process:

- Real employee data
- Real customer data
- Real claims data
- Real financial data
- Real health information
- Employer-owned data
- Personally identifiable production data
- Regulated production workloads

All datasets will be synthetic or generated specifically for demonstration.

### Enterprise commercial services

The repository will not attempt to reproduce:

- Twenty-four-hour operational staffing
- Formal service-level agreements
- Enterprise incident-management systems
- Commercial data-governance platforms
- Enterprise support contracts
- Organization-wide disaster-recovery facilities
- Legal retention policies
- Regulatory certification

The architecture will document how these capabilities would integrate with the platform where relevant.

---

## Architectural Boundary

The platform boundary is illustrated below.

```text
┌─────────────────────────────────────────────────────────────┐
│            Assumed Enterprise Azure Foundation              │
│                                                             │
│  Management Groups                                          │
│  Subscription Governance                                    │
│  Enterprise Identity                                        │
│  Central Policy                                             │
│  Shared Connectivity                                        │
│  Security Operations                                        │
│  Enterprise Cost Management                                 │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│      Enterprise Data Platform Application Landing Zone      │
│                                                             │
│  Terraform                                                  │
│  Networking                                                 │
│  ADLS Gen2                                                  │
│  Key Vault                                                  │
│  Azure SQL                                                  │
│  Azure Data Factory                                         │
│  Azure Databricks                                           │
│  Delta Lake                                                 │
│  Monitoring                                                 │
│  CI/CD                                                      │
│  Data Quality                                               │
│  Data Products                                              │
└─────────────────────────────────────────────────────────────┘