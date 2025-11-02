import os
from celery import Celery
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# 自动加载 .env（支持容器和本地）
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)

# ---------------------------------------------------------------------
# 设置 Django 配置模块（默认使用生产配置）
# ---------------------------------------------------------------------
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.settings_prod'

# ---------------------------------------------------------------------
# 创建 Celery 应用
# ---------------------------------------------------------------------
celery_app = Celery('meiduo')

# 读取 Django settings 中的 Celery 配置
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])

