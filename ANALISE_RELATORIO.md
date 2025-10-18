# Guia de Analise do Relatorio ZAP

## Acessar Relatorio no GitHub Actions

1. Va para: `https://github.com/SEU_USUARIO/cp_cyber/actions`
2. Clique no workflow mais recente
3. Role ate "Artifacts"
4. Baixe `zap-security-report`
5. Extraia os arquivos

## Formatos de Relatorio

### zap-report.html
Relatorio visual completo com:
- Lista de todas as vulnerabilidades
- Descricao detalhada de cada alerta
- Severidade e nivel de confianca
- URLs afetadas
- Solucoes recomendadas

### zap-report.json
Dados estruturados contendo:
```json
{
  "site": [{
    "alerts": [{
      "name": "Nome da Vulnerabilidade",
      "riskcode": "3",
      "riskdesc": "High",
      "desc": "Descricao detalhada",
      "solution": "Como corrigir"
    }]
  }]
}
```

Codigos de risco:
- 0 = Informational
- 1 = Low
- 2 = Medium
- 3 = High
- 4 = Critical

### zap-report.md
Relatorio em Markdown para documentacao.

## Analise Local com Script Python

Execute o script de analise:
```bash
python analyze_zap.py zap-reports/zap-report.json
```

Saida esperada:
```
============================================================
ANALISE COMPLETA DO RELATORIO OWASP ZAP
============================================================

Total de alertas encontrados: 15

Alertas por severidade:
  Critical       : 0
  High           : 2
  Medium         : 5
  Low            : 6
  Informational  : 2

Top 10 tipos de vulnerabilidades mais comuns:
    5x - Cross Site Scripting (Reflected)
    3x - Missing Anti-clickjacking Header
    2x - X-Content-Type-Options Header Missing
    2x - Cookie No HttpOnly Flag
    1x - Server Leaks Version Information
    1x - X-Frame-Options Header Not Set
    1x - Absence of Anti-CSRF Tokens
```

## Tipos Comuns de Vulnerabilidades

### XSS (Cross-Site Scripting)
- **Severidade**: High/Medium
- **Causa**: Entrada de usuario refletida sem sanitizacao
- **Solucao**: Usar escape/sanitizacao (ex: `markupsafe.escape()`)

### Missing Security Headers
- **Severidade**: Low/Medium
- **Headers importantes**: X-Frame-Options, X-Content-Type-Options, CSP
- **Solucao**: Adicionar headers de seguranca na resposta HTTP

### Cookie Flags
- **Severidade**: Low/Medium
- **Problema**: Cookies sem HttpOnly ou Secure flags
- **Solucao**: Configurar flags adequados nos cookies

## Criterios de Aprovacao

Pipeline PASSA se:
- High = 0
- Critical = 0

Pipeline FALHA se:
- High > 0 OU Critical > 0

## Proximos Passos

1. Analisar cada vulnerabilidade High/Critical
2. Implementar correcoes no codigo
3. Fazer commit das alteracoes
4. Verificar se pipeline passa
5. Revisar vulnerabilidades Medium/Low (opcional mas recomendado)
