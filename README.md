# Superstore Sales Intelligence & Analytics Platform

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checker: Pyright](https://img.shields.io/badge/type%20checker-pyright-green.svg)](https://microsoft.github.io/pyright/)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](https://pytest.org/)

Dashboard analítico e pipeline modular em Python para exploração comercial, monitoramento de margem de lucro e identificação de transações deficitárias no varejo utilizando o Superstore Sales Dataset.

---

## Autor

- **Nome:** Ricson Ramos
- **Perfil GitHub:** [github.com/RicsonRamos](https://github.com/RicsonRamos)
- **LinkedIn:** [linkedin.com/in/ricsonramos](https://www.linkedin.com/in/ricsonramos/)
- **Portfólio Web:** [ricsonramos.github.io](https://ricsonramos.github.io)
- **Contato:** ricsonramos@outlook.com

---

## Visão Geral do Projeto

No setor varejista, volumes elevados de faturamento podem mascarar ineficiências operacionais severas, como descontos excessivos ou custos logísticos desproporcionais por categoria e região.

Este projeto implementa uma solução analítica completa de ponta a ponta:
1. **Ingestão Automatizada:** Download programático e validação do dataset a partir do Kaggle via `kagglehub`.
2. **Tratamento e Higienização:** Conversão de tipos estritos, tratamento de valores nulos e estruturação de flags operacionais (como `Is Loss Making` para identificação de vendas com prejuízo).
3. **Cálculo de Métricas de Negócio:** Módulo dedicado (`metrics.py`) para cálculo desacoplado de KPIs: Total Sales, Total Profit, Profit Margin, Ticket Médio e contagem de transações deficitárias.
4. **Análise Exploratória Estruturada:** Notebook Jupyter reprodutível (`notebooks/eda.ipynb`) com análise bivariada, sazonalidade e segmentação.
5. **Dashboard Interativo em Streamlit:** Interface gerencial (`app.py`) com filtros multidimensionais (período, região, categoria) e visualizações dinâmicas de evolução temporal e distribuição de margem.
6. **Padrões de Engenharia de Software:** Gerenciamento de ambiente isolado com `uv`, tipagem estática rigorosa via `Pyright`, linting e formatação com `Ruff`, testes automatizados via `pytest` e conteinerização multi-stage com `Docker`.

---

## Estrutura do Repositório

```text
superstore-sales-dataset/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Pipeline de CI (Ruff, Pyright e Pytest)
├── .vscode/
│   └── settings.json                  # Configurações do VS Code para formatação e tipagem
├── data/
│   ├── 01_raw/                        # Dados brutos imutáveis
│   ├── 02_interim/                    # Dados intermediários de transformação
│   ├── 03_processed/                  # Datasets limpos e prontos para consumo
│   └── 04_external/                   # Dados auxiliares de terceiros
├── models/                            # Artefatos e checkpoints de modelos
├── notebooks/
│   ├── eda.ipynb                      # Análise exploratória de dados detalhada
│   └── eda.html                       # Relatório HTML exportado da análise
├── reports/
│   └── figures/                       # Figuras e gráficos gerados
├── src/
│   └── superstore_sales_dataset/
│       ├── __init__.py                # Inicialização do pacote
│       ├── config.py                  # Gestão centralizada de diretórios e caminhos
│       ├── data_clean.py              # Pipelines de limpeza, tipagem e enriquecimento
│       ├── data_loader.py             # Download automático e verificação do dataset Kaggle
│       └── metrics.py                 # Funções puras de cálculo de métricas de negócio
├── tests/
│   ├── __init__.py
│   └── test_smoke.py                  # Testes automatizados de fumaça e integridade
├── Dockerfile                         # Build multi-stage otimizado para produção com UV
├── .dockerignore                      # Regras de exclusão do contexto Docker
├── .env.example                       # Modelo de variáveis de ambiente
├── .gitignore                         # Exclusão de artefatos temporários e dados sensíveis
├── .pre-commit-config.yaml            # Hooks de pré-commit para garantia de qualidade
├── pyproject.toml                     # Configuração do projeto, ferramentas e dependências
└── uv.lock                            # Lockfile determinístico de dependências
```

---

## Como Executar

### Pré-requisitos

Instale o gerenciador de pacotes [`uv`](https://docs.astral.sh/uv/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Clonar e Sincronizar o Ambiente

```bash
git clone https://github.com/RicsonRamos/superstore-sales-dataset.git
cd superstore-sales-dataset
uv sync --all-groups
```

### 2. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

*(Opcional)* Para o download automático do Kaggle via API, configure as credenciais `KAGGLE_USERNAME` e `KAGGLE_KEY` caso não possua o arquivo `~/.kaggle/kaggle.json`.

### 3. Executar o Dashboard Streamlit

```bash
uv run streamlit run app.py
```

O dashboard estará disponível em `http://localhost:8501`.

### 4. Executar via Docker

Para rodar a aplicação isolada em contêiner Docker:

```bash
# Construir a imagem Docker
docker build -t superstore-sales-dashboard .

# Executar o contêiner na porta 8501
docker run -p 8501:8501 superstore-sales-dashboard
```

---

## Testes e Qualidade de Código

### Testes Automatizados com Pytest

```bash
uv run pytest
```

### Linting e Formatação com Ruff

```bash
# Verificar conformidade de código
uv run ruff check .

# Aplicar correções automáticas
uv run ruff check --fix .

# Verificar formatação
uv run ruff format --check .
```

### Checagem Estática de Tipos com Pyright

```bash
uv run pyright
```
