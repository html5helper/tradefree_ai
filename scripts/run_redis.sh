#!/bin/bash

# 检查redis-server是否在运行
if pgrep -x "redis-server" > /dev/null
then
    echo "Redis is already running."
else
    echo "Starting redis-server..."
    redis-server &
    sleep 2
    if pgrep -x "redis-server" > /dev/null
    then
        echo "Redis started successfully."
    else
        echo "Failed to start Redis. Please check your redis-server installation."
        exit 1
    fi
fi 