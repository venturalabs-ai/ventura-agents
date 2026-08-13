#!/usr/bin/env bash
# setup-sonar-quality-gate.sh — thin wrapper around apply_sonar_quality_gate.py
#
#   export SONAR_TOKEN=...
#   bash scripts/setup-sonar-quality-gate.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ -z "${SONAR_TOKEN:-}" ]; then
  echo "❌ Defina SONAR_TOKEN (token SonarCloud com Administer Quality Gates)."
  exit 1
fi

exec python3 scripts/apply_sonar_quality_gate.py
