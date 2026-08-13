# Quality Gates personalizados — Ventura Agents

## Gate: **Ventura Production**

Fonte da verdade: `sonar/quality-gate.json`  
Aplicação automatizada: `scripts/apply_sonar_quality_gate.py` + workflow **Sonar Quality Gate Setup**.

### Condições

| Escopo | Métrica | Regra | Significado |
|--------|---------|-------|-------------|
| New code | Reliability rating | > 1 falha | Deve permanecer **A** |
| New code | Security rating | > 1 falha | Deve permanecer **A** |
| New code | Maintainability rating | > 1 falha | Deve permanecer **A** |
| New code | Coverage | < 60% falha | Cobertura mínima em código novo |
| New code | Duplicated lines | > 3% falha | Pouca duplicação |
| New code | Security hotspots reviewed | < 100% falha | Hotspots revisados |
| Overall | Security rating | > 1 falha | Security global **A** |
| Overall | Reliability rating | > 2 falha | Reliability global no máximo **B** |

Ratings Sonar: **1=A, 2=B, 3=C, 4=D, 5=E**. Operador `GT` com `error=1` = “pior que A”.

---

## Automação (criação do gate)

### GitHub Actions (recomendado)

Workflow: `.github/workflows/sonar-quality-gate-setup.yml`

Dispara quando:

- **Manual:** Actions → **Sonar Quality Gate Setup** → Run workflow
- **Automático:** push em `main` que altere `sonar/quality-gate.json` (ou o script/workflow)

Requisito: secret `SONAR_TOKEN` com permissão **Administer Quality Gates** na org SonarCloud.

### Local / CI genérico

```bash
export SONAR_TOKEN="seu-token"
python3 scripts/apply_sonar_quality_gate.py
# ou
bash scripts/setup-sonar-quality-gate.sh
```

O script:

1. Lê `sonar/quality-gate.json`
2. Cria o gate se não existir
3. Remove condições antigas e recria a partir do JSON (idempotente)
4. Associa o projeto `venturalabs-ai_ventura-agents`

### Fluxo completo

```text
sonar/quality-gate.json
        │
        ▼
apply_sonar_quality_gate.py  ──API──►  SonarCloud Quality Gate
        │
        ▼
sonarqube.yml (scan + quality-gate-action)  ──►  PR / main bloqueados se ERROR
```

---

## Exemplos de JSON

| Arquivo | Conteúdo |
|---------|----------|
| [quality-gate.json](../sonar/quality-gate.json) | Política real aplicada |
| [definition.example](../sonar/examples/quality-gate.definition.example.json) | Exemplo de definição |
| [api.example](../sonar/examples/api.create-condition.example.json) | Payloads API |
| [status.example](../sonar/examples/quality-gate.status.example.json) | Status OK / ERROR |

### Definição (resumo)

```json
{
  "name": "Ventura Production",
  "projectKey": "venturalabs-ai_ventura-agents",
  "organization": "venturalabs-ai",
  "conditions": [
    {
      "metric": "new_coverage",
      "op": "LT",
      "error": "60",
      "scope": "new_code"
    },
    {
      "metric": "new_security_rating",
      "op": "GT",
      "error": "1",
      "scope": "new_code"
    }
  ]
}
```

### Status ERROR (CI falha)

```json
{
  "projectStatus": {
    "status": "ERROR",
    "conditions": [
      {
        "status": "ERROR",
        "metricKey": "new_coverage",
        "comparator": "LT",
        "errorThreshold": "60",
        "actualValue": "41.2"
      }
    ]
  }
}
```

---

## UI manual (alternativa)

1. [sonarcloud.io](https://sonarcloud.io) → **Quality Gates** → **Create**
2. Nome: `Ventura Production`
3. Condições conforme a tabela
4. Associar o projeto

## CI de análise

`.github/workflows/sonarqube.yml` roda scan + **Quality Gate action** e falha o job se o gate estiver vermelho.

## Ajustar thresholds

1. Edite `sonar/quality-gate.json`
2. Merge em `main` → workflow **Sonar Quality Gate Setup** reaplica sozinho
3. Ou rode o workflow manualmente / script local

## Permissões

| Uso | Permissão no token |
|-----|--------------------|
| Criar/atualizar gate (setup) | **Administer Quality Gates** |
| Scan + ler status (CI Sonar) | **Execute Analysis** |
