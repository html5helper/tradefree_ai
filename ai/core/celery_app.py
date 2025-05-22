from celery import Celery

# 创建Celery应用，指定配置模块
app = Celery('myapp')
app.config_from_object('ai.config.celeryconfig')

# 自动发现任务模块（可根据实际项目结构调整）
app.autodiscover_tasks([
    'ai.business.resource',
    'ai.business.listing',
    'ai.business.maskword',
    'ai.business.image',
    'ai.business.upload_img',
    'ai.business.public',
    'ai.business.social2product'
])

# 引入监听器来记录任务历史到MYSQL的task_history表
import ai.core.history.task_listener