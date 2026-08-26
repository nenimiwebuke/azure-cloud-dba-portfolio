resource "azurerm_mssql_server" "this" {
  name                = var.server_name
  resource_group_name = var.resource_group_name
  location            = var.location
  version             = var.server_version

  administrator_login          = var.administrator_login
  administrator_login_password = var.administrator_login_password

  tags = var.tags

  lifecycle {
    ignore_changes = [administrator_login_password]
  }
}

resource "azurerm_mssql_database" "this" {
  name      = var.database_name
  server_id = azurerm_mssql_server.this.id
  sku_name  = var.database_sku_name

  tags = var.tags
}

resource "azurerm_mssql_firewall_rule" "client" {
  name             = var.firewall_rule_name
  server_id        = azurerm_mssql_server.this.id
  start_ip_address = var.firewall_start_ip_address
  end_ip_address   = var.firewall_end_ip_address
}
