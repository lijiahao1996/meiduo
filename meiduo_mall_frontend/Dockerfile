# ---------- 构建阶段 ----------
FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# ---------- 运行阶段 ----------
FROM nginx:latest

RUN mkdir -p /usr/share/nginx/html

COPY --from=builder /app/dist /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]

