"""
Django production settings for meiduo_mall project.
"""

import os
import sys
import datetime
from pathlib import Path
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# 基础路径与环境变量加载
# ----------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR.parent / '.env'  #  指向 /var/www/html/meiduo_mall/.env
load_dotenv(dotenv_path)

# 添加 apps 导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# ----------------------------------------------------------------------
# 基础安全配置
# ----------------------------------------------------------------------

SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-placeholder-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
# ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

# 从环境变量获取主机白名单
raw_hosts = os.getenv('DJANGO_ALLOWED_HOSTS', '')
if not raw_hosts or raw_hosts.strip() == '*':
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(',') if h.strip()]

# 🔥 强制添加容器内部和常见访问主机
INTERNAL_HOSTS = ['localhost', '127.0.0.1', 'meiduo_server']
for h in INTERNAL_HOSTS:
    if h not in ALLOWED_HOSTS and '*' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(h)



# ----------------------------------------------------------------------
# 应用注册
# ----------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三方模块
    'corsheaders',
    'rest_framework',
    'ckeditor',
    'ckeditor_uploader',
    'haystack',
    'rest_framework_swagger',

    # 自定义应用
    'users',
    'oauth',
    'areas',
    'goods',
    'content',
    'carts',
    'orders',
    'payment',
    # 临时用于调试路由
    'django_extensions',

]

# ----------------------------------------------------------------------
# 中间件
# ----------------------------------------------------------------------

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 解决跨域
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------------------------------------------------
# 路由与模板
# ----------------------------------------------------------------------

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# ----------------------------------------------------------------------
# 数据库配置（主从）
# ----------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB', 'meiduo_mall'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'root'),
        'HOST': os.getenv('MYSQL_HOST', 'md_mysql'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    }
}

DATABASE_ROUTERS = []

# ----------------------------------------------------------------------
# 认证与用户模型
# ----------------------------------------------------------------------

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]

# ----------------------------------------------------------------------
# 语言与时区
# ----------------------------------------------------------------------

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ----------------------------------------------------------------------
# Redis 缓存
# ----------------------------------------------------------------------

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "verify_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/2",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "home_category": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/3",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "home_content": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/4",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "history": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/5",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/6",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# ----------------------------------------------------------------------
# CORS 跨域配置
# ----------------------------------------------------------------------

CORS_ORIGIN_WHITELIST = tuple(os.getenv('CORS_WHITELIST', '').split(','))
CORS_ALLOW_CREDENTIALS = True

# ----------------------------------------------------------------------
# REST framework 配置
# ----------------------------------------------------------------------

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'meiduo_mall.utils.pagination.SetPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

# ----------------------------------------------------------------------
# 邮件配置
# ----------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.163.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '465'))
EMAIL_HOST_USER = os.getenv('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', EMAIL_HOST_USER)
EMAIL_USE_SSL = True

# ----------------------------------------------------------------------
# FastDFS 文件存储
# ----------------------------------------------------------------------

USE_FASTDFS = os.getenv('USE_FASTDFS', 'True') == 'True'

if USE_FASTDFS:
    # ✅ 启用 FastDFS 模式
    FDFS_URL = os.getenv('FDFS_URL', 'http://127.0.0.1:8888/')
    FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')
    DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.FastDFSStorage.FastDFSStorage'
else:
    # ✅ 本地开发模式：使用本地文件系统存储
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ----------------------------------------------------------------------
# 富文本编辑器配置
# ----------------------------------------------------------------------

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
    },
}
CKEDITOR_UPLOAD_PATH = ''

# ----------------------------------------------------------------------
# 支付宝配置
# ----------------------------------------------------------------------

ALIPAY_APPID = os.getenv('ALIPAY_APPID', '')
ALIPAY_URL = os.getenv('ALIPAY_URL', 'https://openapi.alipaydev.com/gateway.do')
ALIPAY_DEBUG = os.getenv('ALIPAY_DEBUG', 'True') == 'True'

# ----------------------------------------------------------------------
# Haystack 搜索配置
# ----------------------------------------------------------------------

ES_HOST = os.getenv('ES_HOST', '127.0.0.1')
ES_PORT = os.getenv('ES_PORT', '9200')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': f"http://{ES_HOST}:{ES_PORT}/",
        'INDEX_NAME': 'meiduo',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# ----------------------------------------------------------------------
# 日志配置（文件 + 控制台）
# ----------------------------------------------------------------------

LOG_PATH = '/var/log/meiduo'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {'format': '%(levelname)s %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'meiduo_mall.log'),
            'maxBytes': 20 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ----------------------------------------------------------------------
# 静态文件配置
# ----------------------------------------------------------------------

STATIC_ROOT = '/var/www/html/static'
STATIC_URL = '/static/'

# Celery 配置
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/3"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/4"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

