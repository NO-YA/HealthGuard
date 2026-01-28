# 🔧 Azure Setup Guide - Jour 1

## 📋 Prérequis

- [ ] Compte Azure actif (créer si nécessaire)
- [ ] Azure CLI installé
- [ ] Git configuré
- [ ] Docker installé (pour test local)

---

## 🚀 ÉTAPE 1 - Azure CLI Setup

### Installer Azure CLI
```bash
# Windows
choco install azure-cli

# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Vérifier installation
```bash
az --version
az login  # Vous ouvre un navigateur pour auth
```

---

## 🚀 ÉTAPE 2 - Créer Resource Group

```bash
# Set variables
$RESOURCE_GROUP="healthguard-rg"
$LOCATION="westeurope"  # Ou votre région préférée

# Créer le groupe
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Vérifier
az group show --name $RESOURCE_GROUP
```

---

## 🚀 ÉTAPE 3 - Créer Azure Container Registry (ACR)

```bash
# Set variables
$ACR_NAME="healthguardacr"
$ACR_SKU="Basic"  # Gratuit/pas cher

# Créer ACR
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku $ACR_SKU \
  --admin-enabled true

# Login ACR
az acr login --name $ACR_NAME

# Récupérer credentials
az acr credential show \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP
```

**Sauvegarder les credentials:**
```json
{
  "username": "healthguardacr",
  "passwords": [
    {
      "name": "password",
      "value": "XXXXX"
    }
  ]
}
```

---

## 🚀 ÉTAPE 4 - Créer Service Principal pour Azure DevOps

```bash
# Créer Service Principal
$SP=$(az ad sp create-for-rbac \
  --name healthguard-sp \
  --role Contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP)

# Afficher credentials (SAUVEGARDEZ LES!)
echo $SP | jq '.'

# Extraire les valeurs
$CLIENT_ID=$(echo $SP | jq -r '.appId')
$CLIENT_SECRET=$(echo $SP | jq -r '.password')
$TENANT_ID=$(echo $SP | jq -r '.tenant')
```

**Credentials à sauvegarder:**
```json
{
  "appId": "CLIENT_ID",
  "password": "CLIENT_SECRET",
  "tenant": "TENANT_ID",
  "subscriptionId": "SUBSCRIPTION_ID"
}
```

---

## 🚀 ÉTAPE 5 - Setup Azure DevOps

### 5a. Créer Azure DevOps Project

1. Aller sur https://dev.azure.com
2. Créer nouveau project `HealthGuard`
3. Importer repo Git (ou connecter GitHub)

### 5b. Créer Service Connection

**Dans Azure DevOps:**
1. Aller à **Project Settings** → **Service connections**
2. Créer **Azure Resource Manager** connection
3. Entrer Service Principal credentials

```
Connection name: healthguard-subscription
Service Principal (manual):
  - Tenant ID: [TENANT_ID]
  - Client ID: [CLIENT_ID]
  - Client Secret: [CLIENT_SECRET]
  - Subscription: [SUBSCRIPTION_ID]
```

### 5c. Créer Docker Registry Connection

**Dans Azure DevOps:**
1. Aller à **Project Settings** → **Service connections**
2. Créer **Docker Registry** connection

```
Connection name: healthguard-acr
Registry type: Azure Container Registry
Subscription: [your subscription]
Azure container registry: healthguardacr
```

---

## 🚀 ÉTAPE 6 - Créer MongoDB Cloud Atlas (Gratuit)

### 6a. Setup Atlas

1. Aller sur https://cloud.mongodb.com
2. Créer compte gratuit
3. Créer cluster M0 (gratuit):
   - Cloud provider: AWS
   - Region: eu-west-1 (Ireland)
   - Cluster name: healthguard

### 6b. Créer Database User

```
Username: healthguard_user
Password: [generate strong password]
Database: healthguard
```

### 6c. Créer Database

```
Database name: healthguard
Collection name: predictions
```

### 6d. Obtenir Connection String

```
mongodb+srv://healthguard_user:PASSWORD@healthguard.xxxxx.mongodb.net/healthguard?retryWrites=true&w=majority
```

**Sauvegarder:** `MONGO_URI_STAGING` et `MONGO_URI_PROD`

---

## 🚀 ÉTAPE 7 - Setup Local Docker Testing

### 7a. Build local Docker image

```bash
cd c:\Users\N.O.Y.A\Documents\HealthGuard

# Build
docker build -t healthguard:local .

# Vérifier image
docker image ls | grep healthguard
```

### 7b. Test docker-compose local

```bash
# Lancer tout
docker-compose up --build

# Vérifier logs
docker-compose logs -f api

# Test API
curl http://localhost:5000/health
# Devrait retourner: {"status": "healthy"}

# Arrêter
docker-compose down
```

---

## 🚀 ÉTAPE 8 - Azure DevOps Pipeline Setup

### 8a. Créer Pipeline

**Dans Azure DevOps:**
1. Aller à **Pipelines** → **New Pipeline**
2. Sélectionner **GitHub** ou **Azure Repos**
3. Sélectionner repository `HealthGuard`
4. Sélectionner **Existing Azure Pipelines YAML file**
5. Sélectionner `azure-pipelines.yml`

### 8b. Variables Pipeline

**Dans Azure DevOps → Pipeline → Edit → Variables:**

```
acrUsername: healthguardacr
acrPassword: [PASSWORD from step 3]
MONGO_URI_STAGING: mongodb+srv://healthguard_user:PASSWORD@healthguard.xxxxx.mongodb.net/healthguard
MONGO_URI_PROD: mongodb+srv://healthguard_user:PASSWORD@healthguard.xxxxx.mongodb.net/healthguard
```

### 8c. Déclencher Pipeline

```bash
# Faire un commit
git add .
git commit -m "JOUR 1: Setup Azure DevOps pipeline"
git push origin main

# Aller voir le pipeline en cours:
# https://dev.azure.com/[your-org]/HealthGuard/_build
```

---

## 🧪 VÉRIFICATION JOUR 1

Checklist:
```
✅ Azure Resource Group créé
✅ Azure Container Registry créé
✅ Service Principal configuré
✅ Service Connection Azure DevOps
✅ Docker Registry Connection Azure DevOps
✅ MongoDB Atlas setup + MONGO_URI
✅ Docker local test: docker-compose up ✓
✅ Pipeline Azure lancé (au moins une fois)
✅ Architecture.md documentée
✅ Code pushé sur main
```

---

## 📊 Coûts Estimés

| Service | Plan | Coût/mois |
|---------|------|-----------|
| Azure Container Registry | Basic | $5 |
| Azure Container Instances | ~50h/mois | $20 |
| MongoDB Atlas | M0 (gratuit) | $0 |
| Azure DevOps | Free tier | $0 |
| **TOTAL** | | **~$25/mois** |

---

## 🆘 Troubleshooting

### Problem: `az acr login` fails
```bash
# Check if Docker running
docker ps

# Check ACR credentials
az acr credential show --name healthguardacr
```

### Problem: Pipeline fails on Docker build
```bash
# Check Docker context
docker context ls

# Build manually
az acr build --registry healthguardacr --image healthguard:latest .
```

### Problem: Container can't connect to MongoDB
```bash
# Check MONGO_URI format
echo $MONGO_URI_STAGING

# Test connection locally
python3 -c "from pymongo import MongoClient; MongoClient('$MONGO_URI')"
```

---

## ✅ Résumé JOUR 1

Tu as maintenant:
- ✅ Infrastructure Azure setup (RG + ACR)
- ✅ Service Principal + DevOps connections
- ✅ Database MongoDB ready
- ✅ Azure Pipeline skeleton
- ✅ Docker tested locally
- ✅ Documentation architecture

**Prochaine étape: JOUR 2 - API & Pipeline**

---

**Date**: 2026-01-28  
**Status**: À exécuter
