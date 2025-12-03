Environment Configuration Samples

The env directory holds tfvars files for each lab variant. Copy a sample like demo.tfvars, rename it to match your deployment, and update values before running Terraform.

Key reminders
- The target Resource Group must already exist and you must have Contributor permissions.
- Adjust region, AI service selections, and naming prefixes to fit your subscription policies.
- Store sensitive values such as API keys and secrets in Key Vault or your secure secret manager.
- For the full workflow, see the root README.md for deployment and flow steps.

Example variables
resource_group_name   = <existing-resource-group>
location              = <supported-region>
ai_services_sku       = standard
project_display_name  = Prisma AIRS Azure Foundry Lab
