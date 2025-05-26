#!/usr/bin/env bash
# run_api_server.sh

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
source .venv/bin/activate

# 设置默认端口
DEFAULT_PORT=8081

# 从环境变量获取端口
if [ -n "$API_PORT" ]; then
    PORT=$API_PORT
    echo "Using port from API_PORT: $PORT"
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

# 启动 API 服务器
echo "--------------------------------"
echo "Starting API server on port $PORT..."
nohup "$PROJECT_ROOT/.venv/bin/uvicorn" ai.core.celery_api:api \
    --host 0.0.0.0 \
    --port $PORT \
    --reload \
    > logs/api_server.log 2>&1 &

# 等待进程启动
sleep 2

# 检查进程是否成功启动
pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/uvicorn ai.core.celery_api:api --host 0.0.0.0 --port $PORT")
if [ -n "$pids" ]; then
    # 计算进程数量
    pid_count=$(echo "$pids" | wc -l | tr -d ' ')
    # 格式化 PID 列表
    pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
    echo "--------------------------------"
    echo "API server started successfully!"
    echo "API server processes:"
    echo "API server($pid_count processes), pid=$pid_list"
    echo "--------------------------------"
    echo "Show API server log: tail -f ./logs/api_server.log"
    # sleep 2
    # tail -f ./logs/api_server.log
else
    echo "Error: API server failed to start!"
    echo "Check the log file for details: ./logs/api_server.log"
    exit 1
fi