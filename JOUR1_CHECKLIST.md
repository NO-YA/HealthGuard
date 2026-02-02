# ✅ JOUR 1 - Checklist Complète

## Phase 1: Setup Infrastructure Azure ⛅

### Resource Group & Container Registry
- [ ] Installer Azure CLI
- [ ] Se connecter: `az login`
- [ ] Créer Resource Group: `healthguard-rg`
- [ ] Créer Azure Container Registry: `healthguardacr`
- [ ] Récupérer credentials ACR

### Service Principal & Authentication
- [ ] Créer Service Principal pour DevOps
- [ ] Sauvegarder credentials (appId, password, tenant)
- [ ] Créer Azure DevOps project
- [ ] Connecter Service Principal à Azure DevOps
- [ ] Créer Docker Registry connection

### Database
- [ ] Créer MongoDB Atlas compte (gratuit)
- [ ] Créer cluster M0
- [ ] Créer user + password
- [ ] Obtenir MONGO_URI connection string
- [ ] Tester connexion local: `python -c "from pymongo import MongoClient; MongoClient('URI')"`

---

## Phase 2: Infrastructure Locale 🐳

### Docker Testing
- [ ] Vérifier Docker installation: `docker --version`
- [ ] Tester docker-compose: `docker-compose --version`
- [ ] Build image local: `docker build -t healthguard:local .`
- [ ] Lancer services: `docker-compose up --build`
- [ ] Tester /health endpoint:
  ```bash
  curl http://localhost:5000/health
  # Doit retourner: {"status": "healthy"}
  ```
- [ ] Vérifier MongoDB connexion:
  ```bash
  # Dans une autre console
  docker-compose exec mongodb mongosh
  > db.admin.ping()
  # Doit retourner: { ok: 1 }
  ```
- [ ] Arrêter services: `docker-compose down`

---

## Phase 3: Azure DevOps Pipeline 🔄

### Pipeline Configuration
- [ ] Créer nouveau pipeline dans Azure DevOps
- [ ] Pointer vers `azure-pipelines.yml`
- [ ] Ajouter variables (ACR username/password, MONGO_URIs)
- [ ] Tester trigger: faire un `git push origin main`
- [ ] Vérifier pipeline execution (doit arriver à stage "Build & Test")

### Expected Pipeline Output
```
✅ Build & Test Stage
  ✅ Install Python 3.11
  ✅ Install dependencies
  ✅ Run unit tests (pas encore, on a pas d'app)
  ✅ Build Docker image
  ✅ Push to ACR
```

---

## Phase 4: Documentation 📚

### Files Created
- [ ] ✅ `ARCHITECTURE.md` - Architecture diagram + data flows
- [ ] ✅ `SETUP_AZURE.md` - Step-by-step Azure setup
- [ ] ✅ `azure-pipelines.yml` - CI/CD pipeline YAML
- [ ] ✅ `backend/requirements.txt` - Updated with all deps

### Files Verified
- [ ] ✅ `Dockerfile` - Multi-stage, optimized
- [ ] ✅ `docker-compose.yml` - Services defined
- [ ] ✅ `README.md` - Project overview
- [ ] ✅ `.gitignore` - Secrets excluded
- [ ] ✅ `.env.example` - Template variables

---

## Phase 5: Code Preparation 🔧

### Backend Structure
- [ ] ✅ `backend/app/config.py` - Configuration ready
- [ ] ✅ `backend/app/logger.py` - Logging setup ready
- [ ] ✅ `backend/app/main.py` - NEEDS UPDATE (Jour 2)
- [ ] ✅ `backend/app/ml_service.py` - NEEDS UPDATE (Jour 2)

### ML Structure
- [ ] ✅ `ml/anemia/loader.py` - Model loader template
- [ ] ✅ `ml/anemia/config.json` - Config file
- [ ] ☐ `ml/anemia/model.tflite` - NEEDS: Download pre-trained model

### Tests Structure
- [ ] ✅ `backend/test/` - Directory ready
- [ ] ☐ `backend/test/test_api.py` - NEEDS UPDATE (Jour 2)

---

## 🧪 Validation Checklist

### ✅ Must Pass
- [ ] `docker build -t healthguard:local .` - Succeeds with no errors
- [ ] `docker-compose up --build` - All services start
- [ ] `curl http://localhost:5000/health` - Returns 200 + JSON
- [ ] Pipeline runs without major errors (will have test failures, c'est OK)
- [ ] Azure ACR shows `healthguard:latest` image

### ⚠️ Expected Issues (Normal)
```
❌ Tests fail (No tests implemented yet)
❌ /api/predict returns 404 (Not implemented yet)
❌ Deploy stages might error (Container doesn't exist yet)

Ces erreurs sont NORMALES pour Jour 1 ✅
```

---

## 📊 Resources Checklist

### Credentials Saved Securely
- [ ] Azure Subscription ID
- [ ] Service Principal (appId, password, tenant)
- [ ] ACR credentials (username, password)
- [ ] MongoDB Atlas connection string
- [ ] GitHub/Azure DevOps token

### Where to Save
```
Créer fichier SÉCURISÉ (NOT in git):
c:\Users\N.O.Y.A\Documents\HealthGuard\CREDENTIALS.txt

Format:
AZURE_SUBSCRIPTION_ID=xxx
AZURE_TENANT_ID=xxx
AZURE_CLIENT_ID=xxx
AZURE_CLIENT_SECRET=xxx
ACR_USERNAME=healthguardacr
ACR_PASSWORD=xxx
MONGO_URI_STAGING=mongodb+srv://...
MONGO_URI_PROD=mongodb+srv://...

⚠️ NEVER commit this file!
```

---

## 📝 Git Commit Strategy

```bash
# Jour 1 commit
git add -A
git commit -m "JOUR 1: Architecture setup + DevOps pipeline

- Added Azure pipelines configuration
- Added architecture documentation
- Created Azure setup guide
- Updated requirements with TensorFlow Lite
- Configured docker-compose for MongoDB
- Added monitoring/logging structure"
git push origin main
```

---

## ⏱️ Timeline JOUR 1

| Task | Time | Status |
|------|------|--------|
| Azure setup | 30 min | ☐ |
| Service Principal | 15 min | ☐ |
| MongoDB Atlas | 15 min | ☐ |
| Local Docker test | 15 min | ☐ |
| Azure Pipeline config | 15 min | ☐ |
| Documentation | 15 min | ☐ |
| **TOTAL** | **105 min** | |

---

## 🎯 Success Criteria JOUR 1

```
✅ Infrastructure: Azure RG + ACR + SP ready
✅ Database: MongoDB Atlas configured
✅ Local: Docker compose runs flawlessly
✅ Pipeline: Azure DevOps pipeline executes (Stage 1)
✅ Code: Ready for app implementation
✅ Docs: Architecture + setup documented
```

---

## 🚀 Jour 2 Preview

**JOUR 2 - API & Pipeline CI/CD** sera:

```
- Implémenter /health endpoint (5 min)
- Implémenter /api/predict endpoint (1h)
- Implémenter /api/results endpoint (30 min)
- Écrire 5 tests unitaires (1h)
- Tester pipeline: run tests ✓ (20 min)
- Déployer en staging (20 min)

Total: 4-5h de dev
```

---

**JOUR 1 Status**: 🔄 IN PROGRESS  
**Created**: 2026-01-28  
**Next**: JOUR 2 - Coding API
