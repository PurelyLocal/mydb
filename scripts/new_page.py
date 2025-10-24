import argparse, pathlib, datetime, textwrap
root = pathlib.Path(__file__).resolve().parents[1] / "docs"

def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(s).lstrip("\n"), encoding="utf-8")

def new_mi(mi_id, sev, service):
    p = root / "incidents/major" / f"{mi_id}.md"
    write(p, f"""
    ---
    id: {mi_id}
    severity: {sev}
    status: Active
    service: {service}
    start: {datetime.datetime.now().isoformat()}
    commander: <name>
    scribe: <name>
    channels: {{ slack: "#mi-{mi_id.lower()}" }}
    visibility: internal
    public_summary: ""
    ---
    # {mi_id}
    """)
    print("Created", p)

def new_prb(prb_id, owner):
    p = root / "problems" / f"{prb_id}.md"
    write(p, f"""
    ---
    id: {prb_id}
    status: Under Investigation
    owner: {owner}
    category: ""
    linked_incidents: []
    milestones: []
    ---
    # Problem {prb_id}
    """)
    print("Created", p)

def new_journal(author):
    d = datetime.date.today().isoformat()
    p = root / "team/journals" / author / f"{d}.md"
    write(p, f"""
    ---
    author: {author}
    date: {d}
    jira: []
    highlights: []
    blockers: []
    ---
    # Update — {d}
    """)
    print("Created", p)

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
s1 = sub.add_parser("mi"); s1.add_argument("--id", required=True); s1.add_argument("--sev", default="SEV2"); s1.add_argument("--service", required=True)
s2 = sub.add_parser("prb"); s2.add_argument("--id", required=True); s2.add_argument("--owner", required=True)
s3 = sub.add_parser("journal"); s3.add_argument("--author", required=True)
args = ap.parse_args()
if args.cmd=="mi": new_mi(args.id, args.sev, args.service)
elif args.cmd=="prb": new_prb(args.id, args.owner)
elif args.cmd=="journal": new_journal(args.author)
