#!/usr/bin/env bash
# run_flower.sh - Flower 启动脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

source .venv/bin/activate

DEFAULT_PORT=5555
if [ -n "$FLOWER_PORT" ]; then
    PORT=$FLOWER_PORT
    echo "Using port from FLOWER_PORT: $PORT"
else
    PORT=$DEFAULT_PORT
    echo "Using default port: $PORT"
fi

export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT
export PYTHONWARNINGS="ignore:urllib3"

# 定义数据文件路径，与 flower_manager.sh 保持一致
DATA_FILE="$PROJECT_ROOT/data/flower/flower"
LOG_FILE="$PROJECT_ROOT/logs/flower.log"

mkdir -p "$(dirname "$DATA_FILE")" "$(dirname "$LOG_FILE")"

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

echo "--------------------------------"
echo "Starting Flower on port $PORT..."
echo "Data file: $DATA_FILE"
echo "Log file: $LOG_FILE"

nohup "$PROJECT_ROOT/.venv/bin/celery" \
    -A ai.core.celery_app \
    flower \
    --port=$PORT \
    --address=0.0.0.0 \
    --persistent=True \
    --db="$DATA_FILE" \
    --max_tasks=10000 \
    --enable_events=True \
    --auto_refresh=True \
    --task_ignore_result=False \
    --task_track_started=True \
    --page_size=50 \
    --natural_time=True \
    > "$LOG_FILE" 2>&1 &

sleep 2
pids=$(pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app flower --port=$PORT")
if [ -n "$pids" ]; then
    pid_count=$(echo "$pids" | wc -l | tr -d ' ')
    pid_list=$(echo "$pids" | tr '\n' ',' | sed 's/,$//')
    echo "--------------------------------"
    echo "Flower started successfully!"
    echo "Flower processes:"
    echo "Flower($pid_count processes), pid=$pid_list"
    echo "--------------------------------"
    echo "Show Flower log: tail -f $LOG_FILE"
    echo "Access URL: http://localhost:$PORT"
else
    echo "Error: Flower failed to start!"
    echo "Check the log file for details: tail -f $LOG_FILE"
    exit 1
fi 