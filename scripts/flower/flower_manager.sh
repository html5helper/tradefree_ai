#!/usr/bin/env bash
# flower_manager.sh - Flower 管理脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# 默认配置
DEFAULT_PORT=5555
LOG_FILE="$PROJECT_ROOT/logs/flower.log"
DATA_FILE="$PROJECT_ROOT/data/flower/flower"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 获取端口
get_port() {
    if [ -n "$FLOWER_PORT" ]; then
        echo "$FLOWER_PORT"
    else
        echo "$DEFAULT_PORT"
    fi
}

# 检查 Flower 是否运行
is_flower_running() {
    local port=$(get_port)
    pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app flower --port=$port" >/dev/null
}

# 获取 Flower PID
get_flower_pid() {
    local port=$(get_port)
    pgrep -f "$PROJECT_ROOT/.venv/bin/celery -A ai.core.celery_app flower --port=$port"
}

# 启动 Flower
start_flower() {
    local port=$(get_port)
    print_info "启动 Flower 服务 (端口: $port)..."
    
    if is_flower_running; then
        print_warning "Flower 已经在运行中"
        return 1
    fi
    
    mkdir -p "$(dirname "$LOG_FILE")"
    mkdir -p "$(dirname "$DATA_FILE")"
    
    cd "$PROJECT_ROOT"
    ./scripts/flower/run_flower.sh
    
    sleep 3
    
    if is_flower_running; then
        local pids=$(get_flower_pid)
        print_success "Flower 启动成功！PID: $pids"
        print_info "访问地址: http://localhost:$port"
        print_info "日志文件: $LOG_FILE"
        print_info "数据文件: $DATA_FILE"
    else
        print_error "Flower 启动失败，请检查日志: $LOG_FILE"
        return 1
    fi
}

# 停止 Flower
stop_flower() {
    print_info "停止 Flower 服务..."
    
    if ! is_flower_running; then
        print_warning "Flower 未在运行"
        return 0
    fi
    
    local pids=$(get_flower_pid)
    if [ -n "$pids" ]; then
        print_info "正在停止 Flower 进程: $pids"
        kill -TERM $pids
        
        local count=0
        while is_flower_running && [ $count -lt 10 ]; do
            sleep 1
            count=$((count + 1))
        done
        
        if is_flower_running; then
            print_warning "优雅停止失败，强制终止进程"
            kill -KILL $pids
            sleep 1
        fi
        
        if ! is_flower_running; then
            print_success "Flower 已停止"
        else
            print_error "无法停止 Flower"
            return 1
        fi
    fi
}

# 重启 Flower
restart_flower() {
    print_info "重启 Flower 服务..."
    stop_flower
    sleep 2
    start_flower
}

# 查看 Flower 状态
status_flower() {
    local port=$(get_port)
    print_info "Flower 服务状态:"
    echo "--------------------------------"
    
    if is_flower_running; then
        local pids=$(get_flower_pid)
        local pid_count=$(echo "$pids" | wc -l | tr -d ' ')
        print_success "Flower 正在运行"
        echo "进程数量: $pid_count"
        echo "进程 PID: $pids"
        echo "端口: $port"
        echo "访问地址: http://localhost:$port"
        
        if lsof -i tcp:$port >/dev/null 2>&1; then
            print_success "端口 $port 正在监听"
        else
            print_warning "端口 $port 未监听"
        fi
    else
        print_error "Flower 未运行"
    fi
    
    echo "--------------------------------"
    
    if [ -f "$LOG_FILE" ]; then
        echo "日志文件: $LOG_FILE"
        echo "日志大小: $(ls -lh "$LOG_FILE" | awk '{print $5}')"
        echo "最后修改: $(ls -lh "$LOG_FILE" | awk '{print $6, $7, $8}')"
    else
        print_warning "日志文件不存在: $LOG_FILE"
    fi
    
    if [ -f "$DATA_FILE" ]; then
        echo "数据文件: $DATA_FILE"
        echo "数据大小: $(ls -lh "$DATA_FILE" | awk '{print $5}')"
        echo "最后修改: $(ls -lh "$DATA_FILE" | awk '{print $6, $7, $8}')"
    else
        print_warning "数据文件不存在: $DATA_FILE"
    fi
}

# 查看 Flower 日志
logs_flower() {
    if [ -f "$LOG_FILE" ]; then
        print_info "显示 Flower 日志 (最后 50 行):"
        echo "--------------------------------"
        tail -50 "$LOG_FILE"
        echo "--------------------------------"
        print_info "实时查看日志: tail -f $LOG_FILE"
    else
        print_error "日志文件不存在: $LOG_FILE"
    fi
}

# 清理 Flower 数据
clean_flower() {
    print_warning "清理 Flower 数据..."
    
    stop_flower
    
    if [ -f "$DATA_FILE" ]; then
        print_info "删除数据文件: $DATA_FILE"
        rm -f "$DATA_FILE"
        print_success "数据文件已删除"
    else
        print_info "数据文件不存在: $DATA_FILE"
    fi
    
    if [ -f "$LOG_FILE" ]; then
        print_info "清空日志文件: $LOG_FILE"
        > "$LOG_FILE"
        print_success "日志文件已清空"
    fi
}

# 显示帮助信息
show_help() {
    echo "Flower 管理脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  start    启动 Flower 服务"
    echo "  stop     停止 Flower 服务"
    echo "  restart  重启 Flower 服务"
    echo "  status   查看 Flower 状态"
    echo "  logs     查看 Flower 日志"
    echo "  clean    清理 Flower 数据"
    echo "  help     显示此帮助信息"
    echo ""
    echo "环境变量:"
    echo "  FLOWER_PORT  Flower 端口 (默认: $DEFAULT_PORT)"
    echo ""
    echo "示例:"
    echo "  $0 start      # 启动 Flower"
    echo "  $0 status     # 查看状态"
    echo "  FLOWER_PORT=6666 $0 start  # 指定端口启动"
}

# 主函数
main() {
    case "${1:-help}" in
        start)
            start_flower
            ;;
        stop)
            stop_flower
            ;;
        restart)
            restart_flower
            ;;
        status)
            status_flower
            ;;
        logs)
            logs_flower
            ;;
        clean)
            clean_flower
            ;;
        help|*)
            show_help
            ;;
    esac
}

main "$@" 