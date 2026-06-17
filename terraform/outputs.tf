output "resource_group_name" {
  value = azurerm_resource_group.portfolio.name
}

output "vnet_name" {
  value = azurerm_virtual_network.portfolio_vnet.name
}

output "subnet_name" {
  value = azurerm_subnet.portfolio_subnet.name
}

output "public_ip_name" {
  value = azurerm_public_ip.portfolio_public_ip.name
}

output "nic_private_ip" {
  value = azurerm_network_interface.portfolio_nic.private_ip_address
}

output "storage_account_name" {
  value = azurerm_storage_account.portfolio_storage.name
}

output "blob_container_name" {
  value = azurerm_storage_container.portfolio_blob.name
}
