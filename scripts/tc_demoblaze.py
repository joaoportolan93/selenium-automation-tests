from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os
import re

# Criar diretórios de relatórios se não existirem
os.makedirs("relatorios", exist_ok=True)

# Configuração do driver
driver = webdriver.Chrome()
driver.maximize_window()

# Função para registrar eventos no log
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("relatorios/relatorio_demoblaze.md", "a") as f:
        f.write(f"- {timestamp}: {message}\n")
    return timestamp

try:
    # Iniciar relatório
    with open("relatorios/relatorio_demoblaze.md", "w") as f:
        f.write("# Relatório de Teste: DemoBlaze\n\n")
        f.write("## TC-004: Simulação de Compra\n\n")
        f.write("### Objetivo\n")
        f.write("Verificar o fluxo completo de compra, desde a seleção do produto até a confirmação do pedido.\n\n")
        f.write("### Passos Executados e Resultados\n\n")
    
    # TC-004: Simulação de compra
    log_event("Iniciando TC-004: Simulação de compra")
    
    # Acessar o site
    driver.get("https://www.demoblaze.com/")
    log_event("Site acessado: https://www.demoblaze.com/")
    
    # Esperar que a página carregue
    wait = WebDriverWait(driver, 10)
    
    # Escolher um produto (primeiro da lista)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card-title a")))
    produto = driver.find_element(By.CSS_SELECTOR, ".card-title a")
    nome_produto = produto.text
    produto.click()
    log_event(f"Produto selecionado: {nome_produto}")
    
    # Adicionar ao carrinho
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-success")))
    add_to_cart = driver.find_element(By.CSS_SELECTOR, ".btn-success")
    add_to_cart.click()
    log_event("Botão 'Add to cart' clicado")
    
    # Lidar com o alerta JavaScript
    try:
        # Esperar até que o alerta esteja presente
        wait.until(EC.alert_is_present())
        # Alternar para o alerta e aceitá-lo
        alert = driver.switch_to.alert
        alert.accept()
        log_event("Alerta aceito")
    except:
        log_event("Nenhum alerta detectado")
    
    # Ir para o carrinho
    time.sleep(1)  # Pausa para garantir que o alerta foi processado
    cart_link = driver.find_element(By.ID, "cartur")
    cart_link.click()
    log_event("Navegou para o carrinho")
    
    # Verificar se o produto está no carrinho
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".success")))
    produtos_no_carrinho = driver.find_elements(By.CSS_SELECTOR, ".success td:nth-child(2)")
    produto_encontrado = any(nome_produto in p.text for p in produtos_no_carrinho)
    
    if produto_encontrado:
        log_event(f"Produto '{nome_produto}' encontrado no carrinho")
    else:
        log_event(f"ERRO: Produto '{nome_produto}' não encontrado no carrinho")
    
    # Clicar em Place Order
    place_order = driver.find_element(By.CSS_SELECTOR, ".btn-success")
    place_order.click()
    log_event("Botão 'Place Order' clicado")
    
    # Preencher formulário de pedido
    wait.until(EC.visibility_of_element_located((By.ID, "name")))
    driver.find_element(By.ID, "name").send_keys("Cliente Teste")
    driver.find_element(By.ID, "country").send_keys("Brasil")
    driver.find_element(By.ID, "city").send_keys("São Paulo")
    driver.find_element(By.ID, "card").send_keys("1234567890123456")
    driver.find_element(By.ID, "month").send_keys("12")
    driver.find_element(By.ID, "year").send_keys("2025")
    log_event("Formulário de pedido preenchido")
    
    # Confirmar compra
    driver.find_element(By.CSS_SELECTOR, "#orderModal .btn-primary").click()
    log_event("Botão de confirmação clicado")
    
    # Verificar confirmação de compra
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sweet-alert h2")))
    confirmation_message = driver.find_element(By.CSS_SELECTOR, ".sweet-alert h2").text
    
    if "Thank you" in confirmation_message:
        # Capturar detalhes da compra
        details = driver.find_element(By.CSS_SELECTOR, ".sweet-alert p.lead").text
        log_event(f"TC-004: PASSOU - Compra confirmada: '{confirmation_message}'")
        log_event(f"Detalhes: {details}")
        
        # Extrair ID do pedido e valor (se disponível)
        id_match = re.search(r"Id: (\d+)", details)
        amount_match = re.search(r"Amount: (\d+) USD", details)
        
        if id_match and amount_match:
            order_id = id_match.group(1)
            amount = amount_match.group(1)
            log_event(f"ID do Pedido: {order_id}, Valor: {amount} USD")
            
            # Adicionar resumo ao relatório
            with open("relatorios/relatorio_demoblaze.md", "a") as f:
                f.write("\n### Resultado da Compra\n\n")
                f.write(f"- Produto: {nome_produto}\n")
                f.write(f"- ID do Pedido: {order_id}\n")
                f.write(f"- Valor: {amount} USD\n")
                f.write(f"- Mensagem: {confirmation_message}\n")
                f.write("\n### Sumário\n\n")
                f.write("- TC-004: Simulação de compra ✅\n")
    else:
        log_event("TC-004: FALHOU - Confirmação de compra não encontrada")
        # Adicionar resumo ao relatório
        with open("relatorios/relatorio_demoblaze.md", "a") as f:
            f.write("\n### Sumário\n\n")
            f.write("- TC-004: Simulação de compra ❌\n")
            f.write(f"- Erro: Confirmação de compra não encontrada\n")
    
except Exception as e:
    error_msg = f"ERRO: {str(e)}"
    log_event(error_msg)
    with open("relatorios/relatorio_demoblaze.md", "a") as f:
        f.write(f"\n### Erro\n\n```\n{error_msg}\n```\n")
    
finally:
    # Encerrar o driver
    driver.quit()
    log_event("Teste finalizado, WebDriver encerrado") 