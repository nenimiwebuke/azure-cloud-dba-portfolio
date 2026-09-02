variable "business_case" {
  description = "Identifier for the business case this stack serves."
  type        = string
  default     = "northstar"
}

variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "East US"
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "rg-cloud-dba-portfolio-dev"
}

variable "vnet_name" {
  type    = string
  default = "vnet-cloud-dba-dev"
}

variable "subnet_name" {
  type    = string
  default = "subnet-cloud-dba-dev"
}

variable "nsg_name" {
  type    = string
  default = "nsg-cloud-dba-dev"
}

variable "public_ip_name" {
  type    = string
  default = "pip-cloud-dba-dev"
}

variable "nic_name" {
  type    = string
  default = "nic-cloud-dba-dev"
}

variable "portfolio_storage_account_name" {
  description = "Legacy general-purpose storage account (predates the ADLS data lake)."
  type        = string
  default     = "stclouddbaportfolio01"
}

variable "portfolio_storage_container_name" {
  type    = string
  default = "portfolio-data"
}

variable "sql_admin_login" {
  default = "sqladminnenim"
}

variable "sql_admin_password" {
  description = "SQL Admin Password"
  type        = string
  sensitive   = true
}

variable "sql_server_name" {
  type    = string
  default = "sql-nenim-portfolio-cus-dev"
}

variable "sql_server_location" {
  type    = string
  default = "Central US"
}

variable "sql_database_name" {
  type    = string
  default = "CloudDBAPortfolioDB"
}

variable "sql_firewall_rule_name" {
  type    = string
  default = "Allow-My-Current-IP"
}

variable "sql_firewall_ip" {
  description = "Single IP allowed through the SQL firewall (start and end)."
  type        = string
  default     = "172.56.222.194"
}

variable "log_analytics_name" {
  type    = string
  default = "law-cloud-dba-dev"
}

variable "key_vault_name" {
  type    = string
  default = "kv-nenim-cloud-dba-dev"
}

variable "data_factory_name" {
  type    = string
  default = "adf-nenim-cloud-dba-dev"
}

variable "data_lake_storage_account_name" {
  type    = string
  default = "stnenimadlsdev01"
}

variable "data_lake_containers" {
  type    = set(string)
  default = ["bronze", "silver", "gold"]
}

variable "databricks_name" {
  type    = string
  default = "dbw-nenim-cloud-dba-dev"
}

variable "databricks_sku" {
  type    = string
  default = "trial"
}
variable "postgres_client_ip" {
  type        = string
  default     = ""
  description = "Client IP allowed through the Postgres firewall, passed at apply time"
}

