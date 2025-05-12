# api_server 说明

## 功能简介
本目录包含基于 Flask 的 AI 图像处理与 SVG 转 EPS 接口服务，支持 GPU 加速和多种部署方式。

- `florence2_api.py`：图像处理与推理接口，支持图片上传和 URL 批量处理。
- `svg_api.py`：SVG 转 EPS 文件接口。
- `config.py`：模型路径、设备等配置。
- `deploy/`：部署与开机自启相关脚本和配置。

## 依赖环境
- Python 3.8+
- Flask
- torch
- transformers
- Pillow
- requests
- cairosvg（如需 SVG 转 EPS）

建议使用 `pip install -r requirements.txt` 安装依赖。

## 启动方式

### 开发环境
```bash
export FLASK_APP=main.py
flask run --host=0.0.0.0 --port=8080

