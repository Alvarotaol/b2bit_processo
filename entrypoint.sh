#!/bin/bash

# Para em caso de erro
set -e

# Espera o banco subir
echo "Esperando o banco de dados estar pronto..."

until nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Banco de dados está pronto!"

# Roda migrações
python manage.py migrate

# Roda o comando passado no docker-compose (runserver)
exec "$@"
