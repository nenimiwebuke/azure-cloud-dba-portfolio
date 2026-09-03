# ADR-0005: Zone-Redundant High Availability Not Available on Burstable Tier

## Status
Accepted

## Context
As part of Phase 1 HA/DR testing for the Northstar PostgreSQL Flexible Server
(psql-northstar-flex, Burstable B1ms, see ADR-0004), an attempt was made to
enable zone-redundant high availability via Terraform:

    high_availability {
      mode = "ZoneRedundant"
      standby_availability_zone = "2"
    }

Prior to attempting this, SKU capability data was checked directly via:

    az postgres flexible-server list-skus --location eastus2

This returned supportedHaMode: SameZone and ZoneRedundant for Standard_B1ms
under the Burstable tier, indicating HA should be supported.

However, the actual terraform apply failed during the update operation with:

    Status: HANotSupportedForBurstableSkuWithMoreInfo
    Message: High availability not supported for burstable server.

This is a genuine discrepancy between what the SKU listing API describes and
what the provisioning API enforces. The list-skus capability data should not
be treated as a guarantee that a feature will succeed at apply time - it
describes the SKU's general capability schema, not necessarily what is
enforced for every combination of tier and feature on a given subscription.

The failed operation did not leave the server in a partially-modified state.
Verified directly via:

    az postgres flexible-server show --resource-group rg-northstar-postgres
      --name psql-northstar-flex
      --query "haState, haMode, status"

which returned HaState NotEnabled, HaMode Disabled, Status Ready - confirming
the server was untouched and remained fully available and reachable
throughout.

Terraform state briefly reflected the attempted high_availability block
despite the failed apply. This was resolved by reverting the Terraform
configuration (removing enable_ha = true) and re-applying, which corrected
state to match the real, unmodified resource with zero actual infrastructure
change required.

## Decision
Do not pursue zone-redundant HA on the current Burstable B1ms tier. Zone-
redundant HA on Azure Database for PostgreSQL Flexible Server requires
General Purpose or Memory Optimized tier, which roughly doubles compute cost
and was evaluated as not justified for a portfolio workload's budget.

Point-in-Time Recovery (PITR), which is supported on all tiers including
Burstable, is adopted as the primary disaster-recovery capability
demonstrated for this project instead. PITR addresses the more common
real-world DR scenario (accidental data loss or corruption) rather than
zone-level infrastructure failure.

## Consequences
- The Northstar Postgres server has no automatic failover to a standby in
  the event of a zone outage. This is an accepted, documented limitation of
  the Burstable tier choice (see ADR-0004), not an oversight.
- Backup retention and point-in-time restore remain fully available and are
  the demonstrated DR mechanism for this project.
- Upgrading to General Purpose tier would be a straightforward Terraform
  sku_name change if HA were required for a production-equivalent
  deployment; this is noted as a natural evolution path rather than
  implemented now.
- Capability and SKU listing APIs should be treated as informative, not
  authoritative, when planning a feature that has real cost or availability
  implications - the provisioning API's actual response is the ground truth.

## Related
- ADR-0004: PostgreSQL Flexible Server deployed to East US 2
