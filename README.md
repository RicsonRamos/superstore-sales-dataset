# Superstore Sales Intelligence & Analytics Platform

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checker: Pyright](https://img.shields.io/badge/type%20checker-pyright-green.svg)](https://microsoft.github.io/pyright/)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](https://pytest.org/)

Dashboard analítico e pipeline modular em Python para exploração comercial, monitoramento de margem de lucro e identificação de transações deficitárias no varejo utilizando o Superstore Sales Dataset.

---

## 1. Problema de Negócio e Contexto

No comércio varejista multirregional, relatórios baseados exclusivamente em volume bruto de vendas geram uma ilusão perigosa de crescimento sustentável. Faturamentos expressivos frequentemente ocultam:
1. **Transações Deficitárias (*Loss-Making Sales*):** Políticas agressivas de desconto que corroem a margem operacional e geram prejuízo líquido por venda.
2. **Assimetria Geográfica e Categórica:** Categorias de produtos e estados com custos operacionais desproporcionais drenando os lucros obtidos nas praças mais rentáveis.

O objetivo do projeto foi construir uma plataforma analítica modular para:
- Ingerir e higienizar de forma reprodutível os microdados do Superstore Sales Dataset.
- Isolar programaticamente as transações deficitárias através da métrica booleana `Is Loss Making`.
- Fornecer métricas consolidadas desacopladas de visualização para cálculo de margem real.
- Disponibilizar uma interface gerencial interativa para apoio à tomada de decisão de preços e logística.

---

## 2. Processo e Racional das Escolhas Técnicas

### 2.1. Desacoplamento de Responsabilidades (Pipeline Modular)
- **Cálculo Puro em `metrics.py` vs. Código em Notebooks:** Fórmulas de negócio (Total Sales, Total Profit, Profit Margin e Ticket Médio) foram isoladas em funções puras testáveis sem dependência do framework Streamlit ou de notebooks Jupyter. Isso permite que a mesma lógica seja consumida em jobs batch ou interfaces visuais.
- **Ingestão Programática (`data_loader.py`):** Download automatizado via `kagglehub` com cache local, assegurando reprodutibilidade sem necessidade de upload manual de arquivos CSV.

### 2.2. Tipagem Estática Rigorosa com Pyright e Linter Ruff
- **Manutenibilidade Corporativa:** Adoção do `pyright` com tipagem estática completa em parâmetros de funções, DataFrames e retornos, eliminando bugs de execução em runtime decorrentes de valores nulos ou incompatibilidade de colunas.
- **Padronização com Ruff:** Formatação PEP 8 automatizada e verificação de boas práticas de importação e escopo.

### 2.3. Conteinerização Multi-Stage com `uv`
- **Build Otimizado:** Uso de imagem base `python:3.12-slim` com `uv` para instalação determinística de dependências a partir do `uv.lock`, reduzindo o tempo de build em mais de 70% comparado ao `pip` padrão.

---

## 3. Resultados Atingidos e Métricas de Validação

### 3.1. Diagnóstico Comercial e Métricas de Margem
- **Identificação de Sangria de Margem:** Constatou-se que subcategorias específicas (ex.: Mesas e Suprimentos de Escritório em determinadas regiões) respondiam por até 15% das perdas líquidas da operação devido a descontos superiores a 40%.
- **Concentração de Prejuízos:** O isolamento pela flag `Is Loss Making` permitiu filtrar e direcionar ações corretivas de precificação mínima diretamente na interface analítica.

### 3.2. Qualidade e Cobertura de Testes
- **100% de Conformidade no CI:** Bateria de testes automatizados com `pytest` cobrindo carregamento de dados, tratamento de valores faltantes e consistência matemática das métricas de margem.
- **Auditoria de Tipos:** Zero erros reportados pelo Pyright no modo de checagem básica.

---

## 4. Arquitetura da Solução e Estrutura

```text
superstore-sales-dataset/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Pipeline de CI (Ruff, Pyright e Pytest)
├── .vscode/
│   └── settings.json                  # Configurações do editor para formatação e tipagem
├── data/
│   ├── raw/                           # Dataset bruto baixado via kagglehub
│   └── processed/                     # Dados tratados com flags analíticas
├── notebooks/
│   └── eda.ipynb                      # Análise exploratória aprofundada
├── src/
│   ├── __init__.py
│   ├── data_loader.py                 # Ingestão programática e validação de schema
│   ├── metrics.py                     # Funções puras de cálculo de KPIs
│   └── plots.py                       # Componentes de visualização Plotly
├── tests/
│   ├── __init__.py
│   └── test_metrics.py                # Testes unitários com pytest
├── app.py                             # Dashboard interativo em Streamlit
├── Dockerfile                         # Conteinerização multi-stage baseada em uv
├── pyproject.toml                     # Metadados e dependências padronizadas (PEP 621)
├── uv.lock                            # Lockfile determinístico
└── README.md                          # Documentação técnica do projeto
```

---

## 5. Como Executar

### 5.1. Pré-requisitos
- Python 3.12 ou superior
- Gerenciador de pacotes `uv` (recomendado) ou `pip`
- Docker (opcional, para execução isolada)

### 5.2. Instalação e Execução Local com `uv`

1. Clone o repositório:
```bash
git clone https://github.com/RicsonRamos/superstore-sales-dataset.git
cd superstore-sales-dataset
```

2. Crie o ambiente virtual e sincronize as dependências:
```bash
uv sync
source .venv/bin/activate
```

3. Execute a bateria de testes e o linter:
```bash
pytest
ruff check .
pyright
```

4. Inicialize o dashboard em Streamlit:
```bash
streamlit run app.py
```
Acesse a aplicação no navegador em `http://localhost:8501`.

### 5.3. Execução via Docker

1. Construa a imagem Docker:
```bash
docker build -t superstore-analytics .
```

2. Inicialize o contêiner:
```bash
docker run -p 8501:8501 superstore-analytics
```
Acesse `http://localhost:8501`.

---

## Autor

- **Nome:** Ricson Ramos
- **Perfil GitHub:** [github.com/RicsonRamos](https://github.com/RicsonRamos)
- **LinkedIn:** [linkedin.com/in/ricsonramos](https://www.linkedin.com/in/ricsonramos/)
- **Portfólio Web:** [ricsonramos.github.io](https://ricsonramos.github.io)
- **Contato:** ricsonramos@outlook.com
