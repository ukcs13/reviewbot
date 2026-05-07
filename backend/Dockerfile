FROM python:3.12-slim AS builder

WORKDIR /build

# Install uv for fast dependency management
RUN pip install uv

COPY pyproject.toml .
COPY app/ ./app/
# Install dependencies and the project to system site-packages
RUN uv pip install --system --no-cache-dir .

FROM python:3.12-slim AS runtime

# Security: Don't run as root
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini entrypoint.sh ./

RUN chmod +x entrypoint.sh && chown -R app:app /app

USER app

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
