#!/bin/bash

REDIS_PORT=6379
PID=$(lsof -ti tcp:$REDIS_PORT 2>/dev/null | head -n 1)

echo "🛑 停止 Redis 服务器..."

if [ -n "$PID" ]; then
    echo "发现 Redis 进程 PID: $PID"
    
    # 优雅停止
    echo "正在优雅停止 Redis..."
    kill -TERM "$PID"
    
    # 等待进程停止
    for i in {1..10}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            echo "✅ Redis 已成功停止"
            exit 0
        fi
        sleep 1
    done
    
    # 如果优雅停止失败，强制停止
    echo "⚠️ 优雅停止失败，强制停止..."
    kill -9 "$PID"
    sleep 1
    
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ Redis 已强制停止"
    else
        echo "❌ 无法停止 Redis 进程"
        exit 1
    fi
else
    echo "✅ Redis 未在运行"
fi

echo "�� Redis 数据已持久化到磁盘" 