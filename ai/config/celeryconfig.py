# celeryconfig.py
from kombu import Exchange, Queue
from celery.schedules import crontab

# Broker 和 Backend 配置
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"

# MySQL 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'tradefree',
    'password': 'c1234%^5678C',
    'database': 'celery',
    'charset': 'utf8mb4'
}

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

# 定义交换机
ex_src = Exchange('product_src', type='direct')
ex_create = Exchange('product_create', type='direct')
ex_public = Exchange('product_public', type='direct')

# 定义队列
task_queues = (
    Queue('product_social_queue', ex_src, routing_key='social2product'),
    Queue('product_src_queue', ex_src, routing_key='product_src'),
    Queue('product_listing_queue', ex_create, routing_key='product_listing'),
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
    # image类任务
    'ai.business.image.tasks.*': {
        'queue': 'product_image_queue',
        'exchange': 'product_create',
        'routing_key': 'product_image',
    },
    # upload_img类任务
    'ai.business.upload_img.tasks.*': {
        'queue': 'product_upload_queue_ali',  # 或根据实际业务拆分
        'exchange': 'product_create',
        'routing_key': 'product_upload_ali',
    },
    # public类任务
    'ai.business.public.tasks.*': {
        'queue': 'product_public_queue_ali',  # 或根据实际业务拆分
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
    "social_to_ali_src": {
        "workflow_id": "c25c3f82-61d0-44f0-bc5a-d0bff52f8aa2",
        "api_key": "app-23SX7AOxwVCZvaXvtupFDsaT"
    },
    "social_to_ali_image": {
        "workflow_id": "41635577-659f-4d56-ae1d-a67131c94185",
        "api_key": "app-CrxTvw9sMXREZohs8jVqsEs3"
    },
    # normal product methods
    "product_listing": {
        "workflow_id": "01835a12-cd11-4e24-a924-3b3fcc64ce77",
        "api_key": "app-RgHCjKMd6QqZTrkwvxoKmalX"
    },
    "product_listing2": {
        "workflow_id": "2a78b74e-a267-4515-888e-8c083b5419b0",
        "api_key": "app-3C1v5XMUl76hBsIqH03QZepb"
    },
    "text2img2oss": {
        "workflow_id": "469a5c98-88d9-491d-819b-54c6b0d2cd5f",
        "api_key": "app-2V0Qcu0azc8WHkxgoE7BoYk6"
    },
    "img2text2img2oss": {
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
        'ai.business.image.tasks.amz_to_ali_image',
        'ai.business.upload_img.tasks.amz_to_ali_upload',
        'ai.business.public.tasks.amz_to_ali_public',
    ],
    "amz_to_1688": [
        'ai.business.resource.tasks.amz_to_1688_src',
        'ai.business.listing.tasks.amz_to_1688_listing',
        'ai.business.image.tasks.amz_to_1688_image',
        'ai.business.upload_img.tasks.amz_to_1688_upload',
        'ai.business.public.tasks.amz_to_1688_public',
    ],
    "ali_to_1688": [
        'ai.business.resource.tasks.ali_to_1688_src',
        'ai.business.listing.tasks.ali_to_1688_listing',
        'ai.business.image.tasks.ali_to_1688_image',
        'ai.business.upload_img.tasks.ali_to_1688_upload',
        'ai.business.public.tasks.ali_to_1688_public',
    ],
    "1688_to_1688": [
        'ai.business.resource.tasks._1688_to_1688_src',
        'ai.business.listing.tasks._1688_to_1688_listing',
        'ai.business.image.tasks._1688_to_1688_image',
        'ai.business.upload_img.tasks._1688_to_1688_upload',
        'ai.business.public.tasks._1688_to_1688_public',
    ],
    "ali_to_ali": [
        'ai.business.resource.tasks.ali_to_ali_src',
        'ai.business.listing.tasks.ali_to_ali_listing',
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