# 图片转正方形API接口使用说明

## 接口说明

该接口用于将图片转换为正方形，通过在图片周围添加背景色（默认为白色）使图片成为正方形。

## 接口地址

```
POST /convert_to_square
```

## 请求参数

请求采用 `multipart/form-data` 格式，支持以下参数：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| image_urls | string | 是 | 图片URL列表，可以是JSON数组字符串或逗号分隔的URL列表 |
| run_id | string | 否 | 任务ID，用于标识本次请求，如不提供则自动生成 |
| background_color | string | 否 | 背景颜色，格式为"R,G,B"，默认为"255,255,255"(白色) |

## 响应结果

### 成功响应

```json
{
  "image_paths": ["/tmp/square_000_image.jpg", "/tmp/square_001_image.jpg"],
  "count": 2,
  "process_time_seconds": 3.45,
  "message": "Images converted to square successfully"
}
```

### 错误响应

```json
{
  "error": "错误信息"
}
```

## 使用示例

### 使用curl

```bash
curl -X POST \
  http://localhost:8080/convert_to_square \
  -F "image_urls=[\"https://example.com/image1.jpg\",\"https://example.com/image2.png\"]" \
  -F "background_color=255,255,255"
```

### 使用Python requests

```python
import requests
import json

url = "http://localhost:8080/convert_to_square"

image_urls = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.png"
]

data = {
    "image_urls": json.dumps(image_urls),
    "background_color": "255,255,255"  # 白色背景，可选
}

response = requests.post(url, data=data)
print(response.json())
```

## 注意事项

1. 图片URL必须是可公开访问的，否则无法下载图片
2. 输出的图片保存在服务器的临时目录中，路径会在响应中返回
3. 背景颜色默认为白色(255,255,255)，可以通过background_color参数修改
4. 转换后的图片保持原始图片的宽高比，只是在周围添加背景色使其成为正方形
5. 如果图片已经是正方形，将直接返回原图路径，不进行额外处理，提高性能
   - 如果指定了输出路径且与输入路径不同，会将原图复制到输出路径
   - 日志中会记录图片已经是正方形的信息
6. 如果提供的URL列表中有部分URL无效，接口会尝试处理有效的URL，并在响应中返回成功处理的图片路径

## 反爬策略说明

本接口已实现防反爬机制，包括以下特性：

1. 随机User-Agent：每次请求使用不同的浏览器标识，减少被识别为爬虫的可能性
2. 随机Referer：模拟从不同来源访问图片
3. 请求延迟：在批量请求图片时添加随机延迟，避免请求过于频繁
4. 重试机制：遇到临时性错误时，采用指数退避策略进行重试
5. 完整请求头：包含Accept、Accept-Language等常见请求头，使请求更接近真实浏览器行为

## 性能考虑

1. 由于实现了反爬策略，批量处理大量图片时可能需要较长时间，请合理控制单次请求的图片数量
2. 对于需要高性能处理的场景，建议考虑使用本地图片路径而非URL
3. 服务器会对每个URL进行最多3次重试，如果仍然失败则跳过该图片
4. 响应中的`process_time_seconds`字段提供了请求处理的总耗时，可用于性能监控
5. 服务器使用流式下载和处理图片，减少内存占用，适合处理大图片

## 图片格式支持

1. 支持的输入图片格式：JPEG、PNG、WebP、GIF、SVG、TIFF、BMP等常见图片格式
2. 输出图片会尽量保持原始格式，对于特殊格式会转换为JPEG格式
3. 对于RGBA格式（带透明通道）的图片，会自动转换为RGB格式，透明部分将使用指定的背景色填充

## 错误处理

1. 接口会验证下载的图片是否为有效图片文件，无效文件会被自动跳过
2. 空文件或无法识别的图片格式会被自动过滤
3. 详细的错误信息会记录在服务器日志中，便于问题排查
4. 即使部分图片处理失败，接口仍会返回成功处理的图片路径