# superstore-sales-dataset

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checker: Pyright](https://img.shields.io/badge/type%20checker-pyright-green.svg)](https://microsoft.github.io/pyright/)

Projeto de Ciência de Dados

---

## 👤 Author

- **Name:** Ricson Ramos
- **Contact:** ricsonramos@outlook.com

---

## 📁 Repository Structure

```text
superstore-sales-dataset/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Continuous integration workflow (Ruff, Pyright, Pytest)
├── .vscode/
│   └── settings.json                  # VS Code formatting & type checking settings
├── data/
│   ├── 01_raw/                        # Immutable raw source data
│   ├── 02_interim/                    # Intermediate transformed data
│   ├── 03_processed/                  # Canonical datasets ready for ML modeling
│   └── 04_external/                   # Third-party or auxiliary datasets
├── models/                            # Trained model artifacts and weights
├── notebooks/                         # Exploratory and analytical Jupyter notebooks
├── reports/
│   └── figures/                       # Generated graphics, plots, and figures
├── src/
│   └── superstore_sales_dataset/
│       ├── __init__.py                # Package root
│       └── config.py                  # Pathlib directory paths and environment loader
├── tests/
│   ├── __init__.py
│   └── test_smoke.py                  # Initial smoke test
├── .copier-answers.yml                # Template configuration (enables 'copier update')
├── .dockerignore                      # Exclusões de contexto de build Docker
├── .env.example                       # Example environment variables
├── .gitignore                         # Data Science gitignore
├── .pre-commit-config.yaml            # Git hooks configuration (pre-commit & pre-push)
├── .python-version                    # Pinned Python version (3.12)
├── Dockerfile                         # Multi-stage production Dockerfile optimized with UV
├── pyproject.toml                     # Project dependencies and tool configurations
└── README.md
```

---

## 🚀 Quickstart

### Prerequisites

Install [`uv`](https://docs.astral.sh/uv/) if not already installed:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Environment Setup

Clone this repository and synchronize all dependencies (including `dev` and `notebooks` groups):

```bash
cd superstore-sales-dataset
uv sync --all-groups
```

This creates the isolated `.venv` environment and installs all dependencies defined in `pyproject.toml`.

### 2. Environment Variables

Create your local `.env` configuration file:

```bash
cp .env.example .env
```

### 3. Verify Installation & CLI

Run the project info CLI entrypoint:

```bash
uv run superstore-sales-dataset
```

### 4. Running JupyterLab

Launch JupyterLab configured to use the project's virtual environment:

```bash
uv run jupyter lab
```

---

## 🧪 Testing & Code Quality

### Running Tests

Execute the test suite using `pytest`:

```bash
uv run pytest
```

### Code Formatting and Linting

Check code formatting and run lint checks using `ruff`:

```bash
# Linting
uv run ruff check .

# Linting with automatic fixes
uv run ruff check --fix .

# Format checking
uv run ruff format --check .

# Apply formatting
uv run ruff format .
```

### Static Type Checking

Perform static type checking using `pyright`:

```bash
uv run pyright
```

---

## 🪝 Git Hooks (Pre-commit & Pre-push)

Pre-commit hooks are configured via `.pre-commit-config.yaml`:
- **Pre-commit:** Runs hygiene checks (whitespace, YAML/TOML syntax, large files), Jupyter notebook visual output cleaning (`nbstripout`), and Ruff lint/format.
- **Pre-push:** Runs Pyright type checking and pytest tests.

To manually trigger the hooks on all files:

```bash
# Pre-commit stage hooks
uv tool run pre-commit run --all-files

# Pre-push stage hooks
uv tool run pre-commit run --hook-stage pre-push --all-files
```

---

## 🐳 Docker Deployment

The project includes an optimized multi-stage `Dockerfile` leveraging UV layer caching and non-root runtime:

```bash
# Build the Docker image
docker build -t superstore-sales-dataset:v1 .

# Run the container
docker run --rm -p 8000:8000 --name superstore-sales-dataset-app superstore-sales-dataset:v1
```

---

## 🔄 Updating from Template

This project was generated using Copier. To pull future updates, enhancements, or bug fixes from the template generator:

```bash
uvx copier update --trust
```
