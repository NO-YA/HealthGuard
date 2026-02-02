# Multi-stage build pour optimiser la taille image

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Installer les dépendances système nécessaires pour la compilation et Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip et installer wheel
RUN python -m pip install --upgrade pip wheel

# Copier requirements et installer Python packages (incluant tflite-runtime)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt \
    || (echo "Fallback: try to install tflite-runtime explicitly" && pip install --no-cache-dir --user tflite-runtime==2.14.0)

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances runtime uniquement (incluant libs pour image & runtime TFLite)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libjpeg62-turbo \
    libstdc++6 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copier les packages Python du builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copier le code application
COPY backend/app ./app
COPY backend/test ./test
COPY ml ./ml
COPY .env.example ./

# Ajouter le chemin Python
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Créer l'utilisateur non-root pour sécurité
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check — use stdlib urllib to avoid extra dependency at healthcheck time
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, sys; \
        (lambda: sys.exit(0) if urllib.request.urlopen('http://localhost:5000/health').status==200 else sys.exit(1))()"

# Port exposé
EXPOSE 5000

# Commande de démarrage
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.main:app"]
