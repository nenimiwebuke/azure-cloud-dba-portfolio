output "storage_account_id" {
  description = "Resource ID of the ADLS Gen2 storage account."
  value       = azurerm_storage_account.this.id
}

output "storage_account_name" {
  description = "Name of the ADLS Gen2 storage account."
  value       = azurerm_storage_account.this.name
}

output "primary_dfs_endpoint" {
  description = "Primary Data Lake Storage DFS endpoint."
  value       = azurerm_storage_account.this.primary_dfs_endpoint
}

output "container_ids" {
  description = "Map of data lake container names to resource IDs."
  value = {
    for name, container in azurerm_storage_container.layers :
    name => container.id
  }
}

output "container_names" {
  description = "Map of data lake layer keys to container names."
  value = {
    for name, container in azurerm_storage_container.layers :
    name => container.name
  }
}
