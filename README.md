# 🛍️ Meiduo Mall 美多商城

> **全容器化电商项目模板**  
> 基于 **Django + Vue** 前后端分离架构，使用 Docker 一键部署，涵盖完整商城业务模块。

---

## 📸 首页预览

（此处可放置一张 `meiduo_index.png` 截图）

---

## 🧩 技术架构

```mermaid
graph TD
    A[用户浏览器] -->|HTTP/HTTPS| B[Nginx (Vue 前端)]
    B -->|uWSGI Socket| C[Django (后端应用)]
    C --> D[(MySQL 数据库)]
    C --> E[(Redis 缓存)]
    C --> F[(Elasticsearch 搜索)]
    C --> G[Celery Worker 异步任务]
```

### 核心组件

| 组件 | 作用 | 备注 |
|------|------|------|
| Django | 后端主框架 | 使用 uWSGI 部署 |
| Vue.js | 前端渲染 | 打包后由 Nginx 提供 |
| uWSGI | WSGI 网关 | 负责 Django 请求调度 |
| Nginx | 静态资源 & 反向代理 | 代理请求到 Django |
| Celery | 异步任务队列 | 基于 Redis broker |
| Redis | 缓存、消息队列 | 提高响应性能 |
| MySQL | 主数据存储 | 读写分离可扩展 |
| Elasticsearch | 商品搜索引擎 | 基于 IK 分词器 |

---

## 🐳 Docker 部署

### 1️⃣ 构建与启动

```bash
bash rebuild_clean.sh
```

该脚本自动完成以下步骤：

1. 清理旧容器、镜像、卷；
2. 重新构建所有服务；
3. 启动 MySQL / Redis / ES；
4. 自动执行数据库迁移与静态文件收集；
5. 进行健康检查。

运行结束后，输出类似：

```
✅ 部署完成并验证通过！
🧠 管理后台: http://localhost/admin/
📜 查看日志: docker compose logs -f
```

---

### 2️⃣ 服务端口

| 服务 | 容器 | 本地端口 | 说明 |
|------|------|-----------|------|
| 前端 (Nginx) | meiduo_web | `8080` | 访问前端页面 |
| 后端 (Django) | meiduo_server | `8000` | uWSGI 服务 |
| Redis | md_redis | `6379` | 缓存与 Celery Broker |
| MySQL | md_mysql | `3306` | 主数据库 |
| Elasticsearch | md_es | `9200` | 搜索引擎接口 |

---

### 3️⃣ 健康检查

```bash
# 检查后端健康状态
curl -fsS http://localhost:8000/healthz/

# 检查 Nginx 反向代理链路
docker exec -it meiduo_web bash -c "curl -fsS http://127.0.0.1/healthz/"
```

返回：
```json
{"status": "ok"}
```

---

## 🧱 项目结构

```bash
meiduo/
├── meiduo_mall/                 # Django 项目目录
│   ├── meiduo_mall/             # 主配置 (settings, urls, wsgi)
│   ├── apps/                    # 各业务模块：users, goods, orders 等
│   ├── celery_tasks/            # 异步任务
│   ├── uwsgi.ini                # uWSGI 配置
│   └── start.sh                 # 启动脚本
├── meiduo_mall_frontend/        # Vue 打包后的前端代码
│   ├── dist/                    # 前端静态资源
│   └── nginx.conf               # Nginx 配置
├── docker-compose.yaml          # 容器编排配置
├── rebuild_clean.sh             # 一键清理 + 部署脚本
├── logs/                        # 挂载日志目录
└── README.md                    # 项目说明
```

---

## 🔐 HTTPS 证书示例

为了模拟生产环境 HTTPS，可添加示例证书：

```
certs/
├── meiduo.site.crt
├── meiduo.site.key
└── nginx.conf （示例启用 HTTPS）
```

Nginx 配置参考：

```nginx
server {
    listen 443 ssl;
    server_name www.meiduo.site;

    ssl_certificate /etc/nginx/ssl/meiduo.site.crt;
    ssl_certificate_key /etc/nginx/ssl/meiduo.site.key;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
}


---

## 🧠 常见问题

| 问题 | 解决方案 |
|------|-----------|
| `meiduo_server` unhealthy | 确保 `/var/log/uwsgi.log` 存在或改为 `/dev/stdout` |
| Vue 页面空白 | 重新执行 `npm run build` 并更新 `dist/` |
| 数据库连接超时 | 检查 `.env` 配置与 MySQL 容器健康状态 |
| ES 搜索无结果 | 重新执行索引同步命令 `python manage.py rebuild_index` |

---

## 📜 License

本项目基于 **MIT License** 开源，可自由用于学习与二次开发。

```
MIT License  
Copyright (c) 2025 Li Jiahao
```

---

## ✨ Maintainer

👤 **Howell (Li Jiahao)**  
🌐 [GitHub](https://github.com/lijiahao1996)

