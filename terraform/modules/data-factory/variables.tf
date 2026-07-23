variable "name" {
  description = "Globally unique name of the Azure Data Factory."
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group containing Azure Data Factory."
  type        = string
}

variable "location" {
  description = "Azure region for Azure Data Factory."
  type        = string
}

variable "tags" {
  description = "Tags applied to Azure Data Factory."
  type        = map(string)
  default     = {}
}
