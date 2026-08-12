# Contributing to Ventura Agents Ecosystem

Obrigado pelo interesse em contribuir com o ecossistema Ventura!

Este repositório contém a fundação técnica (TypeScript + Python) e a documentação dos 76 agentes.

## Fluxo de trabalho

1. **Crie uma branch** a partir de `main`:
   ```bash
   git checkout -b feature/sua-feature
   # ou
   git checkout -b fix/descricao-do-bug
   ```

2. **Faça suas alterações** seguindo os padrões abaixo.

3. **Rode os checks localmente**:
   ```bash
   npm run check          # TypeScript: typecheck + tests + build
   # Python (quando aplicável)
   ruff check .
   pytest
   ```

4. **Abra um Pull Request** para `main`.
   - Título claro e descritivo
   - Descreva o problema e a solução
   - Referencie issues relacionadas

5. Aguarde o CI passar e a revisão.

## Padrões de código

### TypeScript
- Node ≥ 20
- `npm run typecheck` e `npm test` devem passar
- Prefira tipagem explícita e evite `any`

### Python
- Python ≥ 3.12
- Use `ruff` para lint/format
- Type hints obrigatórios
- Testes com `pytest` + `pytest-asyncio`

### Commits
Preferimos mensagens no estilo Conventional Commits:

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `chore:` manutenção, configs, CI
- `refactor:` refatoração sem mudança de comportamento
- `test:` testes

## Estrutura importante

```
agents/base/agent.py   → Classe base Python dos agentes
core/config.py         → Configurações centralizadas
src/                   → Fundação TypeScript (catálogo, platform, context-proxy)
docs/                  → Documentação e ADRs
.github/workflows/     → CI/CD
```

## Code of Conduct

Esperamos que todos os contribuidores mantenham um ambiente profissional e respeitoso.

## Dúvidas?

Abra uma issue ou entre em contato: dev@venturalabs.ai
