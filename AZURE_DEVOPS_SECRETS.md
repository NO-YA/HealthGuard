# 🔐 Configuration Variables Azure DevOps

## 📌 À faire dans Azure DevOps UI

### Étape 1: Aller à Pipeline → Edit → Variables

1. Dans Azure DevOps, ouvrir votre pipeline
2. Cliquer sur **Edit** (en haut à droite)
3. Cliquer sur **Variables** (en haut à droite du panel)

### Étape 2: Ajouter les secrets

```
+--AJOUTER--+
```

**Créer 4 variables:**

#### 1️⃣ ACR_PASSWORD
- **Name**: `ACR_PASSWORD`
- **Value**: [Votre password ACR]
- **🔒 Keep this value secret**: ✅ COCHER
- **Scope**: Current pipeline

Obtenir le password:
```bash
az acr credential show --name healthguardacr --query "passwords[0].value" -o tsv
```

#### 2️⃣ MONGO_URI_STAGING_SECRET
- **Name**: `MONGO_URI_STAGING_SECRET`
- **Value**: `mongodb+srv://[username]:[password]@[cluster].mongodb.net/healthguard`
- **🔒 Keep this value secret**: ✅ COCHER
- **Scope**: Current pipeline

Exemple:
```
mongodb+srv://healthguard_user:mypassword123@healthguard.xxxxx.mongodb.net/healthguard?retryWrites=true&w=majority
```

#### 3️⃣ MONGO_URI_PROD_SECRET
- **Name**: `MONGO_URI_PROD_SECRET`
- **Value**: `mongodb+srv://[username]:[password]@[cluster].mongodb.net/healthguard`
- **🔒 Keep this value secret**: ✅ COCHER
- **Scope**: Current pipeline

(Peut être la même que staging pour MVP)

#### 4️⃣ (Optional) APPINSIGHTS_KEY
- **Name**: `APPINSIGHTS_KEY`
- **Value**: [Votre Application Insights key]
- **🔒 Keep this value secret**: ✅ COCHER
- **Scope**: Current pipeline

---

## 📋 Checklist Variables

```
ACR_PASSWORD:
  ☐ Créé
  ☐ Marqué comme secret
  ☐ Valeur correcte testée

MONGO_URI_STAGING_SECRET:
  ☐ Créé
  ☐ Format correct (mongodb+srv://...)
  ☐ Credentials valides
  ☐ Marqué comme secret

MONGO_URI_PROD_SECRET:
  ☐ Créé
  ☐ Format correct
  ☐ Marqué comme secret

APPINSIGHTS_KEY (Optional):
  ☐ Créé ou skippé
```

---

## 🧪 Vérifier les Variables

Une fois ajoutées:
1. Cliquer **Save**
2. Cliquer **Queue** pour déclencher le pipeline
3. Observer le pipeline qui devrait utiliser ces variables

### Erreurs potentielles:

❌ `Error: Could not find variable 'ACR_PASSWORD'`
→ Vérifier que la variable est créée avec le bon nom

❌ `Error: secret not found`
→ Vérifier que 🔒 Keep this value secret est cochée

❌ `Error: authentication failed to ACR`
→ Vérifier que ACR_PASSWORD est correct:
```bash
az acr credential show --name healthguardacr
```

---

## 🔒 Security Best Practices

✅ **Fait:**
- Variables de secrets marquées avec 🔒
- Credentials stockés dans Azure DevOps UI, pas en dur dans YAML
- MONGO_URI ne contient pas le password en clair

❌ **À éviter:**
- Hardcoder les secrets dans azure-pipelines.yml
- Partager les credentials en clair
- Utiliser les mêmes credentials pour staging et prod (idéalement)

---

## 📝 Notes

- Les variables défendront sont remplacées à l'exécution
- `$(ACR_PASSWORD)` dans le YAML devient la valeur réelle
- Les secrets ne sont pas affichés dans les logs de pipeline

---

**Status**: À configurer manuellement dans Azure DevOps  
**Temps requis**: 5 min  
**Priority**: CRITIQUE pour JOUR 2+
