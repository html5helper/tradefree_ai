# celeryconfig_dev.py - 开发环境配置
import os

# MySQL 配置
MYSQL_CONFIG = {
    "workflow_db": {
        'host': os.getenv("MYSQL_HOST", "47.253.40.62"),
        # 'host': os.getenv("MYSQL_HOST", "127.0.0.1"),
        'port': os.getenv("MYSQL_PORT", "3306"),
        'user':  os.getenv("MYSQL_USER", "tradefree"),
        'password': os.getenv("MYSQL_PASSWORD", "c1234%^5678C"),
        'database': 'celery_dev',
        'charset': 'utf8mb4',
    },
    "manager_db": {
        'host': os.getenv("MYSQL_HOST", "47.253.40.62"),
        # 'host': os.getenv("MYSQL_HOST", "127.0.0.1"),
        'port': os.getenv("MYSQL_PORT", "3306"),
        'user':  os.getenv("MYSQL_USER", "tradefree"),
        'password': os.getenv("MYSQL_PASSWORD", "c1234%^5678C"),
        'database': 'tf_dev',
        'charset': 'utf8mb4',
    }
}


# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_DB_BROKER = "2"
REDIS_DB_BACKEND = "3"
REDIS_DB_EMPLOYEE = "5"
broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BROKER}"
result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BACKEND}"
employee_catch = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_EMPLOYEE}"


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
    
    # normal product methods
    "product_listing": {
        "workflow_id": "b7b7e631-e5c0-4fa9-b105-17d2137f0b88",
        "api_key": "app-H0aaAlTrthGMrabomhiVGDVl"
    },
    "verify_listing": {
        "workflow_id": "8a086d07-aec1-4626-8b3d-4f68fabf8d9c",
        "api_key": "app-4KWMzLNpy5zpI8OnQqHHIXzo"
    },
    "maskword_filter": {
        "workflow_id": "530c3d1e-56de-4e94-ae41-349707cbfb8e",
        "api_key": "app-qbYXlCBIOLvAG5vfmL618BKN"
    },
    "img_square":{
        "workflow_id": "43ddbaa8-6454-4f78-974b-6ab87eb578fd",
        "api_key": "app-MzaXlkvilZkluXAFVuf7d6A7"
    },
    "text2img2download": {
        "workflow_id": "58a2386c-4743-40cb-ab1f-6cf1611c0997",
        "api_key": "app-HqaViz4DyXoszmUXX7Ln1dxp"
    },
    "img2text2img2download": {
        "workflow_id": "15057dc0-bef6-40ef-b745-499c867a61f4",
        "api_key": "app-aHottX9s7ptJQLEeU6SOL1MA"
    },
    "download_image":{
        "workflow_id": "b3312600-9a12-4cdc-9639-9085afe3b772",
        "api_key": "app-cUVu3yHyHSxkijm2RjBNc7x5"
    },
    "img_inpaint":{
        "workflow_id": "66153121-0883-45ac-9b9d-23670e471838",
        "api_key": "app-WXlHyJIbJNOEsScbzjnWJdZe"
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

# 日志配置
log_level = "DEBUG"