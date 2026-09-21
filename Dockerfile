# Stage 1: Build the Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the Python Backend
FROM python:3.13-slim
WORKDIR /app

# Install system dependencies if any (e.g. for Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for super-fast dependency installs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy python configuration files
COPY pyproject.toml uv.lock ./
COPY README.md ./

# Copy the source code
COPY src/ ./src

# Install python dependencies
RUN uv sync --frozen --no-dev

# Copy compiled Svelte assets from Stage 1 into the static directory
COPY --from=frontend-builder /app/static ./static

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Run the app
CMD ["uvicorn", "amma_yt.server:app", "--host", "0.0.0.0", "--port", "8000"]
