# Technical Guide (TeamDocs v0.9)

## Stack
- MkDocs + Material
- Python 3.12 for build scripts
- Docker/Nginx, optional Kubernetes (Ingress + oauth2‑proxy)

## Install
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
```

## Commands
- `make serve` — local dev with auto index build
- `make build` — build single site
- `make bundle` — build multi‑audience bundles
- `make new-...` — scaffold content (MI/PRB/Journal/OKR)

## Deployment
- **Docker compose** for Ubuntu (Nginx serving static `site/`).
- **Kubernetes**: build multi‑stage image (`Dockerfile`) with site content; use `k8s/ingress-*.yaml` for subdomains.
- **Auth/SSO**: put `oauth2-proxy` in front of Internal/Admin bundles.

## CI/CD
See `.github/workflows/` examples for build & sync jobs.
