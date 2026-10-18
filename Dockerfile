# ---- Étape 1 : installation des dépendances ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Étape 2 : image finale légère ----
FROM python:3.12-slim
# Utilisateur non-root
RUN useradd --create-home --shell /usr/sbin/nologin app
WORKDIR /home/app
COPY --from=builder /install /usr/local
COPY app ./app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

# 0.0.0.0 : sinon l'API est injoignable depuis l'extérieur du conteneur
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
