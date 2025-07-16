# celeryconfig.py - 基础配置文件
import os
from kombu import Exchange, Queue
from celery.schedules import crontab

# 环境配置
ENV = os.getenv("ENV", "development")

# 通用配置

# Token Key 配置
USER_TOKEN_CONFIG = {
    "token2_def456": {
        "user_name":"fenghetong",
        "user_group":"GENERATE",
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

# USER_GROUP_ACCESS = {
#     "COPY": ["amz_copy_ali", "amz_copy_1688", "ali_copy_1688", "1688_copy_1688", "ali_copy_ali"],
#     "GENERATE": ["amz_to_ali", "amz_to_1688", "ali_to_1688", "1688_to_1688", "ali_to_ali", "social_to_ali"],
# }

# 任务配置
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

# 任务结果持久化配置
result_expires = 86400  # 任务结果保存24小时
task_track_started = True  # 跟踪任务开始状态
task_ignore_result = False  # 不忽略任务结果，保持功能正常
task_always_eager = False  # 不总是立即执行

# 任务状态持久化
task_annotations = {
    '*': {
        'rate_limit': '10/s'  # 限制任务执行频率10次每秒 
    }
}

# 定义交换机
ex_resource = Exchange('product_resource', type='direct')
ex_create = Exchange('product_create', type='direct')
ex_public = Exchange('product_public', type='direct')
ex_maskword = Exchange('maskword_filter', type='direct')
ex_store = Exchange('product_store', type='direct')

# 定义队列
task_queues = (
    Queue('product_social_queue', ex_resource, routing_key='social2product'),
    Queue('product_resource_queue', ex_resource, routing_key='product_resource'),
    Queue('product_listing_queue', ex_create, routing_key='product_listing'),
    Queue('product_maskword_queue', ex_maskword, routing_key='maskword_filter'),
    Queue('product_image_queue', ex_create, routing_key='product_image'),
    Queue('product_video_queue', ex_create, routing_key='product_video'),
    Queue('product_download_image_queue', ex_public, routing_key='product_download_image'),
    Queue('product_upload_image_queue', ex_public, routing_key='product_upload_image'),
    Queue('product_upload_video_queue', ex_public, routing_key='product_upload_video'),
    Queue('product_public_queue', ex_public, routing_key='product_public'),
    Queue('product_store_queue', ex_store, routing_key='product_store'),
)

# 路由配置
task_routes = {
    # social2product类任务
    'ai.business.social2product.tasks.*': {
        'queue': 'product_social_queue',
        'exchange': 'product_resource',
        'routing_key': 'social2product',
    },
    # 存储resource类任务
    'ai.business.resource.tasks.*': {
        'queue': 'product_resource_queue',
        'exchange': 'product_resource',
        'routing_key': 'product_resource',
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
    # 生成video类任务
    'ai.business.video.tasks.*': {
        'queue': 'product_video_queue',
        'exchange': 'product_create',
        'routing_key': 'product_video',
    },
    # download_img类任务
    'ai.business.download_img.tasks.*': {
        'queue': 'product_download_image_queue',
        'exchange': 'product_public',
        'routing_key': 'product_download_image',
    },
    # upload_img类任务
    'ai.business.upload_img.tasks.*': {
        'queue': 'product_upload_image_queue',
        'exchange': 'product_public',
        'routing_key': 'product_upload_image',
    },
    # upload_video类任务
    'ai.business.upload_video.tasks.*': {
        'queue': 'product_upload_video_queue',
        'exchange': 'product_public',
        'routing_key': 'product_upload_video',
    },
    # public类任务
    'ai.business.public.tasks.*': {
        'queue': 'product_public_queue',
        'exchange': 'product_public',
        'routing_key': 'product_public',
    },
    # storage类任务
    'ai.business.storage.tasks.*': {
        'queue': 'product_store_queue',
        'exchange': 'product_store',
        'routing_key': 'product_store',
    },
}
# 链式工作流配置
VERIFY_VERIFY_WORKFLOW_CHAIN = [
    'ai.business.resource.tasks.normal_store_resource',
    'ai.business.listing.tasks.normal_verify_listing',
    'ai.business.storage.tasks.normal_storage',
]
TOB_GENERATE_WORKFLOW_CHAIN = [
    'ai.business.resource.tasks.normal_store_resource',
    'ai.business.listing.tasks.normal_generate_listing',
    'ai.business.maskword.tasks.normal_filter_maskword',
    'ai.business.image.tasks.img_square',
    'ai.business.image.tasks.image_text_image',
    'ai.business.storage.tasks.normal_storage',
]
TOB_PUBLISH_WORKFLOW_CHAIN = [
    'ai.business.download_img.tasks.normal_download_image',
    'ai.business.upload_img.tasks.api_upload_image',
    'ai.business.public.tasks.api_publish_product',
]
TOC_GENERATE_WORKFLOW_CHAIN = [
    'ai.business.resource.tasks.normal_store_resource',
    'ai.business.listing.tasks.normal_generate_listing',
    'ai.business.maskword.tasks.normal_filter_maskword',
    'ai.business.image.tasks.img_square',
    'ai.business.image.tasks.image_text_image',
    'ai.business.storage.tasks.normal_storage',
]
CHAIN_MAP = {
    #商品有效性验证工作流
    "verify_to_verify": VERIFY_VERIFY_WORKFLOW_CHAIN,
    # 常规迁移工作流
    "amz_copy_ali": [
        'ai.business.resource.tasks.normal_store_resource',
        'ai.business.listing.tasks.listing_adapter',
        'ai.business.maskword.tasks.normal_filter_maskword'
    ],
    # ToB 智能迁移工作流_接口发布
    "amz_to_ali": TOB_GENERATE_WORKFLOW_CHAIN,
    "amz_to_1688": TOB_GENERATE_WORKFLOW_CHAIN,
    "ali_to_1688": TOB_GENERATE_WORKFLOW_CHAIN,
    "1688_to_1688": TOB_GENERATE_WORKFLOW_CHAIN,
    "ali_to_ali": TOB_GENERATE_WORKFLOW_CHAIN,
    "publish_to_b":TOB_PUBLISH_WORKFLOW_CHAIN,
    # ToC   智能迁移工作流_浏览器插件发布
    "taobao_to_jd_plugin": TOC_GENERATE_WORKFLOW_CHAIN,
        # "social_total": [
    #     'ai.business.resource.tasks.normal_store_resource'
    # ],
    # Social 社交平台迁移工作流
    # "social_pages": [
    #     'ai.business.listing.tasks.normal_generate_listing'
    # ],
    # "social_to_ali": [
    #     'ai.business.maskword.tasks.normal_filter_maskword',
    #     'ai.business.image.tasks.social_to_ali_image',
    #     'ai.business.upload_img.tasks.api_upload_image',
    #     'ai.business.public.tasks.api_publish_product',
    # ],

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


# 其他配置
worker_prefetch_multiplier = 1 # 每个 Worker 只预取 1 个任务，确保任务分配更均匀
worker_max_tasks_per_child = 500  # 每执行 500 个任务后重启 Worker 进程
task_time_limit = 3600  # 任务硬超时时间（秒）,超时的任务不会触发 task_postrun 信号
task_soft_time_limit = 3000  # 任务软超时时间（秒),比硬超时更优雅，可以保存中间结果

# Worker 稳定性配置
worker_max_memory_per_child = 200000  # Worker 子进程最大内存使用量（KB）
worker_disable_rate_limits = False  # 是否禁用速率限制:False(启用速率限制)
# worker_send_task_events = True  # 控制是否向监控系统发送任务状态事件(支持 Flower 监控、任务状态跟踪)

# 日志配置
worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'

# 根据环境导入对应的配置
if ENV == "production":
    from ai.config.celeryconfig_prod import *
else:
    from ai.config.celeryconfig_dev import *

