locals {
  tags = {
    APPLICATION = var.application_name
    ENVIRONMENT = var.environment
    COST_CENTER = var.cost_center
    PROJECT     = var.project
    OWNER       = var.owner
  }
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "this" {
  name     = "${var.application_name}-rg"
  location = var.location

  tags = local.tags
}

resource "azurerm_linux_function_app" "this" {
  name                       = "${var.application_name}-functionapp"
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  service_plan_id            = azurerm_service_plan.this.id
  storage_account_name       = azurerm_storage_account.this.name
  storage_account_access_key = azurerm_storage_account.this.primary_access_key

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      # docker {
      #   registry_url = azurerm_container_registry.acr.login_server
      #   image_name = 
      #   image_tag = 
      # }
      python_version = var.python_version
    }
  }
  tags = local.tags
}

resource "azurecaf_name" "acr" {
  name          = var.application_name
  resource_type = "azurerm_container_registry"
  prefixes      = []
  suffixes      = []
  clean_input   = true
}

resource "azurerm_container_registry" "acr" {
  name                = azurecaf_name.acr.result
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = "Standard"
  admin_enabled       = false

  tags = local.tags
}

resource "azurerm_service_plan" "this" {
  name                = "lillypoc2-appserviceplan"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name

  os_type  = "Linux"
  sku_name = "S1"

  tags = local.tags
}

resource "azurerm_storage_account" "this" {
  name                     = "lillypoc2storacc"
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = local.tags
}

resource "azurerm_key_vault" "this" {
  name                      = "${var.application_name}-kv"
  location                  = azurerm_resource_group.this.location
  resource_group_name       = azurerm_resource_group.this.name
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  enable_rbac_authorization = true

  tags = local.tags
}

resource "azurerm_storage_account" "blob_storage" {
  count                    = var.enable_blob_storage ? 1 : 0
  name                     = "lillypocblobstoracc"
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = local.tags
}

resource "azurerm_storage_container" "blob_container" {
  count                 = var.enable_blob_storage ? 1 : 0
  name                  = "content"
  storage_account_name  = azurerm_storage_account.blob_storage[0].name
  container_access_type = "private"
}

resource "azurerm_role_assignment" "fnapp_to_acr" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_function_app.this.identity[0].principal_id
}

resource "azurerm_role_assignment" "fnapp_to_kv" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_function_app.this.identity[0].principal_id
}