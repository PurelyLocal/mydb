import argparse, subprocess, sys

ap = argparse.ArgumentParser(description="Create hotfix branch/tag from MI")
ap.add_argument("--mi", required=True, help="MI id, e.g., MI-2025-10-24-001")
ap.add_argument("--version", default="0.0.0", help="base version like 1.2.3")
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

branch = f"hotfix/{args.version}+{args.mi.lower()}"
cmds = [
    ["git", "checkout", "-b", branch],
    ["git", "commit", "--allow-empty", "-m", f"chore(hotfix): start {args.mi}"],
    ["git", "tag", f"{args.version}-hotfix-{args.mi.lower()}"]
]

for c in cmds:
    print("$", " ".join(c))
    if not args.dry_run:
        subprocess.check_call(c)

print("Hotfix flow prepared.")
