# World Class 2026 architecture

This repository uses capability maturity instead of empty folders or unsupported production claims.

## Runtime flow

1. The supervisor accepts an `AgentTask` with trace context and a hard budget.
2. Policy evaluation can allow, reject, or require human approval.
3. The model router selects a provider against task and budget constraints.
4. A specialist agent executes and returns output, evidence, status, and cost.
5. The validator evaluates acceptance criteria before results are released.
6. AgentOps records trace, session, cost, latency, and evaluation outcomes.

## Maturity levels

| Level | Meaning |
| --- | --- |
| `implemented` | Executable code is included in the build and covered by an automated check. |
| `contract` | A typed interface or integration boundary exists, but no production adapter is claimed. |
| `planned` | Architecture intent only; it must not be presented as operational. |

The machine-readable registry is `src/platform/architecture.ts` and is exposed at `GET /v1/platform/capabilities`.

## Target domains

The target boundaries are `core`, `agents`, `protocols`, `memory`, `rag`, `models`, `evals`, `data-platform`, `connectors`, `mlops`, `agentops`, `security`, `observability`, `human-loop`, and `deployment`. Implementations should be added only when accompanied by a contract test and operational evidence.

## Architectural rules

- Provider SDKs stay behind adapters; domain contracts do not import vendor packages.
- Every task carries trace, actor, budget, and deadline information.
- High-risk actions stop at a human approval boundary.
- Agent results include evidence and measured cost.
- New capabilities begin as `planned`, move to `contract`, and become `implemented` only after an executable test passes.
