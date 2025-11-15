#!/bin/bash
set -e

BACKEND="meiduo_server"

echo "=============================="
echo "🚀 重建环境..."
echo "=============================="

docker compose down --remove-orphans || true

rm -rf data/mysql/* data/redis/* data/logs/* data/es/* || true
mkdir -p data/mysql data/redis data/logs data/es

docker compose build --no-cache
docker compose up -d

echo "⏳ 等待容器启动..."
sleep 12

echo "🔧 Django 初始化..."
docker exec ${BACKEND} bash -c "
  python manage.py migrate --fake-initial &&
  python manage.py collectstatic --noinput
"

echo "💚 检查后端："
curl -f http://localhost:8000/healthz || echo "❌ 后端失败"

echo "💚 检查前端："
curl -f http://localhost:8080/healthz/ || echo "❌ 前端失败"

echo "🎉 完成！"

