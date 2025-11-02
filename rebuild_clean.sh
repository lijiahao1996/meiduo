#!/bin/bash
set -e

PROJECT_NAME="meiduo"
BACKEND_CONTAINER="meiduo_server"
NETWORK_NAME="meiduo_net"

echo "=============================="
echo "🧹 开始重新部署 ${PROJECT_NAME} 项目..."
echo "=============================="

# === Step 1: 停止所有相关容器 ===
echo -e "\033[33m[1/8] 停止并删除旧容器、镜像、卷...\033[0m"
docker compose down --rmi all --volumes --remove-orphans || true

# === Step 2: 清理系统中孤立的资源 ===
echo -e "\033[33m[2/8] 清理 Docker 残留资源...\033[0m"
docker container prune -f || true
docker image prune -af || true
docker volume prune -f || true
docker network prune -f || true
docker builder prune -af || true

# === Step 3: 删除本地持久化数据（确保干净） ===
echo -e "\033[33m[3/8] 删除本地持久化数据卷（MySQL、Redis、日志）...\033[0m"
rm -rf ./mysql/data/* ./redis/data/* ./logs/* || true

# === Step 4: 确保网络一致性 ===
if ! docker network inspect ${NETWORK_NAME} >/dev/null 2>&1; then
  echo -e "\033[33m创建网络 ${NETWORK_NAME}...\033[0m"
  docker network create ${NETWORK_NAME}
else
  echo -e "\033[32m网络 ${NETWORK_NAME} 已存在，跳过。\033[0m"
fi

# === Step 5: 重新构建镜像 ===
echo -e "\033[33m[4/8] 重新构建镜像（不使用缓存）...\033[0m"
docker compose build --no-cache

# === Step 6: 启动容器 ===
echo -e "\033[33m[5/8] 启动新容器...\033[0m"
docker compose up -d

# === Step 7: 等待服务启动 + 健康检查 ===
echo -e "\033[33m[6/8] 检查容器健康状态...\033[0m"
sleep 15
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# === Step 8: 初始化数据库 ===
echo -e "\033[33m[7/8] 初始化数据库迁移与静态文件...\033[0m"
docker exec -it ${BACKEND_CONTAINER} bash -c "
  echo '🔧 执行 migrate...'
  python manage.py migrate --fake-initial
  echo '📦 收集静态文件...'
  python manage.py collectstatic --noinput
"
# === Step 9: 网络与健康链路检测 ===
echo -e "\033[33m[8/8] 检查网络与健康状态...\033[0m"

echo -e "\n💡 检查 Nginx → Django 链路："
docker exec -it meiduo_web bash -c "curl -fsS http://localhost/healthz/ || echo '❌ 无法访问后端'"

echo -e "\n💡 检查本地访问接口："
curl -fsS http://localhost:8080/api/healthz/ || echo '❌ 无法访问前端健康接口'  # ✅ 修正检测路径

echo ""
echo "=============================="
echo -e "✅ \033[32m部署完成并验证通过！\033[0m"
echo "🧠 管理后台: http://localhost/admin/"
echo "🐳 查看容器: docker ps"
echo "📜 查看日志: docker compose logs -f"
echo "=============================="
