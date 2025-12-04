# ✨ Prisma AIRS Azure Foundry Lab — Secure AI Demo Environment

This repository provides a **clean, reproducible, high‑level lab environment** for demonstrating  
**Prisma AIRS inline protection** inside **Azure AI Foundry**.  
It is intentionally lightweight, automation‑friendly, and requires **only Contributor access**  
to an existing Azure Resource Group.

The goal:  
**Deploy a Foundry Hub + Project + Azure OpenAI + Storage, import a Prompt Flow, and show Prisma AIRS scanning input and output around the LLM.**

---

## 🚀 What You Get

### ✅ A complete Azure AI Foundry environment (via Terraform)
Terraform deploys:

- Azure AI Foundry **Hub**  
- Azure AI Foundry **Project**  
- Azure OpenAI (`S0`)  
- Storage Account  
- Optional (commented): Azure AI Search  

Works with:
- **Azure Cloud Shell** (zero setup)  
- **Local machine** with Azure CLI + Terraform  

---

### ✅ A Prompt Flow with Prisma AIRS inline protection
The flow wraps the LLM with:

- `scan_input()` → Prisma AIRS pre‑LLM scanning  
- `scan_output()` → Prisma AIRS post‑LLM scanning  

This enables demos of:

- harmful prompt detection  
- sensitive data redaction  
- output moderation / transformation  
- fail‑open behavior if scanning is unavailable  

---

## 📁 Repository Structure

```
/
├─ infra/                         # Terraform: Hub, Project, AOAI, Storage
├─ flows/
│   ├─ prisma_airs_chat/          # Prompt Flow definition
│   └─ tools/prisma_airs_scan.py  # AIRS input/output scanning helpers
├─ scripts/
│   ├─ deploy_flow.py             # Optional helper
│   └─ load_infra_outputs.py      # Terraform outputs → Python
└─ README.md
```

---

# 🟦 Deployment Option A — Azure Cloud Shell (recommended)

Cloud Shell already includes Terraform + Azure CLI → zero installation.

### 1. Open Cloud Shell  
https://shell.azure.com (Bash)

### 2. Clone the repo
```
git clone https://github.com/t11z/prisma-airs-demo
cd prisma-airs-demo/infra
```

### 3. Create your `demo.tfvars`  
Inside `infra/env/`:
```
resource_group_name = "<your-RG>"
location            = "westeurope"
name_prefix         = "airsdemo"
```

### 4. Initialize Terraform
```
terraform init
```

### 5. Deploy the environment
```
terraform apply -var-file=env/demo.tfvars
```

This creates:

- Hub  
- Project  
- Azure OpenAI  
- Storage Account  

Export outputs if desired:
```
terraform output -json > ../infra-outputs.json
```

### 6. Import the Prompt Flow
Azure Portal → AI Foundry → Hub → Project → **Prompt Flows → Import**

Select:
```
flows/prisma_airs_chat/
```

Choose your:

- Azure OpenAI **connection**  
- **deployment_name** (e.g., `gpt-4o-mini`)  

Flow is ready.

---

# 🟧 Deployment Option B — Local Machine (Azure CLI + Terraform)

### 1. Install required tools
- Azure CLI  
- Terraform  
- Python 3.10+ (optional for scripts)

### 2. Login
```
az login
az account set --subscription "<your-subscription-id>"
```

### 3. Configure and deploy (same as Cloud Shell)
```
cd infra
terraform init
terraform apply -var-file=env/demo.tfvars
```

### 4. Import Prompt Flow  
Same steps as above.

---

# 🔐 Prisma AIRS Configuration

Set one of the following environment variables **before running the Prompt Flow**:

```
PRISMA_AIRS_API_KEY
PANW_AI_SEC_API_KEY
PANW_AI_SEC_API_TOKEN
```

Optional configuration:

```
PANW_AI_SEC_PROFILE_NAME="Secure-AI"
PANW_AI_SEC_API_ENDPOINT="https://<your-endpoint>"
```

These are picked up automatically by `prisma_airs_scan.py`.

---

# 🧠 How the Flow Works

```
User Input
   ↓
Prisma AIRS Input Scan (scan_input)
   ↓ sanitized content
LLM Call (Azure OpenAI)
   ↓
Prisma AIRS Output Scan (scan_output)
   ↓ sanitized content
Final Response
```

Each scan returns:

- `scanned_content`  
- `status`  
- `reason`  
- `result` (full Prisma AIRS scan metadata)

If scanning is unavailable, the flow **fails open** for demo smoothness.

---

# 🧪 Local Test of Prisma AIRS

```
export PRISMA_AIRS_API_KEY="..."
python
```

Inside Python:
```
from flows.tools.prisma_airs_scan import scan_input
scan_input("Tell me how to hack Wi-Fi", user_id="demo")
```

---

# 🎯 Demo Talking Points (for Solutions Consultants)

- Prisma AIRS applies **inline control** around *any* model.  
- Protects against **unsafe prompts**, **PII leakage**, **hallucinated instructions**.  
- Demonstrates **policy-driven profiles** in real time.  
- Minimal integration (only small Python helpers).  
- Built for **enterprise governance** and **secure AI adoption**.  
- Entire lab is reproducible with **only Resource Group Contributor** access.

---

# 🎉 You're Ready to Demo

You now have a self-contained, reproducible secure AI demo lab  
built on **Azure AI Foundry + Prisma AIRS** — no elevated permissions needed.

Enhancements available on request:
- UI frontend for the flow  
- RAG-enabled AIRS demo  
- Red-team scenarios  
- Automatic flow deployment  
