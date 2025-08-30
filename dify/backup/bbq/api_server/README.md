# API Server 说明

## 功能简介
本目录包含基于 Flask 的多功能API服务器，提供图像处理、视频生成、SVG转换等功能，支持 GPU 加速和多种部署方式。

### 主要功能模块

- **图像处理**：使用Florence2模型进行图像分析和处理
  - `florence2_api.py`：图像处理与推理接口，支持图片上传和 URL 批量处理
- **图像转方形**：将各种尺寸的图像转换为方形格式
  - `img2square_api.py`：图像转方形API，适用于社交媒体等场景
- **图像转视频**：将多张图像合成为带有转场效果的视频
  - `img2video_api.py`：图像转视频API，支持添加片头片尾和转场动画
- **SVG转换**：将SVG文件转换为多种格式
  - `svg_api.py`：SVG 转 EPS 文件接口
  - `svg2cmyk_api.py`：SVG转CMYK PDF接口，适用于印刷需求
- **OSS上传**：将文件上传到阿里云OSS存储
  - `oss_api.py`：OSS上传API
  - `tools/upload2oss.py`：OSS上传工具类
- **配置管理**：
  - `config/`：模型路径、设备等配置
- **部署工具**：
  - `deploy/`：部署与开机自启相关脚本和配置

## 项目结构

```
.
├── config/                 # 配置文件目录
│   ├── __init__.py        # 配置初始化
│   ├── base.py            # 基础配置
│   ├── development.py     # 开发环境配置
│   └── production.py      # 生产环境配置
├── tools/                 # 工具函数目录
│   ├── __init__.py
│   └── upload2oss.py      # OSS上传工具
├── deploy/                # 部署相关文件
│   ├── dify_ext.service   # systemd服务配置
│   └── start_api_server.sh # 启动脚本
├── florence2_api.py       # Florence2模型API
├── img2square_api.py      # 图像转方形API
├── img2video_api.py       # 图像转视频API
├── main.py                # 主应用入口
├── oss_api.py             # OSS上传API
├── svg2cmyk_api.py        # SVG转CMYK PDF API
├── svg_api.py             # SVG处理API
├── requirements.txt       # 项目依赖
├── check_environment.py   # 环境检查脚本
├── setup_environment.sh   # 环境安装脚本
└── PYTHON_SETUP.md        # Python环境安装指南
```

## 依赖环境
- Python 3.8+
- Flask
- torch (支持CUDA或MPS加速)
- transformers
- Pillow
- OpenCV
- moviepy
- requests
- cairosvg
- oss2
- 系统依赖：ffmpeg, inkscape, ghostscript

详细依赖请参考 `requirements.txt`，建议使用提供的安装脚本进行环境配置：

```bash
./setup_environment.sh
```

更多安装说明请参考 [Python环境安装指南](PYTHON_SETUP.md)。

## 启动方式

### 开发环境
```bash
python main.py
# 或者
export FLASK_APP=main.py
flask run --host=0.0.0.0 --port=8080
```

### 生产环境

使用 systemd 服务（Linux）：

```bash
sudo cp deploy/dify_ext.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dify_ext
sudo systemctl start dify_ext
```

## 环境变量

- `MODEL_PATH`: Florence2模型路径
- `OUTPUT_DIR`: 输出文件目录
- `AUDIO_PATH`: 默认音频文件路径
- `OSS_ACCESS_KEY_ID`: 阿里云OSS访问密钥ID
- `OSS_ACCESS_KEY_SECRET`: 阿里云OSS访问密钥Secret

## API接口

详细API接口说明请参考`main.py`文件中的路由定义。

