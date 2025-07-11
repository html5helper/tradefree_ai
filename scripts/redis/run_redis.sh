#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
# 获取项目根目录（scripts目录的上级目录）
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

REDIS_PORT=6379
REDIS_CONFIG_FILE="$SCRIPT_DIR/redis_${REDIS_PORT}.conf"
REDIS_BIN=$(which redis-server)
# 统一从 conf 文件读取 dir 配置
REDIS_DATA_DIR=$(grep -E '^dir ' "$REDIS_CONFIG_FILE" | awk '{print $2}' | tr -d '"')
if [[ "$REDIS_DATA_DIR" != /* ]]; then
  REDIS_DATA_DIR="$PROJECT_ROOT/$REDIS_DATA_DIR"
fi

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo "脚本目录: $SCRIPT_DIR"
echo "项目根目录: $PROJECT_ROOT"
echo "配置文件: $REDIS_CONFIG_FILE"
echo "数据目录: $REDIS_DATA_DIR"

# === 检查 redis-server 是否存在 ===
if [ -z "$REDIS_BIN" ]; then
    log_error "redis-server 未安装或未在 PATH 中"
    echo "请安装 Redis: brew install redis"
    exit 1
fi

# === 检查配置文件是否存在 ===
if [ ! -f "$REDIS_CONFIG_FILE" ]; then
    log_error "Redis 配置文件不存在: $REDIS_CONFIG_FILE"
    echo "请先创建配置文件"
    exit 1
fi

# === 创建数据目录 ===
mkdir -p "$REDIS_DATA_DIR"
log_success "数据目录已创建/确认: $REDIS_DATA_DIR"

# === 智能检查 Redis 是否已运行 ===
check_redis_running() {
    # 方法1: 检查端口占用
    local port_pid=$(lsof -ti tcp:$REDIS_PORT 2>/dev/null | head -n 1)
    
    if [ -n "$port_pid" ]; then
        # 方法2: 检查进程名称
        local proc_name=$(ps -p "$port_pid" -o comm= 2>/dev/null | head -n 1)
        
        if [ -n "$proc_name" ] && echo "$proc_name" | grep -q "redis-server"; then
            return 0  # Redis 正在运行
        fi
    fi
    
    # 方法3: 尝试连接 Redis
    if redis-cli ping > /dev/null 2>&1; then
        return 0  # Redis 正在运行
    fi
    
    return 1  # Redis 未运行
}

# === 检查 Redis 运行状态 ===
if check_redis_running; then
    log_success "Redis 已经在运行中"
    
    # 显示当前 Redis 信息
    echo ""
    log_info "当前 Redis 状态:"
    if redis-cli ping > /dev/null 2>&1; then
        echo "连接状态: 正常"
        echo "端口: $REDIS_PORT"
        echo "数据目录: $REDIS_DATA_DIR"
        
        # 显示基本统计信息
        echo ""
        log_info "Redis 统计信息:"
        redis-cli info server | grep -E "(redis_version|uptime_in_seconds|connected_clients|used_memory_human)" 2>/dev/null || echo "无法获取统计信息"
        
        # 显示持久化状态
        echo ""
        log_info "持久化状态:"
        redis-cli info persistence | grep -E "(rdb_last_save_time|aof_enabled|aof_current_size)" 2>/dev/null || echo "无法获取持久化信息"
        
    else
        log_warning "Redis 进程存在但无法连接"
    fi
    
    echo ""
    log_info "如需重启 Redis，请先运行: ./scripts/redis/stop_redis.sh"
    exit 0
fi

# === 检查端口是否被其他程序占用 ===
port_pid=$(lsof -i tcp:$REDIS_PORT 2>/dev/null | grep LISTEN | awk '{print $2}' | head -n 1)
if [ -n "$port_pid" ]; then
    proc_name=$(ps -p "$port_pid" -o comm= 2>/dev/null | head -n 1)
    log_error "端口 $REDIS_PORT 被其他程序占用: $proc_name (PID: $port_pid)"
    echo "请手动停止该进程或使用其他端口"
    exit 1
fi

# === 启动 Redis ===
log_info "正在启动 Redis..."
echo "配置文件: $REDIS_CONFIG_FILE"
echo "数据目录: $REDIS_DATA_DIR"

# 切换到项目根目录，确保相对路径正确
cd "$PROJECT_ROOT"

# 启动 Redis 并捕获输出
log_info "启动命令: $REDIS_BIN $REDIS_CONFIG_FILE"
REDIS_OUTPUT=$($REDIS_BIN "$REDIS_CONFIG_FILE" 2>&1)
REDIS_EXIT_CODE=$?

# 等待启动
sleep 2

# 检查 Redis 是否成功启动
if [ $REDIS_EXIT_CODE -eq 0 ] && check_redis_running; then
    log_success "Redis 启动成功！"
    echo "端口: $REDIS_PORT"
    echo "数据目录: $REDIS_DATA_DIR"
    
    # 显示基本信息
    echo ""
    log_info "Redis 信息:"
    redis-cli info server | grep -E "(redis_version|uptime_in_seconds|connected_clients|used_memory_human)" 2>/dev/null || echo "无法获取 Redis 信息"
    
    echo ""
    log_info "持久化状态:"
    redis-cli info persistence | grep -E "(rdb_last_save_time|aof_enabled|aof_current_size)" 2>/dev/null || echo "无法获取持久化信息"
    
    # 检查持久化文件
    echo ""
    log_info "持久化文件检查:"
    if [ -f "$REDIS_DATA_DIR/dump.rdb" ]; then
        rdb_size=$(du -h "$REDIS_DATA_DIR/dump.rdb" | cut -f1)
        echo "RDB 文件: 存在 (${rdb_size})"
    else
        echo "RDB 文件: 不存在 (首次启动)"
    fi
    
    if [ -f "$REDIS_DATA_DIR/appendonly.aof" ]; then
        aof_size=$(du -h "$REDIS_DATA_DIR/appendonly.aof" | cut -f1)
        echo "AOF 文件: 存在 (${aof_size})"
    else
        echo "AOF 文件: 不存在 (首次启动)"
    fi
    
    echo ""
    log_success "Redis 已准备就绪！"
    echo "管理命令: ./scripts/redis/redis_manager.sh help"
    
else
    log_error "Redis 启动失败"
    echo "退出代码: $REDIS_EXIT_CODE"
    if [ -n "$REDIS_OUTPUT" ]; then
        echo "Redis 输出:"
        echo "$REDIS_OUTPUT"
    fi
    echo ""
    log_info "故障排除建议:"
    echo "1. 检查端口 $REDIS_PORT 是否被占用"
    echo "2. 检查配置文件语法: $REDIS_CONFIG_FILE"
    echo "3. 检查数据目录权限: $REDIS_DATA_DIR"
    echo "4. 查看详细日志: tail -f $REDIS_DATA_DIR/redis.log"
    exit 1
fi