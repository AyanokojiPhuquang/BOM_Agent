# ---- Build stage ----
FROM python:3.11-slim AS builder

# Install uv from the official distroless image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Use system Python (no downloads)
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first (cached layer — only rebuilds when lockfile/pyproject change)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy project source and install it
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# ---- Runtime stage (minimal image) ----
FROM python:3.11-slim

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source and configs needed at runtime
COPY --from=builder /app/src /app/src
COPY --from=builder /app/configs /app/configs

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8030

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8030"]
