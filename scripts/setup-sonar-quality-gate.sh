#!/usr/bin/env bash
# setup-sonar-quality-gate.sh
# Cria/atualiza o Quality Gate "Ventura Production" no SonarQube Cloud e associa ao projeto.
#
# Requisitos:
#   export SONAR_TOKEN=...   # token com permissão Administer Quality Gates
#
# Uso:
#   bash scripts/setup-sonar-quality-gate.sh

set -euo pipefail

API="${SONAR_HOST_URL:-https://sonarcloud.io/api}"
GATE_NAME="Ventura Production"
PROJECT_KEY="${SONAR_PROJECT_KEY:-venturalabs-ai_ventura-agents}"
ORG="${SONAR_ORGANIZATION:-venturalabs-ai}"

if [ -z "${SONAR_TOKEN:-}" ]; then
  echo "❌ Defina SONAR_TOKEN (token SonarCloud com Administer Quality Gates)."
  exit 1
fi

auth_header() {
  # SonarCloud aceita token como usuário, senha vazia
  echo "Authorization: Bearer ${SONAR_TOKEN}"
}

echo "========================================="
echo "🎯 Sonar Quality Gate: $GATE_NAME"
echo "   Project: $PROJECT_KEY"
echo "   Org:     $ORG"
echo "========================================="
echo ""

# 1) Criar gate (ignora erro se já existir)
echo "→ Creating quality gate (if missing)..."
curl -sS -X POST "$API/qualitygates/create" \
  -H "$(auth_header)" \
  -d "name=${GATE_NAME}" \
  -d "organization=${ORG}" \
  >/tmp/qg-create.json 2>/dev/null || true

if grep -qi "already exists\|already been taken" /tmp/qg-create.json 2>/dev/null; then
  echo "   ℹ️  Gate already exists"
elif grep -qi '"name"' /tmp/qg-create.json 2>/dev/null; then
  echo "   ✅ Gate created"
else
  echo "   ℹ️  Create response: $(head -c 200 /tmp/qg-create.json 2>/dev/null || true)"
fi

# 2) Listar condições atuais e remover (para reaplicar de forma idempotente)
echo "→ Fetching current conditions..."
SHOW=$(curl -sS "$API/qualitygates/show?name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$GATE_NAME'''))")&organization=${ORG}" \
  -H "$(auth_header)" || echo "{}")

echo "$SHOW" > /tmp/qg-show.json

# Extrair ids de condições existentes (JSON simples)
python3 - <<'PY' || true
import json, os, subprocess, sys
path = "/tmp/qg-show.json"
try:
    data = json.load(open(path))
except Exception:
    sys.exit(0)
conds = data.get("conditions") or []
for c in conds:
    cid = c.get("id")
    if not cid:
        continue
    print(f"Removing condition id={cid} metric={c.get('metric')}")
    os.system(
        f'curl -sS -X POST "{os.environ.get("API", "https://sonarcloud.io/api")}/qualitygates/delete_condition" '
        f'-H "Authorization: Bearer {os.environ["SONAR_TOKEN"]}" '
        f'-d "id={cid}" >/dev/null'
    )
PY

# Export API for python helper above
export API
export SONAR_TOKEN

# Re-run deletion with env visible
python3 - <<'PY' || true
import json, os, urllib.request, urllib.parse

api = os.environ.get("API", "https://sonarcloud.io/api")
token = os.environ["SONAR_TOKEN"]

def post(path, data):
    req = urllib.request.Request(
        api + path,
        data=urllib.parse.urlencode(data).encode(),
        headers={"Authorization": f"Bearer {token}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.read().decode()
    except Exception as e:
        return str(e)

try:
    data = json.load(open("/tmp/qg-show.json"))
except Exception:
    data = {}
for c in data.get("conditions") or []:
    cid = c.get("id")
    if cid:
        print(f"   Removing condition {cid} ({c.get('metric')})")
        post("/qualitygates/delete_condition", {"id": str(cid)})
PY

# 3) Adicionar condições do Ventura Production
echo "→ Adding Ventura Production conditions..."

add_condition() {
  local metric="$1" op="$2" error="$3"
  echo "   + $metric $op $error"
  curl -sS -X POST "$API/qualitygates/create_condition" \
    -H "$(auth_header)" \
    -d "gateName=${GATE_NAME}" \
    -d "organization=${ORG}" \
    -d "metric=${metric}" \
    -d "op=${op}" \
    -d "error=${error}" \
    >/dev/null || echo "     (warn: condition may already exist or metric unsupported)"
}

# New code — ratings: 1 = A; GT 1 fails worse than A
add_condition new_reliability_rating GT 1
add_condition new_security_rating GT 1
add_condition new_maintainability_rating GT 1
add_condition new_coverage LT 60
add_condition new_duplicated_lines_density GT 3
add_condition new_security_hotspots_reviewed LT 100

# Overall
add_condition security_rating GT 1
add_condition reliability_rating GT 2

# 4) Associar projeto ao gate
echo "→ Associating project $PROJECT_KEY ..."
curl -sS -X POST "$API/qualitygates/select" \
  -H "$(auth_header)" \
  -d "projectKey=${PROJECT_KEY}" \
  -d "gateName=${GATE_NAME}" \
  -d "organization=${ORG}" \
  >/tmp/qg-select.json || true

echo "   Response: $(head -c 180 /tmp/qg-select.json 2>/dev/null || echo ok)"
echo ""
echo "✅ Quality Gate '$GATE_NAME' configurado e associado."
echo "   Verifique em: https://sonarcloud.io/organizations/${ORG}/quality_gates"
echo "   Projeto: https://sonarcloud.io/project/overview?id=${PROJECT_KEY}"
