#!/bin/bash

# 检查是否提供了进程名称
if [ -z "$1" ]; then
    echo "Usage: $0 <process_name>"
    exit 1
fi

PROCESS_NAME=$1

# 使用模糊匹配查找进程ID
PIDS=$(pgrep -f $PROCESS_NAME)

# 检查是否找到了进程ID
if [ -z "$PIDS" ]; then
    echo "No process found matching: $PROCESS_NAME"
    exit 1
fi

# 显示找到的进程ID
echo "Found process IDs: $PIDS"

# 杀死进程
echo "Killing processes matching: $PROCESS_NAME"
kill $PIDS

# 检查进程是否成功被杀死
if pgrep -f $PROCESS_NAME > /dev/null; then
    echo "Failed to kill process. Trying force kill..."
    kill -9 $PIDS
else
    echo "Processes matching $PROCESS_NAME killed successfully."
fi

