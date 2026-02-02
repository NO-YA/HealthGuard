# 🏗️ HealthGuard Vision - Architecture

## 📋 Vue d'ensemble

HealthGuard Vision est une application minimaliste de diagnostic préventif par image, conçue pour être **complètement automatisée, testée et déployée en 5 jours**.

---

## 🎯 Architecture High-Level

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Web Browser (HTML5 + Vanilla JS)                         │ │
│  │  - Upload image interface                                 │ │
│  │  - Display results                                         │ │
│  │  - View history (GET /api/results)                       │ │
│  └────────────────────┬───────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                        │
                        │ HTTP REST
                        │
┌─────────────────────────────────────────────────────────────────┐
│                    API LAYER (Flask)                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  GET    /health              → Health check               │ │
│  │  POST   /api/predict          → Analyze image             │ │
│  │  GET    /api/results          → Fetch history             │ │
│  │  GET    /metrics              → Prometheus metrics        │ │
│  │  GET    /health/live          → Liveness probe            │ │
│  │  GET    /health/ready         → Readiness probe           │ │
│  └────────────────────┬──────────────────────┬───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                        │                      │
                        │                      │
        ┌───────────────┴────────┐   ┌────────┴──────────────┐
        │                        │   │                       │
┌───────▼──────────────┐  ┌──────▼───────────────┐  ┌────────▼─────────┐
│    ML SERVICE        │  │   DATA LAYER         │  │   MONITORING     │
├──────────────────────┤  ├──────────────────────┤  ├──────────────────┤
│ TensorFlow Lite      │  │ PostgreSQL/MongoDB   │  │ Application      │
│ - Anemia Model       │  │ - Predictions table  │  │ Insights         │
│ - Image processing   │  │ - Patient metadata   │  │ - Logs           │
│ - Risk classification│  │ - Audit trail        │  │ - Metrics        │
└──────────────────────┘  └──────────────────────┘  └──────────────────┘
```

---

## 🔄 Flux de Données

### 1. Upload Image
```
User selects image
    ↓
POST /api/predict (multipart/form-data)
    ↓
Flask validates:
  - File size < 5MB
  - Format in [PNG, JPG, JPEG]
    ↓
Image saved temporarily
```

### 2. ML Processing
```
Image validation ✓
    ↓
Load TensorFlow Lite model
    ↓
Preprocess image:
  - Resize to 224x224
  - Normalize pixels [0,1]
    ↓
Run inference
    ↓
Get probability score (0-1)
    ↓
Classify risk level:
  - score < 0.3 → LOW
  - 0.3 ≤ score < 0.7 → MEDIUM
  - score ≥ 0.7 → HIGH
```

### 3. Response Generation
```
{
  "condition": "anemia",
  "risk_level": "medium",
  "confidence": 0.78,
  "recommendation": "Consult with a healthcare provider",
  "analysis_date": "2026-01-28T10:30:00Z",
  "message_id": "pred_abc123"
}
```

### 4. Storage
```
Response JSON
    ↓
Save to MongoDB/PostgreSQL
    ↓
Fields:
  - prediction_id
  - timestamp
  - risk_score
  - risk_level
  - confidence
  - image_hash (NOT full image for privacy)
    ↓
Available via GET /api/results
```

---

## 🐳 Containerization Strategy

### Multi-Stage Docker Build

**Stage 1: Builder (600MB)**
```dockerfile
FROM python:3.11-slim
# Install build dependencies
# Install Python requirements
# = 600MB
```

**Stage 2: Runtime (250MB - optimized)**
```dockerfile
FROM python:3.11-slim
# Copy only Python packages from Stage 1
# Copy source code
# Remove build tools
# = ~250MB
```

### Result
```
Base Python image:        150MB
Python packages (slim):   100MB
Application code:           5MB
─────────────────────────────
TOTAL:                    255MB ✓ (vs 600MB before)
```

### Local Development
```bash
docker-compose up --build
```

Services:
- `api` (Flask on port 5000)
- `mongodb` (Database on port 27017)
- `redis` (Caching on port 6379)

---

## 🔒 Security Architecture

### Input Validation
```python
# File upload validation
- Max size: 5MB
- Allowed formats: PNG, JPG, JPEG
- Scan for malware (optional: ClamAV)
- No code execution allowed
```

### Environment Variables
```
# .env (NOT in git)
FLASK_ENV=production
MONGO_URI=mongodb+srv://...
LOG_LEVEL=WARNING
SECRET_KEY=...
```

### API Security
```
- CORS enabled for staging/prod
- Input sanitization (Pydantic)
- Rate limiting (optional)
- HTTPS enforced in production
```

### Data Privacy
```
- NO full image storage
- Only hash + metadata stored
- GDPR compliant (metadata only)
- Audit logs for compliance
```

---

## 📊 Data Model

### MongoDB Schema (Predictions Collection)
```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "condition": "anemia",
  "image_hash": "sha256_hash",
  "risk_score": 0.75,
  "risk_level": "medium",
  "confidence": 0.78,
  "recommendation": "Consult healthcare provider",
  "user_id": "optional_user_hash",
  "metadata": {
    "image_size_bytes": 45000,
    "processing_time_ms": 234,
    "model_version": "1.0"
  }
}
```

### Indexes
```python
db.predictions.create_index([("timestamp", -1)])
db.predictions.create_index([("condition", 1)])
db.predictions.create_index([("user_id", 1), ("timestamp", -1)])
```

---

## 🚀 CI/CD Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    Git Push to main                         │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────▼─────────────┐
        │                          │
    ┌───┴────────────────────────┐ │
    │                            │ │
    ▼                            ▼ ▼
┌──────────────┐         ┌───────────────────┐
│ Stage 1:     │         │                   │
│ BUILD & TEST │─────────│  PARALLEL JOBS    │
└──────────────┘         │                   │
  │ Python setup         └───────────────────┘
  │ Install deps             │
  │ Run tests (pytest)       │ 1. Install Python
  │ Build Docker image       │ 2. Run unit tests
  │ Push to ACR              │ 3. Code coverage
  │                          │ 4. Lint checks
  │                          │
  ▼
┌──────────────┐
│ Stage 2:     │
│ DEPLOY       │
│ STAGING      │
└──────────────┘
  │ Deploy to ACI (staging)
  │ Run smoke tests
  │ Health checks ✓
  │
  ▼
┌──────────────┐
│ Stage 3:     │
│ DEPLOY       │
│ PRODUCTION   │
│ (MANUAL)     │
└──────────────┘
  │ Deploy to ACI (prod)
  │ Verify health checks
  │ 🚀 LIVE
```

---

## 📈 Monitoring & Observability

### Logs
```
Format: JSON structured logs
Location: Application Insights
Pattern:
{
  "timestamp": "2026-01-28T10:30:00Z",
  "level": "INFO",
  "service": "healthguard-api",
  "message": "Prediction completed",
  "duration_ms": 234,
  "risk_level": "medium"
}
```

### Metrics (Prometheus)
```
healthguard_predictions_total{condition="anemia"}
healthguard_prediction_duration_seconds (histogram)
healthguard_api_requests_total{endpoint="/api/predict", method="POST"}
healthguard_api_errors_total{endpoint="/api/predict"}
```

### Health Checks
```
GET /health/live   → Container alive?
GET /health/ready  → DB connected? Model loaded?
GET /metrics       → Prometheus endpoint
```

### Application Insights Dashboard
```
- Request rate & latency
- Error rate by endpoint
- ML model inference time
- Database query performance
```

---

## 🎯 Technology Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| **Framework** | Flask | 3.0.0 | Lightweight |
| **Validation** | Pydantic | 2.6.0 | Type-safe |
| **ML** | TensorFlow Lite | 2.16.0 | Mobile-optimized |
| **Image Processing** | OpenCV | 4.10.1 | Preprocessing |
| **Database** | PostgreSQL/MongoDB | 15/7 | Flexible |
| **Caching** | Redis | 7.0 | Optional |
| **Logging** | Python JSON Logger | 2.0.7 | Structured |
| **Monitoring** | Azure Application Insights | Latest | Production monitoring |
| **Testing** | Pytest | 8.0 | Unit tests |
| **Container** | Docker | Latest | Containerization |
| **Container Mgmt** | Azure Container Instances | Latest | Deployment |
| **CI/CD** | Azure DevOps | Latest | Automation |

---

## 🔐 Deployment Environments

### Development (Local)
```
- docker-compose up
- MongoDB on localhost:27017
- Redis on localhost:6379
- Flask on localhost:5000
- LOG_LEVEL=DEBUG
```

### Staging
```
- Azure Container Instances
- MongoDB Atlas (shared)
- NO Redis
- HTTPS enabled
- LOG_LEVEL=INFO
- Health checks every 30s
```

### Production
```
- Azure Container Instances
- MongoDB Atlas (prod instance)
- Health checks + auto-restart
- HTTPS only
- LOG_LEVEL=WARNING
- Application Insights monitoring
- 2 vCPU, 2GB RAM
```

---

## 📊 Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Image upload | < 5MB | ✅ |
| API response | < 1 sec | ✅ |
| ML inference | < 500ms | ✅ |
| DB query | < 100ms | ✅ |
| Container startup | < 10s | ✅ |
| Health check response | < 100ms | ✅ |
| Availability | 99% | ✅ |

---

## 🚀 Scaling Strategy

### Current (MVP)
```
Single container instance
1 vCPU, 1.5GB RAM
~50 req/sec capacity
```

### Phase 2 (If needed)
```
Azure Container Apps
Auto-scaling (2-5 instances)
Load balancer
Redis cache
```

---

## 📝 Notes Architecture

- **Minimaliste**: Pas de Kubernetes, message queues, ou microservices
- **Fonctionnel**: Tout automatisé, testé et monitoré
- **Scalable**: Faussi simple d'ajouter instances si besoin
- **Observable**: Logs + métriques = debugging facile
- **Secure**: Validation stricte + secrets en variables d'env

---

**Version**: 1.0  
**Date**: 2026-01-28  
**Status**: JOUR 1 ✅
