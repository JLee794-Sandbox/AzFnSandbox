terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
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
data "azurerm_client_config" "current" {}
resource "azurerm_resource_group" "example" {
  name     = "lillypoc"
  location = "eastus"
}

resource "azurerm_function_app" "example" {
  name                       = "lilly-poc2-functionapp"
  location                   = "eastus"
  resource_group_name        = "lillypoc"
  app_service_plan_id        = azurerm_app_service_plan.example.id
  storage_account_name       = azurerm_storage_account.example.name
  storage_account_access_key = azurerm_storage_account.example.primary_access_key
}

resource "azurerm_app_service_plan" "example" {
  name                = "lillypoc2-appserviceplan"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_storage_account" "example" {
  name                     = "lillypoc2storacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_key_vault" "example" {
  name                = "lilly-poc2-keyvault"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name = "standard"
}
resource "azurerm_storage_account" "blob_storage" {
  count                    = var.enable_blob_storage ? 1 : 0
  name                     = "lillypocblobstoracc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "staging"
  }
}

resource "azurerm_storage_container" "blob_container" {
  count               = var.enable_blob_storage ? 1 : 0
  name                = "content"
  storage_account_name = azurerm_storage_account.blob_storage[0].name
  container_access_type = "private"
}
