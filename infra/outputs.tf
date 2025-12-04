// Terraform outputs for downstream scripts and deployments.

output "ai_foundry_hub_name" {
  description = "Name of the Azure AI Foundry Hub."
  value       = azurerm_ai_foundry.hub.name
}

output "ai_foundry_project_name" {
  description = "Name of the Azure AI Foundry Project."
  value       = azurerm_ai_foundry_project.project.name
}

output "location" {
  description = "Deployment location."
  value       = var.location
}

output "ai_services_name" {
  description = "Name of the Azure AI Services resource."
  value       = azurerm_ai_services.ai.name
}

output "ai_services_endpoint" {
  description = "Endpoint for the Azure AI Services resource."
  value       = azurerm_ai_services.ai.endpoint
}

output "storage_account_name" {
  description = "Name of the Storage Account used by the lab."
  value       = data.azurerm_storage_account.storage.name
}
