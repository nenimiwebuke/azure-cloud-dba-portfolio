output "server_id"    { value = azurerm_postgresql_flexible_server.northstar.id }
output "server_fqdn"  { value = azurerm_postgresql_flexible_server.northstar.fqdn }
output "database_name" { value = azurerm_postgresql_flexible_server_database.northstar_db.name }
