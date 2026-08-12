# Changelog

All notable changes to the Ventura Agents Ecosystem will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Python `BaseAgent` completo com lifecycle, governança, retries, métricas e observabilidade (`agents/base/agent.py`)
- Configuração central multi-jurisdição e níveis de autonomia A0–A4 (`core/config.py`)
- LICENSE proprietária, SECURITY.md, CONTRIBUTING.md e automação de release

### Changed
- CI unificado (Node + Python)
- .gitignore expandido para Python e artefatos de build

## [3.0.0] - 2026-08-09

### Added
- Context Proxy TypeScript com redução de ~90% de tokens
- RAG Pipeline production-ready (Python + ChromaDB)
- Plataforma TypeScript: Event Driven, Knowledge Graph, Risk Management, Human Loop, Agent Registry
- Documentação completa (PROMPT MASTER V3, Resumo Executivo, ADRs)
- Docker Compose + OpenTelemetry Collector
- Matriz de completude 100%

### Notes
- Versão considerada **Production Ready** para o catálogo técnico e fundação de agentes.
