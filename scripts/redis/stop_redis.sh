#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
# 获取项目根目录（scripts目录的上级目录）
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

REDIS_PORT=6379
REDIS_CONFIG_FILE="$SCRIPT_DIR/redis_${REDIS_PORT}.conf"
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

# 检查 Redis 是否运行
check_redis_running() {
    local port_pid=$(lsof -ti tcp:$REDIS_PORT 2>/dev/null | head -n 1)
    
    if [ -n "$port_pid" ]; then
        local proc_name=$(ps -p "$port_pid" -o comm= 2>/dev/null | head -n 1)
        
        if [ -n "$proc_name" ] && echo "$proc_name" | grep -q "redis-server"; then
            echo "$port_pid"
            return 0
        fi
    fi
    
    # 尝试连接 Redis
    if redis-cli ping > /dev/null 2>&1; then
        # 如果能连接但找不到进程，可能是网络连接
        echo "connected"
        return 0
    fi
    
    return 1
}

log_info "停止 Redis 服务器 (端口: $REDIS_PORT)..."

# 检查 Redis 是否运行
REDIS_STATUS=$(check_redis_running)

if [ -n "$REDIS_STATUS" ]; then
    if [ "$REDIS_STATUS" = "connected" ]; then
        log_warning "检测到 Redis 连接但无法确定进程 PID"
        log_info "尝试通过 redis-cli 关闭连接..."
        
        # 尝试通过 redis-cli 关闭
        if redis-cli shutdown > /dev/null 2>&1; then
            log_success "Redis 已通过 redis-cli 关闭"
        else
            log_error "无法通过 redis-cli 关闭 Redis"
            exit 1
        fi
    else
        PID="$REDIS_STATUS"
        log_info "发现 Redis 进程 PID: $PID"
        
        # 显示进程信息
        proc_info=$(ps -p "$PID" -o pid,ppid,command --no-headers 2>/dev/null)
        if [ -n "$proc_info" ]; then
            log_info "进程信息: $proc_info"
        fi
        
        # 优雅停止
        log_info "正在优雅停止 Redis..."
        kill -TERM "$PID"
        
        # 等待进程停止
        wait_count=0
        max_wait=15
        
        while [ $wait_count -lt $max_wait ]; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                log_success "Redis 已成功停止"
                break
            fi
            sleep 1
            wait_count=$((wait_count + 1))
            echo -n "."
        done
        echo ""
        
        # 如果优雅停止失败，强制停止
        if ps -p "$PID" > /dev/null 2>&1; then
            log_warning "优雅停止失败，强制停止..."
            kill -9 "$PID"
            sleep 2
            
            if ! ps -p "$PID" > /dev/null 2>&1; then
                log_success "Redis 已强制停止"
            else
                log_error "无法停止 Redis 进程"
                exit 1
            fi
        fi
    fi
    
    # 验证端口是否释放
    sleep 1
    if ! lsof -i tcp:$REDIS_PORT > /dev/null 2>&1; then
        log_success "端口 $REDIS_PORT 已释放"
    else
        log_warning "端口 $REDIS_PORT 仍被占用，可能不是 Redis 进程"
    fi
    
    # 检查持久化文件
    if [ -d "$REDIS_DATA_DIR" ]; then
        echo ""
        log_info "持久化文件状态:"
        
        if [ -f "$REDIS_DATA_DIR/dump.rdb" ]; then
            rdb_size=$(du -h "$REDIS_DATA_DIR/dump.rdb" | cut -f1)
            rdb_time=$(stat -f "%Sm" "$REDIS_DATA_DIR/dump.rdb" 2>/dev/null || stat -c "%y" "$REDIS_DATA_DIR/dump.rdb" 2>/dev/null)
            echo "RDB 文件: $REDIS_DATA_DIR/dump.rdb (${rdb_size}, 修改时间: $rdb_time)"
        fi
        
        if [ -f "$REDIS_DATA_DIR/appendonly.aof" ]; then
            aof_size=$(du -h "$REDIS_DATA_DIR/appendonly.aof" | cut -f1)
            aof_time=$(stat -f "%Sm" "$REDIS_DATA_DIR/appendonly.aof" 2>/dev/null || stat -c "%y" "$REDIS_DATA_DIR/appendonly.aof" 2>/dev/null)
            echo "AOF 文件: $REDIS_DATA_DIR/appendonly.aof (${aof_size}, 修改时间: $aof_time)"
        fi
        
        log_success "Redis 数据已持久化到磁盘"
    fi
    
else
    log_success "Redis 未在运行"
fi

echo ""
log_info "Redis 停止完成"
log_info "如需重新启动，请运行: ./scripts/redis/run_redis.sh" 