variable "resource_group_name" {
  description = "Name of the resource group containing the storage resources."
  type        = string
}

variable "location" {
  description = "Azure region for the storage account."
  type        = string
}

variable "storage_account_name" {
  description = "Globally unique name of the Azure Storage account."
  type        = string

  validation {
    condition = (
      length(var.storage_account_name) >= 3 &&
      length(var.storage_account_name) <= 24 &&
      can(regex("^[a-z0-9]+$", var.storage_account_name))
    )
    error_message = "Storage account name must contain 3-24 lowercase letters and numbers only."
  }
}

variable "account_tier" {
  description = "Performance tier of the storage account."
  type        = string
  default     = "Standard"

  validation {
    condition     = contains(["Standard", "Premium"], var.account_tier)
    error_message = "Account tier must be Standard or Premium."
  }
}

variable "account_replication_type" {
  description = "Replication strategy used by the storage account."
  type        = string
  default     = "LRS"

  validation {
    condition = contains(
      ["LRS", "GRS", "RAGRS", "ZRS", "GZRS", "RAGZRS"],
      var.account_replication_type
    )
    error_message = "Replication type must be a supported Azure Storage replication option."
  }
}

variable "container_name" {
  description = "Name of the private Blob container."
  type        = string
}

variable "container_access_type" {
  description = "Access level assigned to the Blob container."
  type        = string
  default     = "private"

  validation {
    condition     = contains(["private", "blob", "container"], var.container_access_type)
    error_message = "Container access type must be private, blob, or container."
  }
}

variable "tags" {
  description = "Tags applied to the storage account."
  type        = map(string)
  default     = {}
}
