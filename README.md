# tasks-platform

![CI](https://github.com/Nada1231/tasks-platform/actions/workflows/ci.yml/badge.svg)

API de gestion de tâches (FastAPI + PostgreSQL) livrée par un pipeline CI/CD complet :
lint, tests, build Docker multi-étapes, scan de sécurité Trivy et publication sur GHCR.

## Architecture

> TODO : ajouter un schéma (draw.io / Excalidraw) dans `docs/architecture.png`

`git push` → GitHub Actions (Ruff → pytest → build Docker → Trivy → push GHCR)

## Stack

| Outil | Rôle | Pourquoi |
|---|---|---|
| FastAPI | API | Rapide à écrire, doc auto sur `/docs` |
| Docker (multi-étapes) | Conteneur | Image légère, non-root |
| GitHub Actions | CI/CD | Intégré au dépôt |
| Trivy | Scan de vulnérabilités | Bloque les failles CRITICAL |
| GHCR | Registre d'images | Authentification par `GITHUB_TOKEN`, aucun mot de passe |

## Lancer en local

```bash
# Avec PostgreSQL
docker compose -f docker/docker-compose.yml up --build
# puis ouvrir http://localhost:8000/health et http://localhost:8000/docs

# Sans Docker (SQLite)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
uvicorn app.main:app --reload
```

## Sécurité

- Conteneur exécuté en non-root
- Scan Trivy bloquant sur les failles CRITICAL
- Aucun secret dans le dépôt (`GITHUB_TOKEN` fourni par GitHub)

## Ce qui a cassé et comment je l'ai réparé

| Symptôme | Cause | Solution |
|---|---|---|
| _à compléter_ | | |

## Améliorations prévues

- Déploiement sur Kubernetes (projet 3), monitoring (projet 4)
