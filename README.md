# Ventura Agents Ecosystem V3.0

**Ecossistema de Agentes Autônomos Empresariais** — Fundação técnica (TypeScript + Python) open source. O catálogo técnico verificado atual contém **4 agentes**; o roadmap planeja **76 agentes especializados** em 11 camadas.

[![CI](https://github.com/venturalabs-ai/ventura-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/venturalabs-ai/ventura-agents/actions/workflows/ci.yml)
[![SonarQube](https://github.com/venturalabs-ai/ventura-agents/actions/workflows/sonarqube.yml/badge.svg)](https://github.com/venturalabs-ai/ventura-agents/actions/workflows/sonarqube.yml)
[![Version](https://img.shields.io/badge/version-3.0.0-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-yellow)](pyproject.toml)
[![Node](https://img.shields.io/badge/node-%3E%3D20-green)](package.json)

## Visão Geral

Ecossistema **open source** de agentes especializados. O roadmap cobre 11 camadas:
Governança, Executiva, Financeiro, Jurídico, RH, Comercial, Compras, Operações, Logística, TI e ESG.
A fundação técnica atual implementa e testa as primitivas centrais e agentes verificáveis.

### Diferenciais V3

- **Código real e testado**: Context Proxy (TypeScript) + RAG Pipeline (Python + ChromaDB) + **BaseAgent Python**
- **MCP**: arquitetura definida — integração futura (ver `docs/MCP_FOR_AGENTS.md`)
- **Observabilidade**: OpenTelemetry + Collector
- **Multi-jurisdição**: BR, US, EU, CN, IN
- **Governança**: níveis de autonomia A0–A4 + hard gates, com fail-closed em produção
- **Compressão de contexto** com `compressionRatio` mensurável (Context Proxy)

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
| `src/core/context-proxy.ts` | Context Proxy — estado comprimido determinístico (em memória) |
| `src/rag/pipeline.py` | RAG production-ready (ChromaDB) |
| `src/platform/` | Event Driven, Knowledge, Risk, Human Loop, Registry |
| `docs/` | ADRs, matriz de completude, MCP, SonarQube |
| `.github/workflows/` | CI + Health + Release + SonarQube + Dependabot |

## Documentação

| Arquivo | Descrição |
|---------|-----------|
| [PROMPT_MASTER_GLOBAL_AGENTS_ECOSYSTEM_V3_COMPLETE.md](PROMPT_MASTER_GLOBAL_AGENTS_ECOSYSTEM_V3_COMPLETE.md) | Documento técnico completo |
| [README_PROMPT_MASTER_V3.md](README_PROMPT_MASTER_V3.md) | Guia de uso e comparativo V2→V3 |
| [RESUMO_EXECUTIVO_V3.md](RESUMO_EXECUTIVO_V3.md) | Visão executiva + checklists |
| [docs/MCP_FOR_AGENTS.md](docs/MCP_FOR_AGENTS.md) | Model Context Protocol |
| [docs/COMPLETENESS_MATRIX.md](docs/COMPLETENESS_MATRIX.md) | Matriz de completude |
| [docs/SONARQUBE.md](docs/SONARQUBE.md) | Setup SonarQube Cloud |
| [docs/TEST_ENVIRONMENT.md](docs/TEST_ENVIRONMENT.md) | Ambiente de auditoria |
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
| Context Proxy (compressão) | ✅ |
| RAG Pipeline | ✅ |
| BaseAgent (Python) | ✅ |
| ADR | ✅ |

> Critério: ✅ exige implementação + teste automatizado + documentação versionada (ver `docs/COMPLETENESS_MATRIX.md`).

## Automação Production-Ready

- **CI** (`ci.yml`): Node typecheck/test/build + Python ruff/pytest + Docker build
- **SonarQube** (`sonarqube.yml`): scan + Quality Gate em PRs e `main`
- **Health Check** (`health-check.yml`): validação horária
- **Release** (`release.yml`): GitHub Release em tags `v*`
- **Dependabot**: npm / pip / GitHub Actions

### SonarQube (setup único)

Guia completo: **[docs/SONARQUBE.md](docs/SONARQUBE.md)**

1. Projeto em [sonarcloud.io](https://sonarcloud.io) — org `venturalabs-ai`, key `venturalabs-ai_ventura-agents`
2. Secret no GitHub: `SONAR_TOKEN`
3. Workflow roda em todo push/PR em `main`

## Licença

Distribuído sob a licença **MIT**. Veja [LICENSE](LICENSE) para detalhes.

---

**Versão:** 3.0.0  
**Owner:** [venturalabs-ai](https://github.com/venturalabs-ai)  
**Repositório mestre:** [ventura-agents-master](https://github.com/venturalabs-ai/ventura-agents-master)
