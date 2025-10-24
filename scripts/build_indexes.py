import frontmatter, pathlib, yaml, re
from datetime import datetime
root = pathlib.Path(__file__).resolve().parents[1] / "docs"

def collect(pattern):
    return list(root.glob(pattern))

def load_meta(p):
    post = frontmatter.load(p)
    meta = post.metadata or {}
    meta["_path"] = str(p.relative_to(root))
    return meta

def render_table(rows, headers):
    from tabulate import tabulate
    return tabulate(rows, headers=headers, tablefmt="github")

def inject(marker, content, path):
    s = pathlib.Path(path).read_text(encoding="utf-8")
    s = re.sub(rf"<!--{marker}-->[\s\S]*?(?=<!--|$)", f"<!--{marker}-->\n\n{content}\n", s, flags=re.M)
    pathlib.Path(path).write_text(s, encoding="utf-8")

# Active MI
mi_files = collect("incidents/major/*.md")
mis = [load_meta(p) for p in mi_files if p.name.endswith(".md")]
active = [m for m in mis if m.get("status","").lower() in {"active","mitigated"}]
active_rows = [[m.get("id"), m.get("severity"), m.get("service"), m.get("start"), m.get("commander")] for m in active]
inject("AUTO:ACTIVE_MI", render_table(active_rows, ["ID","SEV","Service","Start","Commander"]) if active_rows else "_No active MI._", root/"incidents/index.md")

# Recent MI
recent_rows = [[m.get("id"), m.get("status"), m.get("_path")] for m in sorted(mis, key=lambda x: x.get("start",""), reverse=True)[:10]]
inject("AUTO:RECENT_MI", render_table(recent_rows, ["ID","Status","Path"]) if recent_rows else "_No recent MI._", root/"incidents/index.md")

# Problems
prb = [load_meta(p) for p in collect("problems/*.md")]
rows = [[p.get("id"), p.get("status"), p.get("owner"), ", ".join(p.get("linked_incidents", []))] for p in prb]
inject("AUTO:PROBLEMS", render_table(rows, ["ID","Status","Owner","Linked MI"]), root/"problems/index.md")

# OKR rollup (simple demo)
okr = [load_meta(p) for p in collect("okrs/**/*.*") if p.suffix==".md" and p.name!="index.md"]
okr_rows = [[o.get("id"), o.get("quarter"), o.get("owner"), o.get("objective")] for o in okr]
inject("AUTO:OKR", render_table(okr_rows, ["ID","Quarter","Owner","Objective"]), root/"okrs/index.md")
print("Indexes built.")
