# Step 1: Build the application
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

# Copy the project into the intermediate image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable

# Step 2: Run the application
FROM python:3.12-slim

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv

EXPOSE 3000

# Run the application
CMD ["/app/.venv/bin/uvicorn", "emush_rag.api.main:app", "--host", "0.0.0.0", "--port", "3000"]