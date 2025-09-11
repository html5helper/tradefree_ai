import requests
import json
import time
import base64
import os
from typing import Dict, List, Union, Generator, Any, Optional


# 配置类
class DifyConfig:
    """Dify配置类"""

    # API配置
    BASE_URL = "http://dify.html5core.com"
    ENDPOINTS = {"file_upload": "/v1/files/upload", "workflow_run": "/v1/workflows/run"}

    # 文件类型配置
    FILE_TYPES = {
        "document": [
            "TXT",
            "MD",
            "MARKDOWN",
            "PDF",
            "HTML",
            "XLSX",
            "XLS",
            "DOCX",
            "CSV",
            "EML",
            "MSG",
            "PPTX",
            "PPT",
            "XML",
            "EPUB",
        ],
        "image": ["JPG", "JPEG", "PNG", "GIF", "WEBP", "SVG"],
        "audio": ["MP3", "M4A", "WAV", "WEBM", "AMR"],
        "video": ["MP4", "MOV", "MPEG", "MPGA"],
    }

    # 默认配置
    DEFAULT_USER_ID = "difyuser"
    DEFAULT_RESPONSE_MODE = "blocking"
    DEFAULT_API_KEY = "app-LSSiswHmw3cmKDYdYx7yIeV7"

    # 响应模式
    RESPONSE_MODES = ["streaming", "blocking"]


# Dify客户端类
class DifyClient:
    """Dify API客户端类"""

    def __init__(self, api_key: str = None, user_id: str = None, debug: bool = False):
        """初始化Dify客户端

        参数:
            api_key: Dify API密钥
            user_id: 用户标识
            debug: 是否启用调试模式
        """
        self.api_key = api_key or DifyConfig.DEFAULT_API_KEY
        self.user_id = user_id or DifyConfig.DEFAULT_USER_ID
        self.debug = debug

    def upload_file(self, file_path: str, user: str = None) -> Optional[str]:
        """上传文件到Dify平台

        参数:
            file_path: 文件路径
            user: 用户标识，默认使用初始化时设置的user_id

        返回:
            成功返回文件ID，失败返回None
        """
        upload_url = f"{DifyConfig.BASE_URL}{DifyConfig.ENDPOINTS['file_upload']}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            if self.debug:
                print("上传文件中...")

            with open(file_path, "rb") as file:
                # 根据文件扩展名确定文件类型
                file_extension = file_path.split(".")[-1].upper()
                file_type = "custom"  # 默认类型

                # 根据扩展名确定文件类型
                for type_name, extensions in DifyConfig.FILE_TYPES.items():
                    if file_extension in extensions:
                        file_type = type_name
                        break

                files = {
                    "file": (
                        os.path.basename(file_path),
                        file,
                        f"application/octet-stream",
                    )  # 使用通用MIME类型
                }
                data = {"user": user or self.user_id, "type": file_type}

                response = requests.post(
                    upload_url, headers=headers, files=files, data=data
                )
                if response.status_code == 201:  # 201 表示创建成功
                    if self.debug:
                        print("文件上传成功")
                    return response.json().get("id")  # 获取上传的文件 ID
                else:
                    if self.debug:
                        print(f"文件上传失败，状态码: {response.status_code}")
                        print(f"错误信息: {response.text}")
                    return None
        except Exception as e:
            if self.debug:
                print(f"发生错误: {str(e)}")
            return None

    def run_workflow(self, workflow_inputs, user=None, response_mode=None):
        """
        执行Dify workflow

        参数:
            workflow_inputs: 工作流输入参数，格式为字典
            user: 用户标识，默认使用初始化时设置的user_id
            response_mode: 响应模式，支持'streaming'或'blocking'，默认使用初始化时设置的response_mode

        返回:
            如果response_mode为blocking，返回完整响应
            如果response_mode为streaming，返回生成器对象，可迭代获取流式响应
        """
        # 使用默认值或传入的参数
        user = user or self.user_id
        response_mode = response_mode or DifyConfig.DEFAULT_RESPONSE_MODE

        # 验证响应模式
        if response_mode not in DifyConfig.RESPONSE_MODES:
            return {
                "status": "error",
                "message": f"Invalid response_mode: {response_mode}. Must be one of {DifyConfig.RESPONSE_MODES}",
            }

        workflow_url = f"{DifyConfig.BASE_URL}{DifyConfig.ENDPOINTS['workflow_run']}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {"inputs": workflow_inputs, "response_mode": response_mode, "user": user}

        try:
            if self.debug:
                print(f"运行工作流，响应模式: {response_mode}...")

            if response_mode == "blocking":
                # 阻塞模式，等待完整响应
                response = requests.post(workflow_url, headers=headers, json=data)
                if response.status_code == 200:
                    if self.debug:
                        print("工作流执行成功")
                    return response.json()
                else:
                    if self.debug:
                        print(f"工作流执行失败，状态码: {response.status_code}")
                        print(f"错误信息: {response.text}")
                    return {
                        "status": "error",
                        "message": f"Failed to execute workflow, status code: {response.status_code}",
                    }

            elif response_mode == "streaming":
                # 流式模式，使用SSE处理
                response = requests.post(
                    workflow_url, headers=headers, json=data, stream=True
                )
                if response.status_code == 200:
                    if self.debug:
                        print("工作流开始执行，返回流式响应...")
                    return self._process_streaming_response(response)
                else:
                    if self.debug:
                        print(f"工作流执行失败，状态码: {response.status_code}")
                        print(f"错误信息: {response.text}")
                    return {
                        "status": "error",
                        "message": f"Failed to execute workflow, status code: {response.status_code}",
                    }

        except Exception as e:
            if self.debug:
                print(f"发生错误: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _process_streaming_response(self, response):
        """
        处理流式响应，返回生成器对象

        参数:
            response: 请求响应对象

        返回:
            生成器对象，可迭代获取流式响应事件
        """
        for line in response.iter_lines():
            if line:
                # 移除 'data: ' 前缀并解析JSON
                if line.startswith(b"data: "):
                    json_str = line[6:].decode("utf-8")
                    try:
                        event_data = json.loads(json_str)
                        yield event_data

                        # 如果是workflow_finished事件，打印完成信息
                        if (
                            self.debug
                            and event_data.get("event") == "workflow_finished"
                        ):
                            status = event_data.get("data", {}).get("status")
                            print(f"工作流执行{status}")

                    except json.JSONDecodeError as e:
                        if self.debug:
                            print(f"JSON解析错误: {e}")

    def example_document_workflow(self, file_path):
        """
        文档文件上传并处理示例

        参数:
            file_path: 文档文件路径
        """
        # 上传文件
        file_id = self.upload_file(file_path)
        if not file_id:
            if self.debug:
                print("文件上传失败，无法执行工作流")
            return

        # 构建workflow输入
        workflow_inputs = {
            "document_input": [
                {
                    "transfer_method": "local_file",
                    "upload_file_id": file_id,
                    "type": "document",
                }
            ]
        }

        # 阻塞模式执行
        if self.debug:
            print("\n使用阻塞模式执行工作流:")
        result = self.run_workflow(workflow_inputs, response_mode="blocking")
        if self.debug:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        # 流式模式执行
        if self.debug:
            print("\n使用流式模式执行工作流:")
        stream_generator = self.run_workflow(workflow_inputs, response_mode="streaming")
        if (
            isinstance(stream_generator, dict)
            and stream_generator.get("status") == "error"
        ):
            if self.debug:
                print(f"流式执行失败: {stream_generator.get('message')}")
        else:
            try:
                for event in stream_generator:
                    event_type = event.get("event")
                    if self.debug:
                        print(f"收到事件: {event_type}")

                    # 处理文本块事件
                    if event_type == "text_chunk":
                        text = event.get("data", {}).get("text", "")
                        if self.debug:
                            print(f"文本块: {text}")

                    # 处理TTS音频事件
                    elif event_type == "tts_message":
                        audio_base64 = event.get("audio", "")
                        if self.debug:
                            print(f"收到音频块，长度: {len(audio_base64)}字节")
                        # 这里可以添加音频处理逻辑

                    # 处理工作流完成事件
                    elif event_type == "workflow_finished":
                        status = event.get("data", {}).get("status")
                        if self.debug:
                            print(f"工作流执行完成，状态: {status}")
                        break

            except Exception as e:
                if self.debug:
                    print(f"处理流式响应时发生错误: {str(e)}")

    def example_image_url_workflow(self, image_url):
        """
        图片URL处理示例

        参数:
            image_url: 图片URL

        返回:
            工作流执行结果
        """
        # 构建workflow输入 - 使用远程URL
        workflow_inputs = {
            "image_input": [
                {"transfer_method": "remote_url", "url": image_url, "type": "image"}
            ]
        }

        # 执行工作流
        result = self.run_workflow(workflow_inputs, response_mode="blocking")
        if self.debug:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return result


def x4_workflow(file_path="/Users/qinbinbin/Desktop/鞋/xie_base/xie_22.png"):
    dify_client = DifyClient(
        api_key="app-LSSiswHmw3cmKDYdYx7yIeV7",  # 替换为您的API密钥
        user_id="difyuser",  # 替换为您的用户ID
        debug=True,  # 开启调试模式
    )

    # 上传图片文件
    file_id = dify_client.upload_file(file_path)
    if file_id:
        # 构建只有一个图片参数的工作流输入
        workflow_inputs = {
            "img": {
                "transfer_method": "local_file",
                "upload_file_id": file_id,
                "type": "image",
            }
        }

        # 执行工作流
        result = dify_client.run_workflow(workflow_inputs)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        try:
            return result.get("data").get("outputs").get("files")[0]["url"]
        except:
            return None


def xie_workflow(image_url, steps=20):
    dify_client = DifyClient(
        api_key="app-sFg3I1tvXWso46YqzOkP2jOx",  # 替换为您的API密钥
        user_id="difyuser",  # 替换为您的用户ID
        debug=True,  # 开启调试模式
    )

    data = {
        "imageUrl": "https://safc.oss-cn-hangzhou.aliyuncs.com/safc/test/xie_base.png",
        "layerImages": [
            image_url,
            "https://safc.oss-cn-hangzhou.aliyuncs.com/safc/test/xie_mask.png",
        ],
        "prompt": "Replace the blue area with the white slip-on shoe sole while keeping the collar style, original shape, and texture details unchanged, emphasizing that the shoe is a slip-on design",
    }

    workflow_inputs = {
        "data": json.dumps(data),
        "steps": steps,
    }

    # 执行工作流
    result = dify_client.run_workflow(workflow_inputs)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def download_image(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(response.content)


# 主函数
if __name__ == "__main__":
    # 从指定目录读取所有图片文件
    base_dir = "/Users/qinbinbin/Desktop/xxx/xinglix/三叉戟"
    image_files = [
        f for f in os.listdir(base_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    # 按照文件名排序
    image_files.sort()

    # 处理每个图片
    for image_file in image_files:
        file_path = os.path.join(base_dir, image_file)
        print(f"处理图片: {file_path}")
        image_url = x4_workflow(file_path)
        print(f"生成的图片URL: {image_url}")
        if image_url:
            download_dir = os.path.join(base_dir, "x4")
            os.makedirs(download_dir, exist_ok=True)
            download_image(image_url, f"{download_dir}/{image_file}")
        # if image_url:
        #     xie_workflow(image_url)

    print("\n您可以通过取消注释上面的示例代码并提供正确的文件路径或URL来运行更多示例")
    print("或者创建自定义的工作流输入来调用run_workflow方法")
