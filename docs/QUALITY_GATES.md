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
5. Ou no projeto: **Quality Gate → Use a specific quality gate**

## CI

O workflow `.github/workflows/sonarqube.yml` já:

1. Roda o scan
2. Espera o **Quality Gate** (`sonarqube-quality-gate-action`)
3. **Falha o job** se o gate estiver vermelho

Com `sonar.qualitygate.wait=true` em `sonar-project.properties`, o scanner também aguarda o resultado quando suportado.

## Ajustar thresholds

1. Edite `sonar/quality-gate.json` (documentação da política)
2. Ajuste as chamadas `add_condition` em `scripts/setup-sonar-quality-gate.sh`
3. Rode o script de novo
4. Ou altere no UI e mantenha o JSON alinhado

## Permissões

O token usado no script precisa de **Administer Quality Gates** na organização SonarCloud.  
O token do GitHub Actions (`SONAR_TOKEN`) precisa ao menos de **Execute Analysis**; para o quality gate action, o token de análise costuma bastar para *ler* o status do gate do projeto.
