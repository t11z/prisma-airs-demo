Prisma AIRS + Azure AI Foundry Lab
A guided lab for Palo Alto Networks Solutions Consultants to deploy and demonstrate Prisma AIRS protections inside Azure AI Foundry.

Why this project exists
- Solutions Consultants need a repeatable, fast lab environment that mirrors customer-ready deployments.
- The lab uses the native Azure AI Foundry UI, so no custom frontend or app build is required.
- Prisma AIRS integrates into Prompt Flow to scan both prompts and responses for safer AI interactions.

Prerequisites
- An existing Azure Resource Group where you have Contributor access (the group must be created before running Terraform).
- An Azure subscription that supports Azure AI Foundry and associated services in your chosen region.
- A Prisma AIRS tenant and API key available for scanning requests and responses.
- Local tools installed: az CLI, terraform, python, and pip available on your PATH.
- Awareness of Key Vault and secrets: the deployment expects to store secrets securely; ensure you can set and read secrets in the target Resource Group.

Architecture Overview
The lab layers Prisma AIRS into an Azure AI Foundry deployment inside a pre-created Resource Group. The flow below shows the main components and how Prisma AIRS wraps the Prompt Flow traffic.

[ Resource Group ]
  |
  |-- Terraform provisioning layer
  |     |
  |     |-- Azure AI Foundry Hub
  |     |     |
  |     |     '-- Project
  |     |
  |     |-- Azure AI Services (model endpoints)
  |     |-- Storage Account
  |     '-- Optional Azure AI Search
  |
  |-- Prompt Flow (runs inside the Project)
        |
        '-- Prisma AIRS scans input and output traffic

End-to-End Usage Guide
Follow these steps to deploy and test the lab end to end:
1) Clone the repository
   git clone https://github.com/PaloAltoNetworks/prisma-airs-azure-foundry-lab.git
   cd prisma-airs-azure-foundry-lab
2) Configure environment variables
   Copy infra/env/demo.tfvars and edit values for your Resource Group, region, and service choices.
3) Initialize and apply Terraform
   cd infra
   terraform init
   terraform apply -var-file=env/demo.tfvars
4) Capture outputs for flow deployment
   terraform output -json > ../infra-outputs.json
   cd ..
5) Install flow dependencies
   pip install -r flows/requirements.txt
6) Deploy the Prompt Flow with Prisma AIRS integration
   python scripts/deploy_flow.py --config infra-outputs.json
7) Open Azure AI Foundry
   In the Azure portal, open the AI Foundry Project, navigate to Prompt Flow, and run a test chat to verify Prisma AIRS scanning.

Troubleshooting
- Region not supported: Switch the region in your tfvars file to one that offers Azure AI Foundry and Azure AI Services.
- Missing Contributor access: Confirm your account has Contributor on the target Resource Group; owners can assign via Access control (IAM).
- Missing Prisma AIRS API key: Request a valid key from your Prisma AIRS tenant admin and set it before deploying the flow.
- Key Vault scope or credential issues: Ensure the Key Vault resides in the same Resource Group and your identity has set/get permissions for secrets.
- Flow deployment failure: Re-run terraform output to refresh infra-outputs.json, reinstall dependencies, and verify your network connectivity to Azure endpoints.

Roadmap
- [x] PR 1–6 completed
- [ ] PR 8 GitHub Actions
- [ ] PR 9 RAG Add-on
- [ ] PR 10 Demo Profiles

License
This project is licensed under the MIT License. See LICENSE for details.
