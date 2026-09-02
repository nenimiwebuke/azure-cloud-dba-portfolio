# ADR-0004: PostgreSQL Flexible Server Deployed to East US 2

## Status
Accepted

## Context
All platform resources are deployed to eastus by default (see ADR-0002,
ADR-0003). During provisioning of Azure Database for PostgreSQL Flexible
Server for the Northstar Postgres workstream, deployment failed against
eastus with the following error:

    Error: creating Flexible Server ... unexpected status 400 (400 Bad Request)
    with error: ParameterOutOfRange: The value of the 'Version' should be in: [].

This error is misleading on its face - it presents as an invalid PostgreSQL
version, but an empty allowed-versions list is the API's way of signaling
that the region itself is restricted for this resource type on this
subscription, not that the requested version was invalid.

This was confirmed directly via:

    az postgres flexible-server list-skus --location eastus

which returned:

    "reason": "Provisioning is restricted in this region. Please choose a
    different region. For exceptions to this rule please open a support
    request with Issue type of 'Service and subscription limits'."

Notably, this restriction is specific to PostgreSQL Flexible Server on this
subscription - every other platform resource (Azure SQL, Databricks, Data
Factory, storage, networking) provisions in eastus without issue. Regional
capability is not uniform across services within a single subscription, even
for standard SKUs on standard tiers.

## Decision
Deploy the PostgreSQL Flexible Server and its dedicated resource group
(rg-northstar-postgres) to eastus2 instead of eastus.

eastus2 was chosen over other unrestricted alternatives (centralus,
westus2, both verified unrestricted via the same list-skus check) because
it is the Azure-paired region to eastus, minimizing cross-region latency
and keeping the exception geographically close to the rest of the platform.

Target SKU/version (Standard_B1ms, Burstable tier, PostgreSQL 16) was
verified as unrestricted in eastus2 before committing to the change.

This is documented as an explicit, isolated exception via inline comment in
terraform/postgres.tf rather than changing the platform-wide default
region, since every other workload remains unaffected by and unrelated to
this restriction.

## Consequences
- rg-northstar-postgres and all resources within it are the only platform
  resources not deployed to eastus.
- Minor cross-region latency between Postgres and other platform services
  (Databricks, Data Factory) if/when they interact - acceptable for a
  portfolio workload, would need re-evaluation for a production SLA.
- Future Azure resources should verify regional SKU/version availability via
  az <service> list-skus --location <region> before assuming parity with
  resources already running successfully in eastus, rather than discovering
  restrictions mid-deployment.

## Related
- ADR-0002: Terraform as the Infrastructure as Code standard
- ADR-0003: Environment strategy
