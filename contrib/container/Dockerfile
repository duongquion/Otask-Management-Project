FROM python:3.12-slim AS pybase
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /src/backend
COPY src/backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

### Backend ###
FROM pybase AS backend_dev
WORKDIR /src/backend/otaskmanagement
EXPOSE 8000
CMD ["python","-V"]