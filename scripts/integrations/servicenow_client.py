import os, requests

class ServiceNowClient:
    def __init__(self, base=None, user=None, password=None):
        self.base = (base or os.environ.get("SN_BASE", "")).rstrip("/")
        self.user = user or os.environ.get("SN_USER", "")
        self.password = password or os.environ.get("SN_PASS", "")
        if not (self.base and self.user and self.password):
            raise RuntimeError("Missing SN_BASE, SN_USER, or SN_PASS")

        self.session = requests.Session()
        self.session.auth = (self.user, self.password)
        self.session.headers.update({"Accept": "application/json"})

    def query(self, table, sysparm_query="", fields=None, limit=100):
        url = f"{self.base}/api/now/table/{table}"
        params = {
            "sysparm_query": sysparm_query,
            "sysparm_limit": limit,
        }
        if fields:
            params["sysparm_fields"] = ",".join(fields)
        r = self.session.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("result", [])

    def incident_slim(self, rec):
        return {
            "number": rec.get("number"),
            "short_description": rec.get("short_description"),
            "priority": rec.get("priority"),
            "state": rec.get("state"),
            "opened_at": rec.get("opened_at"),
            "resolved_at": rec.get("resolved_at"),
            "assignment_group": rec.get("assignment_group"),
            "assigned_to": rec.get("assigned_to"),
        }

    def problem_slim(self, rec):
        return {
            "number": rec.get("number"),
            "short_description": rec.get("short_description"),
            "state": rec.get("state"),
            "opened_at": rec.get("opened_at"),
            "known_error": rec.get("known_error"),
            "assignment_group": rec.get("assignment_group"),
            "assigned_to": rec.get("assigned_to"),
        }
