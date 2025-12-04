# ✨ Azure AI Foundry Lab with Prisma AIRS Integration

This repository provides a reproducible lab environment for experimenting with Azure AI Foundry and Prisma AIRS.  
It is designed as a self-contained, infrastructure‑as‑code–driven project that deploys the necessary Azure resources and a Prompt Flow integrating Prisma AIRS input/output scanning.

The repository operates entirely without CI/CD or service principals.  
All deployments are performed either:

- **locally**, using Azure CLI + Terraform, or  
- **inside Azure Cloud Shell**, which already includes all required tools.

---

# 📘 Overview

The lab environment includes:

- An **Azure AI Foundry Hub**
- An **Azure AI Foundry Project**
- An **Azure AI Services** resource (successor to Azure OpenAI)
- A **Storage Account** for Foundry metadata
- A **Key Vault** used by the Foundry Hub
- A **Prompt Flow** that applies Prisma AIRS inline scanning before and after model inference

This setup enables evaluation of AI application behavior under Prisma AIRS policies with minimal manual wiring.

---

# 📂 Repository Structure

```
/
├─ infra/                      Infrastructure-as-code for Azure resources (Terraform)
│   ├─ main.tf
│   ├─ outputs.tf
│   ├─ variables.tf
│   ├─ providers.tf
│   └─ env/
│       └─ demo.tfvars        Example variable file (created by the user)
│
├─ flows/
│   ├─ prisma_airs_chat/      Prompt Flow definition
│   └─ tools/
│       └─ prisma_airs_scan.py  AIRS scanning helper functions
│
├─ scripts/
│   ├─ deploy_flow.py         Optional helper for manual experimentation
│   └─ load_infra_outputs.py  Parses Terraform outputs for scripts
│
└─ README.md
```

---

# 🏗️ Infrastructure Architecture

The infrastructure creates:

1. **Azure AI Foundry Hub**  
   A workspace‑level container for AI development components.

2. **Azure AI Foundry Project**  
   A project environment mapped into the hub.

3. **Azure AI Services Resource**  
   Required for Prompt Flow model access.

4. **Storage Account**  
   Stores Foundry metadata and artifacts.

5. **Key Vault**  
   Provides secrets and encryption keys referenced by the Foundry Hub.

The Terraform configuration requires an existing Resource Group.  
No elevated privileges (e.g., subscription-level Contributor) are necessary.

---

# 🔧 Terraform Configuration

Terraform requires the following variables:

```
subscription_id      = "<your-subscription-id>"
resource_group_name  = "<existing-resource-group>"
location             = "<region-of-resource-group>"
name_prefix          = "<short-prefix-for-names>"
```

These are provided in a `.tfvars` file, e.g. `infra/env/demo.tfvars`.

Retrieve subscription ID:

```
az account show --query id -o tsv
```

---

# 🌐 Deploying the Infrastructure

## Option A: Azure Cloud Shell (recommended)

Azure Cloud Shell includes Terraform and Azure CLI.

### 1. Open Cloud Shell  
https://shell.azure.com  
Select **Bash**.

### 2. Clone the repository

```
git clone <your-repo-url>
cd <repo-name>/infra
```

### 3. Create `env/demo.tfvars`

```
subscription_id      = "<your-subscription-id>"
resource_group_name  = "<your-existing-rg>"
location             = "westeurope"
name_prefix          = "airsdemo"
```

### 4. Initialize Terraform

```
terraform init -upgrade
```

### 5. Deploy

```
terraform apply -var-file=env/demo.tfvars
```

---

## Option B: Local Machine Deployment

### 1. Install prerequisites
- Azure CLI
- Terraform
- Python 3.10+

### 2. Authenticate

```
az login
az account set --subscription "<your-subscription-id>"
```

### 3. Deploy (same steps as Cloud Shell)

```
cd infra
terraform init -upgrade
terraform apply -var-file=env/demo.tfvars
```

---

# 🤖 Prompt Flow With Prisma AIRS

Flow structure:

```
User Input
   ↓
Prisma AIRS Input Scan
   ↓ sanitized content
Model Invocation
   ↓
Prisma AIRS Output Scan
   ↓ sanitized content
Final Response
```

Each scan returns:

- `scanned_content`
- `status`
- `reason`
- `result`

---

# 🔐 Configuring Prisma AIRS

Set one of these environment variables:

```
PRISMA_AIRS_API_KEY
PANW_AI_SEC_API_KEY
PANW_AI_SEC_API_TOKEN
```

Optional overrides:

```
PANW_AI_SEC_PROFILE_NAME
PANW_AI_SEC_API_ENDPOINT
```

---

# 🧪 Local Testing

```
export PRISMA_AIRS_API_KEY="..."
python
```

```
from flows.tools.prisma_airs_scan import scan_input
scan_input("test message", user_id="local-demo")
```

---

# 🧱 Design Principles

- Minimal prerequisites  
- No CI/CD dependency  
- Predictable infrastructure  
- Clear separation of concerns  

---

# 📜 License

This project is provided for demonstration and exploration purposes.
