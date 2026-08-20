# Auditoria Técnica — Ventura Agents

Auditoria estrutural do repositório `venturalabs-ai/ventura-agents` (v3.0.0) comparando as
afirmações de `README.md`/`docs/` com o código real. Data: 2026-08-20.

## Resumo

| Métrica | Antes | Depois |
|---|---|---|
| Testes TypeScript | 9 | 16 |
| Testes Python | 1 (contrato AST) | 20 |
| `ruff check` | 91 erros | 0 |
| `npm run check` | verde | verde |
| Compilação `context-proxy.ts` | 21+ erros (fora do build) | OK (no build) |
| CI Python | falhas mascaradas (`\|\| true`) | falhas bloqueiam |

## Achados críticos (claims vs. código real)

### 1. `src/core/context-proxy.ts` — arquivo morto vendido como código real
- Excluído do `tsconfig.json` (`include` não cobria `src/core/**`), então `npm run check` ficava verde.
- Compilação isolada falhava com **21+ erros**:
  - módulos `ioredis`, `openai`, `@anthropic-ai/sdk`, `zod` não declarados no `package.json`;
  - tipos `AgentResponse`, `AgentContext`, `SubagentResult` inexistentes;
  - ~12 métodos invocados mas nunca implementados (`getCompressedState`, `saveCompressedState`,
    `loadPolicy`, `callAgent`, `logExecution`, `compressContext`, `cosineSimilarity`, `chunkArray`, `hash`, etc.).
- README anunciava "90% redução de tokens" sem código executável.
- **Remediação**: reescrito como primitiva TS determinística e provider-agnostic (em memória), com
  `compressionRatio` mensurável, incluído no `tsconfig` e coberto por `tests/context-proxy.test.ts`.

### 2. `src/rag/pipeline.py` — defeitos de runtime e dependências não declaradas
- `_chunk_recursive` e `_chunk_by_structure` eram chamados em `_chunk_document` mas **não existiam** → `AttributeError`.
- `retrieve` com `rerank=False` fazia `results[:top_k]` sobre um `dict` → `TypeError`.
- `_rerank` chamava o LLM mas **retornava a entrada sem re-ranking**.
- Modelo `claude-haiku-3.5` inexistente na API Anthropic.
- Imports `openai`, `anthropic`, `numpy` fora de `pyproject.toml`.
- **Remediação**: chunkers recursivo e por estrutura implementados; truncamento corrigido;
  re-ranking determinístico por overlap léxico; modelo inválido removido; clientes OpenAI/ChromaDB
  inicializados de forma lazy; extra `rag` declara `numpy` e `openai`; 10 testes funcionais em
  `tests/test_rag_pipeline.py`.

### 3. `agents/base/agent.py` — governança auto-aprovava em produção
- `_wait_for_approval` em produção apenas aguardava 1s e **retornava `True`**, contornando o HITL
  e os hard gates anunciados no README.
- **Remediação**: fail-closed em produção — sem canal HITL configurado a tarefa é rejeitada
  (`Rejected by governance`). Auto-aprovação fora de development só com `hitl_auto_approve=true`.
  9 testes em `tests/test_base_agent.py`.

### 4. CI não executava as validações Python
- `ci.yml` e `sonarqube.yml` usavam `|| true` em `pip install -e ".[dev]"`, `ruff` e `pytest` →
  qualquer quebra Python passava silenciosamente.
- **Remediação**: removidos os `|| true`; falhas de instalação, lint e teste agora bloqueiam a pipeline.

### 5. Claims de catálogo e MCP
- README afirmava **76 agentes / 11 camadas**; o catálogo técnico real (`src/catalog.ts`) tem **4 agentes**.
- MCP descrito como "comunicação inter-agentes" sem código MCP no repositório.
- **Remediação**: README e matriz de completude agora distinguem roadmap (76) de catálogo verificado
  (4) e MCP como integração futura arquitetada (`docs/MCP_FOR_AGENTS.md`).

## Achados menores corrigidos
- `src/index.ts`: `decodeURIComponent` sem `try/catch` (URL malformada gerava 500).
- `core/config.py`: `class Config` (deprecation Pydantic v2) → `SettingsConfigDict`.
- 91 violações de lint `ruff` (W293, UP006/UP035/UP045, B905, E501, etc.) → 0.

## Validação
```bash
npm ci
npm run check                # typecheck + testes (16) + build
python3 -m pytest tests/ -q  # 20 testes
python3 -m ruff check agents core src/rag tests
bash scripts/validate-ventura-agents.sh
bash scripts/validate-community.sh
```

## Itens não executados localmente
- Docker build / `docker compose config` (Docker indisponível no ambiente de auditoria; validado no CI).
- SonarQube Cloud scan e Quality Gate (dependem de `SONAR_TOKEN`; fluxo em `docs/SONARQUBE.md`).
