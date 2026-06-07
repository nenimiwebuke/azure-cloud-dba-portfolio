terraform {
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
