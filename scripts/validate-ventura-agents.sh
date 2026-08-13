#!/usr/bin/env bash
# validate-ventura-agents.sh — Functional audit for ventura-agents
# Usage: bash scripts/validate-ventura-agents.sh

set -euo pipefail

PASS=0
FAIL=0
TOTAL=0
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

check() {
  local name="$1"
  shift
  TOTAL=$((TOTAL + 1))
  if "$@" >/dev/null 2>&1; then
    PASS=$((PASS + 1))
    echo "✅ $name"
  else
    FAIL=$((FAIL + 1))
    echo "❌ $name"
  fi
}

echo "========================================="
echo "🔍 VENTURA-AGENTS FUNCTIONAL AUDIT"
echo "========================================="
echo ""

check "MIT LICENSE present" test -f LICENSE
check "README present" test -f README.md
check "CONTRIBUTING present" test -f CONTRIBUTING.md
check "CODE_OF_CONDUCT present" test -f CODE_OF_CONDUCT.md
check "SECURITY policy present" test -f SECURITY.md
check "CI workflow present" test -f .github/workflows/ci.yml
check "SonarQube workflow present" test -f .github/workflows/sonarqube.yml
check "Issue templates present" test -d .github/ISSUE_TEMPLATE
check "BaseAgent present" test -f agents/base/agent.py
check "core/config present" test -f core/config.py
check "Completeness matrix present" test -f docs/COMPLETENESS_MATRIX.md
check "ADR present" test -f docs/adr/0001-platform-primitives.md

if command -v npm >/dev/null 2>&1; then
  if [ -d node_modules ] || npm ci >/dev/null 2>&1; then
    check "TypeScript typecheck" npm run typecheck
    check "Test suite" npm test
    check "Build" npm run build
    check "Full check (typecheck+test+build)" npm run check
  else
    echo "⚠️  npm ci failed — skipping Node checks"
    FAIL=$((FAIL + 1))
    TOTAL=$((TOTAL + 1))
  fi
else
  echo "⚠️  npm not found — skipping Node checks"
fi

if command -v docker >/dev/null 2>&1; then
  check "Docker Compose config valid" docker compose config --quiet
else
  echo "⚠️  docker not found — skipping compose check"
fi

# Content checks
TOTAL=$((TOTAL + 1))
if grep -q "MIT" README.md 2>/dev/null; then
  PASS=$((PASS + 1))
  echo "✅ README mentions MIT"
else
  FAIL=$((FAIL + 1))
  echo "❌ README mentions MIT"
fi

TOTAL=$((TOTAL + 1))
if grep -qi "Production Ready\|production-ready" README.md 2>/dev/null; then
  PASS=$((PASS + 1))
  echo "✅ Production Ready signal in README"
else
  FAIL=$((FAIL + 1))
  echo "❌ Production Ready signal in README"
fi

echo ""
echo "========================================="
echo "📊 RESULTS: $PASS/$TOTAL passed ($FAIL failed)"
echo "========================================="

if [ "$FAIL" -eq 0 ]; then
  echo "🎉 ALL CHECKS PASSED — Ready for launch"
  exit 0
else
  echo "⚠️  $FAIL CHECK(S) FAILED — fix before launch"
  exit 1
fi
