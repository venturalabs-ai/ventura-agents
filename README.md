# Ventura Global Agents

An evolving enterprise multi-agent platform with explicit boundaries for orchestration, specialist agents, protocols, memory, RAG, model routing, evaluations, operations, security, observability, human approval, and deployment.

> Current status: foundation under active development. Capabilities are classified as `implemented`, `contract`, or `planned`; this repository does not claim production readiness for planned components.

## What runs today

- TypeScript agent catalog with supervisor, planning, delivery, data, AI, security, MLOps, and AgentOps roles.
- HTTP endpoints for health, registered agents, and the architecture capability registry.
- Container build and local Docker Compose stack with an OpenTelemetry Collector.
- Type checking, unit tests, build validation, Docker configuration validation, and image build in CI.
- A Python RAG prototype whose public contract is checked statically; external-provider integration is not yet an end-to-end test.

## Quick start

```bash
npm ci
npm run check
npm start
```

Available endpoints:

- `GET /health`
- `GET /v1/agents`
- `GET /v1/agents/:id`
- `GET /v1/platform/capabilities`

For containers:

```bash
docker compose up --build
```

## Architecture

The [World Class 2026 architecture](docs/architecture/WORLD_CLASS_2026.md) defines the target domains, runtime flow, architectural rules, and objective maturity model. The machine-readable source of truth is [`src/platform/architecture.ts`](src/platform/architecture.ts).

| Critical capability | Current maturity |
| --- | --- |
| Multi-agent catalog | Implemented |
| Docker / Compose / CI deployment foundation | Implemented |
| Orchestration, routing, policy, evals, RAG, MLOps, AgentOps, security, observability, human loop | Contract |
| MCP, A2A, knowledge graph, data platform, production connectors | Planned |

## Existing design documents

- [Global Agents Ecosystem V3](PROMPT_MASTER_GLOBAL_AGENTS_ECOSYSTEM_V3_COMPLETE.md)
- [V3 guide](README_PROMPT_MASTER_V3.md)
- [Executive summary](RESUMO_EXECUTIVO_V3.md)
- [MCP exploration](docs/MCP_FOR_AGENTS.md)

These documents describe direction and design. Runtime support is authoritative only when the capability registry marks it `implemented` and CI provides evidence.

## Ownership

Ventura Labs AI · Wemerson Mota de Oliveira
