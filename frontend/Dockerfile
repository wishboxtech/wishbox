FROM node:22-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund \
      --registry=https://repo.hmirror.ir/npm/ \
      --fetch-retries=2 \
      --fetch-timeout=60000 \
      --loglevel=verbose
COPY . .
EXPOSE 80
CMD ["npm", "run", "dev", "--", "--port", "80"]

FROM development AS build
RUN npm run build

FROM nginx:1.28-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
