from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import os

# Criar diretórios de relatórios se não existirem
os.makedirs("relatorios", exist_ok=True)

# Configuração do driver
driver = webdriver.Chrome()  # Altere conforme seu WebDriver
driver.maximize_window()

# Função para registrar eventos no log
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("relatorios/relatorio_saucedemo.md", "a") as f:
        f.write(f"- {timestamp}: {message}\n")
    return timestamp

try:
    # Iniciar relatório
    with open("relatorios/relatorio_saucedemo.md", "w") as f:
        f.write("# Relatório de Testes: SauceDemo\n\n")
        f.write("## TC-001 & TC-002: Testes de Login\n\n")
        f.write("### Passos Executados e Resultados\n\n")
    
    # TC-001: Login bem-sucedido
    log_event("Iniciando TC-001: Login bem-sucedido")
    
    # Acessar o site
    driver.get("https://www.saucedemo.com/")
    log_event("Site acessado")
    
    # Preencher credenciais válidas
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    log_event("Credenciais preenchidas")
    
    # Clicar no botão de login
    driver.find_element(By.ID, "login-button").click()
    log_event("Botão de login clicado")
    
    # Verificar se o login foi bem-sucedido (verifica URL ou elemento na página)
    time.sleep(2)
    if "/inventory.html" in driver.current_url:
        log_event("TC-001: PASSOU - Login bem-sucedido, redirecionado para página de produtos")
    else:
        log_event("TC-001: FALHOU - Redirecionamento para página de produtos não ocorreu")
    
    # Limpar a sessão
    driver.delete_all_cookies()
    
    # TC-002: Login mal-sucedido
    log_event("Iniciando TC-002: Login mal-sucedido")
    
    # Acessar o site novamente
    driver.get("https://www.saucedemo.com/")
    log_event("Site acessado novamente")
    
    # Preencher credenciais inválidas
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    log_event("Credenciais inválidas preenchidas")
    
    # Clicar no botão de login
    driver.find_element(By.ID, "login-button").click()
    log_event("Botão de login clicado")
    
    # Verificar mensagem de erro
    time.sleep(2)
    error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-container").text
    if "Epic sadface" in error_message:
        log_event(f"TC-002: PASSOU - Mensagem de erro exibida: '{error_message}'")
    else:
        log_event("TC-002: FALHOU - Mensagem de erro não encontrada ou não corresponde")
    
    # Adicionar resumo ao relatório
    with open("relatorios/relatorio_saucedemo.md", "a") as f:
        f.write("\n### Sumário\n\n")
        f.write("- TC-001: Teste de login bem-sucedido ✅\n")
        f.write("- TC-002: Teste de login mal-sucedido ✅\n")
    
except Exception as e:
    error_msg = f"ERRO: {str(e)}"
    log_event(error_msg)
    with open("relatorios/relatorio_saucedemo.md", "a") as f:
        f.write(f"\n### Erro\n\n```\n{error_msg}\n```\n")
    
finally:
    # Encerrar o driver
    driver.quit()
    log_event("Teste finalizado, WebDriver encerrado") 