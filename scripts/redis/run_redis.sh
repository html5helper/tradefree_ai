#!/bin/bash

REDIS_PORT=6379
REDIS_CONFIG_FILE="./scripts/redis/redis_${REDIS_PORT}.conf"
REDIS_BIN=$(which redis-server)
REDIS_DATA_DIR="./redis_data_${REDIS_PORT}"

# === 检查 redis-server 是否存在 ===
if [ -z "$REDIS_BIN" ]; then
    echo "❌ redis-server 未安装或未在 PATH 中"
    echo "请安装 Redis: brew install redis"
    exit 1
fi

# === 检查配置文件是否存在 ===
if [ ! -f "$REDIS_CONFIG_FILE" ]; then
    echo "❌ Redis 配置文件不存在: $REDIS_CONFIG_FILE"
    echo "请先创建配置文件"
    exit 1
fi

# === 创建数据目录 ===
mkdir -p "$REDIS_DATA_DIR"

# === 检查端口占用并获取 PID ===
PID=$(lsof -ti tcp:$REDIS_PORT 2>/dev/null | head -n 1)

if [ -n "$PID" ]; then
    echo "⚠️ 端口 $REDIS_PORT 已被占用，PID: $PID"
    
    # 检查 PID 是否仍然存在
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️ 进程 $PID 已不存在，可能是瞬时占用，继续启动 Redis..."
        PID=""
    else
        # 检查是否是 Redis 进程
        PROC_NAME=$(ps -p "$PID" -o command= 2>/dev/null | head -n 1)
        
        if echo "$PROC_NAME" | grep -q "redis-server"; then
            echo "🔍 发现 Redis 进程正在运行"
            read -p "是否停止现有 Redis 并重启？[y/N] " answer
            if [[ "$answer" =~ ^[Yy]$ ]]; then
                echo "🛑 停止 Redis 进程 $PID..."
                kill -TERM "$PID"
                sleep 2
                
                # 检查是否成功停止
                if ps -p "$PID" > /dev/null 2>&1; then
                    echo "⚠️ 进程仍在运行，强制停止..."
                    kill -9 "$PID"
                    sleep 1
                fi
                
                echo "✅ Redis 进程已停止"
            else
                echo "✅ 保持现有 Redis 运行"
                exit 0
            fi
        else
            echo "❌ 端口被其他程序占用: $PROC_NAME（PID: $PID）"
            echo "请手动停止该进程或使用其他端口"
            exit 1
        fi
    fi
fi

# === 启动 Redis ===
echo "🚀 正在启动 Redis..."
echo "配置文件: $REDIS_CONFIG_FILE"
echo "数据目录: $REDIS_DATA_DIR"

$REDIS_BIN "$REDIS_CONFIG_FILE" &

# 等待启动
sleep 3

# 检查是否成功启动
if lsof -i tcp:$REDIS_PORT > /dev/null 2>&1; then
    echo "✅ Redis 启动成功！"
    echo "端口: $REDIS_PORT"
    echo "数据目录: $REDIS_DATA_DIR"
    echo "日志文件: $REDIS_DATA_DIR/redis.log"
    
    # 显示基本信息
    echo ""
    echo "📊 Redis 信息:"
    redis-cli info server | grep -E "(redis_version|uptime_in_seconds|connected_clients|used_memory_human)"
    
    echo ""
    echo "💾 持久化状态:"
    redis-cli info persistence | grep -E "(rdb_last_save_time|aof_enabled|aof_current_size)"
    
else
    echo "❌ Redis 启动失败"
    echo "请检查日志: $REDIS_DATA_DIR/redis.log"
    exit 1
fi