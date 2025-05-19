#!/usr/bin/env bash
# run_flower.sh

# 激活虚拟环境
source .venv/bin/activate

# 检查是否有 Flower 进程在运行
if pgrep -f "celery -A ai.core.celery_app flower" > /dev/null; then
    echo "Found running Celery flower. Stopping it first..."
    ./scripts/kill_process.sh "celery -A ai.core.celery_app flower"
    # 等待进程完全停止
    sleep 2
fi

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 设置环境变量
export FLOWER_UNAUTHENTICATED_API=1
export PYTHONWARNINGS="ignore:urllib3"

# 确保日志目录存在
mkdir -p logs

# 启动 Flower 并将日志输出到文件
echo "Starting Flower..."
nohup celery -A ai.core.celery_app flower --port=5555 > logs/flower.log 2>&1 &

# 等待进程启动
sleep 5

# 检查进程是否成功启动
if ! pgrep -f "celery -A ai.core.celery_app flower" > /dev/null; then
    echo "Error: Flower failed to start!"
    echo "Check the log file for details: ./logs/flower.log"
    exit 1
fi

echo "--------------------------------"
echo "Flower started successfully!"
echo "Process ID: $(pgrep -f "celery -A ai.core.celery_app flower")"
echo "Log file: ./logs/flower.log"
echo "--------------------------------"
echo "Visit Flower dashboard at: http://localhost:5555"
echo "--------------------------------"

tail -f ./logs/flower.log