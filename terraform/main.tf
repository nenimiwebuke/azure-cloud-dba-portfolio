terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate-cloud-dba"
    storage_account_name = "stcloudbdatfstate6869"
    container_name       = "tfstate"
    key                  = "cloud-dba-portfolio.tfstate"
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "4cef5174-3663-46bd-9870-d117cf748336"
}

locals {
  common_tags = {
    Environment = "dev"
    Project     = "enterprise-data-platform"
    Owner       = "Nenim Iwebuke"
    ManagedBy   = "Terraform"
    CostCenter  = "Engineering"
  }
}

module "resource_group" {
  source = "./modules/resource-group"

  name     = "rg-cloud-dba-portfolio-dev"
  location = "East US"

  tags = local.common_tags
}

moved {
  from = azurerm_resource_group.portfolio
  to   = module.resource_group.azurerm_resource_group.this
}

module "networking" {
  source = "./modules/networking"

  resource_group_name = module.resource_group.name
  location            = module.resource_group.location

  vnet_name               = "vnet-cloud-dba-dev"
  vnet_address_space      = ["10.0.0.0/16"]
  subnet_name             = "subnet-cloud-dba-dev"
  subnet_address_prefixes = ["10.0.1.0/24"]
  nsg_name                = "nsg-cloud-dba-dev"
  public_ip_name          = "pip-cloud-dba-dev"
  nic_name                = "nic-cloud-dba-dev"

  tags = local.common_tags
}

moved {
  from = azurerm_virtual_network.portfolio_vnet
  to   = module.networking.azurerm_virtual_network.this
}

moved {
  from = azurerm_subnet.portfolio_subnet
  to   = module.networking.azurerm_subnet.this
}

moved {
  from = azurerm_network_security_group.portfolio_nsg
  to   = module.networking.azurerm_network_security_group.this
}

moved {
  from = azurerm_subnet_network_security_group_association.portfolio_subnet_nsg
  to   = module.networking.azurerm_subnet_network_security_group_association.this
}

moved {
  from = azurerm_public_ip.portfolio_public_ip
  to   = module.networking.azurerm_public_ip.this
}

moved {
  from = azurerm_network_interface.portfolio_nic
  to   = module.networking.azurerm_network_interface.this
}

module "storage_account" {
  source = "./modules/storage-account"

  resource_group_name = module.resource_group.name
  location            = module.resource_group.location

  storage_account_name     = "stclouddbaportfolio01"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  container_name           = "portfolio-data"
  container_access_type    = "private"

  # Preserve the current Azure configuration during structural migration.
  # Enterprise tags will be introduced in a separate reviewed change.
  tags = {}
}

moved {
  from = azurerm_storage_account.portfolio_storage
  to   = module.storage_account.azurerm_storage_account.this
}

moved {
  from = azurerm_storage_container.portfolio_blob
  to   = module.storage_account.azurerm_storage_container.this
}

module "azure_sql" {
  source = "./modules/azure-sql"

  resource_group_name = module.resource_group.name
  location            = "Central US"

  server_name                  = "sql-nenim-portfolio-cus-dev"
  server_version               = "12.0"
  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password

  database_name     = "CloudDBAPortfolioDB"
  database_sku_name = "Basic"

  firewall_rule_name        = "Allow-My-Current-IP"
  firewall_start_ip_address = "172.56.222.194"
  firewall_end_ip_address   = "172.56.222.194"

  # Preserve the current Azure configuration during structural migration.
  tags = {}
}

moved {
  from = azurerm_mssql_server.portfolio_sql_server
  to   = module.azure_sql.azurerm_mssql_server.this
}

moved {
  from = azurerm_mssql_database.portfolio_sql_db
  to   = module.azure_sql.azurerm_mssql_database.this
}

moved {
  from = azurerm_mssql_firewall_rule.allow_my_ip
  to   = module.azure_sql.azurerm_mssql_firewall_rule.client
}

module "log_analytics" {
  source = "./modules/log-analytics"

  name                = "law-cloud-dba-dev"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name

  sku               = "PerGB2018"
  retention_in_days = 30

  # Preserve the current configuration during structural migration.
  tags = {}
}

moved {
  from = azurerm_log_analytics_workspace.portfolio_law
  to   = module.log_analytics.azurerm_log_analytics_workspace.this
}

data "azurerm_client_config" "current" {}

module "key_vault" {
  source = "./modules/key-vault"

  name                = "kv-nenim-cloud-dba-dev"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  tenant_id           = data.azurerm_client_config.current.tenant_id

  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7

  # Preserve the current configuration during structural migration.
  tags = {}
}

moved {
  from = azurerm_key_vault.portfolio_kv
  to   = module.key_vault.azurerm_key_vault.this
}

resource "azurerm_data_factory" "portfolio_adf" {
  name                = "adf-nenim-cloud-dba-dev"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
}

module "data_lake" {
  source = "./modules/data-lake"

  resource_group_name = module.resource_group.name
  location            = module.resource_group.location

  storage_account_name     = "stnenimadlsdev01"
  account_tier             = "Standard"
  account_replication_type = "LRS"

  containers = [
    "bronze",
    "silver",
    "gold"
  ]

  # Preserve the current configuration during structural migration.
  tags = {}
}

moved {
  from = azurerm_storage_account.portfolio_adls
  to   = module.data_lake.azurerm_storage_account.this
}

moved {
  from = azurerm_storage_container.bronze
  to   = module.data_lake.azurerm_storage_container.layers["bronze"]
}

moved {
  from = azurerm_storage_container.silver
  to   = module.data_lake.azurerm_storage_container.layers["silver"]
}

moved {
  from = azurerm_storage_container.gold
  to   = module.data_lake.azurerm_storage_container.layers["gold"]
}

resource "azurerm_databricks_workspace" "portfolio_databricks" {
  name                = "dbw-nenim-cloud-dba-dev"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  sku                 = "trial"
}
