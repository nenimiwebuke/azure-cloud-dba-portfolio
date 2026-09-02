resource "random_password" "postgres_admin" {
  length      = 20
  special     = true
  min_upper   = 2
  min_lower   = 2
  min_numeric = 2
  min_special = 2
}

resource "azurerm_key_vault_secret" "postgres_admin_password" {
  name         = "northstar-postgres-admin-password"
  value        = random_password.postgres_admin.result
  key_vault_id = module.key_vault.id
}

resource "azurerm_resource_group" "postgres" {
  name     = "rg-northstar-postgres"
  # Postgres Flexible Server provisioning is restricted in eastus (the platform's
  # default region) for this subscription; eastus2 is the paired region and unrestricted.
  location = "eastus2"
}

module "postgres" {
  source = "./modules/postgres-flexible-server"

  server_name          = "psql-northstar-flex"
  resource_group_name  = azurerm_resource_group.postgres.name
  location             = azurerm_resource_group.postgres.location

  admin_username = "northstaradmin"
  admin_password = random_password.postgres_admin.result
  database_name  = "northstar"

  client_ip_address = var.postgres_client_ip

  tags = {
    project = "northstar"
    phase   = "postgres-fundamentals"
  }
}
