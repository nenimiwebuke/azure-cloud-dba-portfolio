output "id" {
  description = "Resource ID of Azure Data Factory."
  value       = azurerm_data_factory.this.id
}

output "name" {
  description = "Name of Azure Data Factory."
  value       = azurerm_data_factory.this.name
}

output "principal_id" {
  description = "Principal ID of the Data Factory system-assigned managed identity, when enabled."
  value       = try(azurerm_data_factory.this.identity[0].principal_id, null)
}
