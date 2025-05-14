#!/bin/bash

for i in {1..5}
do
  # 测试 amz_to_ali 工作流
  curl -X POST \
    http://127.0.0.1:8000/workflow/run/amz_to_ali \
    -H 'Content-Type: application/json' \
    -d '{"trace_id": "test-trace-ali-'"$i"'", "event_type": "amz_to_ali", "payload": {}}'
  echo -e "\n---\n"
#   sleep 1
done

for i in {1..5}
do
  # 测试 amz_to_1688 工作流
  curl -X POST \
    http://127.0.0.1:8000/workflow/run/amz_to_1688 \
    -H 'Content-Type: application/json' \
    -d '{"trace_id": "test-trace-1688-'"$i"'", "event_type": "amz_to_1688", "payload": {}}'
  echo -e "\n---\n"
#   sleep 1
done

for i in {1..5}
do
  # 测试 1688_to_1688 工作流
  curl -X POST \
    http://127.0.0.1:8000/workflow/run/1688_to_1688 \
    -H 'Content-Type: application/json' \
    -d '{"trace_id": "test-trace-1688to1688-'"$i"'", "event_type": "1688_to_1688", "payload": {}}'
  echo -e "\n---\n"
#   sleep 1
done

for i in {1..5}
do
  # 测试 ali_to_ali 工作流
  curl -X POST \
    http://127.0.0.1:8000/workflow/run/ali_to_ali \
    -H 'Content-Type: application/json' \
    -d '{"trace_id": "test-trace-alitoali-'"$i"'", "event_type": "ali_to_ali", "payload": {}}'
  echo -e "\n---\n"
#   sleep 1
done

# 测试 social_to_ali 工作流
# curl -X POST \
#     http://127.0.0.1:8000/workflow/run/social_to_ali \
#     -H 'Content-Type: application/json' \
#     -d '{"trace_id": "test-trace-socialtoali", "event_type": "social_to_ali","context": {"platform": "tiktok"}, "payload": {}}'
# echo -e "\n---\n"

# 查询状态
# curl localhost:8000/workflows/<trace_id>/status

# 重试任务
# curl -X POST http://localhost:8000/workflows/tasks/retry/f5a7259e-2b26-44cd-928c-c68790b61c8c
