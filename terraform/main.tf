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

module "resource_group" {
  source = "./modules/resource-group"

  name     = "rg-cloud-dba-portfolio-dev"
  location = "East US"

  tags = {}
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

  tags = {}
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

resource "azurerm_storage_account" "portfolio_storage" {
  name                = "stclouddbaportfolio01"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location

  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "portfolio_blob" {
  name                  = "portfolio-data"
  storage_account_id    = azurerm_storage_account.portfolio_storage.id
  container_access_type = "private"
}

resource "azurerm_mssql_server" "portfolio_sql_server" {
  name                         = "sql-nenim-portfolio-cus-dev"
  resource_group_name          = module.resource_group.name
  location                     = "Central US"
  version                      = "12.0"
  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password
}

resource "azurerm_mssql_database" "portfolio_sql_db" {
  name      = "CloudDBAPortfolioDB"
  server_id = azurerm_mssql_server.portfolio_sql_server.id

  sku_name = "Basic"
}

resource "azurerm_mssql_firewall_rule" "allow_my_ip" {
  name             = "Allow-My-Current-IP"
  server_id        = azurerm_mssql_server.portfolio_sql_server.id
  start_ip_address = "172.56.222.194"
  end_ip_address   = "172.56.222.194"
}

resource "azurerm_log_analytics_workspace" "portfolio_law" {
  name                = "law-cloud-dba-dev"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "portfolio_kv" {
  name                = "kv-nenim-cloud-dba-dev"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
  tenant_id           = data.azurerm_client_config.current.tenant_id

  sku_name = "standard"

  purge_protection_enabled   = false
  soft_delete_retention_days = 7
}

resource "azurerm_data_factory" "portfolio_adf" {
  name                = "adf-nenim-cloud-dba-dev"
  location            = module.resource_group.location
  resource_group_name = module.resource_group.name
}

resource "azurerm_storage_account" "portfolio_adls" {
  name                     = "stnenimadlsdev01"
  resource_group_name      = module.resource_group.name
  location                 = module.resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  is_hns_enabled = true
}

resource "azurerm_storage_container" "bronze" {
  name                  = "bronze"
  storage_account_id    = azurerm_storage_account.portfolio_adls.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "silver" {
  name                  = "silver"
  storage_account_id    = azurerm_storage_account.portfolio_adls.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "gold" {
  name                  = "gold"
  storage_account_id    = azurerm_storage_account.portfolio_adls.id
  container_access_type = "private"
}

resource "azurerm_databricks_workspace" "portfolio_databricks" {
  name                = "dbw-nenim-cloud-dba-dev"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  sku                 = "trial"
}
