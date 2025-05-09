export FLOWER_UNAUTHENTICATED_API=1

celery -A ai.core.celery_app flower --port=5555

# 在浏览器中打开 http://localhost:5555