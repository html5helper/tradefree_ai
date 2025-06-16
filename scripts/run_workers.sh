#!/usr/bin/env bash
# run_workers.sh

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
source .venv/bin/activate

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# 设置环境变量来抑制 urllib3 警告
export PYTHONWARNINGS="ignore:urllib3"

# 确保日志目录存在
mkdir -p logs

# 定义 worker 配置
workers=(
    "social:product_social_queue -c 1 -n social_worker@%h-social"
    "src:product_src_queue -c 5 -n src_worker@%h-src"
    "listing:product_listing_queue -c 5 -n listing_worker@%h-listing"
    "maskword:product_maskword_queue -c 5 -n maskword_worker@%h-maskword"
    "image:product_image_queue -c 1 -n image_worker@%h-image"
    "upload_ali:product_upload_queue_ali -c 2 -n upload_ali_worker@%h-upload_image_ali"
    "public_ali:product_public_queue_ali -c 2 -n public_ali_worker@%h-public_ali"
    "upload_1688:product_upload_queue_1688 -c 2 -n upload_1688_worker@%h-upload_image_1688"
    "video:product_video_queue -c 1 -n video_worker@%h-video"
    "upload_video_1688:product_upload_video_queue_1688 -c 2 -n upload_video_1688_worker@%h-upload_video_1688"
    "public_1688:product_public_queue_1688 -c 2 -n public_1688_worker@%h-public_1688"
)

# 停止所有现有的 worker 进程
echo "--------------------------------"
echo "Stopping existing workers..."

# 首先尝试正常终止进程
for worker_config in "${workers[@]}"; do
    IFS=':' read -r worker_name worker_cmd <<< "$worker_config"
    pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app worker.*$worker_cmd")
    if [ -n "$pids" ]; then
        # 计算进程数量
        pid_count=$(echo "$pids" | wc -l | tr -d ' ')
        # 格式化 PID 列表
        pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
        echo "Stopping $worker_name(1 main , $((pid_count-1)) sub), pid=$pid_list"
        for pid in $pids; do
            kill -TERM $pid 2>/dev/null
        done
    fi
done

# 等待进程正常终止
sleep 2

# 检查是否还有进程在运行，如果有则强制终止
echo "--------------------------------"
for worker_config in "${workers[@]}"; do
    IFS=':' read -r worker_name worker_cmd <<< "$worker_config"
    pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app worker.*$worker_cmd")
    if [ -n "$pids" ]; then
        # 计算进程数量
        pid_count=$(echo "$pids" | wc -l | tr -d ' ')
        # 格式化 PID 列表
        pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
        echo "Force stopping $worker_name(1 main , $((pid_count-1)) sub), pid=$pid_list"
        for pid in $pids; do
            kill -9 $pid 2>/dev/null
        done
    fi
done

# 最后检查是否还有任何 Celery worker 进程在运行
echo "--------------------------------"
remaining_pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app worker")
if [ -n "$remaining_pids" ]; then
    # 计算进程数量
    pid_count=$(echo "$remaining_pids" | wc -l | tr -d ' ')
    # 格式化 PID 列表
    pid_list=$(echo "$remaining_pids" | tr '\n' ',' | sed 's/,$//')
    echo "Warning: Some worker processes are still running ($pid_count processes)"
    echo "Attempting to force stop all remaining workers, pid=$pid_list"
    for pid in $remaining_pids; do
        kill -9 $pid 2>/dev/null
    done
    sleep 1
fi

# 启动所有 worker
echo "--------------------------------"
echo "Starting workers..."
for worker_config in "${workers[@]}"; do
    IFS=':' read -r worker_name worker_cmd <<< "$worker_config"
    echo "Starting $worker_name worker..."
    nohup "$PROJECT_ROOT/.venv/bin/celery" -A ai.core.celery_app worker \
        --loglevel=info \
        -Q $worker_cmd \
        > "logs/${worker_name}_worker.log" 2>&1 &
done

# 等待所有 worker 启动
sleep 5

# 检查所有 worker 是否成功启动
echo "Checking worker status..."
all_started=true
for worker_config in "${workers[@]}"; do
    IFS=':' read -r worker_name worker_cmd <<< "$worker_config"
    if ! pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app worker.*$worker_cmd" > /dev/null; then
        echo "Error: $worker_name worker failed to start!"
        echo "Check the log file for details: ./logs/${worker_name}_worker.log"
        all_started=false
    fi
done

if [ "$all_started" = true ]; then
    echo "--------------------------------"
    echo "All workers started successfully!"
    echo "Worker processes:"
    for worker_config in "${workers[@]}"; do
        IFS=':' read -r worker_name worker_cmd <<< "$worker_config"
        pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app worker.*$worker_cmd")
        if [ -n "$pids" ]; then
            # 计算进程数量
            pid_count=$(echo "$pids" | wc -l | tr -d ' ')
            # 格式化 PID 列表
            pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
            # 提取并发数
            concurrency=$(echo "$worker_cmd" | grep -o -- '-c [0-9]\+' | cut -d' ' -f2)
            echo "$worker_name(1 main , $((pid_count-1)) sub), pid=$pid_list"
        fi
    done
    echo "--------------------------------"
    echo "Worker logs:"
    for worker_config in "${workers[@]}"; do
        IFS=':' read -r worker_name worker_cmd <<< "$worker_config"
        echo "./logs/${worker_name}_worker.log"
    done
    echo "--------------------------------"
else
    echo "Some workers failed to start. Please check the logs above."
    exit 1
fi