# celeryconfig_prod.py - 生产环境配置
import os

# MySQL 配置
MYSQL_CONFIG = {
    "workflow_db": {
        'host': os.getenv("MYSQL_HOST", "127.0.0.1"),
        'port': os.getenv("MYSQL_PORT", "3306"),
        'user':  os.getenv("MYSQL_USER", "tradefree"),
        'password': os.getenv("MYSQL_PASSWORD", "c1234%^5678C"),
        'database': 'celery_prod',
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

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_DB_BROKER = "0"
REDIS_DB_BACKEND = "1"
REDIS_DB_EMPLOYEE = "4"
broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BROKER}"
result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BACKEND}"
employee_catch = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_EMPLOYEE}"


# Dify 工作流配置
DIFY_BASE_URL = "http://dify.tradefree.ai/v1"
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
    "img2video":{
        "workflow_id":"97b580a2-e800-4d92-bd1c-5cc4d6786ad7",
        "api_key":"app-9A8tchJLEBjyCuftThxVxUr8"
    },
    "upload_photos": {
        "workflow_id": "8bae616a-8be9-496b-b087-a300cd660210",
        "api_key": "app-Gxld5HWVZPOWYPu9B8BMrv9d"
    },
    "upload_video": {
        "workflow_id": "9d40d789-2823-4e71-bda3-23b7992df032",
        "api_key": "app-O5sLeZAN0upNHFpSzqiZnc7I"
    },
    "publish_product": {
        "workflow_id": "1aeeb7f4-c7ff-48e0-9f29-749d764d5637",
        "api_key": "app-q7bXCU359F464cgUMz5Q0zhK"
    }
}
# 日志配置
log_level = "INFO"
