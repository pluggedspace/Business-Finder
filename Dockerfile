# syntax=docker/dockerfile:1.4
FROM python:3.11-slim AS base

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# System deps for psycopg, pandas, numpy, tensorflow, lxml, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copy project code
COPY . .

# Default entrypoint is Gunicorn
CMD ["gunicorn", "businessfinder.wsgi:application", "--bind", "0.0.0.0:8010", "--timeout=120"]