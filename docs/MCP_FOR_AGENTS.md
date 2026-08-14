# Explorar MCP (Model Context Protocol) para Agentes

## O que é MCP?

O **Model Context Protocol (MCP)** é um protocolo aberto para conectar modelos de linguagem a ferramentas, dados e contextos externos de forma padronizada e segura.

No ecossistema Ventura Global Agents V3.0, o MCP é usado para:

- Comunicação entre os 76 agentes (meta-orchestrator ↔ agentes especializados)
- Acesso a tools (GitHub, bancos, ERP, APIs fiscais, etc.)
- Compartilhamento de contexto comprimido (Context Proxy)
- Evidências e audit trail

## Por que MCP no Ventura?

1. **Padronização** — Todos os agentes falam a mesma "língua" de tools e resources
2. **Segurança** — Scopes e permissões por agente (A0-A4)
3. **Observabilidade** — Toda chamada MCP é logada no OpenTelemetry
4. **Extensibilidade** — Novas skills e connectors são plugins MCP

## Arquitetura MCP no Ecossistema

```
ventura.ia-governanca (Meta)
        │ MCP Server / Client
        │
   ┌─────────────────────────────────┐
   │  Specialized Agents (76)         │
   │  (cada um é um MCP Client)       │
   └─────────────────────────────────┘
        │
        │ MCP Tools / Resources
        │
   Tools: GitHub, SAP, SPED, ChromaDB, Redis, etc.
```

## Como usar no código

Os agentes usam MCP para:

- `tools/list` e `tools/call` — invocar ferramentas permitidas pelo `tool_profile`
- `resources/read` — ler políticas, evidências e knowledge base
- `prompts/get` — obter o Prompt Híbrido Universal personalizado

## Próximos passos de implementação

1. Registrar cada agente como MCP Client com seu `autonomy_level`
2. Expor o Context Proxy como MCP Resource
3. Expor o RAG Pipeline (ChromaDB) como MCP Tool
4. Usar MCP para dual-approval (A4) e audit trail

## Referências

- Spec oficial: https://modelcontextprotocol.io
- No Ventura: integrado via Context Proxy + Orchestration Layer

**Status:** Explorado e arquitetado no V3.0 ✅
