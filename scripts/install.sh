#!/bin/bash

# 创建虚拟环境
echo "Creating virtual environment..."
python3 -m venv .venv

# 激活虚拟环境
echo "Activating virtual environment..."
source .venv/bin/activate

# 安装依赖
echo "Installing dependencies..."
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 创建必要的目录
echo "Creating necessary directories..."
mkdir -p ai/core ai/tasks ai/config

echo "Installation completed!"
echo "To activate the virtual environment, run: source .venv/bin/activate" 