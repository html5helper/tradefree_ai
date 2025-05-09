#!/usr/bin/env bash
# run_api_server.sh

# 激活虚拟环境
source .venv/bin/activate

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

python -m uvicorn ai.core.celery_api:api \
  --host 0.0.0.0 \
  --port 8000 \
  --reload