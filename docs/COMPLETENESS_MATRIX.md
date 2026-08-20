# Matriz de completude da plataforma

Um item só recebe ✅ quando possui implementação, teste automatizado e documentação versionada.

| Capacidade | Estado | Evidência |
| --- | --- | --- |
| Event Driven | ✅ Concluído | `src/platform/events.ts` — publicação, assinatura e idempotência |
| Context Engineering | ✅ Concluído | `src/platform/context.ts` — seleção determinística por relevância e orçamento |
| Knowledge Graph | ✅ Concluído | `src/platform/knowledge.ts` — entidades, relações e consultas |
| Ontologia | ✅ Concluído | `src/platform/knowledge.ts` — tipos e relações permitidas validados |
| Risk Management | ✅ Concluído | `src/platform/risk.ts` — score, nível e decisão allow/review/block |
| Human Loop | ✅ Concluído | `src/platform/human-loop.ts` — solicitação, decisão e responsabilização |
| ADR | ✅ Concluído | `docs/adr/0001-platform-primitives.md` |
| Agent Registry | ✅ Concluído | `src/platform/registry.ts` — registro versionado e descoberta por capacidade |
| Context Proxy | ✅ Concluído | `src/core/context-proxy.ts` — estado comprimido determinístico com `compressionRatio`; teste em `tests/context-proxy.test.ts` |
| RAG Pipeline | ✅ Concluído | `src/rag/pipeline.py` — chunking, retrieval e re-ranking determinístico; teste em `tests/test_rag_pipeline.py` |
| BaseAgent | ✅ Concluído | `agents/base/agent.py` — lifecycle, governança fail-closed e métricas; teste em `tests/test_base_agent.py` |

Validação consolidada: `npm run check` + `pytest tests/` + `ruff check agents core src/rag tests`.
