#!/usr/bin/env python3
import json
import sys
from collections import Counter

def analyze_zap_report(json_file):
    """Analisa o relatorio JSON do OWASP ZAP"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        all_alerts = []
        for site in data.get('site', []):
            all_alerts.extend(site.get('alerts', []))
        
        # Contadores
        severity_map = {
            '0': 'Informational',
            '1': 'Low',
            '2': 'Medium',
            '3': 'High',
            '4': 'Critical'
        }
        
        severity_counts = Counter()
        vuln_types = Counter()
        
        for alert in all_alerts:
            risk = alert.get('riskcode', '0')
            severity_counts[severity_map.get(risk, 'Unknown')] += 1
            vuln_types[alert.get('name', 'Unknown')] += 1
        
        # Resultados
        print("=" * 60)
        print("ANALISE COMPLETA DO RELATORIO OWASP ZAP")
        print("=" * 60)
        print(f"\nTotal de alertas encontrados: {len(all_alerts)}")
        
        print("\nAlertas por severidade:")
        for severity in ['Critical', 'High', 'Medium', 'Low', 'Informational']:
            count = severity_counts.get(severity, 0)
            print(f"  {severity:15s}: {count}")
        
        print("\nTop 10 tipos de vulnerabilidades mais comuns:")
        for vuln_type, count in vuln_types.most_common(10):
            print(f"  {count:3d}x - {vuln_type}")
        
        print("\n" + "=" * 60)
        
        # Retorna codigo de saida baseado em severidade
        high_count = severity_counts.get('High', 0)
        critical_count = severity_counts.get('Critical', 0)
        
        if critical_count > 0 or high_count > 0:
            print(f"\nFALHA: Encontradas {high_count} High e {critical_count} Critical")
            return 1
        
        print("\nSUCESSO: Nenhuma vulnerabilidade critica detectada")
        return 0
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo {json_file} nao encontrado")
        return 2
    except json.JSONDecodeError:
        print(f"ERRO: Arquivo {json_file} nao e um JSON valido")
        return 2
    except Exception as e:
        print(f"ERRO: {str(e)}")
        return 2

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python analyze_zap.py <caminho_para_zap-report.json>")
        sys.exit(2)
    
    exit_code = analyze_zap_report(sys.argv[1])
    sys.exit(exit_code)
