# Makefile

# Nome do container de app
CONTAINER_NAME=backend

# Comando padrão do Docker Compose
DC=docker-compose

# Verifica o status do Docker Compose
status:
	$(DC) ps

# Cria o projeto com migrations e prepara o banco de dados
migrate:
	$(DC) run $(CONTAINER_NAME) python manage.py migrate

# Cria o superuser (se não existir)
createsuperuser:
	$(DC) run $(CONTAINER_NAME) python manage.py createsuperuser

# Recria o ambiente Docker
build:
	$(DC) up --build -d

prod:
	$(DC) -f docker-compose.prod.yml up -d --build

# Sobe o ambiente Docker
up:
	$(DC) up -d

# Para o ambiente Docker
down:
	$(DC) down

# Roda os testes
test:
	$(DC) run $(CONTAINER_NAME) python manage.py test

# Roda o shell do Django
shell:
	$(DC) run $(CONTAINER_NAME) python manage.py shell

# Gera o arquivo de documentação (Swagger)
docs:
	$(DC) run $(CONTAINER_NAME) python manage.py generateschema --output=swagger.yaml

# Executa o Django no modo de desenvolvimento
dev:
	$(DC) up --build

# Limpa volumes do Docker (deixa banco vazio)
clean:
	$(DC) down -v
