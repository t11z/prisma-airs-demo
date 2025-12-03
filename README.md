# Prisma AIRS + Azure AI Foundry Lab

Spin up a Prisma AIRS-protected Azure AI Foundry playground for Palo Alto Networks Solutions Consultants, Domain Consultants, customers evaluating Prisma AIRS, and any other interested practitioner.

## Overview
This repository is a lab and demo starter kit for Palo Alto Networks Solutions Consultants, Domain Consultants, customers evaluating Prisma AIRS, and anyone who wants to explore the integration. It will provision an Azure AI Foundry Hub and Project, connect a Prompt Flow that routes conversations through Prisma AIRS, and showcase a secured AI assistant experience. The long-term goal is to let you use the native Azure AI Foundry UI as your chat surface while Prisma AIRS provides input and output scanning.

Use this project to:
- Stand up an Azure AI Foundry environment inside an existing resource group.
- Deploy a Prompt Flow that leverages Prisma AIRS for safety controls.
- Demonstrate the Prisma AIRS and Azure AI pairing with minimal custom code.

## High-Level Architecture
The environment is designed around a pre-created Azure Resource Group, with Terraform handling the Azure AI components and Prisma AIRS providing security for every prompt and response.

```
[ Azure Resource Group ]
        |
        |-- Terraform deploys: Azure AI Foundry Hub + Project + supporting services
        |
        |-- Prompt Flow runs inside the Project
        |
        '-- Prisma AIRS scans input and output around the Flow
```

## Prerequisites
- Existing empty Azure Resource Group where you have Contributor permissions.
- Access to an Azure subscription that supports Azure AI Foundry and Azure OpenAI.
- Prisma AIRS tenant and API key.
- Local tooling: `az` CLI, `terraform`, `python`, and `pip` (exact versions will be detailed later).

## Folder Structure
- `infra/` — Terraform scaffolding for Azure AI Foundry Hub, Project, and related services.
- `flows/` — Prompt Flow assets, including tools and prompts that will integrate Prisma AIRS.
- `scripts/` — Helper scripts for deploying flows and loading Terraform outputs.
- `.github/` — GitHub Actions workflows for automation.

## Planned End-to-End Flow (Future State)
Once the implementation is complete, the journey should look like this:
1. Clone the repository.
2. Configure `infra/env/demo.tfvars` for your environment.
3. Run `terraform apply` from `infra/` to build Azure AI Foundry resources.
4. Export Terraform outputs into `infra-outputs.json`.
5. Install Python dependencies via `pip install -r flows/requirements.txt`.
6. Deploy the Prompt Flow with `python scripts/deploy_flow.py --config infra-outputs.json`.
7. Open the Azure AI Foundry UI and start chatting with the Prisma AIRS-protected assistant.

Several of these steps are placeholders today and will be delivered in upcoming iterations.

## Status & Roadmap
- [x] Repo scaffold & README
- [ ] Terraform: Azure AI Foundry infra
- [ ] Prisma AIRS tool integration
- [ ] Flow deployment script
- [ ] GitHub Actions automation

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
