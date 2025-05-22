#!/usr/bin/env bash
# run_workers.sh

# 检查是否有 Celery worker 进程在运行
if pgrep -f "celery -A ai.core.celery_app worker" > /dev/null; then
    echo "Found running Celery workers. Stopping them first..."
    ./scripts/kill_process.sh "celery -A ai.core.celery_app worker"
    # 等待进程完全停止
    sleep 2
fi

# 激活虚拟环境
source .venv/bin/activate

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 确保日志目录存在
mkdir -p logs

# 读取社媒信息并按照page分组触发生成商品的工作流，1个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_social_queue -c 1 -n social_worker@%h-social > logs/social_worker.log 2>&1 &

# 源商品接收上报并写入缓存，5个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_src_queue -c 5 -n src_worker@%h-src > logs/src_worker.log 2>&1 &

# 基于LLM的API生成商品Listing，5个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_listing_queue -c 5 -n listing_worker@%h-listing > logs/listing_worker.log 2>&1 &

# 商品listing合规性检查，5个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_maskword_queue -c 5 -n maskword_worker@%h-maskword > logs/maskword_worker.log 2>&1 &

# 基于ComfyUI服务生成商品图片并存储到OSS服务，2个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_image_queue -c 1 -n image_worker@%h-image > logs/image_worker.log 2>&1 &

# 上传商品图片到alibaba图片库，2个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_upload_queue_ali -c 2 -n upload_ali_worker@%h-upload_ali > logs/upload_ali_worker.log 2>&1 &

# 发布商品信息到alibaba草稿箱，2个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_public_queue_ali -c 2 -n public_ali_worker@%h-public_ali > logs/public_ali_worker.log 2>&1 &

# 上传商品图片到1688相册，2个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_upload_queue_1688 -c 2 -n upload_1688_worker@%h-upload_1688 > logs/upload_1688_worker.log 2>&1 &

# 发布商品信息到1688商铺，2个进程
nohup celery -A ai.core.celery_app worker --loglevel=info -Q product_public_queue_1688 -c 2 -n public_1688_worker@%h-public_1688 > logs/public_1688_worker.log 2>&1 &

# 等待所有后台进程启动
sleep 2

# 显示所有 worker 的进程 ID
echo "Worker processes started:"
ps aux | grep "celery -A ai.core.celery_app worker" | grep -v grep

echo "--------------------------------"
echo "Worker logs:"
echo "./logs/social_worker.log"
echo "./logs/src_worker.log"
echo "./logs/listing_worker.log"
echo "./logs/maskword_worker.log"
echo "./logs/image_worker.log"
echo "./logs/upload_ali_worker.log"
echo "./logs/public_ali_worker.log"
echo "./logs/upload_1688_worker.log"
echo "./logs/public_1688_worker.log"
echo "--------------------------------"