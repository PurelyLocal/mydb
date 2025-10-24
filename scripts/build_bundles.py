import yaml, shutil, os, pathlib, frontmatter
from fnmatch import fnmatch

base = pathlib.Path(__file__).resolve().parents[1]
docs = base / "docs"
cfg = yaml.safe_load((base/"build.config.yaml").read_text())

def should_include(relpath, patterns):
    p = str(relpath).replace("\\","/")
    return any(fnmatch(p, pat) for pat in patterns)

def redact_content(text, fields):
    post = frontmatter.loads(text)
    for f in fields or []:
        post.metadata.pop(f, None)
    return frontmatter.dumps(post)

for bundle, spec in cfg["bundles"].items():
    out = base / f"site-{bundle}"
    if out.exists(): shutil.rmtree(out)
    shutil.copytree(docs, out)

    include = spec.get("include", ["docs/**"])
    redact_fields = spec.get("redact", {}).get("fields", [])

    # prune + redact
    for path in list(out.rglob("*")):
        rel = path.relative_to(base)
        if path.is_dir():
            continue
        if not should_include(rel, include):
            path.unlink()
            continue
        if path.suffix == ".md" and redact_fields:
            path.write_text(redact_content(path.read_text(encoding="utf-8"), redact_fields), encoding="utf-8")

    # provide a Dockerfile to serve this bundle
    dockerfile = f"""
    FROM nginx:stable
    COPY . /usr/share/nginx/html
    EXPOSE 80
    """
    (out / "Dockerfile").write_text(dockerfile.strip()+"
", encoding="utf-8")

    print(f"Built bundle: {bundle} → {out} (with Dockerfile)")
