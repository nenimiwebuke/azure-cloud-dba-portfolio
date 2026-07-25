output "id" {
  description = "Resource ID of the Azure Databricks workspace."
  value       = azurerm_databricks_workspace.this.id
}

output "name" {
  description = "Name of the Azure Databricks workspace."
  value       = azurerm_databricks_workspace.this.name
}

output "workspace_url" {
  description = "Workspace URL of the Azure Databricks workspace."
  value       = azurerm_databricks_workspace.this.workspace_url
}
