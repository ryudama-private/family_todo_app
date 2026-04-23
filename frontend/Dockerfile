FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

COPY .env.production .env

RUN npm run build

# 本番用previewサーバーで静的配信
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
