#!/bin/bash

# 设置错误时退出
set -e

echo "开始安装 Tradefree AI 任务系统..."

# 检查 Python 3.10 是否安装
if ! command -v python3.10 &> /dev/null; then
    echo "错误: Python 3.10 未安装"
    echo "请先安装 Python 3.10:"
    echo "1. macOS: brew install python@3.10"
    echo "2. Ubuntu: sudo apt install python3.10"
    echo "3. CentOS: sudo yum install python3.10"
    exit 1
fi

# 检查 Python 版本
python_version=$(python3.10 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$python_version" != "3.10" ]]; then
    echo "错误: 需要 Python 3.10，当前版本: $python_version"
    exit 1
fi

# 检查是否已存在虚拟环境
if [ -d "venv" ]; then
    echo "警告: 虚拟环境已存在，将重新创建"
    rm -rf venv
fi

# 创建虚拟环境
echo "创建 Python 3.10 虚拟环境..."
python3.10 -m venv venv

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装 Python 依赖..."
pip install -r requirements.txt

# 创建必要的目录
echo "创建项目目录..."
mkdir -p logs
mkdir -p config
mkdir -p tests/api

# 设置权限
echo "设置脚本权限..."
chmod +x scripts/*.sh

echo "安装完成！"
echo "请按以下步骤启动服务："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 启动服务: python src/main.py"
echo ""
echo "注意：每次启动服务前都需要先激活虚拟环境" 