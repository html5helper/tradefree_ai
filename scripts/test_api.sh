#!/bin/bash

# 设置错误时退出
set -e

echo "=== 开始 API 测试 ==="

# 检查虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    echo "错误: 未检测到虚拟环境"
    echo "请先激活虚拟环境: source venv/bin/activate"
    exit 1
fi

# 检查 Python 版本
python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$python_version" != "3.10" ]]; then
    echo "错误: 需要 Python 3.10，当前版本: $python_version"
    exit 1
fi

# 检查服务是否运行
echo "检查 API 服务状态..."
if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo "错误: API 服务未运行"
    echo "请先启动服务: python src/main.py"
    exit 1
fi

echo "API 服务运行正常，开始测试..."

# 设置环境变量
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 运行测试
echo "执行测试脚本..."
python tests/api/test_workflow_api.py

# 检查测试结果
if [ $? -eq 0 ]; then
    echo "=== 测试通过 ==="
    echo "所有测试用例执行成功"
else
    echo "=== 测试失败 ==="
    echo "请检查日志文件获取详细信息"
    exit 1
fi 