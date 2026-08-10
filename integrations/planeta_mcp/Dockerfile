FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY integrations/planeta_mcp/requirements.txt /tmp/planeta-requirements.txt
RUN pip install --no-cache-dir -r /tmp/planeta-requirements.txt \
    && python -m playwright install --with-deps chromium \
    && chmod -R a+rX /ms-playwright

RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app/integrations /data/planeta \
    && chown -R app:app /app /data/planeta

COPY --chown=app:app integrations/planeta_mcp /app/integrations/planeta_mcp
RUN touch /app/integrations/__init__.py && chown app:app /app/integrations/__init__.py

USER app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn integrations.planeta_mcp.server:app --host 0.0.0.0 --port ${PORT:-8000}"]
