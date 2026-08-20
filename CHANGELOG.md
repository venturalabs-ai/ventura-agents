# Changelog

All notable changes to the Ventura Agents Ecosystem will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- `src/core/context-proxy.ts` reescrito como primitiva TypeScript determinística (em memória, sem dependência de Redis/OpenAI/zod) e incluído no `tsconfig` — antes o arquivo não compilava e ficava fora do build.
- `src/rag/pipeline.py`: implementados `_chunk_recursive` e `_chunk_by_structure` (antes chamados mas inexistentes), correção de truncamento no `retrieve` (`results[:top_k]` em dict), re-ranking determinístico de fato e remoção de modelo inválido (`claude-haiku-3.5`). Clientes OpenAI/ChromaDB agora são inicializados de forma lazy.
- `agents/base/agent.py`: aprovação HITL agora é **fail-closed em produção** (antes auto-aprovava após 1s). Auto-aprovação fora de development só com `hitl_auto_approve=true`.
- `src/index.ts`: `decodeURIComponent` protegido contra URL malformada (400 em vez de 500).
- `core/config.py`: migrado `class Config` → `SettingsConfigDict` (deprecation do Pydantic v2).

### Changed
- CI (`ci.yml` e `sonarqube.yml`) agora **falham** em falhas de Python (ruff/pytest/instalação) — removidos os `|| true`.
- `pyproject.toml`: extra `rag` passa a declarar `numpy` e `openai`; `pythonpath` adicionado ao pytest; wheel mínimo configurado (`only-include`) para que `pip install -e ".[dev]"` funcione (antes o hatchling falhava por não haver pacote com o nome do projeto).
- `sonarqube.yml`: ação de Quality Gate corrigida para `v1.2.1` (a referência `v1.3.0` não existia e quebrava o job no setup).
- README/`docs/COMPLETENESS_MATRIX.md` atualizados para claims verificáveis (4 agentes no catálogo; MCP como integração futura; compressão mensurável via `compressionRatio`).

### Added
- Testes: `tests/context-proxy.test.ts` (7), `tests/test_base_agent.py` (9), `tests/test_rag_pipeline.py` (10).
- `docs/AUDIT.md` com achados e remediação.

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
