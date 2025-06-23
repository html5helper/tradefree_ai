# SVG转CMYK PDF API使用说明

## 接口信息

- **接口路径**: `/convert_svg_to_cmyk_pdf`
- **请求方法**: `POST`
- **功能**: 将SVG文件转换为CMYK色彩模式的PDF文件

## 请求参数

### 方式一：文件上传

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| svg_file | file | 是 | SVG文件 |
| run_id | string | 否 | 输出文件名标识，默认使用上传文件名 |

### 方式二：文件路径

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| svg_path | string | 是 | 服务器上SVG文件的完整路径 |
| run_id | string | 否 | 输出文件名标识，默认使用文件名 |

## 响应格式

### 成功响应

```json
{
  "success": true,
  "pdf_path": "/tmp/example_CMYK.pdf",
  "pdf_name": "example_CMYK.pdf"
}
```

### 错误响应

```json
{
  "error": "错误信息描述"
}
```

## 使用示例

### 1. 使用curl上传文件

```bash
curl -X POST \
  http://localhost:8080/convert_svg_to_cmyk_pdf \
  -F "svg_file=@/path/to/your/file.svg" \
  -F "run_id=my_logo"
```

### 2. 使用curl指定文件路径

```bash
curl -X POST \
  http://localhost:8080/convert_svg_to_cmyk_pdf \
  -F "svg_path=/path/to/server/file.svg" \
  -F "run_id=my_logo"
```

### 3. 使用Python requests

```python
import requests

# 方式一：文件上传
with open('logo.svg', 'rb') as f:
    files = {'svg_file': f}
    data = {'run_id': 'company_logo'}
    response = requests.post(
        'http://localhost:8080/convert_svg_to_cmyk_pdf',
        files=files,
        data=data
    )
    print(response.json())

# 方式二：文件路径
data = {
    'svg_path': '/path/to/logo.svg',
    'run_id': 'company_logo'
}
response = requests.post(
    'http://localhost:8080/convert_svg_to_cmyk_pdf',
    data=data
)
print(response.json())
```

## 依赖要求

在使用此接口前，请确保服务器已安装以下依赖：

### macOS
```bash
brew install inkscape
brew install ghostscript
```

### Ubuntu/Debian
```bash
sudo apt install inkscape
sudo apt install ghostscript
```

### CentOS/RHEL
```bash
sudo yum install inkscape
sudo yum install ghostscript
```

## 注意事项

1. **文件格式**: 仅支持SVG格式的输入文件
2. **输出位置**: 生成的PDF文件保存在配置的`output_dir`目录中
3. **文件命名**: 输出文件名格式为`{run_id}_CMYK.pdf`
4. **CMYK配置**: 如果存在ICC配置文件`/home/qinbinbin/ai_tools/comfyui/tmp/ISOcoated_v2_300_eci.icc`，将使用该配置文件进行更精确的CMYK转换
5. **临时文件**: 转换过程中产生的临时文件会自动清理

## 错误处理

常见错误及解决方案：

- **缺少依赖**: 确保已安装inkscape和ghostscript
- **文件不存在**: 检查svg_path参数指定的文件路径是否正确
- **权限问题**: 确保服务有读取输入文件和写入输出目录的权限
- **格式错误**: 确保输入文件是有效的SVG格式