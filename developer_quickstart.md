# Developer Quickstart (10 minutes)

## 1) Local Preview
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
make serve
# open http://localhost:8000
```

## 2) Docker Build & Serve
```bash
docker build -t teamdocs:site -f Dockerfile .
docker compose up --build
# open http://localhost:8080
```

## 3) Create Content
```bash
# New Major Incident
python scripts/new_page.py mi --id MI-2025-10-24-001 --sev SEV1 --service "Checkout"
# New Daily Journal
python scripts/new_page.py journal --author nathan
```

## 4) Multi‑Audience Bundles
```bash
make bundle
# outputs: site-public/, site-internal/, site-admin/, site-stakeholder/
```

## 5) VS Code
Open this folder in VS Code. See `.vscode/` for tasks/snippets.
