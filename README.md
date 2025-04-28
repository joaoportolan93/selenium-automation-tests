# Automação de Testes com Selenium

Este projeto contém scripts de automação de testes utilizando Selenium WebDriver com Python para quatro diferentes sites de demonstração, com foco em diferentes aspectos de automação.

## Estrutura do Projeto

```
.
├── drivers/                # Diretório para WebDrivers
├── scripts/                # Scripts de casos de teste
│   ├── tc_saucedemo.py     # TC-001 e TC-002: Testes de Login
│   ├── tc_dynamic_loading.py # TC-003: Teste de Carregamento Dinâmico
│   ├── tc_demoblaze.py     # TC-004: Simulação de Compra
│   └── tc_formy.py         # TC-005: Teste de Formulário
├── relatorios/             # Relatórios de testes
├── run_all_tests.py        # Script para executar todos os testes
└── README.md               # Este arquivo
```

## Pré-requisitos

- Python 3.7 ou superior
- Selenium WebDriver
- Google Chrome e ChromeDriver
- WebDrivers correspondentes a outros navegadores, se desejado

### Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install selenium
```

3. Baixe o ChromeDriver correspondente à sua versão do Chrome e coloque no diretório "drivers" ou no PATH do sistema

## Casos de Teste

### TC-001 e TC-002: SauceDemo (Login)
- TC-001: Teste de login bem-sucedido com credenciais válidas
- TC-002: Teste de login mal-sucedido com credenciais inválidas

### TC-003: Herokuapp Dynamic Loading
- Teste de carregamento dinâmico com espera explícita

### TC-004: DemoBlaze (Simulação de Compra)
- Simulação de fluxo completo de compra (escolher produto, adicionar ao carrinho, finalizar compra)

### TC-005: Formy (Preenchimento de Formulário)
- Teste de preenchimento de formulário com diferentes tipos de campos

## Execução dos Testes

Para executar todos os testes sequencialmente:

```bash
python run_all_tests.py
```

Para executar um teste específico:

```bash
python scripts/tc_saucedemo.py
```

## Relatórios

Após a execução, os relatórios detalhados serão gerados no diretório "relatorios". Cada teste gera seu próprio relatório em formato Markdown, e um relatório geral é criado consolidando todos os resultados.

## Melhores Práticas Implementadas

- Estrutura organizada e modular
- Tratamento de exceções em todos os testes
- Registro detalhado de eventos durante a execução
- Geração de relatórios em formato legível
- Uso de esperas explícitas para maior confiabilidade
- Verificações de resultado após cada ação crítica

## Extensão e Personalização

Para adicionar novos casos de teste:

1. Crie um novo script na pasta "scripts"
2. Siga o padrão dos scripts existentes
3. Atualize o arquivo run_all_tests.py para incluir o novo teste

## Problemas Conhecidos

- Alguns sites de demonstração podem mudar sua estrutura HTML, causando falhas na execução
- Em caso de conectividade lenta, alguns timeouts podem ocorrer

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes. 
