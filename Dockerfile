FROM ghcr.io/astral-sh/uv:0.12.15 AS uv-cli
FROM python:3.12-slim AS builder
WORKDIR /app
COPY --from=uv-cli /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
# Install from the committed hash-bearing lock only; no project model code or external credentials.
RUN uv sync --locked --no-dev --no-install-project --no-cache --python /usr/local/bin/python3.12

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app ./app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
USER 65532:65532
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
