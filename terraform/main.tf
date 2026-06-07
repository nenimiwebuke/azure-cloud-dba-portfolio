terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
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
