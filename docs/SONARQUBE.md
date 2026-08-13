# SonarQube Cloud — Integração

Análise contínua de qualidade e segurança para TypeScript + Python.

## Arquivos no repositório

| Arquivo | Função |
|---------|--------|
| `sonar-project.properties` | Chave do projeto, sources, coverage, exclusões, `qualitygate.wait` |
| `.github/workflows/sonarqube.yml` | Scan em `main` e PRs + Quality Gate action |
| `sonar/quality-gate.json` | Política do gate **Ventura Production** |
| `scripts/setup-sonar-quality-gate.sh` | Cria gate + condições + associa projeto via API |
| `docs/QUALITY_GATES.md` | Detalhes das condições e como ajustar |

## Setup (uma vez)

### 1. Criar projeto no SonarQube Cloud

1. Acesse [https://sonarcloud.io](https://sonarcloud.io) e autentique com GitHub.
2. Importe o repositório **venturalabs-ai/ventura-agents**.
3. Confirme:
   - **Organization key:** `venturalabs-ai`
   - **Project key:** `venturalabs-ai_ventura-agents`

### 2. Gerar token

1. SonarQube Cloud → **My Account → Security**
2. **Generate token** (nome sugerido: `github-actions-ventura-agents`)
3. Copie o valor (só aparece uma vez)

### 3. Secret no GitHub

1. Repo → **Settings → Secrets and variables → Actions**
2. **New repository secret**
   - Name: `SONAR_TOKEN`
   - Value: token do passo 2

### 4. Quality Gate personalizado

```bash
export SONAR_TOKEN="seu-token"  # idealmente com Administer Quality Gates
bash scripts/setup-sonar-quality-gate.sh
```

Isso cria o gate **Ventura Production** e associa ao projeto.  
Detalhes: [QUALITY_GATES.md](QUALITY_GATES.md).

### 5. Validar

- **Actions → SonarQube → Run workflow**

O job deve confirmar o token, analisar o código e **falhar se o Quality Gate estiver vermelho**.

## Branch protection (recomendado)

Marque o check `SonarQube Cloud Scan` como obrigatório em PRs para `main`.

## O que é analisado

- `src/` — plataforma TypeScript
- `agents/`, `core/` — fundação Python
- `tests/` — testes

Excluídos: `docs/`, `scripts/`, `sonar/`, `node_modules/`, `dist/`, markdown.

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| Job falha em "Verify SONAR_TOKEN" | Secret ausente | Criar `SONAR_TOKEN` |
| Project not found | Key/org errados | Ajustar `sonar-project.properties` |
| Quality Gate failed | Issues / cobertura new code | Dashboard SonarCloud + [QUALITY_GATES.md](QUALITY_GATES.md) |
| Script setup-sonar falha | Token sem Administer Quality Gates | Gerar token com permissão na org |
| Analysis ok, sem PR decoration | App SonarCloud | Reinstalar integração GitHub na org |
