# Naming and Tagging Standards

## Document Control

| Attribute | Value |
|---|---|
| Document | Naming and Tagging Standards |
| Platform | Enterprise Azure Data Platform |
| Repository | `azure-cloud-dba-portfolio` |
| Status | Active |
| Owner | Data Platform Engineering |
| Last Reviewed | 2026-07-20 |

---

## 1. Purpose

This document defines the naming, tagging, and identifier standards for the Enterprise Azure Data Platform.

The standard applies to:

- Azure resources
- Terraform modules and configurations
- Git branches and commits
- Documentation
- Architecture diagrams
- Screenshots
- Data Lake objects
- Databricks catalogs, schemas, tables, and jobs
- Azure Data Factory artifacts
- SQL objects

Consistent naming improves:

- Operational clarity
- Searchability
- Cost attribution
- Automation
- Troubleshooting
- Security review
- Environment identification
- Repository maintainability

Names must be predictable, meaningful, and compatible with the technical restrictions of the target service.

---

## 2. Naming Principles

All names must follow these principles.

### 2.1 Use stable attributes

Resource names should contain information unlikely to change during the resource lifecycle.

Appropriate name components include:

- Resource type
- Workload or application
- Environment
- Azure region
- Instance number

Changeable information should be stored in tags instead.

Examples of metadata that should normally remain outside names:

- Individual owner
- Cost center
- Department manager
- Project status
- Business sponsor
- Support contact

### 2.2 Use a consistent component order

The standard Azure naming pattern is:

```text
<resource-type>-<workload>-<environment>-<region>-<instance>
```

Example:

```text
kv-edp-dev-eus2-001
```

Where:

| Component | Value | Meaning |
|---|---|---|
| Resource type | `kv` | Azure Key Vault |
| Workload | `edp` | Enterprise Data Platform |
| Environment | `dev` | Development |
| Region | `eus2` | East US 2 |
| Instance | `001` | First instance |

### 2.3 Prefer lowercase

Lowercase naming is used wherever the Azure service supports it.

This avoids inconsistencies between:

- Azure
- Terraform
- shell scripts
- GitHub Actions
- Linux-based runtimes
- storage paths

### 2.4 Avoid unsupported characters

Hyphens are preferred for Azure resource names where permitted.

Underscores are preferred for Terraform identifiers.

Spaces are prohibited in machine-managed names.

### 2.5 Do not encode sensitive information

Names must not contain:

- Employee names
- Customer names
- Email addresses
- Subscription IDs
- Tenant IDs
- Public IP addresses
- Secrets
- Passwords
- Personally identifiable information
- Production database contents

### 2.6 Do not overpopulate names

Names must remain readable.

A resource name is not a substitute for:

- Tags
- Documentation
- Resource descriptions
- Configuration management
- Monitoring metadata

---

## 3. Standard Codes

### 3.1 Workload code

| Workload | Code |
|---|---|
| Enterprise Data Platform | `edp` |

The workload code remains consistent across the platform.

### 3.2 Environment codes

| Environment | Code |
|---|---|
| Development | `dev` |
| Test | `tst` |
| Production | `prd` |
| Shared | `shr` |
| Sandbox | `sbx` |

`test` is represented as `tst` to keep environment codes consistently concise.

### 3.3 Azure region codes

| Azure Region | Code |
|---|---|
| East US | `eus` |
| East US 2 | `eus2` |
| Central US | `cus` |
| South Central US | `scus` |
| West US 2 | `wus2` |
| West Europe | `weu` |
| North Europe | `neu` |

The platform's preferred deployment region is:

```text
eus2
```

The actual region must be selected based on service availability, cost, compliance, latency, and disaster-recovery requirements.

### 3.4 Instance codes

Instance numbers use three digits:

```text
001
002
003
```

Instance identifiers are used only when multiple resources of the same type and responsibility may exist.

They must not be used unnecessarily.

---

## 4. Azure Resource Naming Pattern

The default Azure resource naming pattern is:

```text
<abbreviation>-edp-<environment>-<region>-<instance>
```

Examples:

```text
rg-edp-dev-eus2-001
vnet-edp-dev-eus2-001
kv-edp-dev-eus2-001
adf-edp-dev-eus2-001
dbw-edp-dev-eus2-001
law-edp-dev-eus2-001
```

Some Azure services impose different character or length restrictions. Their names must adapt while preserving the same logical components where possible.

---

## 5. Azure Resource Abbreviations

The following abbreviations are approved for this platform.

| Azure Resource | Abbreviation | Example |
|---|---|---|
| Resource Group | `rg` | `rg-edp-dev-eus2-001` |
| Virtual Network | `vnet` | `vnet-edp-dev-eus2-001` |
| Subnet | `snet` | `snet-databricks-private-dev-eus2-001` |
| Network Security Group | `nsg` | `nsg-data-dev-eus2-001` |
| Route Table | `rt` | `rt-edp-dev-eus2-001` |
| Public IP Address | `pip` | `pip-edp-dev-eus2-001` |
| Network Interface | `nic` | `nic-edp-dev-eus2-001` |
| Private Endpoint | `pep` | `pep-adls-dev-eus2-001` |
| Private DNS Zone | `pdnsz` | Service-specific Azure DNS name |
| Storage Account | `st` | `stedpdev<suffix>` |
| Data Lake Storage Account | `st` | `stedpdev<suffix>` |
| Key Vault | `kv` | `kv-edp-dev-eus2-001` |
| Log Analytics Workspace | `law` | `law-edp-dev-eus2-001` |
| Application Insights | `appi` | `appi-edp-dev-eus2-001` |
| Action Group | `ag` | `ag-edp-dev-eus2-001` |
| Data Factory | `adf` | `adf-edp-dev-eus2-001` |
| Databricks Workspace | `dbw` | `dbw-edp-dev-eus2-001` |
| Databricks Access Connector | `dac` | `dac-edp-dev-eus2-001` |
| Azure SQL Logical Server | `sql` | `sql-edp-dev-eus2-001` |
| Azure SQL Database | `sqldb` | `sqldb-edp-dev-eus2-001` |
| Managed Identity | `id` | `id-adf-edp-dev-eus2-001` |
| User-Assigned Managed Identity | `id` | `id-databricks-edp-dev-eus2-001` |
| Budget | `bud` | `bud-edp-dev-monthly` |

New resource abbreviations must be checked against Microsoft's published Azure abbreviation guidance before adoption.

---

## 6. Special Azure Naming Rules

### 6.1 Storage accounts

Azure Storage account names:

- Use lowercase letters and numbers only
- Cannot contain hyphens
- Must be globally unique
- Must remain within Azure's service length restrictions

Pattern:

```text
st<workload><environment><unique-suffix>
```

Example:

```text
stedpdev8f31
```

The suffix must be deterministic where practical.

It may be derived from:

- Subscription identifier hash
- Environment identifier
- Terraform random string persisted in state

The full subscription ID must never appear in the name.

### 6.2 Key Vault

Key Vault names must be globally unique.

Preferred pattern:

```text
kv-edp-<environment>-<region>-<suffix>
```

Example:

```text
kv-edp-dev-eus2-8f31
```

### 6.3 Azure SQL logical server

Azure SQL logical server names must be globally unique.

Preferred pattern:

```text
sql-edp-<environment>-<region>-<suffix>
```

Example:

```text
sql-edp-dev-eus2-8f31
```

### 6.4 Private DNS zones

Private DNS zone names must use the Azure service's required domain.

Examples:

```text
privatelink.blob.core.windows.net
privatelink.dfs.core.windows.net
privatelink.database.windows.net
privatelink.vaultcore.azure.net
```

These names must not be changed to match the general workload naming pattern.

---

## 7. Resource Group Standards

Resource groups are organized around lifecycle and operational responsibility.

Approved initial patterns include:

```text
rg-edp-platform-dev-eus2-001
rg-edp-data-dev-eus2-001
rg-edp-observability-dev-eus2-001
```

However, separate resource groups must only be created when there is a real difference in:

- Lifecycle
- Access control
- Ownership
- Deployment cadence
- Policy
- Cost tracking

The platform must not create excessive resource groups solely to appear enterprise-scale.

For an early development deployment, one workload resource group may be acceptable:

```text
rg-edp-dev-eus2-001
```

The Terraform state backend uses a separate administrative resource group because its lifecycle differs from workload resources:

```text
rg-tfstate-edp-shr-eus2-001
```

---

## 8. Subnet Naming

Subnet names describe their functional responsibility.

Pattern:

```text
snet-<function>-<environment>-<region>-<instance>
```

Examples:

```text
snet-data-dev-eus2-001
snet-adf-integration-dev-eus2-001
snet-databricks-public-dev-eus2-001
snet-databricks-private-dev-eus2-001
snet-private-endpoints-dev-eus2-001
```

Subnet names must not be based only on arbitrary numbers such as:

```text
subnet1
subnet2
```

---

## 9. Azure Tagging Standard

Tags provide metadata that should not be embedded in resource names.

### 9.1 Required tags

| Tag | Example | Purpose |
|---|---|---|
| `application` | `enterprise-data-platform` | Identifies the workload |
| `environment` | `dev` | Identifies deployment environment |
| `managed_by` | `terraform` | Identifies the management authority |
| `repository` | `azure-cloud-dba-portfolio` | Links the resource to source control |
| `business_unit` | `data-platform` | Identifies the logical organization |
| `cost_center` | `portfolio` | Supports cost attribution |
| `data_classification` | `internal` | Identifies the expected data sensitivity |
| `criticality` | `medium` | Records business criticality |
| `owner_team` | `data-platform-engineering` | Identifies responsible team |
| `lifecycle` | `persistent` | Identifies persistent or ephemeral resources |

### 9.2 Optional tags

| Tag | Example |
|---|---|
| `created_by` | `github-actions` |
| `service_tier` | `development` |
| `retention_policy` | `30-days` |
| `source_system` | `membership-sql` |
| `portfolio_phase` | `foundation` |
| `expires_on` | `2026-08-31` |

### 9.3 Tag rules

Tag keys must:

- Use lowercase
- Use underscores between words
- Remain consistent across modules

Tag values must:

- Use lowercase where practical
- Avoid personal or sensitive information
- Be controlled through Terraform
- Not be manually modified without updating code

### 9.4 Terraform implementation

Shared tags will be defined centrally:

```hcl
locals {
  common_tags = {
    application         = "enterprise-data-platform"
    environment         = var.environment
    managed_by          = "terraform"
    repository          = "azure-cloud-dba-portfolio"
    business_unit       = "data-platform"
    cost_center         = "portfolio"
    data_classification = "internal"
    criticality         = "medium"
    owner_team          = "data-platform-engineering"
    lifecycle           = "persistent"
  }
}
```

Resource-specific tags may be merged with common tags:

```hcl
tags = merge(
  local.common_tags,
  {
    component = "data-lake"
  }
)
```

---

## 10. Terraform Naming Standards

Terraform identifiers use:

- Lowercase letters
- Underscores between words
- Descriptive nouns
- Singular names for individual resources
- Plural names for collections

### 10.1 Resource labels

Preferred:

```hcl
resource "azurerm_storage_account" "data_lake" {
}
```

Avoid:

```hcl
resource "azurerm_storage_account" "storage1" {
}
```

Avoid repeating the resource type unnecessarily:

```hcl
resource "azurerm_storage_account" "storage_account" {
}
```

The resource type is already visible in the first label.

### 10.2 Module blocks

Preferred:

```hcl
module "data_lake" {
  source = "../../modules/storage-account"
}
```

Module labels describe the module's responsibility within the root configuration.

### 10.3 Variables

Variables use descriptive snake_case nouns.

Examples:

```hcl
variable "environment" {}
variable "location" {}
variable "resource_group_name" {}
variable "storage_account_tier" {}
variable "enable_private_endpoint" {}
```

Boolean variables should clearly indicate intent:

```hcl
enable_public_network_access
enable_zone_redundancy
create_private_endpoint
```

Avoid ambiguous variables:

```hcl
enabled
setting
option
value
```

Every variable must define:

- Type
- Description
- Validation where appropriate
- Default only when a safe default exists
- `sensitive = true` where required

### 10.4 Local values

Local values use descriptive snake_case identifiers:

```hcl
locals {
  name_prefix = "edp-${var.environment}-${local.region_code}"
  common_tags = {}
}
```

### 10.5 Outputs

Outputs describe the exposed value rather than its implementation.

Examples:

```hcl
output "storage_account_id" {}
output "data_lake_primary_dfs_endpoint" {}
output "resource_group_name" {}
output "managed_identity_principal_id" {}
```

Avoid vague output names:

```hcl
output "id" {}
output "name" {}
output "result" {}
```

Sensitive outputs must use:

```hcl
sensitive = true
```

### 10.6 Terraform files

Approved standard files include:

```text
main.tf
variables.tf
outputs.tf
locals.tf
versions.tf
providers.tf
backend.tf
data.tf
```

Additional files may be organized by cohesive responsibility:

```text
networking.tf
diagnostics.tf
role-assignments.tf
private-endpoints.tf
```

Avoid arbitrary numbered names:

```text
01-network.tf
02-storage.tf
03-database.tf
```

Terraform determines dependency from references, not filename order.

### 10.7 Terraform modules

Module directory names use lowercase kebab-case:

```text
resource-group
networking
storage-account
key-vault
log-analytics
data-factory
databricks-workspace
azure-sql
private-endpoint
diagnostic-settings
role-assignment
```

A module must represent a cohesive responsibility.

Avoid broad names such as:

```text
azure
platform
everything
enterprise-module
```

HashiCorp's standard module structure will be used:

```text
modules/storage-account/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── README.md
└── tests/
```

---

## 11. Terraform State Naming

Terraform state is isolated by environment and platform layer.

Recommended backend key pattern:

```text
<platform>/<environment>/<component>.tfstate
```

Examples:

```text
enterprise-data-platform/dev/platform.tfstate
enterprise-data-platform/tst/platform.tfstate
enterprise-data-platform/prd/platform.tfstate
```

If the platform is later divided into independently deployed stacks:

```text
enterprise-data-platform/dev/networking.tfstate
enterprise-data-platform/dev/data-services.tfstate
enterprise-data-platform/dev/observability.tfstate
```

State must not be split without a real lifecycle or ownership reason.

Terraform state files must never be committed to Git.

---

## 12. Data Lake Naming Standards

Data Lake container or filesystem names use lowercase kebab-case.

Approved containers:

```text
landing
quarantine
bronze
silver
gold
system
```

The `system` container may hold platform metadata, checkpoints, audit exports, or controlled operational artifacts.

Folder paths use meaningful business and technical partitions.

Example:

```text
bronze/membership/member/year=2026/month=07/day=20/
```

General pattern:

```text
<layer>/<source-system>/<entity>/<partition-columns>
```

Paths must not contain:

- Spaces
- Email addresses
- Personal names
- Uncontrolled timestamps
- Random local filenames

---

## 13. Databricks Naming Standards

### 13.1 Catalogs

Catalog pattern:

```text
edp_<environment>
```

Examples:

```text
edp_dev
edp_tst
edp_prd
```

### 13.2 Schemas

Schemas represent logical data layers or domains:

```text
bronze
silver
gold
audit
quarantine
reference
```

Where domain separation is needed:

```text
membership_silver
claims_silver
eligibility_gold
```

### 13.3 Tables

Tables use lowercase snake_case.

Examples:

```text
member
member_eligibility
claim_header
claim_line
dim_member
dim_employer
fact_claim
pipeline_run
data_quality_result
```

Recommended analytical prefixes:

| Object Type | Prefix |
|---|---|
| Dimension | `dim_` |
| Fact | `fact_` |
| Bridge | `bridge_` |
| Aggregate | `agg_` |
| Snapshot | `snapshot_` |

### 13.4 Jobs and workflows

Pattern:

```text
<environment>-<domain>-<process>
```

Examples:

```text
dev-membership-bronze-ingestion
dev-membership-silver-transformation
dev-claims-gold-publication
dev-platform-data-quality
```

### 13.5 Notebooks and source files

Production code uses Python modules rather than relying exclusively on notebooks.

Python files use snake_case:

```text
load_membership_bronze.py
transform_member_silver.py
build_eligibility_gold.py
data_quality_rules.py
```

Notebook names may use readable kebab-case:

```text
membership-bronze-validation
claims-silver-investigation
```

---

## 14. Azure Data Factory Naming Standards

ADF artifact names use readable PascalCase where the service interface benefits from it.

### 14.1 Pipelines

Pattern:

```text
PL_<Domain>_<Action>
```

Examples:

```text
PL_Membership_Ingest
PL_Claims_Ingest
PL_Metadata_Orchestrator
PL_DataQuality_Validate
```

### 14.2 Datasets

Pattern:

```text
DS_<Technology>_<Entity>
```

Examples:

```text
DS_SqlServer_Member
DS_ADLS_MemberBronze
DS_ADLS_ClaimsLanding
```

### 14.3 Linked services

Pattern:

```text
LS_<Technology>_<Purpose>
```

Examples:

```text
LS_AzureSql_Source
LS_ADLS_DataLake
LS_KeyVault_Platform
LS_Databricks_Transform
```

### 14.4 Data flows

Pattern:

```text
DF_<Domain>_<Action>
```

Complex business transformation should generally remain in Databricks rather than being duplicated in ADF mapping data flows.

### 14.5 Triggers

Pattern:

```text
TR_<Frequency>_<Purpose>
```

Examples:

```text
TR_Daily_MembershipIngestion
TR_Hourly_PartnerFileCheck
```

### 14.6 Integration runtimes

Pattern:

```text
IR_<Type>_<Purpose>
```

Examples:

```text
IR_Azure_Default
IR_SelfHosted_HybridSources
```

---

## 15. SQL Naming Standards

SQL identifiers use consistent schema ownership and descriptive names.

Approved schemas may include:

```text
src
stg
audit
metadata
ref
mart
```

Examples:

```text
src.Member
stg.MemberEligibility
audit.PipelineRun
metadata.IngestionConfig
ref.Employer
mart.DimMember
mart.FactClaim
```

Stored procedures use:

```text
<schema>.usp_<Action><Entity>
```

Examples:

```text
audit.usp_StartPipelineRun
audit.usp_CompletePipelineRun
metadata.usp_GetActiveIngestionConfig
```

Primary keys use:

```text
PK_<TableName>
```

Foreign keys use:

```text
FK_<ChildTable>_<ParentTable>
```

Indexes use:

```text
IX_<TableName>_<KeyColumns>
```

Unique indexes use:

```text
UX_<TableName>_<KeyColumns>
```

Do not use the `sp_` prefix for user-created stored procedures.

---

## 16. Git Branch Naming

The repository uses a simplified trunk-based workflow.

Branch pattern:

```text
<type>/<short-description>
```

Approved branch types:

```text
feature
fix
refactor
docs
ci
chore
test
```

Examples:

```text
docs/naming-standards
feature/storage-module
feature/adf-ingestion
refactor/terraform-networking
fix/databricks-storage-access
ci/terraform-validation
```

Branch names must:

- Use lowercase
- Use hyphens between words
- Remain concise
- Describe one logical change

Avoid:

```text
nenim-work
test123
new-branch
final-version
```

---

## 17. Commit Message Standard

The repository adopts Conventional Commits.

Pattern:

```text
<type>(<scope>): <description>
```

Examples:

```text
docs(architecture): add naming and tagging standards
feat(terraform): add reusable storage account module
feat(adf): implement metadata-driven ingestion
feat(databricks): add silver membership transformation
fix(terraform): correct private endpoint DNS association
refactor(terraform): separate networking into reusable module
ci(github): add Terraform pull request validation
test(databricks): add membership quality tests
chore(deps): update AzureRM provider constraint
```

Approved commit types include:

| Type | Purpose |
|---|---|
| `feat` | New functionality |
| `fix` | Defect correction |
| `docs` | Documentation change |
| `refactor` | Code restructuring without functional change |
| `test` | Test additions or changes |
| `ci` | CI/CD configuration |
| `chore` | Maintenance |
| `perf` | Performance improvement |
| `build` | Build or dependency configuration |

The description must:

- Use imperative language
- Begin with lowercase
- Avoid a trailing period
- Describe one logical change

Conventional Commits uses the structure `<type>[optional scope]: <description>` to create an explicit, machine-readable history. 

---

## 18. Documentation Naming

Markdown filenames use lowercase kebab-case.

Examples:

```text
platform-overview.md
logical-architecture.md
environment-strategy.md
naming-standards.md
monitoring-strategy.md
cost-management.md
```

ADR filenames retain the approved ADR pattern:

```text
ADR-0001-platform-scope.md
ADR-0002-terraform-standard.md
ADR-0003-environment-strategy.md
```

Documentation headings use sentence-style capitalization unless a product name requires official casing.

Relative Markdown links must be used for repository documents.

---

## 19. Architecture Diagram Naming

Editable architecture source files use lowercase kebab-case:

```text
enterprise-data-platform.drawio
logical-data-flow.drawio
network-architecture.drawio
deployment-flow.drawio
```

Exported files use the same base name:

```text
enterprise-data-platform.png
enterprise-data-platform.svg
```

The editable source must remain version controlled.

---

## 20. Screenshot Naming

Screenshot filenames must explain what the image proves.

Pattern:

```text
<sequence>-<component>-<evidence>.<extension>
```

Examples:

```text
001-terraform-plan-network-foundation.png
002-azure-resource-group-deployment.png
003-adf-membership-pipeline-success.png
004-databricks-bronze-silver-gold-job.png
005-log-analytics-pipeline-failures.png
```

Avoid:

```text
Screenshot 2026-07-20 at 10.15.02 PM.png
image1.png
final.png
new-final-2.png
```

Every published screenshot must be reviewed for:

- Subscription IDs
- Tenant IDs
- Email addresses
- Public IP addresses
- Storage keys
- Secrets
- Tokens
- Local filesystem details
- Irrelevant browser or desktop content

---

## 21. Naming Validation

Naming standards should be enforced through code rather than documentation alone.

Terraform variable validation example:

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment code."

  validation {
    condition     = contains(["dev", "tst", "prd"], var.environment)
    error_message = "Environment must be one of: dev, tst, prd."
  }
}
```

Example resource-name validation:

```hcl
variable "workload_name" {
  type        = string
  description = "Short workload code used in Azure resource names."

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.workload_name))
    error_message = "Workload name must contain only lowercase letters, numbers, and hyphens."
  }
}
```

Future enforcement may include:

- Terraform validation
- TFLint
- Azure Policy
- Checkov
- GitHub Actions
- Pre-commit hooks
- Documentation linting

---

## 22. Exceptions

A naming-standard exception is permitted only when:

- Azure imposes a conflicting technical requirement
- A third-party integration requires a specific name
- Renaming an existing resource would cause unacceptable disruption
- A service-generated object cannot be controlled

Exceptions must be documented in:

- Terraform comments where appropriate
- The relevant architecture document
- An ADR when the impact is significant

Convenience alone is not sufficient justification for an exception.

---

## 23. Current-State Alignment

Existing Azure resources and Terraform identifiers may predate this standard.

They will be reviewed before refactoring.

A noncompliant existing name does not automatically require immediate replacement because some Azure resources cannot be renamed without recreation.

Each discrepancy will be evaluated for:

- Operational impact
- Cost
- State migration
- Data migration
- Downtime
- Portfolio value

Where replacement is not justified, the deviation will be documented.

---

## 24. Related Documentation

- [Platform Overview](./platform-overview.md)
- [Logical Architecture](./logical-architecture.md)
- [Environment Strategy](./environment-strategy.md)
- [ADR-0001: Platform Scope](../adr/ADR-0001-platform-scope.md)
- [ADR-0002: Terraform Standard](../adr/ADR-0002-terraform-standard.md)
- [ADR-0003: Environment Strategy](../adr/ADR-0003-environment-strategy.md)