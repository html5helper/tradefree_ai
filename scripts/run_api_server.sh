#!/usr/bin/env bash
# run_api_server.sh

# 激活虚拟环境
source .venv/bin/activate

set -euo pipefail
IFS=$'\n\t'

# 检查是否有 API 服务器进程在运行
# 1. 检查并 kill 旧进程
PORT=8081
PIDS=( $(lsof -ti tcp:${PORT} || true) )
if [[ ${#PIDS[@]} -gt 0 ]]; then
    echo "🔍 Port ${PORT} in use by PIDs: ${PIDS[*]}"
    echo "🔪 Killing them..."
    kill -9 "${PIDS[@]}"
    sleep 1
    echo "✅ Old process(es) killed."
else
    echo "✅ Port ${PORT} is free."
fi

sleep 5

# 确保日志目录存在
mkdir -p logs

# 2. 启动 uvicorn
echo "🚀 Starting API server on port ${PORT}..."
nohup python -m uvicorn ai.core.celery_api:api \
  --host 0.0.0.0 \
  --port 8081 \
  --reload \
  --log-level info \
  --access-log \
  > logs/api_server.log 2>&1 &

echo "✅ API server started. Logs at './logs/api_server.log'"

# 查看日志
# tail -f ./logs/api_server.log