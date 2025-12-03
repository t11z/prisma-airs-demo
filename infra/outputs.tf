// Terraform outputs for downstream scripts and deployments.

output "ai_foundry_hub_name" {
  description = "Name of the Azure AI Foundry Hub."
  value       = azurerm_ai_foundry_hub.hub.name
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
  description = "Name of the Azure AI Services (Cognitive Services) resource."
  value       = azurerm_cognitive_account.openai.name
}

output "ai_services_endpoint" {
  description = "Endpoint for the Azure AI Services resource." // TODO: Confirm endpoint attribute if resource changes.
  value       = azurerm_cognitive_account.openai.endpoint
}

output "storage_account_name" {
  description = "Name of the Storage Account used by the lab."
  value       = azurerm_storage_account.storage.name
}

// Search service output is optional; uncomment when the resource is enabled.
// output "search_service_name" {
//   description = "Name of the Azure AI Search service."
//   value       = azurerm_search_service.search.name
// }
