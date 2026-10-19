# ==============================================================================
# ESTÁGIO 1: Builder (Compilação e Resolução de Dependências)
# ==============================================================================
FROM python:3.12-slim-bookworm AS builder

# 1. Copia o binário oficial do UV direto da imagem oficial da Astral
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Variáveis de ambiente para otimizar o comportamento do UV no Docker
# - UV_COMPILE_BYTECODE: Compila arquivos .pyc para inicialização mais rápida da aplicação
# - UV_LINK_MODE=copy: Força cópia física de arquivos em vez de tentar hardlinks entre sistemas de arquivos
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 3. PASSO DE CACHE DE DEPENDÊNCIAS:
# Copia APENAS os manifestos primeiro. O Docker reutilizará esta camada
# a menos que as dependências do pyproject.toml ou uv.lock mudem.
COPY pyproject.toml uv.lock ./

# 4. Sincroniza apenas as dependências de produção (sem instalar o próprio projeto ainda)
# Utiliza cache de montagem do Docker para reaproveitar downloads entre builds locais/CI
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# 5. Copia o código-fonte da aplicação e README necessário para o build
COPY src /app/src
COPY README.md /app/README.md

# 6. Sincroniza o projeto final instalado em modo produção dentro do .venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ==============================================================================
# ESTÁGIO 2: Final Runtime (Imagem Mínima e Segura de Produção)
# ==============================================================================
FROM python:3.12-slim-bookworm AS final

WORKDIR /app

# 1. Cria usuário não-root por questões de segurança (Princípio do Menor Privilégio)
RUN useradd -m -u 1001 -s /bin/bash appuser

# 2. Copia o ambiente virtual completo (.venv) e o código compilado do Estágio 1
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app/src /app/src

# 3. Injeta o ambiente virtual no PATH global da imagem
# Dessa forma, 'python' e os executáveis do projeto apontam automaticamente para o .venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# 4. Alterna para o usuário não-root
USER appuser

# 5. Expõe a porta padrão do serviço (caso exponha API ou dashboard)
EXPOSE 8000

# 6. Comando padrão de inicialização (executa o CLI do projeto)
# Caso adicione uma API web (ex: FastAPI/Uvicorn), substitua por:
# CMD ["uvicorn", "superstore_sales_dataset.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["superstore-sales-dataset"]
