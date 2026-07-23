variable "resource_group_name" {
  description = "Name of the resource group containing the data lake."
  type        = string
}

variable "location" {
  description = "Azure region for the data lake storage account."
  type        = string
}

variable "storage_account_name" {
  description = "Globally unique name of the ADLS Gen2 storage account."
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
  description = "Performance tier of the data lake storage account."
  type        = string
  default     = "Standard"

  validation {
    condition     = contains(["Standard", "Premium"], var.account_tier)
    error_message = "Account tier must be Standard or Premium."
  }
}

variable "account_replication_type" {
  description = "Replication strategy for the data lake storage account."
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

variable "containers" {
  description = "Private containers representing data lake layers."
  type        = set(string)

  validation {
    condition     = length(var.containers) > 0
    error_message = "At least one data lake container must be supplied."
  }
}

variable "tags" {
  description = "Tags applied to the data lake storage account."
  type        = map(string)
  default     = {}
}
