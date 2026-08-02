# Reference the Unity Catalog Access Connector automatically created
# with the Azure Databricks workspace.
data "azurerm_databricks_access_connector" "unity_catalog" {
  name                = "unity-catalog-access-connector"
  resource_group_name = "databricks-rg-rg-cloud-dba-portfolio-dev"
}

# Allow the Access Connector managed identity to read Bronze and
# read/write Silver and Gold in the Northstar ADLS Gen2 account.
resource "azurerm_role_assignment" "databricks_adls_contributor" {
  scope                = module.data_lake.storage_account_id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_databricks_access_connector.unity_catalog.identity[0].principal_id
  principal_type       = "ServicePrincipal"

  description = "Allow Azure Databricks managed identity to access Northstar ADLS Gen2."
}
