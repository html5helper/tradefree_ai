# celeryconfig_dev.py - 开发环境配置
import os
from kombu import Exchange, Queue
from celery.schedules import crontab

# Token Key 配置
USER_TOKEN_CONFIG = {
    "token2_def456": {
        "user_name":"fenghetong",
        "user_group":"GENERATE",
        "user_info":{
            "user_name":"fenghetong",
            "user_group":"GENERATE",
        },
        "employer_info":{
            "employer_id": "1",
            "employer_name": "employer_001",
            "employer_cn_name": "员工001"
        },
        "employer_accesses":[
            {
                "employer_id": "1",
                "workflow": "amz_to_ali",
                "workflow_name": "亚马逊到阿里",
                "product_type": "sticker",
                "platform": "ali",
                "category_id": "201304308",
                "shop_name": "阿里国际-店铺001",
                "action_flow_id": "1"
            },
            {
                "employer_id": "2",
                "workflow": "amz_to_1688",
                "workflow_name": "亚马逊到1688",
                "product_type": "sticker",
                "platform": "1688",
                "category_id": "201304308",
                "shop_name": "1688-店铺001",
                "action_flow_id": "2"
            }
        ]
    },
    "tiuGlpGYG6olYLBaIfbvsKI7DIUv9Z3J": {
        "user_name":"user_001",
        "user_group":"COPY"
    },
    "W2armxPmXOMQljPbjgeBFAFJ7jGWkMTU":{
        "user_name":"user_002",
        "user_group":"COPY"
    },
    "go7G14OLyFr4atc94uzuZMwEGrHIn146":{
        "user_name":"user_003",
        "user_group":"COPY"
    }
}

USER_GROUP_ACCESS = {
    "COPY": ["amz_copy_ali", "amz_copy_1688", "ali_copy_1688", "1688_copy_1688", "ali_copy_ali"],
    "GENERATE": ["amz_to_ali", "amz_to_1688", "ali_to_1688", "1688_to_1688", "ali_to_ali", "social_to_ali"],
}

# MySQL 配置
MYSQL_CONFIG = {
    "workflow_db": {
        'host': os.getenv("MYSQL_HOST", "127.0.0.1"),
        'port': os.getenv("MYSQL_PORT", "3306"),
        'user':  os.getenv("MYSQL_USER", "tradefree"),
        'password': os.getenv("MYSQL_PASSWORD", "c1234%^5678C"),
        'database': 'celery_dev',
        'charset': 'utf8mb4',
        # 'auth_plugin': 'mysql_native_password'
    },
    "manager_db": {
        'host': os.getenv("MYSQL_HOST", "127.0.0.1"),
        'port': os.getenv("MYSQL_PORT", "3306"),
        'user':  os.getenv("MYSQL_USER", "tradefree"),
        'password': os.getenv("MYSQL_PASSWORD", "c1234%^5678C"),
        'database': 'tf',
        'charset': 'utf8mb4',
        # 'auth_plugin': 'mysql_native_password'
    }
}

# Dify API 配置
DIFY_BASE_URL = "http://dify.tradefree.ai/v1"

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_DB_BROKER = "2"
REDIS_DB_BACKEND = "3"
broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BROKER}"
result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BACKEND}"



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
DIFY_BASE_URL = "http://dify.html5core.com/v1"

DIFY_CONFIG = {
    # social methods
    "social_fetch_total": {
        "workflow_id": "9d8c70ca-e5ca-47ae-a3bc-b0f239275672",
        "api_key": "app-iuH21hu72REChudBDXQ9ryZj"
    },
    "social_pages_listing": {
        "workflow_id": "2f489587-7ad7-46a6-91bb-359bad38ea27",
        "api_key": "app-Py50u0qC4AupCOSTDdn0MWaC"
    },
    # listing adapter methods
    "listing_adapter": {
        "workflow_id": "4bca7121-1a19-424c-86a4-c2f1664ac979",
        "api_key": "app-9BKKSzrzf5D1DHcHqk5Gz6Z8"
    },
    
    # normal product methods
    "product_listing": {
        "workflow_id": "b7b7e631-e5c0-4fa9-b105-17d2137f0b88",
        "api_key": "app-H0aaAlTrthGMrabomhiVGDVl"
    },
    "maskword_filter": {
        "workflow_id": "530c3d1e-56de-4e94-ae41-349707cbfb8e",
        "api_key": "app-qbYXlCBIOLvAG5vfmL618BKN"
    },
    "text2img2download": {
        "workflow_id": "58a2386c-4743-40cb-ab1f-6cf1611c0997",
        "api_key": "app-HqaViz4DyXoszmUXX7Ln1dxp"
    },
    "img2text2img2download": {
        "workflow_id": "15057dc0-bef6-40ef-b745-499c867a61f4",
        "api_key": "app-aHottX9s7ptJQLEeU6SOL1MA"
    },
    "img2video":{
        "workflow_id":"66194caf-3538-44d0-9a97-d72c97051476",
        "api_key":"app-UuFhL6LIYfF7mSJ4gKShzFNG"
    },
    "upload_photos": {
        "workflow_id": "d1af9703-2931-4b16-b236-6d91c1c9f10c",
        "api_key": "app-KfLeimdKVEsvoAMSqCPRtSAo"
    },
    "upload_video": {
        "workflow_id": "5b69322e-73cd-48ea-9361-7586b35062a4",
        "api_key": "app-ntZSqH195mizqTVKMbD5OIRh"
    },
    "publish_product": {
        "workflow_id": "352b74de-8e61-45d8-bbf1-6ebb76980185",
        "api_key": "app-NHZR6CX01FrytLhSjPuAi2s7"
    }
}

# 链式工作流配置
CHAIN_MAP = {
    "amz_copy_ali": [
        'ai.business.resource.tasks.amz_to_ali_src',
        'ai.business.listing.tasks.listing_adapter',
        'ai.business.maskword.tasks.amz_to_ali_maskword_filter',
        # 'ai.business.image.tasks.amz_to_ali_image',
        # 'ai.business.upload_img.tasks.amz_to_ali_upload',
        # 'ai.business.public.tasks.amz_to_ali_public',
    ],
    "amz_to_ali": [
        'ai.business.resource.tasks.amz_to_ali_src',
        'ai.business.listing.tasks.amz_to_ali_listing',
        'ai.business.maskword.tasks.amz_to_ali_maskword_filter',
        'ai.business.image.tasks.amz_to_ali_image',
        'ai.business.upload_img.tasks.amz_to_ali_upload',
    ],
    "amz_to_1688": [
        'ai.business.resource.tasks.amz_to_1688_src',
        'ai.business.listing.tasks.amz_to_1688_listing',
        'ai.business.maskword.tasks.amz_to_1688_maskword_filter',
        'ai.business.image.tasks.amz_to_1688_image',
        'ai.business.upload_img.tasks.amz_to_1688_upload',
        'ai.business.video.tasks.amz_to_1688_video',
        'ai.business.upload_video.tasks.amz_to_1688_upload'
        'ai.business.public.tasks.amz_to_1688_public',
    ],
    "ali_to_1688": [
        'ai.business.resource.tasks.ali_to_1688_src',
        'ai.business.listing.tasks.ali_to_1688_listing',
        'ai.business.maskword.tasks.ali_to_1688_maskword_filter',
        'ai.business.image.tasks.ali_to_1688_image',
        'ai.business.upload_img.tasks.ali_to_1688_upload',
        'ai.business.video.tasks.ali_to_1688_video',
        'ai.business.upload_video.tasks.ali_to_1688_upload'
        'ai.business.public.tasks.ali_to_1688_public',
    ],
    "1688_to_1688": [
        'ai.business.resource.tasks._1688_to_1688_src',
        'ai.business.listing.tasks._1688_to_1688_listing',
        'ai.business.maskword.tasks._1688_to_1688_maskword_filter',
        'ai.business.image.tasks._1688_to_1688_image',
        'ai.business.upload_img.tasks._1688_to_1688_upload',
        'ai.business.video.tasks._1688_to_1688_video',
        'ai.business.upload_video.tasks._1688_to_1688_upload'
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
log_level = "DEBUG"

# 其他配置
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000
task_time_limit = 3600  # 1小时
task_soft_time_limit = 3000  # 50分钟 