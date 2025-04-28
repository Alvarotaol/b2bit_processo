# Dockerfile para o Frontend (React)
FROM node:22-slim

#USER node
# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY package.json package-lock.json /app/
RUN npm install

# Copiar código da aplicação
COPY . /app/

