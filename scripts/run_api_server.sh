#!/usr/bin/env bash
# run_api_server.sh

# 检查是否有 API 服务器进程在运行
if pgrep -f "uvicorn ai.core.celery_api:api" > /dev/null; then
    echo "Found running API server. Stopping it first..."
    ./scripts/kill_process.sh "uvicorn ai.core.celery_api:api"
    # 等待进程完全停止
    sleep 2
fi

# 激活虚拟环境
source .venv/bin/activate

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 确保日志目录存在
mkdir -p logs

# 启动 API 服务器并将日志输出到文件
nohup python -m uvicorn ai.core.celery_api:api \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --log-level info \
  --access-log \
  > logs/api_server.log 2>&1 &

# 等待进程启动
sleep 2

# 显示 API 服务器进程 ID
echo "API server started:"
ps aux | grep "uvicorn ai.core.celery_api:api" | grep -v grep

echo "--------------------------------"
echo "API server log:"
echo "./logs/api_server.log"
echo "--------------------------------"

tail -f ./logs/api_server.log