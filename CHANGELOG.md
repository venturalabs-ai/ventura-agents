# Changelog

All notable changes to the Ventura Agents Ecosystem will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0] - 2026-08-12

### Added
- Python `BaseAgent` completo com lifecycle, governança, retries, métricas e observabilidade (`agents/base/agent.py`)
- Configuração central multi-jurisdição e níveis de autonomia A0–A4 (`core/config.py`)
- LICENSE **MIT** (open source)
- SECURITY.md, CONTRIBUTING.md, CHANGELOG.md
- CI unificado (Node 22 + Python 3.12 + Docker)
- Workflow de Release automático em tags `v*`
- Dependabot (npm, pip, GitHub Actions)
- CODEOWNERS e `.env.example` expandido
- `pyproject.toml` com classifiers production/stable

### Changed
- README reescrito para open source production-ready
- .gitignore expandido (Node + Python + secrets + IDE)
- Workflow Python legado marcado como deprecated

### Notes
- Primeira release **open source** e production-ready da fundação técnica.
- Context Proxy TypeScript + RAG Pipeline + plataforma de agentes já presentes desde 2026-08-09.
