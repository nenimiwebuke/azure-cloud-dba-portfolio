variable "name" {
  description = "Name of the Azure Databricks workspace."
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group containing the Databricks workspace."
  type        = string
}

variable "location" {
  description = "Azure region for the Databricks workspace."
  type        = string
}

variable "sku" {
  description = "SKU for the Azure Databricks workspace."
  type        = string
}

variable "tags" {
  description = "Tags applied to the Databricks workspace."
  type        = map(string)
  default     = {}
}
