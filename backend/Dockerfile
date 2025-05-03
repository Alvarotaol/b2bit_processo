# backend/Dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y gcc libpq-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN adduser --uid 1000 --disabled-password --gecos "" appuser

WORKDIR /app

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Altera dono dos arquivos para o appuser
RUN chown -R appuser:appuser /app /entrypoint.sh

USER appuser

ENTRYPOINT [ "/entrypoint.sh" ]]