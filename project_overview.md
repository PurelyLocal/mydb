# Project Overview

## Goal
Provide a Git‑driven, Markdown portal for incident/status/OKR/ways‑of‑working that
publishes to multiple audiences (public/internal/admin/stakeholder) with redactions.

## Key Features
- Major Incident, Problem, OKR, Journal templates with YAML front‑matter.
- Auto‑generated dashboards (Active MI, Problem Register, OKR rollup).
- Multi‑bundle builds with subdomain routing (e.g., public.docs.example.com).
- VS Code + Obsidian friendly.
- Optional Scrum UI for ceremonies (stand‑up, planning, retro).

## High Level Architecture
- **MkDocs Material** renders docs → static site(s).
- **Scripts** read front‑matter & data/ to build dashboards & bundles.
- **Nginx/K8s** serves bundles per audience with SSO (oauth2‑proxy).

## Roadmap (v1.0+)
- Finer ACLs per page, real‑time MI panels, deeper metrics, AI helpers.
