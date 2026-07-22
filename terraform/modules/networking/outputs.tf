output "virtual_network_id" {
  description = "Resource ID of the virtual network."
  value       = azurerm_virtual_network.this.id
}

output "virtual_network_name" {
  description = "Name of the virtual network."
  value       = azurerm_virtual_network.this.name
}

output "subnet_id" {
  description = "Resource ID of the subnet."
  value       = azurerm_subnet.this.id
}

output "subnet_name" {
  description = "Name of the subnet."
  value       = azurerm_subnet.this.name
}

output "network_security_group_id" {
  description = "Resource ID of the network security group."
  value       = azurerm_network_security_group.this.id
}

output "public_ip_id" {
  description = "Resource ID of the public IP address."
  value       = azurerm_public_ip.this.id
}

output "public_ip_name" {
  description = "Name of the public IP address."
  value       = azurerm_public_ip.this.name
}

output "network_interface_id" {
  description = "Resource ID of the network interface."
  value       = azurerm_network_interface.this.id
}

output "network_interface_private_ip" {
  description = "Private IP address assigned to the network interface."
  value       = azurerm_network_interface.this.private_ip_address
}
