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

resource "azurerm_ai_foundry_hub" "hub" {
  name                = "${var.name_prefix}-hub"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.target.name

  identity {
    type = "SystemAssigned"
  }

  # Ensure the Resource Group and the hub share the same region.
  tags = local.tags
}

resource "azurerm_ai_foundry_project" "project" {
  name                = "${var.name_prefix}-proj"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.target.name
  hub_id              = azurerm_ai_foundry_hub.hub.id

  identity {
    type = "SystemAssigned"
  }

  tags = local.tags
}

resource "azurerm_cognitive_account" "openai" {
  name                = "${var.name_prefix}aoai"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.target.name

  kind     = "OpenAI"
  sku_name = "S0"

  network_acls {
    default_action = "Allow"
  }

  public_network_access_enabled = true

  tags = local.tags
}

resource "azurerm_storage_account" "storage" {
  name                     = "${lower(replace(var.name_prefix, "-", ""))}sa"
  location                 = var.location
  resource_group_name      = data.azurerm_resource_group.target.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  enable_https_traffic_only      = true
  min_tls_version                = "TLS1_2"
  public_network_access_enabled  = true
  shared_access_key_enabled      = true
  allow_nested_items_to_be_public = false

  tags = local.tags
}

# Optional Azure AI Search service for retrieval scenarios.
# TODO: Uncomment and adjust if search is required for Prompt Flow deployments.
# resource "azurerm_search_service" "search" {
#   name                = "${var.name_prefix}-search"
#   location            = var.location
#   resource_group_name = data.azurerm_resource_group.target.name
#
#   sku              = "basic"
#   partition_count  = 1
#   replica_count    = 1
#   hosting_mode     = "Default"
#
#   public_network_access_enabled = true
#
#   tags = local.tags
# }
