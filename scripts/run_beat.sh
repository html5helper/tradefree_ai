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

# 确保日志目录存在
mkdir -p logs

# 启动 Celery beat 并将日志输出到文件
nohup celery -A ai.core.celery_app beat \
  --loglevel=info \
  > logs/beat.log 2>&1 &

# 等待进程启动
sleep 2

# 显示 Celery beat 进程 ID
echo "Celery beat started:"
ps aux | grep "celery -A ai.core.celery_app beat" | grep -v grep

echo "--------------------------------"
echo "Celery beat log:"
echo "./logs/beat.log"
echo "--------------------------------"

tail -f ./logs/beat.log