#!/usr/bin/env bash
# run_flower.sh

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
source .venv/bin/activate

# 设置默认端口
DEFAULT_PORT=5555

# 从环境变量获取端口
if [ -n "$FLOWER_PORT" ]; then
    PORT=$FLOWER_PORT
    echo "Using port from FLOWER_PORT: $PORT"
else
    PORT=$DEFAULT_PORT
    echo "Using default port: $PORT"
fi

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# 设置环境变量来抑制 urllib3 警告
export PYTHONWARNINGS="ignore:urllib3"

# 确保日志目录存在
mkdir -p logs

# 检查端口是否被占用
echo "--------------------------------"
echo "Checking port $PORT..."
PIDS=( $(lsof -ti tcp:${PORT} || true) )
if [[ ${#PIDS[@]} -gt 0 ]]; then
    echo "Port ${PORT} in use by PIDs: ${PIDS[*]}"
    echo "Killing them..."
    kill -9 "${PIDS[@]}"
    sleep 1
    echo "Old process(es) killed."
else
    echo "Port ${PORT} is free."
fi

# 启动 Flower
echo "--------------------------------"
echo "Starting Flower on port $PORT..."
nohup "$PROJECT_ROOT/.venv/bin/celery" \
    -A ai.core.celery_app \
    flower \
    --port=$PORT \
    --address=0.0.0.0 \
    > logs/flower.log 2>&1 &

# 等待进程启动
sleep 2

# 检查进程是否成功启动
pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app flower --port=$PORT")
if [ -n "$pids" ]; then
    # 计算进程数量
    pid_count=$(echo "$pids" | wc -l | tr -d ' ')
    # 格式化 PID 列表
    pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
    echo "--------------------------------"
    echo "Flower started successfully!"
    echo "Flower processes:"
    echo "Flower($pid_count processes), pid=$pid_list"
    echo "--------------------------------"
    echo "Show Flower log: tail -f ./logs/flower.log"
    tail -f ./logs/flower.log
else
    echo "Error: Flower failed to start!"
    echo "Check the log file for details: tail -f ./logs/flower.log"
    exit 1
fi