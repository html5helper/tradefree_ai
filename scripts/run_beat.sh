#!/usr/bin/env bash
# run_beat.sh

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

# 停止所有现有的 beat 进程
echo "--------------------------------"
echo "Stopping existing beat..."

# 首先尝试正常终止进程
pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app beat")
if [ -n "$pids" ]; then
    # 计算进程数量
    pid_count=$(echo "$pids" | wc -l | tr -d ' ')
    # 格式化 PID 列表
    pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
    echo "Stopping beat($pid_count processes), pid=$pid_list"
    for pid in $pids; do
        kill -TERM $pid 2>/dev/null
    done
fi

# 等待进程正常终止
sleep 2

# 检查是否还有进程在运行，如果有则强制终止
echo "--------------------------------"
pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app beat")
if [ -n "$pids" ]; then
    # 计算进程数量
    pid_count=$(echo "$pids" | wc -l | tr -d ' ')
    # 格式化 PID 列表
    pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
    echo "Force stopping beat($pid_count processes), pid=$pid_list"
    for pid in $pids; do
        kill -9 $pid 2>/dev/null
    done
fi

# 启动 beat
echo "--------------------------------"
echo "Starting beat..."
nohup "$PROJECT_ROOT/.venv/bin/celery" -A ai.core.celery_app beat \
    --loglevel=info \
    > logs/beat.log 2>&1 &

# 等待进程启动
sleep 2

# 检查进程是否成功启动
pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app beat")
if [ -n "$pids" ]; then
    # 计算进程数量
    pid_count=$(echo "$pids" | wc -l | tr -d ' ')
    # 格式化 PID 列表
    pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
    echo "--------------------------------"
    echo "Beat started successfully!"
    echo "Beat processes:"
    echo "beat($pid_count processes), pid=$pid_list"
    echo "--------------------------------"
    echo "Beat log: ./logs/beat.log"
    echo "--------------------------------"
    tail -f ./logs/beat.log
else
    echo "Error: Beat failed to start!"
    echo "Check the log file for details: ./logs/beat.log"
    exit 1
fi
