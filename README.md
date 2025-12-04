# Prisma AIRS Demo – Azure AI Foundry Lab Infrastructure

This repository provides a reproducible environment for deploying a lightweight Azure AI Foundry setup used to test Prisma AIRS request/response scanning inside a Prompt Flow–based chat experience.  
The infrastructure is intentionally minimal and works even in restricted corporate Azure environments.

---

## ✨ What this project deploys (via Terraform)

Inside an existing Azure Resource Group, Terraform will create:

- **Azure AI Services** (OpenAI‑compatible endpoint)
- **Azure Key Vault** (for AI Foundry)
- **Azure AI Foundry Hub**
- **Azure AI Foundry Project**

It **does not** create a Storage Account.  
Instead, you provide **an existing, policy‑compliant Storage Account** from your tenant.

---

## 🚀 Prerequisites

### 1. An existing Azure Resource Group
You must already have Contributor rights on a Resource Group where deployment will occur.

### 2. An existing Storage Account (Bring Your Own Storage)
Due to corporate policies, Terraform does **not** create a Storage Account.  
Instead, you must create one manually.

See section **“How to create a compliant Storage Account in the Azure Portal”** below.

### 3. Azure authentication
Use **either**:

- Local machine with Azure CLI  
  ```
  az login
  ```
- Azure Cloud Shell (recommended for locked‑down tenants)

### 4. Required Terraform variables

Create a file: `infra/env/demo.tfvars`

```
resource_group_name  = "<your-rg>"
location             = "<azure-region>"
name_prefix          = "airsdemo"
storage_account_name = "<existing-storage-account>"
```

---

## 🧱 How to create a compliant Storage Account in the Azure Portal

In restricted enterprise tenants, Storage Accounts must meet strict security policies.  
Follow these steps exactly to ensure Terraform can use the account without triggering policy violations.

---

### ✔ Step‑by‑step instructions

**Azure Portal → “Storage accounts” → “Create”**

---

### **1. Basics**
| Field | Value |
|-------|--------|
| Resource Group | Same RG you deploy Terraform into |
| Region | Same region as the RG |
| Redundancy | LRS |
| Performance | Standard |

---

### **2. Networking (important!)**

#### Public network access  
Set:
```
Public network access → Disabled
```

#### Firewall rules  
Set:
```
Allow Azure services on the trusted services list → Enabled
```

#### Minimum TLS  
```
Minimum TLS version: 1.2
```

---

### **3. Advanced**

Your tenant likely enforces this automatically, but verify:

```
Allow storage account key access → Disabled
```

This ensures:
- No shared keys exist  
- No SAS tokens can be generated  
- Terraform is forced to stay on the control plane only

This matches your corporate policies and avoids 403 errors.

---

### **4. Review and Create**

Once created, note the Storage Account name and add it to `demo.tfvars`.

---

## 🔧 Deploying the Infrastructure

From the repository root:

```
cd infra
terraform init
terraform apply -var-file=env/demo.tfvars
```

Terraform will **not** attempt to access the Storage Account’s data plane.  
It only reads metadata from the Azure Resource Manager control plane.

If everything is correct, you will see output values including:

- Hub name  
- Project name  
- Storage account name  

---

## 📦 What happens next?

Once the infrastructure is deployed:

- Open Azure AI Foundry  
- Navigate into your Hub → Project  
- Import and run the Prompt Flow under `flows/prisma_airs_chat`  
- Provide your Prisma AIRS API key when running the flow

The system will then scan:
- User input → before model call  
- Model output → before returning a response  

---

## 🛠 Need to re‑deploy?

Update your `.tfvars` file or run:

```
terraform apply
```

State remains local unless you configure remote state.

---

## 📘 Notes

- The Storage Account is “bring your own” to avoid enterprise policy violations.  
- Terraform intentionally avoids creating or modifying the Storage Account.  
- Azure AI Foundry accesses the Storage Account through its own managed identity.

---

Enjoy exploring Prisma AIRS in a fully reproducible Azure AI environment!
