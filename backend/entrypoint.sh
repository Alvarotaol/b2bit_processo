#!/bin/sh

# Espera o banco ficar pronto
echo "Aguardando o banco..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Rodando migrations e collectstatic..."
python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
