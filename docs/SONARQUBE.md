# SonarQube Cloud — Integração

Análise contínua de qualidade e segurança para TypeScript + Python.

## Arquivos no repositório

| Arquivo | Função |
|---------|--------|
| `sonar-project.properties` | Chave do projeto, sources, coverage, exclusões |
| `.github/workflows/sonarqube.yml` | Scan em `main` e PRs + Quality Gate |

## Setup (uma vez)

### 1. Criar projeto no SonarQube Cloud

1. Acesse [https://sonarcloud.io](https://sonarcloud.io) e autentique com GitHub.
2. Importe o repositório **venturalabs-ai/ventura-agents**.
3. Confirme:
   - **Organization key:** `venturalabs-ai`
   - **Project key:** `venturalabs-ai_ventura-agents`

Se a org/key forem diferentes, atualize `sonar-project.properties`.

### 2. Gerar token

1. SonarQube Cloud → **My Account → Security**
2. **Generate token** (nome sugerido: `github-actions-ventura-agents`)
3. Copie o valor (só aparece uma vez)

### 3. Secret no GitHub

1. Repo → **Settings → Secrets and variables → Actions**
2. **New repository secret**
   - Name: `SONAR_TOKEN`
   - Value: token do passo 2

### 4. Validar

- Push em `main` ou abra um PR, ou
- **Actions → SonarQube → Run workflow**

O job deve:
1. Confirmar que `SONAR_TOKEN` existe
2. Rodar typecheck/testes
3. Executar o scanner
4. Avaliar o **Quality Gate**

## Branch protection (recomendado)

Em **Settings → Rules / Branches**, marque o check:

- `SonarQube Cloud Scan` (ou o nome do job no workflow)

como status check obrigatório em PRs para `main`.

## O que é analisado

- `src/` — plataforma TypeScript
- `agents/`, `core/` — fundação Python
- `tests/` — testes

Excluídos: `docs/`, `scripts/`, `node_modules/`, `dist/`, markdown.

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| Job falha em "Verify SONAR_TOKEN" | Secret ausente | Criar `SONAR_TOKEN` |
| Project not found | Key/org errados | Ajustar `sonar-project.properties` |
| Quality Gate failed | Issues novos / cobertura | Ver dashboard no SonarCloud |
| Analysis succeeds but no PR decoration | Permissões / app Sonar | Reinstalar app SonarQube Cloud no org |
