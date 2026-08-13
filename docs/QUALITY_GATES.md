# Quality Gates personalizados — Ventura Agents

## Gate: **Ventura Production**

Definido em `sonar/quality-gate.json` e aplicado via API com `scripts/setup-sonar-quality-gate.sh`.

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

### Por que esses valores?

- Foco em **new code** (padrão Sonar “clean as you code”).
- Coverage 60% em new code é realista enquanto a suíte cresce; suba para 80% quando os testes estiverem maduros.
- Security overall em A evita regressão de vulnerabilidades no baseline.

---

## Exemplos de JSON

Arquivos em `sonar/examples/`:

| Arquivo | Conteúdo |
|---------|----------|
| [quality-gate.definition.example.json](../sonar/examples/quality-gate.definition.example.json) | Definição completa do gate |
| [api.create-condition.example.json](../sonar/examples/api.create-condition.example.json) | Payloads da API `create_condition` / `select` |
| [quality-gate.status.example.json](../sonar/examples/quality-gate.status.example.json) | Resposta de status OK e ERROR |

### 1. Definição do gate (resumo)

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
      "scope": "new_code",
      "meaning": "Cobertura de new code deve ser >= 60%"
    },
    {
      "metric": "new_security_rating",
      "op": "GT",
      "error": "1",
      "scope": "new_code",
      "meaning": "Security em new code deve ser A"
    }
  ]
}
```

### 2. Criar condição via API (conceito)

```json
{
  "endpoint": "POST https://sonarcloud.io/api/qualitygates/create_condition",
  "form": {
    "gateName": "Ventura Production",
    "organization": "venturalabs-ai",
    "metric": "new_coverage",
    "op": "LT",
    "error": "60"
  }
}
```

Associar ao projeto:

```json
{
  "endpoint": "POST https://sonarcloud.io/api/qualitygates/select",
  "form": {
    "projectKey": "venturalabs-ai_ventura-agents",
    "gateName": "Ventura Production",
    "organization": "venturalabs-ai"
  }
}
```

### 3. Status do Quality Gate (OK)

```json
{
  "projectStatus": {
    "status": "OK",
    "conditions": [
      {
        "status": "OK",
        "metricKey": "new_coverage",
        "comparator": "LT",
        "errorThreshold": "60",
        "actualValue": "72.5"
      }
    ]
  }
}
```

### 4. Status com falha (ERROR → CI vermelho)

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

Quando `status` é `ERROR`, o step **SonarQube Quality Gate** no GitHub Actions falha.

---

## Aplicar no SonarQube Cloud

### Opção A — Script (recomendado)

```bash
export SONAR_TOKEN="seu-token"   # precisa de Administer Quality Gates na org
bash scripts/setup-sonar-quality-gate.sh
```

O script:

1. Cria o gate `Ventura Production` (se não existir)
2. Recria as condições de forma idempotente
3. Associa ao projeto `venturalabs-ai_ventura-agents`

### Opção B — UI

1. [sonarcloud.io](https://sonarcloud.io) → sua org → **Quality Gates** → **Create**
2. Nome: `Ventura Production`
3. **Add Condition** conforme a tabela acima
4. Em **Projects**, associe `ventura-agents`

## CI

O workflow `.github/workflows/sonarqube.yml` já:

1. Roda o scan
2. Espera o **Quality Gate** (`sonarqube-quality-gate-action`)
3. **Falha o job** se o gate estiver vermelho

Com `sonar.qualitygate.wait=true` em `sonar-project.properties`, o scanner também aguarda o resultado quando suportado.

## Ajustar thresholds

1. Edite `sonar/quality-gate.json` e os exemplos em `sonar/examples/`
2. Ajuste `scripts/setup-sonar-quality-gate.sh`
3. Rode o script de novo

## Permissões

O token do script precisa de **Administer Quality Gates** na organização SonarCloud.  
O `SONAR_TOKEN` do GitHub Actions precisa de **Execute Analysis** (e leitura do status do gate do projeto).
