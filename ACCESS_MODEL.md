# Access Model

Audiences: public, internal, admin, stakeholder.
We build **separate static bundles**, each with redactions applied per `build.config.yaml`.

## Example mapping
- public: home, ways-of-working (sanitized), selected incidents (public_summary only)
- internal: all standard docs
- admin: full MI/PRB/OKR data
- stakeholder: dashboards only

SSO: place oauth2-proxy before internal/admin/stakeholder subdomains.
