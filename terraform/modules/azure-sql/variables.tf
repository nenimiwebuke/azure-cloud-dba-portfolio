variable "resource_group_name" {
  description = "Name of the resource group containing the Azure SQL resources."
  type        = string
}

variable "location" {
  description = "Azure region for the Azure SQL logical server."
  type        = string
}

variable "server_name" {
  description = "Globally unique name of the Azure SQL logical server."
  type        = string
}

variable "server_version" {
  description = "Version of the Azure SQL logical server."
  type        = string
  default     = "12.0"
}

variable "administrator_login" {
  description = "SQL administrator login name."
  type        = string
}

variable "administrator_login_password" {
  description = "SQL administrator password."
  type        = string
  sensitive   = true
}

variable "database_name" {
  description = "Name of the Azure SQL database."
  type        = string
}

variable "database_sku_name" {
  description = "SKU assigned to the Azure SQL database."
  type        = string
  default     = "Basic"
}

variable "firewall_rule_name" {
  description = "Name of the Azure SQL firewall rule."
  type        = string
}

variable "firewall_start_ip_address" {
  description = "Starting IPv4 address allowed by the firewall rule."
  type        = string
}

variable "firewall_end_ip_address" {
  description = "Ending IPv4 address allowed by the firewall rule."
  type        = string
}

variable "tags" {
  description = "Tags applied to supported Azure SQL resources."
  type        = map(string)
  default     = {}
}
