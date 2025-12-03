# ✨ Prisma AIRS Azure Foundry Lab — One-Click Demo Environment

**Your reproducible, high-level lab to demonstrate Prisma AIRS inside Azure AI Foundry.**  
Deploy a complete sandbox — Hub, Project, Azure OpenAI, Storage, GitHub Actions automations —  
and run a Prompt Flow that wraps your model with **Prisma AIRS input/output scanning**.

Designed for:

- 🏴 Palo Alto Networks **Solutions Consultants & Domain Consultants**
- 🧪 **POVs, Workshops, Executive Demos**
- 🤖 Anyone who wants a **zero-pain**, reproducible, secure AI sandbox

---

## 🧠 What This Lab Gives You

### ✅ 1. Fully automated Azure AI Foundry environment (Terraform)
You get:

- Azure AI Foundry **Hub**
- Azure AI Foundry **Project**
- Azure OpenAI (SKU ```S0```)
- Storage Account
- GitHub Actions pipelines for:
  - **```deploy-infra```** → Provision the entire environment  
  - **```deploy-flow```** → Import your Prisma AIRS–secured Prompt Flow

Everything deploys with a single button click.

---

### ✅ 2. Prisma AIRS secured Prompt Flow
The included Prompt Flow performs:

🛡 **Input Scan** — User prompt scanned via Prisma AIRS before it reaches the model  
🤖 **LLM Invocation** — Azure OpenAI model of your choice  
🛡 **Output Scan** — Model response scanned before reaching the user

This demonstrates the **full inline protection pattern** recommended for secure AI applications.

---

## 📦 Repository Structure

```
/
├─ infra/ → Terraform modules for Hub, Project, AOAI, Storage
├─ flows/
│ ├─ prisma_airs_chat/ → Prompt Flow DAG, schema, inputs
│ └─ tools/
│ └─ prisma_airs_scan.py → Prisma AIRS input/output scan logic
├─ scripts/
│ ├─ deploy_flow.py → (Optional) automation helper for Prompt Flow deployment
│ └─ load_infra_outputs.py → Parses Terraform outputs for automation
└─ .github/workflows/
├─ deploy-infra.yml → Creates entire Azure AI Foundry environment
└─ deploy-flow.yml → Deploys Prompt Flow (optional placeholder logic)
```


## 🧩 Prerequisites

You must have:

### Azure
- A **Resource Group** where you are at least ```Contributor```  
  (SC/DCs: create via the internal **Torque**)

### Prisma AIRS
- A valid **Prisma AIRS API Key** (or API Token)
- Recommended environment variables:

```bash
PANW_AI_SEC_API_KEY
PANW_AI_SEC_API_TOKEN (optional)
PANW_AI_SEC_PROFILE_NAME (default: Secure-AI)
PANW_AI_SEC_API_ENDPOINT (EU/US depending on tenant)
```
(You can also use ```PRISMA_AIRS_API_KEY``` as fallback.)

### GitHub
- Fork or copy this repository
- Configure the following GitHub secrets:
  - ```AZURE_CLIENT_ID```  
  - ```AZURE_TENANT_ID```  
  - ```AZURE_SUBSCRIPTION_ID```  
  - (optional) ```AZURE_RESOURCE_GROUP``` if you want your Actions to target a fixed RG

---

## 🚀 Deployment — 2 Steps

### **Step 1 — Deploy Infrastructure**
Go to:

**GitHub → Actions → Deploy Infra (Terraform) → Run workflow**

This will:
- authenticate via OIDC  
- initialize Terraform  
- create the Hub, Project, AOAI, and Storage resources  
- export ```infra-outputs.json```

🟢 When it finishes, your Azure environment is ready.

---

### **Step 2 — Deploy the Prompt Flow**
Run:

**GitHub → Actions → Deploy Prompt Flow → Run workflow**

This will:
- read ```infra-outputs.json```  
- install Prisma AIRS + Azure ML SDK dependencies  
- prepare the Prompt Flow for import  

Because the Foundry Flow API is not yet fully exposed via Python,  
you finalize the Flow in Azure AI Foundry:

1. Open Azure Portal → AI Foundry → Hub → Project  
2. Go to **Prompt Flows**  
3. Click **Import**, select: ```flows/prisma_airs_chat/```
4. Select your Azure OpenAI connection + model deployment  
5. Run it in the built-in Chat UI

Your secured chat flow is now ready.

---

## 🔐 How Prisma AIRS Is Integrated

The core logic lives in:

```bash
flows/tools/prisma_airs_scan.py
```

It performs:

- ```scan_input(content, user_id)```  
- ```scan_output(content, user_id)```  

Both use:

- ```Scanner.sync_scan(...)```  
- ```AiProfile(profile_name="Secure-AI")```  
- Prisma AIRS inline scanning for:
  - sensitive data
  - harmful prompts
  - harmful model outputs
  - hallucination detection (depending on your profile)
  - content transformations / sanitization

The Prompt Flow uses the fields:

- ```output.scanned_content```  
- ```output.status```  
- ```output.result```  

to route cleaned text into and out of the LLM.

---

## 🛠 Customization

### Model
In ```flow.dag.yaml```, update:

```yaml
connection: <your-AOAI-connection>
deployment_name: <your-model-deployment>
```

### Profiles
Control Prisma AIRS behavior via:

```
PANW_AI_SEC_PROFILE_NAME
PANW_AI_SEC_API_ENDPOINT
```

### Environment Naming
Set in Terraform:

```yaml
name_prefix = "<your-prefix>"
location = "westeurope" | "eastus2" | ...
```

## 🧪 Troubleshooting

### Prisma AIRS scan always returns “skipped”
Check env vars:

```yaml
PANW_AI_SEC_API_KEY
PANW_AI_SEC_API_TOKEN (if used)
```

### Prompt Flow can’t find the model
Make sure your AOAI deployment name matches exactly.

### Deployment script doesn't upload the flow
This is expected — the Flow Upload API is in preview.  
For now, import manually inside AI Foundry (takes 5 seconds).