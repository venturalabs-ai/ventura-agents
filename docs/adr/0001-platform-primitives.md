# ADR 0001: Primitivas verificáveis da plataforma multiagente

- Status: Accepted
- Date: 2026-08-09
- Decision owners: Ventura Labs AI

## Context

O repositório descrevia recursos corporativos importantes, mas nem todos possuíam contratos executáveis ou testes independentes.

## Decision

Adotar primitivas TypeScript pequenas e desacopladas para eventos, engenharia de contexto, grafo de conhecimento com ontologia, risco, aprovação humana e registro de agentes. Cada primitiva deve ser determinística, sem dependência de provedor de modelo e coberta por testes.

## Consequences

- Integrações futuras podem trocar Redis, Kafka, bancos de grafo ou serviços externos atrás desses contratos.
- Decisões de alto risco podem ser encaminhadas ao Human Loop.
- O registro permite descoberta por capacidade e estado operacional.
- Mudanças incompatíveis exigem novo ADR e versionamento semântico.
