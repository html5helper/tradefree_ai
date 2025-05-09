# celeryconfig.py
from kombu import Exchange, Queue

# Broker 和 Backend 配置
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"

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

# 并发度建议通过worker启动参数 -c 指定