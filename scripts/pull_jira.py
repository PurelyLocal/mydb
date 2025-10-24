import os, json, pathlib
from integrations.jira_client import JiraClient

out_dir = pathlib.Path(__file__).resolve().parents[1] / "docs/data/jira"
out_dir.mkdir(parents=True, exist_ok=True)

def main():
    jql_mi = os.environ.get("JIRA_JQL_MI", "ORDER BY updated DESC")
    jql_prb = os.environ.get("JIRA_JQL_PRB", "issuetype=Problem ORDER BY updated DESC")
    client = JiraClient()
    mi = client.search(jql_mi, max_results=100).get("issues", [])
    prb = client.search(jql_prb, max_results=100).get("issues", [])

    mi_slim = [client.issue_slim(x) for x in mi]
    prb_slim = [client.issue_slim(x) for x in prb]

    (out_dir / "major_incidents.json").write_text(json.dumps(mi_slim, indent=2), encoding="utf-8")
    (out_dir / "problems.json").write_text(json.dumps(prb_slim, indent=2), encoding="utf-8")
    print(f"Wrote {len(mi_slim)} MI; {len(prb_slim)} PRB")

if __name__ == "__main__":
    main()
