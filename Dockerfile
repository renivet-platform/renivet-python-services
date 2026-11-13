FROM ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 AS uv-cli
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1 AS builder
WORKDIR /app
COPY --from=uv-cli /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
# Install from the committed hash-bearing lock only; no project model code or external credentials.
RUN uv sync --locked --no-dev --no-install-project --no-cache --python /usr/local/bin/python3.12

FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
# Patch the known Debian 13 APT/zlib CVEs in the pinned runtime base image.
# Refuse to build if the Debian security repository cannot provide fixed versions.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends --only-upgrade apt libapt-pkg7.0 zlib1g; \
    dpkg --compare-versions "$(dpkg-query -W -f='${Version}' apt)" ge 3.0.4; \
    dpkg --compare-versions "$(dpkg-query -W -f='${Version}' zlib1g)" ge '1:1.3.dfsg+really1.3.1-1+deb13u1'; \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app ./app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
USER 65532:65532
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
