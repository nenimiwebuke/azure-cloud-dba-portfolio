output "storage_account_id" {
  description = "Resource ID of the storage account."
  value       = azurerm_storage_account.this.id
}

output "storage_account_name" {
  description = "Name of the storage account."
  value       = azurerm_storage_account.this.name
}

output "primary_blob_endpoint" {
  description = "Primary Blob service endpoint of the storage account."
  value       = azurerm_storage_account.this.primary_blob_endpoint
}

output "container_id" {
  description = "Resource ID of the Blob container."
  value       = azurerm_storage_container.this.id
}

output "container_name" {
  description = "Name of the Blob container."
  value       = azurerm_storage_container.this.name
}
