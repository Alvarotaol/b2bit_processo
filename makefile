# Makefile

# Nome do container de app
CONTAINER_NAME=web

# Comando pra rodar o Django
DJANGO_CMD="python manage.py"

# Comando padrão do Docker Compose
DC=docker-compose

# Verifica o status do Docker Compose
status:
	$(DC) ps

# Cria o projeto com migrations e prepara o banco de dados
migrate:
	$(DC) run $(CONTAINER_NAME) $(DJANGO_CMD) migrate

# Cria o superuser (se não existir)
createsuperuser:
	$(DC) run $(CONTAINER_NAME) $(DJANGO_CMD) createsuperuser

# Sobe o ambiente Docker
up:
	$(DC) up --build -d

# Para o ambiente Docker
down:
	$(DC) down

# Roda os testes
test:
	$(DC) run $(CONTAINER_NAME) $(DJANGO_CMD) test

# Roda o shell do Django
shell:
	$(DC) run $(CONTAINER_NAME) $(DJANGO_CMD) shell

# Gera o arquivo de documentação (Swagger)
docs:
	$(DC) run $(CONTAINER_NAME) $(DJANGO_CMD) generateschema --output=swagger.yaml

# Executa o Django no modo de desenvolvimento
dev:
	$(DC) up --build

# Limpa volumes do Docker (deixa banco vazio)
clean:
	$(DC) down -v
