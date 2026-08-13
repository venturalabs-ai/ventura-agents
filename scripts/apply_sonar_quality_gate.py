#!/usr/bin/env python3
"""Apply Ventura Production Quality Gate to SonarQube Cloud from sonar/quality-gate.json.

Idempotent: creates gate if missing, replaces conditions, associates project.

Env:
  SONAR_TOKEN          required (Administer Quality Gates recommended)
  SONAR_HOST_URL       default https://sonarcloud.io
  SONAR_ORGANIZATION   override org from JSON
  SONAR_PROJECT_KEY    override project from JSON
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_FILE = ROOT / "sonar" / "quality-gate.json"

HOST = os.environ.get("SONAR_HOST_URL", "https://sonarcloud.io").rstrip("/")
API = f"{HOST}/api"
TOKEN = os.environ.get("SONAR_TOKEN", "")


def die(msg: str, code: int = 1) -> None:
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)


def req(method: str, path: str, data: dict | None = None) -> tuple[int, dict | str]:
    url = f"{API}{path}"
    body = None
    headers = {"Authorization": f"Bearer {TOKEN}"}
    if data is not None:
        body = urllib.parse.urlencode(data).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as resp:
            raw = resp.read().decode() or "{}"
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode() if e.fp else str(e)
        try:
            payload = json.loads(raw)
        except Exception:
            payload = raw
        return e.code, payload
    except urllib.error.URLError as e:
        return 0, str(e.reason)


def main() -> None:
    if not TOKEN:
        die("SONAR_TOKEN is required")

    if not GATE_FILE.is_file():
        die(f"Missing {GATE_FILE}")

    cfg = json.loads(GATE_FILE.read_text(encoding="utf-8"))
    gate_name = cfg["name"]
    org = os.environ.get("SONAR_ORGANIZATION") or cfg.get("organization") or "venturalabs-ai"
    project_key = os.environ.get("SONAR_PROJECT_KEY") or cfg.get("projectKey") or "venturalabs-ai_ventura-agents"
    conditions = cfg.get("conditions") or []

    print("=========================================")
    print(f"🎯 Apply Quality Gate: {gate_name}")
    print(f"   Organization: {org}")
    print(f"   Project:      {project_key}")
    print(f"   Conditions:   {len(conditions)}")
    print(f"   Source:       {GATE_FILE.relative_to(ROOT)}")
    print("=========================================")
    print()

    # 1) Create gate if missing
    print("→ Create gate (if missing)...")
    status, payload = req(
        "POST",
        "/qualitygates/create",
        {"name": gate_name, "organization": org},
    )
    if status in (200, 204):
        print("   ✅ Gate created")
    else:
        text = json.dumps(payload) if isinstance(payload, dict) else str(payload)
        if "already" in text.lower() or status == 400:
            print("   ℹ️  Gate already exists (or create returned 400)")
        else:
            print(f"   ⚠️  create status={status} body={text[:300]}")

    # 2) Show + delete existing conditions
    print("→ Reset conditions...")
    q = urllib.parse.urlencode({"name": gate_name, "organization": org})
    status, show = req("GET", f"/qualitygates/show?{q}")
    if status != 200 or not isinstance(show, dict):
        die(f"Could not load quality gate show (status={status}): {show}")

    for cond in show.get("conditions") or []:
        cid = cond.get("id")
        if not cid:
            continue
        print(f"   - delete condition id={cid} metric={cond.get('metric')}")
        req("POST", "/qualitygates/delete_condition", {"id": str(cid)})

    # 3) Create conditions from JSON
    print("→ Add conditions from JSON...")
    for c in conditions:
        metric = c["metric"]
        op = c["op"]
        error = str(c["error"])
        print(f"   + {metric} {op} {error} ({c.get('scope', '')})")
        st, body = req(
            "POST",
            "/qualitygates/create_condition",
            {
                "gateName": gate_name,
                "organization": org,
                "metric": metric,
                "op": op,
                "error": error,
            },
        )
        if st not in (200, 204):
            print(f"     ⚠️  status={st} body={body}")

    # 4) Associate project
    print("→ Associate project...")
    st, body = req(
        "POST",
        "/qualitygates/select",
        {
            "projectKey": project_key,
            "gateName": gate_name,
            "organization": org,
        },
    )
    if st in (200, 204):
        print("   ✅ Project associated")
    else:
        print(f"   ⚠️  select status={st} body={body}")

    # 5) Verify
    print("→ Verify...")
    st, show = req("GET", f"/qualitygates/show?{q}")
    if st == 200 and isinstance(show, dict):
        n = len(show.get("conditions") or [])
        print(f"   ✅ Gate has {n} condition(s)")
    else:
        print(f"   ⚠️  verify status={st}")

    print()
    print(f"✅ Done. UI: {HOST}/organizations/{org}/quality_gates")
    print(f"   Project: {HOST}/project/overview?id={project_key}")


if __name__ == "__main__":
    main()
