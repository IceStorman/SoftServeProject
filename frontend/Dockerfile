# Для React або подібного проекту
FROM node:16 AS build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Сервер для фронтенду
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
