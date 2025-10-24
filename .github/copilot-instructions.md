# TeamDocs Copilot Instructions

## Architecture Overview
TeamDocs is a multi-audience documentation platform that builds different versions (public/internal/admin/stakeholder) from a single Markdown source. The system uses:

- **MkDocs Material** for static site generation
- **Python build scripts** that process YAML frontmatter and auto-generate dashboards  
- **Multi-bundle system** with content filtering and field redaction per audience
- **ITSM integration** with Jira/ServiceNow data pulls

## Essential Workflows

### Content Creation
Use `scripts/new_page.py` for structured content:
```bash
# Major incidents with required frontmatter
python scripts/new_page.py mi --id MI-2025-10-24-001 --sev SEV1 --service "Checkout"

# Problem records linked to incidents  
python scripts/new_page.py prb --id PRB-2025-10-19-NET-EDGE --owner saban

# Daily journals with metadata
python scripts/new_page.py journal --author nathan
```

### Build Process
**Critical**: Always run `python scripts/build_indexes.py` before serving/building. This:
- Scans YAML frontmatter from `docs/incidents/major/*.md`, `docs/problems/*.md`, `docs/okrs/**/*.md`
- Auto-generates dashboard tables using `<!--AUTO:MARKER-->` injection points
- Must complete before MkDocs processes the files

Build commands:
- `make serve` - Local development (auto-rebuilds indexes)
- `make bundle` - Multi-audience builds → `site-public/`, `site-internal/`, etc.

## Content Patterns

### YAML Frontmatter Structure
All structured content uses specific frontmatter schemas:

**Major Incidents** (`docs/incidents/major/MI-*.md`):
```yaml
id: MI-2025-10-24-001
severity: SEV1|SEV2|SEV3
status: Active|Mitigated|Resolved
service: string
start: ISO timestamp
commander: string
channels: 
  slack: "#channel-name"
visibility: internal|public
impacted_metrics: [{name, before, during}]
timeline: [string array]
```

**Problems** (`docs/problems/PRB-*.md`):
```yaml
id: PRB-YYYY-MM-DD-TOPIC
status: Under Investigation|Root Cause Identified|Resolved
owner: string
linked_incidents: [MI-IDs]
milestones: [{name, due}]
```

### Multi-Audience System
Content filtering defined in `build.config.yaml`:
- **Public**: Limited paths + field redaction (removes `impacted_metrics`, `timeline`)
- **Internal/Admin**: Full access
- **Stakeholder**: Curated paths + selective redaction

When adding sensitive fields, update redaction rules in `build.config.yaml`.

## Key Scripts Behavior

### `build_indexes.py`
- Uses `frontmatter` library to parse metadata
- Generates tables with `tabulate` library  
- Injects content using regex replacement of `<!--AUTO:MARKER-->` comments
- **Never edit** auto-generated sections manually - they'll be overwritten

### `build_bundles.py`
- Creates filtered copies in `site-{bundle}/` directories
- Applies `fnmatch` patterns for inclusion
- Strips frontmatter fields per redaction config
- Adds bundle-specific Dockerfile for deployment

### Integration Scripts
- `pull_jira.py`, `pull_servicenow.py` output to `docs/data/{service}/`
- Data enriches dashboards via `build_indexes.py` processing
- Require environment variables: `JIRA_BASE`, `JIRA_EMAIL`, `JIRA_TOKEN`, etc.

## Development Notes
- Content files use `visibility: internal` by default for incident management
- Template files (like `_JOURNAL_TEMPLATE.md`) provide schema reference
- All paths in navigation and scripts assume `docs/` as content root
- Docker deployment serves static files via Nginx with oauth2-proxy for auth