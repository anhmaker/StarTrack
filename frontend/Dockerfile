# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Установка зависимостей
COPY package.json package-lock.json* ./
RUN npm install

# Копирование исходников и сборка
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Копирование собранного приложения
COPY --from=build /app/dist /usr/share/nginx/html

# Копирование конфигурации Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
