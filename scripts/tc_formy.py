from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"- {timestamp}: {message}\n")
    return timestamp

# Função para registrar valores selecionados
def register_field(field_name, value):
    msg = f"Campo '{field_name}': '{value}'"
    log_event(msg)
    return msg

try:
    # Iniciar relatório
    with open("relatorios/relatorio_formy.md", "w") as f:
        f.write("# Relatório de Teste: Formy\n\n")
        f.write("## TC-005: Teste de Preenchimento de Formulário\n\n")
        f.write("### Objetivo\n")
        f.write("Verificar a funcionalidade de preenchimento e submissão de um formulário com diferentes tipos de campos.\n\n")
        f.write("### Dados de Entrada\n\n")
        f.write("| Campo | Valor |\n")
        f.write("|-------|-------|\n")
    
    # TC-005: Preenchimento de formulário
    log_event("Iniciando TC-005: Teste de preenchimento de formulário")
    
    # Acessar o site
    driver.get("https://formy-project.herokuapp.com/form")
    log_event("Site acessado: https://formy-project.herokuapp.com/form")
    
    # Aguardar carregamento do formulário
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "first-name")))
    
    # Preencher campos de texto
    first_name = "Maria"
    driver.find_element(By.ID, "first-name").send_keys(first_name)
    register_field("Primeiro Nome", first_name)
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"| Primeiro Nome | {first_name} |\n")
    
    last_name = "Silva"
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    register_field("Sobrenome", last_name)
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"| Sobrenome | {last_name} |\n")
    
    job_title = "QA Engineer"
    driver.find_element(By.ID, "job-title").send_keys(job_title)
    register_field("Cargo", job_title)
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"| Cargo | {job_title} |\n")
    
    # Selecionar nível de educação (radio button)
    education = "College"
    driver.find_element(By.ID, "radio-button-2").click()
    register_field("Educação", education)
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"| Educação | {education} |\n")
    
    # Selecionar gênero (checkbox)
    gender = "Female"
    driver.find_element(By.ID, "checkbox-2").click()
    register_field("Gênero", gender)
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"| Gênero | {gender} |\n")
    
    # Selecionar experiência (dropdown)
    experience_dropdown = Select(driver.find_element(By.ID, "select-menu"))
    experience = "5-9"
    experience_dropdown.select_by_visible_text(experience + " years")
    register_field("Experiência", experience + " years")
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"| Experiência | {experience} years |\n")
    
    # Selecionar data
    date = "04/27/2025"
    driver.find_element(By.ID, "datepicker").send_keys(date)
    register_field("Data", date)
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"| Data | {date} |\n")
    
    # Adicionar à seção Passos Executados
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write("\n### Passos Executados e Resultados\n\n")
    
    # Submeter o formulário
    submit_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-primary")
    submit_button.click()
    log_event("Formulário submetido")
    
    # Verificar confirmação
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success")))
    success_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-success").text
    
    if "The form was successfully submitted!" in success_message:
        result_msg = f"TC-005: PASSOU - Formulário enviado com sucesso: '{success_message}'"
        log_event(result_msg)
        # Adicionar resumo ao relatório
        with open("relatorios/relatorio_formy.md", "a") as f:
            f.write("\n### Confirmação\n\n")
            f.write(f"- Mensagem de confirmação: \"{success_message}\"\n")
            f.write("\n### Sumário\n\n")
            f.write("- TC-005: Teste de preenchimento de formulário ✅\n")
    else:
        result_msg = f"TC-005: FALHOU - Mensagem de sucesso não encontrada"
        log_event(result_msg)
        # Adicionar resumo ao relatório
        with open("relatorios/relatorio_formy.md", "a") as f:
            f.write("\n### Sumário\n\n")
            f.write("- TC-005: Teste de preenchimento de formulário ❌\n")
            f.write(f"- Erro: Mensagem de confirmação não encontrada\n")
    
except Exception as e:
    error_msg = f"ERRO: {str(e)}"
    log_event(error_msg)
    with open("relatorios/relatorio_formy.md", "a") as f:
        f.write(f"\n### Erro\n\n```\n{error_msg}\n```\n")
    
finally:
    # Encerrar o driver
    driver.quit()
    log_event("Teste finalizado, WebDriver encerrado") 