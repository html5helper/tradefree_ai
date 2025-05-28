# celeryconfig_prod.py - 生产环境配置
import os
from kombu import Exchange, Queue
from celery.schedules import crontab

# API Key 配置
API_KEY = os.getenv("API_KEY", "token2_def456")
MYSQL_USER = os.getenv("MYSQL_USER", "tradefree")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "c1234%^5678C")
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_DB_BROKER = "0"
REDIS_DB_BACKEND = "1"
broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BROKER}"
result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BACKEND}"

# MySQL 配置
MYSQL_CONFIG = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': 'celery_prod',
    'charset': 'utf8mb4'
}

# 任务配置
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

# 定义交换机
ex_src = Exchange('product_src', type='direct')
ex_create = Exchange('product_create', type='direct')
ex_public = Exchange('product_public', type='direct')
ex_maskword = Exchange('maskword_filter', type='direct')

# 定义队列
task_queues = (
    Queue('product_social_queue', ex_src, routing_key='social2product'),
    Queue('product_src_queue', ex_src, routing_key='product_src'),
    Queue('product_listing_queue', ex_create, routing_key='product_listing'),
    Queue('product_maskword_queue', ex_maskword, routing_key='maskword_filter'),
    Queue('product_image_queue', ex_create, routing_key='product_image'),
    Queue('product_upload_queue_ali', ex_create, routing_key='product_upload_ali'),
    Queue('product_upload_queue_1688', ex_create, routing_key='product_upload_1688'),
    Queue('product_public_queue_ali', ex_public, routing_key='product_public_ali'),
    Queue('product_public_queue_1688', ex_public, routing_key='product_public_1688'),
)

# 路由配置
task_routes = {
    # social2product类任务
    'ai.business.social2product.tasks.*': {
        'queue': 'product_social_queue',
        'exchange': 'product_src',
        'routing_key': 'social2product',
    },
    # resource类任务
    'ai.business.resource.tasks.*': {
        'queue': 'product_src_queue',
        'exchange': 'product_src',
        'routing_key': 'product_src',
    },
    # listing类任务
    'ai.business.listing.tasks.*': {
        'queue': 'product_listing_queue',
        'exchange': 'product_create',
        'routing_key': 'product_listing',
    },
    # maskword类任务
    'ai.business.maskword.tasks.*': {
        'queue': 'product_maskword_queue',
        'exchange': 'maskword_filter',
        'routing_key': 'maskword_filter',
    },
    # image类任务
    'ai.business.image.tasks.*': {
        'queue': 'product_image_queue',
        'exchange': 'product_create',
        'routing_key': 'product_image',
    },
    # upload_img类任务
    'ai.business.upload_img.tasks.*': {
        'queue': 'product_upload_queue_ali',
        'exchange': 'product_create',
        'routing_key': 'product_upload_ali',
    },
    # public类任务
    'ai.business.public.tasks.*': {
        'queue': 'product_public_queue_ali',
        'exchange': 'product_public',
        'routing_key': 'product_public_ali',
    },
}

# Dify 工作流配置
DIFY_CONFIG = {
    # social methods
    "social_fetch_total": {
        "workflow_id": "b811f832-47e7-4a92-8aff-82a6859be328",
        "api_key": "app-GvSm89L42OluDU2JFyaDOCvM"
    },
    "social_pages_listing": {
        "workflow_id": "71012911-41b9-4d66-9c19-d666f2389d7e",
        "api_key": "app-JMJ87fMuTgYtOPlRGJNk5DVH"
    },
    # normal product methods
    "product_listing": {
        "workflow_id": "01835a12-cd11-4e24-a924-3b3fcc64ce77",
        "api_key": "app-RgHCjKMd6QqZTrkwvxoKmalX"
    },
    "maskword_filter": {
        "workflow_id": "fa1c6b8b-b85a-4410-a0e8-ad1a68dffc09",
        "api_key": "app-c7sGD7RM6q8cn4JaPqbk9Pqq"
    },
    "text2img2download": {
        "workflow_id": "469a5c98-88d9-491d-819b-54c6b0d2cd5f",
        "api_key": "app-2V0Qcu0azc8WHkxgoE7BoYk6"
    },
    "img2text2img2download": {
        "workflow_id": "401c549a-f85f-4f8f-ac12-745dd41b2d81",
        "api_key": "app-8ZEQ0dk4CQxvb0u3erw4n2Ea"
    },
    "upload_photos": {
        "workflow_id": "8bae616a-8be9-496b-b087-a300cd660210",
        "api_key": "app-Gxld5HWVZPOWYPu9B8BMrv9d"
    },
    "publish_product": {
        "workflow_id": "1aeeb7f4-c7ff-48e0-9f29-749d764d5637",
        "api_key": "app-q7bXCU359F464cgUMz5Q0zhK"
    }
}

# 链式工作流配置
CHAIN_MAP = {
    "amz_to_ali": [
        'ai.business.resource.tasks.amz_to_ali_src',
        'ai.business.listing.tasks.amz_to_ali_listing',
        'ai.business.maskword.tasks.amz_to_ali_maskword_filter',
        'ai.business.image.tasks.amz_to_ali_image',
        'ai.business.upload_img.tasks.amz_to_ali_upload',
        'ai.business.public.tasks.amz_to_ali_public',
    ],
    "amz_to_1688": [
        'ai.business.resource.tasks.amz_to_1688_src',
        'ai.business.listing.tasks.amz_to_1688_listing',
        'ai.business.maskword.tasks.amz_to_1688_maskword_filter',
        'ai.business.image.tasks.amz_to_1688_image',
        'ai.business.upload_img.tasks.amz_to_1688_upload',
        'ai.business.public.tasks.amz_to_1688_public',
    ],
    "ali_to_1688": [
        'ai.business.resource.tasks.ali_to_1688_src',
        'ai.business.listing.tasks.ali_to_1688_listing',
        'ai.business.maskword.tasks.ali_to_1688_maskword_filter',
        'ai.business.image.tasks.ali_to_1688_image',
        'ai.business.upload_img.tasks.ali_to_1688_upload',
        'ai.business.public.tasks.ali_to_1688_public',
    ],
    "1688_to_1688": [
        'ai.business.resource.tasks._1688_to_1688_src',
        'ai.business.listing.tasks._1688_to_1688_listing',
        'ai.business.maskword.tasks._1688_to_1688_maskword_filter',
        'ai.business.image.tasks._1688_to_1688_image',
        'ai.business.upload_img.tasks._1688_to_1688_upload',
        'ai.business.public.tasks._1688_to_1688_public',
    ],
    "ali_to_ali": [
        'ai.business.resource.tasks.ali_to_ali_src',
        'ai.business.listing.tasks.ali_to_ali_listing',
        'ai.business.maskword.tasks.ali_to_ali_maskword_filter',
        'ai.business.image.tasks.ali_to_ali_image',
        'ai.business.upload_img.tasks.ali_to_ali_upload',
        'ai.business.public.tasks.ali_to_ali_public',
    ],
    "social_total": [
        'ai.business.resource.tasks.social_to_ali_src'
    ],
    "social_pages": [
        'ai.business.listing.tasks.social_to_ali_listing'
    ],
    "social_to_ali": [
        'ai.business.maskword.tasks.social_to_ali_maskword_filter',
        'ai.business.image.tasks.social_to_ali_image',
        'ai.business.upload_img.tasks.social_to_ali_upload',
        'ai.business.public.tasks.social_to_ali_public',
    ],
}

# 周期性执行任务
beat_schedule = {
    'run-social-to-ali-everyday-tiktok': {
        'task': 'ai.business.social2product.tasks.fetch_social_total',
        'schedule': crontab(hour=14, minute=22),
        'args': [{
            "trace_id": "cron-trace-socialtoali",
            "event_type": "social_to_ali",
            "context": {"platform": "tiktok"},
            "payload": {}
        }]
    },
    'run-social-to-ali-everyday-youtube': {
        'task': 'ai.business.social2product.tasks.fetch_social_total',
        'schedule': crontab(hour=14, minute=22),
        'args': [{
            "trace_id": "cron-trace-socialtoali",
            "event_type": "social_to_ali",
            "context": {"platform": "youtube"},
            "payload": {}
        }]
    },
}

# 日志配置
log_level = "INFO"

# 其他配置
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000
task_time_limit = 3600  # 1小时
task_soft_time_limit = 3000  # 50分钟 