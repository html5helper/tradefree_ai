#!/bin/bash

# Redis 管理器 - 基于 Service 运行方式
# 提供检测、管理、备份等功能

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
REDIS_PID_FILE="/tmp/redis_${REDIS_PORT}.pid"

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
check_redis_status() {
    local pid=$(lsof -ti tcp:$REDIS_PORT 2>/dev/null | head -n 1)
    if [ -n "$pid" ]; then
        local proc_name=$(ps -p "$pid" -o comm= 2>/dev/null | head -n 1)
        if [ -n "$proc_name" ] && echo "$proc_name" | grep -q "redis-server"; then
            echo "running:$pid"
        else
            echo "port_occupied:$pid"
        fi
    else
        echo "stopped"
    fi
}

# 获取 Redis 信息
get_redis_info() {
    if redis-cli ping > /dev/null 2>&1; then
        echo "=== Redis 基本信息 ==="
        redis-cli info server | grep -E "(redis_version|uptime_in_seconds|connected_clients|used_memory_human|total_commands_processed)"
        
        echo -e "\n=== 持久化状态 ==="
        redis-cli info persistence | grep -E "(rdb_last_save_time|aof_enabled|aof_current_size|aof_rewrite_in_progress|aof_last_rewrite_time_sec)"
        
        echo -e "\n=== 内存使用 ==="
        redis-cli info memory | grep -E "(used_memory_human|maxmemory_human|maxmemory_policy)"
        
        echo -e "\n=== 连接信息 ==="
        redis-cli info clients | grep -E "(connected_clients|blocked_clients)"
    else
        log_error "无法连接到 Redis"
        return 1
    fi
}

# 检查持久化文件
check_persistence_files() {
    log_info "检查持久化文件..."
    
    if [ -d "$REDIS_DATA_DIR" ]; then
        echo "数据目录: $REDIS_DATA_DIR"
        
        # 检查 RDB 文件
        local rdb_file="$REDIS_DATA_DIR/dump.rdb"
        if [ -f "$rdb_file" ]; then
            local rdb_size=$(du -h "$rdb_file" | cut -f1)
            local rdb_time=$(stat -f "%Sm" "$rdb_file" 2>/dev/null || stat -c "%y" "$rdb_file" 2>/dev/null)
            echo "RDB 文件: $rdb_file (${rdb_size}, 修改时间: $rdb_time)"
        else
            echo "RDB 文件: 不存在"
        fi
        
        # 检查 AOF 文件
        local aof_file="$REDIS_DATA_DIR/appendonly.aof"
        if [ -f "$aof_file" ]; then
            local aof_size=$(du -h "$aof_file" | cut -f1)
            local aof_time=$(stat -f "%Sm" "$aof_file" 2>/dev/null || stat -c "%y" "$aof_file" 2>/dev/null)
            echo "AOF 文件: $aof_file (${aof_size}, 修改时间: $aof_time)"
        else
            echo "AOF 文件: 不存在"
        fi
        
        # 检查 AOF 重写文件
        local aof_rewrite_file="$REDIS_DATA_DIR/appendonly.aof.rewrite"
        if [ -f "$aof_rewrite_file" ]; then
            local rewrite_size=$(du -h "$aof_rewrite_file" | cut -f1)
            echo "AOF 重写文件: $aof_rewrite_file (${rewrite_size})"
        fi
    else
        log_warning "数据目录不存在: $REDIS_DATA_DIR"
    fi
}

# 备份持久化文件
backup_persistence_files() {
    local backup_dir="$PROJECT_ROOT/redis_backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    log_info "备份持久化文件到: $backup_dir"
    
    if [ -d "$REDIS_DATA_DIR" ]; then
        # 备份 RDB 文件
        if [ -f "$REDIS_DATA_DIR/dump.rdb" ]; then
            cp "$REDIS_DATA_DIR/dump.rdb" "$backup_dir/"
            log_success "RDB 文件已备份"
        fi
        
        # 备份 AOF 文件
        if [ -f "$REDIS_DATA_DIR/appendonly.aof" ]; then
            cp "$REDIS_DATA_DIR/appendonly.aof" "$backup_dir/"
            log_success "AOF 文件已备份"
        fi
        
        # 创建备份信息文件
        cat > "$backup_dir/backup_info.txt" << EOF
备份时间: $(date)
Redis 端口: $REDIS_PORT
数据目录: $REDIS_DATA_DIR
备份目录: $backup_dir

Redis 状态:
$(redis-cli info server 2>/dev/null | grep -E "(redis_version|uptime_in_seconds)" || echo "无法获取 Redis 信息")
EOF
        
        log_success "备份完成: $backup_dir"
        echo "备份内容:"
        ls -la "$backup_dir"
    else
        log_error "数据目录不存在: $REDIS_DATA_DIR"
        return 1
    fi
}

# 清理旧备份
cleanup_old_backups() {
    local backup_root="$PROJECT_ROOT/redis_backups"
    local keep_days=7
    
    if [ -d "$backup_root" ]; then
        log_info "清理 $keep_days 天前的备份文件..."
        find "$backup_root" -type d -name "*_*" -mtime +$keep_days -exec rm -rf {} \; 2>/dev/null
        log_success "旧备份清理完成"
    fi
}

# 监控 Redis 健康状态
monitor_redis_health() {
    log_info "监控 Redis 健康状态..."
    
    # 检查连接
    if ! redis-cli ping > /dev/null 2>&1; then
        log_error "Redis 连接失败"
        return 1
    fi
    
    # 检查内存使用
    local used_memory=$(redis-cli info memory | grep "used_memory:" | cut -d: -f2)
    local max_memory=$(redis-cli info memory | grep "maxmemory:" | cut -d: -f2)
    
    if [ "$max_memory" != "0" ]; then
        local memory_usage=$((used_memory * 100 / max_memory))
        if [ $memory_usage -gt 80 ]; then
            log_warning "内存使用率较高: ${memory_usage}%"
        else
            log_success "内存使用率正常: ${memory_usage}%"
        fi
    fi
    
    # 检查 AOF 重写状态
    local aof_rewrite=$(redis-cli info persistence | grep "aof_rewrite_in_progress:" | cut -d: -f2)
    if [ "$aof_rewrite" = "1" ]; then
        log_warning "AOF 重写正在进行中"
    else
        log_success "AOF 状态正常"
    fi
    
    # 检查连接数
    local connected_clients=$(redis-cli info clients | grep "connected_clients:" | cut -d: -f2)
    if [ "$connected_clients" -gt 100 ]; then
        log_warning "连接数较多: $connected_clients"
    else
        log_success "连接数正常: $connected_clients"
    fi
}

# 显示帮助信息
show_help() {
    echo "Redis 管理器 - 基于 Service 运行方式"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  status      检查 Redis 运行状态"
    echo "  info        显示 Redis 详细信息"
    echo "  health      监控 Redis 健康状态"
    echo "  backup      备份持久化文件"
    echo "  cleanup     清理旧备份文件"
    echo "  files       检查持久化文件"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 status    # 检查状态"
    echo "  $0 backup    # 备份文件"
    echo "  $0 health    # 健康检查"
}

# 主函数
main() {
    local command="${1:-status}"
    
    case "$command" in
        "status")
            local status=$(check_redis_status)
            case "$status" in
                "running:"*)
                    local pid=${status#running:}
                    log_success "Redis 正在运行 (PID: $pid)"
                    ;;
                "port_occupied:"*)
                    local pid=${status#port_occupied:}
                    log_warning "端口被占用 (PID: $pid)，但可能不是 Redis"
                    ;;
                "stopped")
                    log_error "Redis 未运行"
                    ;;
            esac
            ;;
        "info")
            get_redis_info
            ;;
        "health")
            monitor_redis_health
            ;;
        "backup")
            backup_persistence_files
            ;;
        "cleanup")
            cleanup_old_backups
            ;;
        "files")
            check_persistence_files
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@" 