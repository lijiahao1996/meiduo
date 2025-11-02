#!/bin/sh
set -e

echo "🚀 Starting Meiduo Django Server..."

# ===== [1] 环境检查 =====
echo "Checking database connection..."
python3 manage.py check --database default || echo "⚠️ DB check failed, continue anyway."

# ===== [2] 收集静态文件（可选）=====
# python3 manage.py collectstatic --noinput

# ===== [3] 启动 uWSGI（主进程）=====
echo "Starting uWSGI service..."
exec uwsgi --ini /var/www/html/meiduo_mall/uwsgi.ini

