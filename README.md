# ClickSeguro - ZAP Pipeline

Projeto para demonstrar testes de seguranca automatizados com **OWASP ZAP GitHub Actions**:
- Escaneia `http://localhost:8080`
- Gera relatorios (HTML/JSON)
- Falha automaticamente se houver **High** ou **Critical**
- Publica os relatorios como **artefatos** do workflow

## Requisitos locais
- Python 3.10+
- Docker (para executar o ZAP localmente, opcional)

## Rodando localmente

1) Instale dependencias:
```bash
pip install -r requirements.txt
```

2) Inicie a aplicacao:
```bash
python app.py
# acessa http://localhost:8080
```

3) (Opcional) Rode o ZAP via Docker e gere relatorios em `./zap-reports`:
```bash
mkdir zap-reports

docker run --rm -v "%cd%\zap-reports":/zap/wrk/:rw ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:8080 -r zap-report.html -J zap-report.json
```

## Como o CI funciona
O workflow `security-scan.yml`:
- Sobe a app em `localhost:8080` com validacao de status
- Executa ZAP (Docker) gerando relatorios HTML, JSON e Markdown
- Analisa o relatorio com script Python customizado
- Exibe estatisticas detalhadas (total, severidades, top vulnerabilidades)
- **Falha** o pipeline se detectar High ou Critical
- Publica todos os relatorios como artefato `zap-security-report`
- Para a aplicacao gracefully ao final

## Configuracao GitHub

### 1. Inicializar repositorio Git
```bash
git init
git add .
git commit -m "Pipeline seguranca OWASP ZAP"
```

### 2. Criar repositorio no GitHub
Criar novo repositorio chamado `cp_cyber` e fazer push:
```bash
git remote add origin https://github.com/SEU_USUARIO/cp_cyber.git
git branch -M main
git push -u origin main
```

### 3. Acessar relatorio
Apos execucao do pipeline:
- GitHub > Actions > Workflow executado
- Secao "Artifacts"
- Download "zap-security-report"

## Analise do relatorio
Abrir `zap-report.html` e identificar:
- Total de alertas
- Alertas por severidade (Informational, Low, Medium, High, Critical)
- Tipos de vulnerabilidades (XSS, SQL Injection, etc)

## Vulnerabilidade proposital
O endpoint `POST /login` reflete `username` **sem validacao ou escape**.
- Arquivo `app.py` contem XSS na linha 32:
```python
message = f"Tentativa de login com usuario: {username}"
```
- O ZAP costuma sinalizar entradas refletidas (p. ex., potenciais XSS) e endpoints sem protecao.
- Campo username sem sanitizacao permite injecao de scripts.

## Corrigir vulnerabilidade (apos analise)
Substituir linha 32 por:
```python
from markupsafe import escape
message = f"Tentativa de login com usuario: {escape(username)}"
```

## Estrutura do Projeto
```
cp_cyber/
├── .github/
│   └── workflows/
│       └── security-scan.yml
├── app.py
├── analyze_zap.py
├── requirements.txt
└── README.md
```

## Criterios de Falha do Pipeline
Pipeline falha se detectar:
- riskcode == 3 (High)
- riskcode == 4 (Critical)

## Artefatos Gerados
- zap-report.html (relatorio visual completo)
- zap-report.json (dados estruturados para parsing)
- zap-report.md (relatorio em Markdown)
- Artefato mantido por 30 dias no GitHub Actions

## Analise Automatica
Script `analyze_zap.py` fornece:
- Total de alertas encontrados
- Distribuicao por severidade
- Top 10 tipos de vulnerabilidades mais comuns
- Saida formatada para logs do GitHub Actions

## Observacoes
- Este projeto e **didatico**.
