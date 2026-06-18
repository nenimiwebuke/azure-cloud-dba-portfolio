output "resource_group_name" {
  value = azurerm_resource_group.portfolio.name
}

output "vnet_name" {
  value = azurerm_virtual_network.portfolio_vnet.name
}

output "subnet_name" {
  value = azurerm_subnet.portfolio_subnet.name
}

output "public_ip_name" {
  value = azurerm_public_ip.portfolio_public_ip.name
}

output "nic_private_ip" {
  value = azurerm_network_interface.portfolio_nic.private_ip_address
}

output "storage_account_name" {
  value = azurerm_storage_account.portfolio_storage.name
}

output "blob_container_name" {
  value = azurerm_storage_container.portfolio_blob.name
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
