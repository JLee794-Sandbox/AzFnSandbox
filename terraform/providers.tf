terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    azurecaf = {
      source = "aztfmod/azurecaf"
    }
  }
  backend "azurerm" {
    resource_group_name  = "validation-rg"
    storage_account_name = "tfstateadoutilities"
    container_name       = "azfnsandboxtf"
    key                  = "terraform.tfstate"
  }

}
provider "azurerm" {
  features {}
  skip_provider_registration = true
}