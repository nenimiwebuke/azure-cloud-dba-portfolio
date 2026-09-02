variable "server_name" {
  type        = string
  description = "Globally unique, lowercase, hyphens only"
}

variable "resource_group_name" { type = string }
variable "location"            { type = string }

variable "postgres_version" {
  type    = string
  default = "16"
}

variable "sku_name" {
  type        = string
  default     = "B_Standard_B1ms"
  description = "Burstable for portfolio/dev cost control"
}

variable "storage_mb" {
  type    = number
  default = 32768
}

variable "admin_username" { type = string }

variable "admin_password" {
  type      = string
  sensitive = true
}

variable "database_name" {
  type    = string
  default = "northstar"
}

variable "backup_retention_days" {
  type    = number
  default = 7
}

variable "geo_redundant_backup_enabled" {
  type    = bool
  default = false
}

variable "enable_ha" {
  type        = bool
  default     = false
  description = "Set true when you get to the HA/DR phase"
}

variable "availability_zone" {
  type    = string
  default = "1"
}

variable "standby_availability_zone" {
  type    = string
  default = "2"
}

variable "client_ip_address" {
  type    = string
  default = ""
}

variable "tags" {
  type    = map(string)
  default = {}
}
