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

resource "azurerm_resource_group" "portfolio" {
  name     = "rg-cloud-dba-portfolio-dev"
  location = "East US"
}

resource "azurerm_virtual_network" "portfolio_vnet" {
  name                = "vnet-cloud-dba-dev"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.portfolio.location
  resource_group_name = azurerm_resource_group.portfolio.name
}

resource "azurerm_subnet" "portfolio_subnet" {
  name                 = "subnet-cloud-dba-dev"
  resource_group_name  = azurerm_resource_group.portfolio.name
  virtual_network_name = azurerm_virtual_network.portfolio_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_security_group" "portfolio_nsg" {
  name                = "nsg-cloud-dba-dev"
  location            = azurerm_resource_group.portfolio.location
  resource_group_name = azurerm_resource_group.portfolio.name

  security_rule {
    name                       = "Deny-All-Inbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "portfolio_subnet_nsg" {
  subnet_id                 = azurerm_subnet.portfolio_subnet.id
  network_security_group_id = azurerm_network_security_group.portfolio_nsg.id
}

resource "azurerm_public_ip" "portfolio_public_ip" {
  name                = "pip-cloud-dba-dev"
  location            = azurerm_resource_group.portfolio.location
  resource_group_name = azurerm_resource_group.portfolio.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_network_interface" "portfolio_nic" {
  name                = "nic-cloud-dba-dev"
  location            = azurerm_resource_group.portfolio.location
  resource_group_name = azurerm_resource_group.portfolio.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.portfolio_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.portfolio_public_ip.id
  }
}

resource "azurerm_storage_account" "portfolio_storage" {
  name                = "stclouddbaportfolio01"
  resource_group_name = azurerm_resource_group.portfolio.name
  location            = azurerm_resource_group.portfolio.location

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
  resource_group_name          = azurerm_resource_group.portfolio.name
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
