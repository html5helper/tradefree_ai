# celeryconfig.py
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True


# 定义交换机和队列
default_exchange = Exchange('default', type='direct')
social2product_exchange = Exchange('social2product', type='direct')
reporting_exchange = Exchange('reporting', type='direct')
task_queues = (
    # 默认队列
    Queue('default', default_exchange, routing_key='default'),
    # social2product 工作流相关任务队列
    Queue('social2product', social2product_exchange, routing_key='social2product'),
    # 报表/统计相关任务队列
    Queue('reporting', reporting_exchange, routing_key='reporting'),
)

# 根据任务名称将任务路由到不同队列
task_routes = {
    # 所有 social2product 相关的任务都走 social2product 队列
    'ai.business.social2product.tasks.*': {
        'queue':        'social2product',
        'exchange':     'social2product',
        'routing_key':  'social2product',
    },
    # 报表统计类任务走 reporting 队列
    'ai.business.reporting.tasks.*': {
        'queue':       'reporting',
        'exchange':    'reporting',
        'routing_key': 'reporting',
    },
    # 其他所有任务都走 default
    '*': {
        'queue':       'default',
        'exchange':    'default',
        'routing_key': 'default',
    },
}