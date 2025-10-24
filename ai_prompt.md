# AI Prompt — Canonical Context

This file summarises the intent and constraints of TeamDocs for future AI continuation.

## Intent
- Build a Markdown‑first, rapid‑commit ITSM portal with multi‑audience outputs and DevOps helpers.

## Core Objects (front‑matter YAML)
- Major Incident (MI), Problem (PRB), OKR, Journal

## Non‑Goals (v0.9)
- Fine‑grained per‑page runtime ACL in a single bundle (use multi‑bundle + subdomains instead).

## Editing Rules
- Preserve templates and schema keys.
- Respect visibility/redactions in bundles.
- Run `scripts/build_indexes.py` before mkdocs build/serve.

## Useful Prompts
- “Add a new MI template with fields X/Y/Z.”
- “Update build_bundles.py to support a new audience ‘partners’.”
