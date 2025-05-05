from celery import Celery

# Initialize Celery app
app = Celery('ai',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['ai.business.social2product.tasks'])

# Optional configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
) 