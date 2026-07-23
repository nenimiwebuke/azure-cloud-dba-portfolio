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
  value = azurerm_mssql_server.portfolio_sql_server.name
}

output "sql_database_name" {
  value = azurerm_mssql_database.portfolio_sql_db.name
}

output "sql_server_fqdn" {
  value = azurerm_mssql_server.portfolio_sql_server.fully_qualified_domain_name
}

output "log_analytics_workspace_name" {
  value = azurerm_log_analytics_workspace.portfolio_law.name
}

output "key_vault_name" {
  value = azurerm_key_vault.portfolio_kv.name
}

output "data_factory_name" {
  value = azurerm_data_factory.portfolio_adf.name
}

output "adls_storage_account_name" {
  value = azurerm_storage_account.portfolio_adls.name
}

output "adls_bronze_container" {
  value = azurerm_storage_container.bronze.name
}

output "adls_silver_container" {
  value = azurerm_storage_container.silver.name
}

output "adls_gold_container" {
  value = azurerm_storage_container.gold.name
}

output "databricks_workspace_name" {
  value = azurerm_databricks_workspace.portfolio_databricks.name
}

output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.portfolio_databricks.workspace_url
}
