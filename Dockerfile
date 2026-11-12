# ==============================================================================
# Multi-stage Dockerfile para producción - API Sacré (FastAPI)
# Base: Alpine Linux
# ==============================================================================

# ------------------------------------------------------------------------------
# Etapa 1: Builder
# ------------------------------------------------------------------------------
FROM python:3.14-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=2.4.3

# Actualizar repositorios e instalar paquetes de compilación necesarios en Alpine
# Incluye Rust/Cargo y OpenSSL requeridos para compilar cryptography y bcrypt en musl/Alpine
RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache \
        build-base \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev \
        cargo \
        rust \
        postgresql-dev \
        linux-headers

# Actualizar herramientas de empaquetado e instalar Poetry
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Configurar Poetry para crear el virtualenv localmente en /app/.venv
RUN poetry config virtualenvs.in-project true

# Copiar manifiestos de dependencias
COPY pyproject.toml poetry.lock ./

# Instalar dependencias de producción únicamente
RUN poetry install --no-root --without development,testing --no-interaction --no-ansi

# ------------------------------------------------------------------------------
# Etapa 2: Runner
# ------------------------------------------------------------------------------
FROM python:3.14-alpine AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

# Actualizar paquetes de seguridad del sistema e instalar librerías runtime mínimas
RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache \
        libpq \
        libffi \
        openssl \
        ca-certificates

# Crear usuario y grupo de sistema sin privilegios en Alpine
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup -s /sbin/nologin -h /app

# Copiar el entorno virtual con las dependencias instaladas desde el builder
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

# Copiar el código fuente de la aplicación y artefactos requeridos
COPY --chown=appuser:appgroup pyproject.toml ./
COPY --chown=appuser:appgroup alembic/ ./alembic/
COPY --chown=appuser:appgroup src/ ./src/

# Cambiar al usuario no privilegiado
USER appuser

# Exponer el puerto por defecto de la aplicación
EXPOSE 8000

# Ejecutar migraciones, carga de datos iniciales e iniciar el servidor con Gunicorn
CMD alembic upgrade head && \
    python -m src.scripts.configure_roles && \
    python -m src.scripts.load_countries && \
    python -m src.scripts.create_admin && \
    exec gunicorn -c src/api/gunicorn.py src.api.main:app
