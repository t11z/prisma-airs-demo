// Input variables for the Azure AI Foundry lab deployment.

// Name of the existing Resource Group where all resources will be created.
variable "resource_group_name" {
  type        = string
  description = "Name of the existing Azure Resource Group to deploy into."
}

// Azure region where the resources should live (should match the Resource Group).
variable "location" {
  type        = string
  description = "Azure region for the deployment (must align with the Resource Group location)."
}

// Prefix used to build unique resource names across the deployment.
variable "name_prefix" {
  type        = string
  description = "Prefix for resource naming to ensure uniqueness across the environment."
}

// Name of an existing, policy-compliant Storage Account used by the deployment.
variable "storage_account_name" {
  type        = string
  description = "Name of an existing, policy-compliant Storage Account in the target Resource Group."
}
