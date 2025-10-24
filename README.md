# TeamDocs v0.9 — Rapid‑Commit ITSM & Multi‑Audience Markdown

TeamDocs is a Markdown‑first, Confluence‑like portal for Support/SRE/Operations teams.
It doubles as a **rapid‑commit ITSM** system (Major Incidents, Problems, OKRs, Journals)
and builds separate **public/internal/admin/stakeholder** sites with redactions.

## Quick Start
- See **developer_quickstart.md** for a 10‑minute setup.
- See **TECHNICAL_GUIDE.md** for full Docker/K8s & CI/CD.
- See **project_overview.md** for an executive + architecture summary.

## Integrations (Jira & ServiceNow)
- Copy `.env.example` to `.env` and fill credentials.
- Run:
  ```bash
  export $(grep -v '^#' .env | xargs)
  python scripts/pull_jira.py
  python scripts/pull_servicenow.py
  ```
- Output JSON lands in `docs/data/jira/` and `docs/data/servicenow/` and is used by `scripts/build_indexes.py` to enrich dashboards (extend as needed).
