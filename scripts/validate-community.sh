#!/usr/bin/env bash
# validate-community.sh — Open-source community readiness audit
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PASS=0
FAIL=0

ok() { PASS=$((PASS+1)); echo "   ✅ $1"; }
bad() { FAIL=$((FAIL+1)); echo "   ❌ $1"; }

echo "👥 VENTURA-AGENTS COMMUNITY AUDIT"
echo "================================="
echo ""

echo "1. License"
if [ -f LICENSE ] && head -1 LICENSE | grep -qi MIT; then ok "MIT LICENSE"; else bad "MIT LICENSE"; fi

echo "2. README"
if [ -f README.md ]; then ok "README.md exists"; else bad "README.md exists"; fi
BADGE_COUNT=$(grep -c '!\[.*\](' README.md 2>/dev/null || echo 0)
echo "   📊 Badge-like markers: $BADGE_COUNT"

echo "3. CONTRIBUTING.md"
if [ -f CONTRIBUTING.md ]; then
  ok "File exists"
  grep -qi "pull request\|PR" CONTRIBUTING.md && ok "PR guidance" || bad "PR guidance"
  grep -qi "commit" CONTRIBUTING.md && ok "Commit guidance" || bad "Commit guidance"
else
  bad "CONTRIBUTING.md missing"
fi

echo "4. CODE_OF_CONDUCT.md"
if [ -f CODE_OF_CONDUCT.md ]; then
  ok "File exists"
  grep -qi "contributor covenant" CODE_OF_CONDUCT.md && ok "Contributor Covenant" || bad "Contributor Covenant"
else
  bad "CODE_OF_CONDUCT.md missing"
fi

echo "5. SECURITY.md"
if [ -f SECURITY.md ]; then ok "Security policy"; else bad "Security policy"; fi

echo "6. Issue templates"
if [ -d .github/ISSUE_TEMPLATE ]; then
  COUNT=$(find .github/ISSUE_TEMPLATE -name '*.md' -o -name '*.yml' | wc -l | tr -d ' ')
  ok "Template dir ($COUNT files)"
else
  bad "Issue templates missing"
fi

echo "7. PR template"
if [ -f .github/pull_request_template.md ] || [ -f .github/PULL_REQUEST_TEMPLATE.md ]; then
  ok "PR template"
else
  bad "PR template"
fi

echo "8. CI / automation"
for f in ci.yml release.yml sonarqube.yml dependabot.yml; do
  if [ -f ".github/workflows/$f" ] || [ -f ".github/$f" ]; then ok "$f"; else bad "$f"; fi
done

echo "9. Versioning"
if [ -f package.json ]; then
  VER=$(node -p "require('./package.json').version" 2>/dev/null || echo "?")
  echo "   📦 package.json version: $VER"
  ok "package.json present"
else
  bad "package.json"
fi
if [ -f CHANGELOG.md ]; then ok "CHANGELOG.md"; else bad "CHANGELOG.md"; fi

echo ""
echo "================================="
echo "📊 Community: $PASS passed, $FAIL failed"
echo "================================="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
