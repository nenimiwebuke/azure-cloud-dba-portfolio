variable "resource_group_name" {
  description = "Name of the resource group that contains the networking resources"
  type        = string
}

variable "location" {
  description = "Azure region for the networking resources"
  type        = string
}

variable "vnet_name" {
  description = "Name of the virtual network"
  type        = string
}

variable "vnet_address_space" {
  description = "Address space assigned to the virtual network"
  type        = list(string)
}

variable "subnet_name" {
  description = "Name of the subnet"
  type        = string
}

variable "subnet_address_prefixes" {
  description = "Address prefixes assigned to the subnet"
  type        = list(string)
}

variable "nsg_name" {
  description = "Name of the network security group"
  type        = string
}

variable "public_ip_name" {
  description = "Name of the public IP address"
  type        = string
}

variable "nic_name" {
  description = "Name of the network interface"
  type        = string
}

variable "tags" {
  description = "Tags applied to networking resources"
  type        = map(string)
  default     = {}
}