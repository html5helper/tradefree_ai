#!/bin/bash

export PYTHONPATH=$(pwd)

# 读取社媒信息并按照page分组触发生成商品的工作流，1个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_social_queue -c 1 -n social_worker@%h &

# 源商品接收上报并写入缓存，5个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_src_queue -c 5 -n src_worker@%h &

# 基于LLM的API生成商品Listing，5个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_listing_queue -c 5 -n listing_worker@%h &

# 基于ComfyUI服务生成商品图片并存储到OSS服务，2个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_image_queue -c 1 -n image_worker@%h &

# 上传商品图片到alibaba图片库，2个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_upload_queue_ali -c 2 -n upload_ali_worker@%h &

# 发布商品信息到alibaba草稿箱，2个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_public_queue_ali -c 2 -n public_ali_worker@%h &

# 上传商品图片到1688相册，2个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_upload_queue_1688 -c 2 -n upload_1688_worker@%h &

# 发布商品信息到1688商铺，2个进程
celery -A ai.core.celery_app worker --loglevel=info -Q product_public_queue_1688 -c 2 -n public_1688_worker@%h &

wait 