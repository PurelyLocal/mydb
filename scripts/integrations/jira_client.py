import os, requests

class JiraClient:
    def __init__(self, base=None, email=None, token=None):
        self.base = (base or os.environ.get("JIRA_BASE", "")).rstrip("/")
        self.email = email or os.environ.get("JIRA_EMAIL", "")
        self.token = token or os.environ.get("JIRA_TOKEN", "")
        if not (self.base and self.email and self.token):
            raise RuntimeError("Missing JIRA_BASE, JIRA_EMAIL, or JIRA_TOKEN")

        self.session = requests.Session()
        self.session.auth = (self.email, self.token)
        self.session.headers.update({"Accept": "application/json"})

    def search(self, jql, fields=None, max_results=100):
        url = f"{self.base}/rest/api/3/search"
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "fields": fields or ["summary","status","issuetype","priority","updated","created","assignee","labels","customfield_10016"]
        }
        r = self.session.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def issue_slim(self, issue):
        f = issue.get("fields", {})
        return {
            "key": issue.get("key"),
            "summary": f.get("summary"),
            "status": (f.get("status") or {}).get("name"),
            "type": (f.get("issuetype") or {}).get("name"),
            "priority": (f.get("priority") or {}).get("name"),
            "updated": f.get("updated"),
            "created": f.get("created"),
            "assignee": ((f.get("assignee") or {}).get("displayName") if f.get("assignee") else None),
            "labels": f.get("labels") or [],
            "storyPoints": f.get("customfield_10016")
        }
