import os
import subprocess
import time
from datetime import datetime

# Criar estrutura de diretórios
os.makedirs("drivers", exist_ok=True)
os.makedirs("scripts", exist_ok=True)
os.makedirs("relatorios", exist_ok=True)

# Função para registrar eventos no log
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("relatorios/relatorio_geral.md", "a") as f:
        f.write(f"- {timestamp}: {message}\n")
    return timestamp

# Iniciar relatório geral
with open("relatorios/relatorio_geral.md", "w") as f:
    f.write("# Relatório Geral de Testes Automatizados\n\n")
    f.write(f"Data de execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
    f.write("## Casos de Teste Executados\n\n")

test_scripts = [
    {"file": "scripts/tc_saucedemo.py", "name": "TC-001 & TC-002: SauceDemo (Login)"},
    {"file": "scripts/tc_dynamic_loading.py", "name": "TC-003: Dynamic Loading (Herokuapp)"},
    {"file": "scripts/tc_demoblaze.py", "name": "TC-004: DemoBlaze (Simulação de Compra)"},
    {"file": "scripts/tc_formy.py", "name": "TC-005: Formy (Preenchimento de Formulário)"}
]

# Executar cada script de teste
for test in test_scripts:
    log_event(f"Iniciando execução do teste: {test['name']}")
    
    try:
        # Executar o script Python
        process = subprocess.run(["python3", test["file"]], capture_output=True, text=True)
        
        # Verificar se o script foi executado com sucesso
        if process.returncode == 0:
            log_event(f"Teste {test['name']} concluído com sucesso!")
        else:
            log_event(f"Teste {test['name']} falhou com código de saída {process.returncode}")
            log_event(f"Erro: {process.stderr}")
            
        # Aguardar um momento antes de iniciar o próximo teste
        time.sleep(2)
        
    except Exception as e:
        log_event(f"Erro ao executar {test['name']}: {str(e)}")

# Finalizar o relatório
with open("relatorios/relatorio_geral.md", "a") as f:
    f.write("\n## Sumário dos Resultados\n\n")
    
    # Verificar resultados de cada relatório individual
    for test in test_scripts:
        report_file = test["file"].replace("scripts/tc_", "relatorios/relatorio_").replace(".py", ".md")
        test_name = test["name"]
        
        try:
            with open(report_file, "r") as report:
                content = report.read()
                if "PASSOU" in content and not "FALHOU" in content:
                    result = "✅ PASSOU"
                elif "FALHOU" in content:
                    result = "❌ FALHOU"
                else:
                    result = "⚠️ INCONCLUSIVO"
                
                f.write(f"- {test_name}: {result}\n")
        except:
            f.write(f"- {test_name}: ❓ RELATÓRIO NÃO ENCONTRADO\n")
    
    f.write("\n## Próximos Passos\n\n")
    f.write("1. Revisar os casos de teste que falharam\n")
    f.write("2. Corrigir eventuais problemas de implementação\n")
    f.write("3. Adicionar novos casos de teste conforme necessário\n")

log_event("Execução de todos os testes concluída!")
print("\nRelatórios detalhados disponíveis no diretório 'relatorios/'")
print("Para visualizar o relatório geral: 'relatorios/relatorio_geral.md'") 