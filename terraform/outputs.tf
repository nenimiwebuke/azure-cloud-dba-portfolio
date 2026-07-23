output "resource_group_name" {
  value = module.resource_group.name
}

output "vnet_name" {
  value = module.networking.virtual_network_name
}

output "subnet_name" {
  value = module.networking.subnet_name
}

output "public_ip_name" {
  value = module.networking.public_ip_name
}

output "nic_private_ip" {
  value = module.networking.network_interface_private_ip
}

output "storage_account_name" {
  value = module.storage_account.storage_account_name
}

output "blob_container_name" {
  value = module.storage_account.container_name
}

output "sql_server_name" {
  value = module.azure_sql.server_name
}

output "sql_database_name" {
  value = module.azure_sql.database_name
}

output "sql_server_fqdn" {
  value = module.azure_sql.server_fqdn
}

output "log_analytics_workspace_name" {
  value = module.log_analytics.name
}

output "key_vault_name" {
  value = module.key_vault.name
}

output "data_factory_name" {
  value = module.data_factory.name
}

output "adls_storage_account_name" {
  value = module.data_lake.storage_account_name
}

output "adls_bronze_container" {
  value = module.data_lake.container_names["bronze"]
}

output "adls_silver_container" {
  value = module.data_lake.container_names["silver"]
}

output "adls_gold_container" {
  value = module.data_lake.container_names["gold"]
}

output "databricks_workspace_name" {
  value = azurerm_databricks_workspace.portfolio_databricks.name
}

output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.portfolio_databricks.workspace_url
}
