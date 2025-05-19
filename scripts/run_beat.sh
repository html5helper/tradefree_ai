#!/usr/bin/env bash
# run_beat.sh

# 检查是否有 Celery beat 进程在运行
if pgrep -f "celery -A ai.core.celery_app beat" > /dev/null; then
    echo "Found running Celery beat. Stopping it first..."
    ./scripts/kill_process.sh "celery -A ai.core.celery_app beat"
    # 等待进程完全停止
    sleep 2
fi

# 激活虚拟环境
source .venv/bin/activate

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 设置环境变量来抑制 urllib3 警告
export PYTHONWARNINGS="ignore:urllib3"

# 确保日志目录存在
mkdir -p logs

# 启动 Celery beat 并将日志输出到文件
echo "Starting Celery beat..."
nohup celery -A ai.core.celery_app beat \
  --loglevel=info \
  > logs/beat.log 2>&1 &

# 等待进程启动
sleep 2

# 检查进程是否成功启动
if ! pgrep -f "celery -A ai.core.celery_app beat" > /dev/null; then
    echo "Error: Celery beat failed to start!"
    echo "Check the log file for details: ./logs/beat.log"
    exit 1
fi

echo "--------------------------------"
echo "Celery beat started successfully!"
echo "Process ID: $(pgrep -f "celery -A ai.core.celery_app beat")"
echo "Log file: ./logs/beat.log"
echo "--------------------------------"
tail -f ./logs/beat.log
