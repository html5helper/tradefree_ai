export FLOWER_UNAUTHENTICATED_API=1

nohup celery -A ai.core.celery_app flower --port=5555 > logs/flower.log 2>&1 &

# 在浏览器中打开 http://localhost:5555