#!/bin/bash

export PYTHONPATH=$(pwd)

# 通过API触发重试
#curl -X POST http://localhost:8000/workflows/tasks/retry/<原task_id>

# 通过API触发重试
curl -X POST http://localhost:8000/workflows/tasks/retry/1234567890
