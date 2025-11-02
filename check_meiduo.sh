#!/bin/bash
echo "🧩 Checking meiduo cluster..."

check() {
  printf "\n--- $1 ---\n"
  eval "$2"
}

check "1️⃣ Docker containers" "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
check "2️⃣ Redis" "docker exec md_redis redis-cli ping"
check "3️⃣ MySQL" "docker exec md_mysql mysql -uroot -pYOURPASS -e 'SHOW DATABASES;' | head"
check "4️⃣ Elasticsearch" "curl -s http://127.0.0.1:9200 | jq '.version.number' || curl -s http://127.0.0.1:9200"
check "5️⃣ Django" "curl -I http://127.0.0.1:8000 | head -n 1"
check "6️⃣ Frontend Nginx" "curl -I http://127.0.0.1:8080 | head -n 1"
check "7️⃣ Celery" "docker logs meiduo_worker | grep 'celery@' | tail -n 2"

