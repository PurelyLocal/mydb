import os, json, pathlib
from integrations.servicenow_client import ServiceNowClient

out_dir = pathlib.Path(__file__).resolve().parents[1] / "docs/data/servicenow"
out_dir.mkdir(parents=True, exist_ok=True)

def main():
    q_inc = os.environ.get("SN_INCIDENT_QUERY", "priority<=2^active=true")
    q_prb = os.environ.get("SN_PROBLEM_QUERY", "active=true")
    client = ServiceNowClient()

    inc = client.query("incident", q_inc, fields=["number","short_description","priority","state","opened_at","resolved_at","assignment_group","assigned_to"], limit=200)
    prb = client.query("problem", q_prb, fields=["number","short_description","state","opened_at","known_error","assignment_group","assigned_to"], limit=200)

    inc_slim = [client.incident_slim(x) for x in inc]
    prb_slim = [client.problem_slim(x) for x in prb]

    (out_dir / "incidents.json").write_text(json.dumps(inc_slim, indent=2), encoding="utf-8")
    (out_dir / "problems.json").write_text(json.dumps(prb_slim, indent=2), encoding="utf-8")
    print(f"Wrote {len(inc_slim)} SN incidents; {len(prb_slim)} SN problems")

if __name__ == "__main__":
    main()
