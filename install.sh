#!/bin/bash

# 设置错误时退出
set -e

echo "开始安装 Tradefree AI 任务系统..."

# 检查 Python 版本
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$python_version" < "3.8" ]]; then
    echo "错误: 需要 Python 3.8 或更高版本"
    exit 1
fi

# 检查是否已存在虚拟环境
if [ -d "venv" ]; then
    echo "警告: 虚拟环境已存在，将重新创建"
    rm -rf venv
fi

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装 Python 依赖..."
pip install -r requirements.txt

# 安装 MySQL
echo "检查 MySQL..."
if ! command -v mysql &> /dev/null; then
    echo "MySQL 未安装，请先安装 MySQL"
    exit 1
fi

# 安装 Redis
echo "检查 Redis..."
if ! command -v redis-server &> /dev/null; then
    echo "Redis 未安装，请先安装 Redis"
    exit 1
fi

# 创建必要的目录
echo "创建项目目录..."
mkdir -p logs
mkdir -p config
mkdir -p backups

# 初始化数据库
echo "初始化数据库..."
mysql -u root -p < scripts/setup_db.sh

# 设置权限
echo "设置脚本权限..."
chmod +x run.sh
chmod +x scripts/*.sh

echo "安装完成！"
echo "请按以下步骤启动服务："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 启动服务: ./run.sh"
echo ""
echo "注意：每次启动服务前都需要先激活虚拟环境" 