from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os

# Criar diretórios de relatórios se não existirem
os.makedirs("relatorios", exist_ok=True)

# Configuração do driver
driver = webdriver.Chrome()
driver.maximize_window()

# Função para registrar eventos no log
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("relatorios/relatorio_dynamic_loading.md", "a") as f:
        f.write(f"- {timestamp}: {message}\n")
    return timestamp

try:
    # Iniciar relatório
    with open("relatorios/relatorio_dynamic_loading.md", "w") as f:
        f.write("# Relatório de Teste: Herokuapp Dynamic Loading\n\n")
        f.write("## TC-003: Teste de Carregamento Dinâmico\n\n")
        f.write("### Objetivo\n")
        f.write("Verificar o comportamento de elementos com carregamento dinâmico e a funcionalidade de espera explícita.\n\n")
        f.write("### Passos Executados e Resultados\n\n")
    
    # TC-003: Teste de carregamento dinâmico
    start_time = log_event("Iniciando TC-003: Teste de carregamento dinâmico")
    
    # Acessar o site
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    log_event("Site acessado: https://the-internet.herokuapp.com/dynamic_loading/1")
    
    # Clicar no botão Start
    start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
    start_button.click()
    log_event("Botão Start clicado")
    
    # Registrar início da espera
    wait_start = datetime.now()
    
    try:
        # Configurar espera explícita (máximo 30 segundos)
        wait = WebDriverWait(driver, 30)
        # Aguardar até que o texto "Hello World!" esteja visível
        hello_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(), 'Hello World!')]"))
        )
        
        # Calcular tempo de espera
        wait_end = datetime.now()
        wait_duration = (wait_end - wait_start).total_seconds()
        
        # Verificar se o elemento contém o texto esperado
        if hello_element.text == "Hello World!":
            result_msg = f"TC-003: PASSOU - Texto 'Hello World!' encontrado após {wait_duration:.2f} segundos"
            log_event(result_msg)
        else:
            result_msg = f"TC-003: FALHOU - Texto encontrado '{hello_element.text}' não corresponde ao esperado"
            log_event(result_msg)
            
    except Exception as wait_error:
        wait_duration = (datetime.now() - wait_start).total_seconds()
        result_msg = f"TC-003: FALHOU - Timeout após {wait_duration:.2f} segundos: {str(wait_error)}"
        log_event(result_msg)
    
    # Adicionar resumo ao relatório
    with open("relatorios/relatorio_dynamic_loading.md", "a") as f:
        f.write("\n### Sumário\n\n")
        if "PASSOU" in result_msg:
            f.write("- TC-003: Teste de carregamento dinâmico ✅\n")
            f.write(f"- Tempo de carregamento: {wait_duration:.2f} segundos\n")
        else:
            f.write("- TC-003: Teste de carregamento dinâmico ❌\n")
            f.write(f"- Erro: {result_msg}\n")
    
except Exception as e:
    error_msg = f"ERRO: {str(e)}"
    log_event(error_msg)
    with open("relatorios/relatorio_dynamic_loading.md", "a") as f:
        f.write(f"\n### Erro\n\n```\n{error_msg}\n```\n")
    
finally:
    # Encerrar o driver
    driver.quit()
    log_event("Teste finalizado, WebDriver encerrado") 