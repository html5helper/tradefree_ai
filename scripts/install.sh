#!/bin/bash

# 创建虚拟环境
echo "Creating virtual environment..."
python3 -m venv .venv

# 激活虚拟环境
echo "Activating virtual environment..."
source .venv/bin/activate

# 安装依赖
echo "Installing dependencies..."
# 先尝试阿里云源
# pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ || \
# 如果失败则使用官方源
pip install -r requirements.txt -i https://pypi.org/simple/



echo "Installation completed!"
echo "To activate the virtual environment, run: source .venv/bin/activate" 