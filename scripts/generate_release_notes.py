import subprocess
import argparse
import os
import requests

# GitHub API URL
GITHUB_API_URL = "https://api.github.com"

def get_git_log(since_tag):
    """Get Git log since the last tag."""
    cmd = ["git", "log", f"{since_tag}..HEAD", "--pretty=format:%s"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()

def format_release_notes(logs, version):
    """Format release notes using a template."""
    notes = [f"# Release Notes for v{version}\n"]
    notes.append("## 🚀 Features")
    for log in logs:
        if "feat:" in log.lower():
            notes.append(f"- {log}")

    notes.append("\n## 🐛 Bug Fixes")
    for log in logs:
        if "fix:" in log.lower():
            notes.append(f"- {log}")

    notes.append("\n## 🔧 Improvements")
    for log in logs:
        if "chore:" in log.lower() or "refactor:" in log.lower():
            notes.append(f"- {log}")

    return "\n".join(notes)

def publish_to_github(repo, version, notes, token):
    """Publish release notes to GitHub."""
    url = f"{GITHUB_API_URL}/repos/{repo}/releases"
    headers = {"Authorization": f"token {token}"}
    payload = {
        "tag_name": f"v{version}",
        "name": f"v{version}",
        "body": notes,
        "draft": False,
        "prerelease": False
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    print("Release published successfully.")

def main():
    parser = argparse.ArgumentParser(description="Generate and publish release notes.")
    parser.add_argument("--since", required=True, help="Tag to start from (e.g., v1.0.0).")
    parser.add_argument("--version", required=True, help="Release version (e.g., 1.1.0).")
    parser.add_argument("--repo", required=True, help="GitHub repository (e.g., user/repo).")
    parser.add_argument("--token", required=True, help="GitHub token.")
    args = parser.parse_args()

    logs = get_git_log(args.since)
    notes = format_release_notes(logs, args.version)
    print(notes)

    publish_to_github(args.repo, args.version, notes, args.token)

if __name__ == "__main__":
    main()