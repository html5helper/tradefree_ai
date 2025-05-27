#!/usr/bin/env bash
# install.sh

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 检查 Python 版本
echo "--------------------------------"
echo "Checking Python version..."
if ! command -v python3.9 &> /dev/null; then
    echo "Error: python3.9 is not installed"
    echo "Please install Python 3.9.19 and try again"
    echo "You can download it from: https://www.python.org/downloads/release/python-3919/"
    exit 1
fi

PYTHON_VERSION=$(python3.9 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.9.19"

if [ "$PYTHON_VERSION" != "$REQUIRED_VERSION" ]; then
    echo "Warning: Current Python version is $PYTHON_VERSION"
    echo "Recommended Python version is $REQUIRED_VERSION"
    echo "Please install Python $REQUIRED_VERSION and try again"
    echo "You can download it from: https://www.python.org/downloads/release/python-3919/"
    exit 1
fi

echo "Python version $PYTHON_VERSION is compatible"

# 检查 pip 版本
echo "--------------------------------"
echo "Checking pip version..."
python3.9 -m pip --version

# 创建虚拟环境
echo "--------------------------------"
echo "Creating virtual environment..."
python3.9 -m venv .venv

# 激活虚拟环境
echo "--------------------------------"
echo "Activating virtual environment..."
source .venv/bin/activate

# 升级 pip
echo "--------------------------------"
echo "Upgrading pip..."
"$PROJECT_ROOT/.venv/bin/pip" install --upgrade pip

# 安装依赖
echo "--------------------------------"
echo "Installing dependencies..."
# 先尝试阿里云源
# "$PROJECT_ROOT/.venv/bin/pip" install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ || \
# 如果失败则使用官方源
"$PROJECT_ROOT/.venv/bin/pip" install -r requirements.txt -i https://pypi.org/simple/

# 安装 uvicorn
echo "--------------------------------"
echo "Installing uvicorn..."
"$PROJECT_ROOT/.venv/bin/pip" install uvicorn -i https://pypi.org/simple/

# 添加环境变量到 activate 脚本
echo "--------------------------------"
echo "Adding environment variables to activate script..."
ACTIVATE_SCRIPT="$PROJECT_ROOT/.venv/bin/activate"

# 在 deactivate 函数中添加清除环境变量的代码
sed -i '' '/unset VIRTUAL_ENV/a\
    # 清除环境变量\
    unset ENV\
    unset API_PORT\
    unset FLOWER_PORT\
    unset API_KEY\
    unset MYSQL_HOST\
    unset MYSQL_PORT\
    unset MYSQL_USER\
    unset MYSQL_PASSWORD\
    unset PYTHONPATH\
    unset PYTHONWARNINGS' "$ACTIVATE_SCRIPT"

# 在文件末尾添加环境变量设置
cat << 'EOF' >> "$ACTIVATE_SCRIPT"

# 设置环境变量
export ENV="development"
export API_PORT="8081"
export FLOWER_PORT="5555"

# 设置 API 密钥
export API_KEY="token2_def456"

# 设置 MySQL 连接信息
export MYSQL_HOST="127.0.0.1"
export MYSQL_PORT="3306"
export MYSQL_USER="tradefree"
export MYSQL_PASSWORD="c1234%^5678C"

# 设置 Python 相关环境变量
export PYTHONPATH="${PYTHONPATH:-}:${VIRTUAL_ENV}/.."
export PYTHONWARNINGS="ignore:urllib3"
EOF

echo "--------------------------------"
echo "Installation completed!"
echo "--------------------------------"
echo "To activate the virtual environment, run:"
echo "source .venv/bin/activate"
echo "--------------------------------" 