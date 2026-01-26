# HealthGuard 🏥

Application de diagnostic médical assisté par intelligence artificielle.

## 📋 Description

HealthGuard est une plateforme web permettant l'analyse d'images et données médicales pour:
- Détection de diabète rétinopathique
- Détection d'anémie
- Détection de carences nutritionnelles

## 🛠️ Stack Technologique

- **Backend**: Flask 3.0.0
- **ML**: TensorFlow 2.16.0
- **Base de données**: MongoDB
- **API**: REST avec validation Pydantic
- **Conteneurisation**: Docker & Docker Compose
- **CI/CD**: Azure Pipelines

## 📁 Structure du Projet

```
HealthGuard/
├── backend/                    # API Flask
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Point d'entrée Flask
│   │   ├── config.py          # Configuration
│   │   ├── logger.py          # Logging
│   │   └── ml_service.py      # Service ML
│   ├── test/
│   │   └── test_api.py        # Tests unitaires
│   └── requirements.txt        # Dépendances Python
├── ml/                        # Modèles ML
│   ├── anemia/
│   │   └── config.json
│   ├── diabetes/
│   │   └── config.json
│   └── deficiency/
│       └── config.json
├── .env.example               # Template environnement
├── .gitignore                 # Git ignore
├── Dockerfile                 # Image Docker
├── docker-compose.yml         # Orchestration
└── README.md                  # Ce fichier
```

## 🚀 Installation Rapide

### Prérequis
- Python 3.9+
- Docker & Docker Compose (optionnel)
- MongoDB 5.0+

### Sans Docker

1. **Clone et setup**
   ```bash
   git clone https://github.com/yourusername/HealthGuard.git
   cd HealthGuard/backend
   ```

2. **Environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Installation dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   ```bash
   cp ../.env.example ../.env
   # Éditer .env avec vos paramètres
   ```

5. **Lancement**
   ```bash
   python -m flask run
   ```

### Avec Docker

```bash
docker-compose up --build
```

L'API sera disponible à `http://localhost:5000`

## 📚 API Documentation

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Prédiction
```http
POST /api/predict
Content-Type: application/json

{
  "image": "base64_encoded_image",
  "analysis_type": "diabetes|anemia|deficiency"
}
```

**Response:**
```json
{
  "success": true,
  "diagnosis": {
    "diabetes_risk": 0.15,
    "anemia_risk": 0.08,
    "deficiency_risk": 0.022
  },
  "recommendations": [...]
}
```

## 🧪 Tests

```bash
pytest backend/test/ -v
pytest backend/test/ --cov=backend/app
```

## 📊 Logging

Logs structurés en format JSON. Configuration dans `backend/app/logger.py`.

```bash
tail -f logs/app.log
```

## 🔒 Sécurité

- Variables sensibles dans `.env` (ignoré par git)
- CORS configuré
- Validation Pydantic de tous les inputs
- Chiffrement des données sensibles (cryptography)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

MIT License - voir LICENSE file

## 👥 Support

Pour tout problème ou question, ouvrir une issue sur GitHub.

---

**Version**: 1.0.0  
**Dernière mise à jour**: 2026-01-26
