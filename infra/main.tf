// Terraform entry point for Azure AI Foundry lab infrastructure.

locals {
  tags = {
    project = "prisma-airs-lab"
  }
}

# Use the existing Resource Group without managing its lifecycle.
data "azurerm_resource_group" "target" {
  name = var.resource_group_name
}

# Needed for Key Vault tenant id
data "azurerm_client_config" "current" {}

# Storage Account for AI Foundry + general lab usage
resource "azurerm_storage_account" "storage" {
  name                     = "${lower(replace(var.name_prefix, "-", ""))}sa"
  location                 = var.location
  resource_group_name      = data.azurerm_resource_group.target.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  https_traffic_only_enabled      = true
  min_tls_version                 = "TLS1_2"
  public_network_access_enabled   = true
  shared_access_key_enabled       = true
  allow_nested_items_to_be_public = false

  tags = local.tags
}

resource "azurerm_key_vault" "kv" {
  name                = "${lower(replace(var.name_prefix, "-", ""))}kv"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.target.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  purge_protection_enabled = false

  tags = local.tags
}

resource "azurerm_ai_services" "ai" {
  name                = "${var.name_prefix}-aisvc"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.target.name

  sku_name = "S0"

  custom_subdomain_name = lower(replace("${var.name_prefix}-aisvc", "_", "-"))

  tags = local.tags
}

resource "azurerm_ai_foundry" "hub" {
  name                = "${var.name_prefix}-hub"
  location            = azurerm_ai_services.ai.location
  resource_group_name = data.azurerm_resource_group.target.name

  storage_account_id = azurerm_storage_account.storage.id
  key_vault_id       = azurerm_key_vault.kv.id

  identity {
    type = "SystemAssigned"
  }
  
  tags = local.tags
}

resource "azurerm_ai_foundry_project" "project" {
  name               = "${var.name_prefix}-proj"
  location           = azurerm_ai_foundry.hub.location
  ai_services_hub_id = azurerm_ai_foundry.hub.id

  identity {
    type = "SystemAssigned"
  }

  tags = local.tags
}
