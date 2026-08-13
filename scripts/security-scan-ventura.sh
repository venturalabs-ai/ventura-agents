#!/usr/bin/env bash
# security-scan-ventura.sh — Lightweight security audit (local + CI friendly)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
REPORT_DIR="artifacts/security"
mkdir -p "$REPORT_DIR"

echo "========================================="
echo "🔒 VENTURA-AGENTS SECURITY AUDIT"
echo "========================================="
echo ""

# 1. npm audit (if node_modules available)
if command -v npm >/dev/null 2>&1; then
  echo "📦 npm audit..."
  npm audit --audit-level=high > "$REPORT_DIR/npm-audit.txt" 2>&1 || true
  if grep -qiE "found 0 vulnerabilities|0 vulnerabilities" "$REPORT_DIR/npm-audit.txt" 2>/dev/null; then
    echo "   ✅ No high+ vulnerabilities reported"
  else
    echo "   ⚠️  Review $REPORT_DIR/npm-audit.txt"
    head -20 "$REPORT_DIR/npm-audit.txt" || true
  fi
else
  echo "⚠️  npm not available — skip npm audit"
fi
echo ""

# 2. Secret heuristics (no external binary required)
echo "🔍 Scanning for likely secrets in tracked files..."
SECRET_HITS=0
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # Avoid scanning lockfiles / large generated files
  while IFS= read -r file; do
    if grep -nE '(AKIA[0-9A-Z]{16}|-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----|api[_-]?key\s*=\s*["'\''][^"'\'']{16,}|password\s*=\s*["'\''][^"'\'']{8,})' "$file" 2>/dev/null; then
      SECRET_HITS=$((SECRET_HITS + 1))
    fi
  done < <(git ls-files | grep -vE 'package-lock\.json|node_modules|dist/|\.png$|\.jpg$' || true)
fi
if [ "$SECRET_HITS" -eq 0 ]; then
  echo "   ✅ No obvious hardcoded secrets found"
else
  echo "   ❌ Potential secret patterns: $SECRET_HITS file(s) — investigate"
fi
echo ""

# 3. .env not committed
echo "🔐 Checking .env is not tracked..."
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "   ❌ .env is tracked — remove it from git"
else
  echo "   ✅ .env not tracked"
fi
echo ""

# 4. LICENSE + SECURITY presence
echo "📋 Policy files..."
[ -f LICENSE ] && echo "   ✅ LICENSE" || echo "   ❌ LICENSE"
[ -f SECURITY.md ] && echo "   ✅ SECURITY.md" || echo "   ❌ SECURITY.md"
echo ""

echo "========================================="
echo "📊 Security scan finished — reports in $REPORT_DIR"
echo "========================================="
