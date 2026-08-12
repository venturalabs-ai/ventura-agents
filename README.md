# Ventura Agents Ecosystem V3.0

**Sistema de 76 Agentes Autônomos Empresariais** — Fundação técnica (TypeScript + Python) open source e production-ready.

[![CI](https://github.com/venturalabs-ai/ventura-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/venturalabs-ai/ventura-agents/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-3.0.0-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-yellow)](pyproject.toml)
[![Node](https://img.shields.io/badge/node-%3E%3D20-green)](package.json)

## Visão Geral

Ecossistema **open source** e production-ready de **76 agentes especializados** cobrindo 11 camadas:
Governança, Executiva, Financeiro, Jurídico, RH, Comercial, Compras, Operações, Logística, TI e ESG.

### Diferenciais V3

- **Código real**: Context Proxy (TypeScript) + RAG Pipeline (Python + ChromaDB) + **BaseAgent Python**
- **MCP**: comunicação inter-agentes
- **Observabilidade**: OpenTelemetry + Collector
- **Multi-jurisdição**: BR, US, EU, CN, IN
- **Governança**: níveis de autonomia A0–A4 + hard gates
- **90% redução de tokens** via Context Compression

## Quick Start

```bash
git clone https://github.com/venturalabs-ai/ventura-agents.git
cd ventura-agents

# TypeScript catalog
npm ci
npm run check
npm run dev

# Docker (catálogo + OTEL Collector)
docker compose up --build
```

Endpoints:
- `GET /v1/agents` — lista agentes técnicos
- `GET /v1/agents/:id` — detalhe de capacidade
- `GET /health` — readiness

## Estrutura Principal

| Caminho | Descrição |
|---------|-----------|
| `agents/base/agent.py` | **BaseAgent** Python (lifecycle, governança, retries, métricas) |
| `core/config.py` | Settings central (autonomia, jurisdição, LLM, MCP, OTEL) |
| `src/core/context-proxy.ts` | Context Proxy com compressão de tokens |
| `src/rag/pipeline.py` | RAG production-ready (ChromaDB) |
| `src/platform/` | Event Driven, Knowledge, Risk, Human Loop, Registry |
| `docs/` | ADRs, matriz de completude, MCP |
| `.github/workflows/` | CI unificado + Release + SonarQube + Dependabot |

## Documentação

| Arquivo | Descrição |
|---------|-----------|
| [PROMPT_MASTER_GLOBAL_AGENTS_ECOSYSTEM_V3_COMPLETE.md](PROMPT_MASTER_GLOBAL_AGENTS_ECOSYSTEM_V3_COMPLETE.md) | Documento técnico completo |
| [README_PROMPT_MASTER_V3.md](README_PROMPT_MASTER_V3.md) | Guia de uso e comparativo V2→V3 |
| [RESUMO_EXECUTIVO_V3.md](RESUMO_EXECUTIVO_V3.md) | Visão executiva + checklists |
| [docs/MCP_FOR_AGENTS.md](docs/MCP_FOR_AGENTS.md) | Model Context Protocol |
| [docs/COMPLETENESS_MATRIX.md](docs/COMPLETENESS_MATRIX.md) | Matriz de completude |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como contribuir |
| [SECURITY.md](SECURITY.md) | Política de segurança |

## Capacidades verificadas

| Capacidade | Estado |
|------------|--------|
| Event Driven | ✅ |
| Context Engineering | ✅ |
| Knowledge Graph / Ontologia | ✅ |
| Risk Management | ✅ |
| Human Loop | ✅ |
| Agent Registry | ✅ |
| BaseAgent (Python) | ✅ |
| ADR | ✅ |

## Automação Production-Ready

- **CI** (`ci.yml`): Node typecheck/test/build + Python ruff/pytest + Docker build
- **SonarQube** (`sonarqube.yml`): análise de qualidade + Quality Gate em PRs e `main`
- **Release** (`release.yml`): GitHub Release automático em tags `v*`
- **Dependabot**: atualizações semanais (npm / pip / GitHub Actions) com groups e conventional commits
- **Branch protection**: PR obrigatório + status checks + block force pushes em `main`

### SonarQube (setup único)

1. Crie o projeto em [SonarQube Cloud](https://sonarcloud.io) (org: `venturalabs-ai`)
2. Gere um token e adicione o secret no repositório:
   - **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `SONAR_TOKEN`
   - Value: o token gerado
3. O arquivo `sonar-project.properties` já está configurado.

## Licença

Distribuído sob a licença **MIT**. Veja [LICENSE](LICENSE) para detalhes.

```
MIT License — Copyright (c) 2026 Ventura Labs AI
```

---

**Versão:** 3.0.0  
**Owner:** [venturalabs-ai](https://github.com/venturalabs-ai)  
**Repositório mestre (índice de agentes):** [ventura-agents-master](https://github.com/venturalabs-ai/ventura-agents-master)
