# ==========================================
# STAGE 1: Base (Chuẩn bị môi trường & Thư viện)
# ==========================================
FROM python:3.12-slim AS pybase
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off

WORKDIR /src/backend
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY src/backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ==========================================
# STAGE 2: Development (Chạy ứng dụng)
# ==========================================
FROM pybase AS backend_dev

RUN useradd -m backend_user
COPY --chown=backend_user:backend_user src/backend/otaskmanagement ./otaskmanagement
WORKDIR /src/backend/otaskmanagement
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]