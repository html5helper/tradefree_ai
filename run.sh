#!/bin/bash

# 设置错误时退出
set -e

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "错误: 未检测到虚拟环境"
    echo "请先激活虚拟环境: source venv/bin/activate"
    exit 1
fi

# 检查虚拟环境路径是否正确
if [[ "$VIRTUAL_ENV" != *"tradefree_ai/venv"* ]]; then
    echo "错误: 虚拟环境路径不正确"
    echo "当前虚拟环境: $VIRTUAL_ENV"
    echo "请确保在项目根目录下运行: source venv/bin/activate"
    exit 1
fi

# 检查 Redis 是否运行
if ! redis-cli ping &> /dev/null; then
    echo "启动 Redis..."
    redis-server --daemonize yes
    sleep 2  # 等待 Redis 启动
fi

# 检查 MySQL 是否运行
if ! mysqladmin ping &> /dev/null; then
    echo "错误: MySQL 未运行，请先启动 MySQL"
    exit 1
fi

# 检查 Python 依赖
echo "检查 Python 依赖..."
pip install -r requirements.txt

# 启动 Celery Worker
echo "启动 Celery Worker..."
celery -A src.tasks.worker worker --loglevel=info --concurrency=4 &

# 启动 API 服务
echo "启动 API 服务..."
python src/main.py &

# 等待所有后台进程
wait 