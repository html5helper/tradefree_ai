#!/bin/bash

REDIS_PORT=6379
REDIS_DATA_DIR="./redis_data_${REDIS_PORT}"

echo "=== Redis 监控信息 ==="
echo "时间: $(date)"
echo ""

# 检查Redis是否运行
if ! lsof -i tcp:$REDIS_PORT > /dev/null 2>&1; then
    echo "❌ Redis 未运行"
    exit 1
else
    echo "✅ Redis 正在运行"
fi

echo ""

# 基础信息
echo "=== 基础信息 ==="
redis-cli info server | grep -E "(redis_version|uptime_in_seconds|connected_clients|used_memory_human)"

echo ""

# 持久化信息
echo "=== 持久化信息 ==="
redis-cli info persistence | grep -E "(rdb_last_save_time|aof_enabled|aof_current_size)"

echo ""

# 内存信息
echo "=== 内存信息 ==="
redis-cli info memory | grep -E "(used_memory_human|maxmemory_human|maxmemory_policy)"

echo ""

# Celery 相关队列信息
echo "=== Celery 队列信息 ==="
echo "Broker DB (DB 2):"
redis-cli -n 2 info keyspace
echo ""
echo "Backend DB (DB 3):"
redis-cli -n 3 info keyspace
echo ""
echo "Employee Cache DB (DB 5):"
redis-cli -n 5 info keyspace

echo ""

# 数据文件信息
echo "=== 数据文件信息 ==="
if [ -d "$REDIS_DATA_DIR" ]; then
    echo "数据目录: $REDIS_DATA_DIR"
    ls -lh "$REDIS_DATA_DIR" 2>/dev/null || echo "无法访问数据目录"
else
    echo "数据目录不存在: $REDIS_DATA_DIR"
fi

echo ""
echo "=== 监控完成 ===" 