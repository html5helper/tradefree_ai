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
    -d '{"imgs":["https://s.alicdn.com/@sc04/kf/H6a89b5a266bb4f44ae9aa8389c7a6d1aY.png","https://s.alicdn.com/@sc04/kf/H13b3b1644189475fa74c103643b56a115.png","https://s.alicdn.com/@sc04/kf/Ha01b39a810004b30b2094a40a3b1f36e2.png","https://s.alicdn.com/@sc04/kf/Hbdc17f49587a4410bb305bb427cc6a4fM.png","https://s.alicdn.com/@sc04/kf/H4b34d09ad8ce435895dd4bc346659be9x.png","https://s.alicdn.com/@sc04/kf/H9592d57e7aa5475ebadc45d0f48f4317a.png"],"product_type":"sticker","price":"","description":"","prodid":"https://www.alibaba.com/product-detail/Free-Proofing-Custom-Waterproof-Printing-logo_1600831251894.html","reference_product_platform":"ali","title":"Free Proofing Custom Waterproof Printing logo Packaging Gloss Vinyl Holographic Custom Die Cut Sticker","employee":"thanos_zhang","published_shop":"ali_shop2"}'
  echo -e "\n---\n"
#   sleep 1
done

# 测试 social_to_ali 工作流
curl -X POST \
    http://127.0.0.1:8000/workflow/run/social_to_ali \
    -H 'Content-Type: application/json' \
    -d '{"platform": "tiktok", "page_size": 30}'
echo -e "\n---\n"

# 查询状态
# curl localhost:8000/workflows/<trace_id>/status

# 重试任务
# curl -X POST http://localhost:8000/workflows/tasks/retry/f5a7259e-2b26-44cd-928c-c68790b61c8c
