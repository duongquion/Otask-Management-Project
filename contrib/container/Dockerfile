# ---------- STAGE 1: builder ----------
FROM python:3.12-slim AS builder

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY src/backend/requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---------- STAGE 2: runtime ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY src/backend/requirements.txt .

RUN pip install --no-cache-dir --find-links /wheels -r requirements.txt \
    && rm -rf /wheels

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY src/backend/otaskmanagement/ .

COPY contrib/container/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Phân quyền
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "otaskmanagement.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]