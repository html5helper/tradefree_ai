# 触发一个 social2product 工作流
curl -X POST http://localhost:8000/workflows/run \
  -H "Content-Type: application/json" \
  -d '{
        "workflow": "social2product_total",
        "payload": {
          "platform": "tiktok",
          "event_id": "82fb09b2-37d6-43e1-86a6-555aa9edde24"
        },
        "context": {
          "platform": "tiktok"
        }
      }'

# 查询状态
# curl localhost:8000/workflows/<trace_id>/status