variable "name" {
  description = "Name of the Azure resource group."
  type        = string

  validation {
    condition     = length(trimspace(var.name)) > 0
    error_message = "Resource group name must not be empty."
  }
}

variable "location" {
  description = "Azure region in which the resource group is created."
  type        = string

  validation {
    condition     = length(trimspace(var.location)) > 0
    error_message = "Azure location must not be empty."
  }
}

variable "tags" {
  description = "Tags applied to the resource group."
  type        = map(string)
  default     = {}
}
