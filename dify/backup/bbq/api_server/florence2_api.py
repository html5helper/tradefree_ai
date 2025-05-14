import requests
import torch
import traceback
import io
import logging
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from flask import request, jsonify
from config import device, torch_dtype, model_path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 启动时一次性加载模型到合适 device
logger.info(f"正在加载模型，路径: {model_path}, 设备: {device}, 数据类型: {torch_dtype}")
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
logger.info("模型加载完成")

def process_image(image, task_prompt, text_input=None):
    try:
        logger.info(f"开始处理图片，尺寸: {image.size}, task_prompt: {task_prompt}, text_input: {text_input}")
        # prompt 拼接优化
        prompt = task_prompt if text_input is None else task_prompt + text_input
        logger.debug(f"拼接后的 prompt: {prompt}")

        inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)
        logger.debug("输入处理完成，开始生成")

        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3
        )
        logger.debug("生成完成，开始解码")

        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        parsed_answer = processor.post_process_generation(generated_text, task=task_prompt,
                                                          image_size=(image.width, image.height))
        logger.info("图片处理完成")
        return parsed_answer
    except Exception as e:
        logger.error(f"处理图片时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def process_image_api_route():
    try:
        logger.info("收到单图处理请求")
        if 'image' not in request.files:
            logger.warning("请求中未包含图片文件")
            return jsonify({"error": "No image provided"}), 400

        image_file = request.files['image']
        task_prompt = request.form.get('task_prompt', '<MORE_DETAILED_CAPTION>')
        text_input = request.form.get('text_input')

        logger.info(f"处理请求参数 - 文件名: {image_file.filename}, task_prompt: {task_prompt}, text_input: {text_input}")

        image = Image.open(image_file.stream).convert('RGB')
        result = process_image(image, task_prompt, text_input)
        logger.info("单图处理完成")
        return result[task_prompt]
    except Exception as e:
        logger.error(f"处理单图请求时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

def process_image_urls_api_route():
    try:
        logger.info("收到批量URL图片处理请求")
        data = request.get_json()
        if 'url_list' not in data:
            logger.warning("请求中缺少 url_list 字段")
            return jsonify({"error": "Missing 'url_list' in the request"}), 400

        url_list = data['url_list']
        task_prompt = data.get('task_prompt', '<MORE_DETAILED_CAPTION>')
        text_input = data.get('text_input')

        logger.info(f"处理请求参数 - URL数量: {len(url_list)}, task_prompt: {task_prompt}, text_input: {text_input}")

        results = []
        for idx, url in enumerate(url_list, 1):
            try:
                logger.info(f"开始处理第 {idx}/{len(url_list)} 个URL: {url}")
                # 增加重试次数和超时设置
                session = requests.Session()
                session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
                session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))

                response = session.get(url, timeout=(5, 10))  # 连接超时5秒，读取超时10秒
                response.raise_for_status()

                image = Image.open(io.BytesIO(response.content)).convert('RGB')
                result = process_image(image, task_prompt, text_input)
                results.append(result)
                logger.info(f"第 {idx} 个URL处理成功")
            except requests.exceptions.RequestException as e:
                error_msg = f"Error processing {url}: {str(e)}"
                if isinstance(e, requests.exceptions.ConnectionError):
                    error_msg = f"Connection failed for {url}: {str(e)}"
                    logger.error(f"第 {idx} 个URL连接失败: {str(e)}")
                elif isinstance(e, requests.exceptions.Timeout):
                    error_msg = f"Timeout while processing {url}: {str(e)}"
                    logger.error(f"第 {idx} 个URL处理超时: {str(e)}")
                elif isinstance(e, requests.exceptions.HTTPError):
                    error_msg = f"HTTP error for {url}: {str(e)}"
                    logger.error(f"第 {idx} 个URL HTTP错误: {str(e)}")
                results.append({"error": error_msg})
            except Exception as e:
                error_msg = f"Unexpected error processing {url}: {str(e)}"
                logger.error(f"第 {idx} 个URL处理时发生未预期错误: {str(e)}")
                logger.error(traceback.format_exc())
                results.append({"error": error_msg})

        logger.info(f"批量URL处理完成，成功: {sum(1 for r in results if 'error' not in r)}/{len(results)}")
        return jsonify([i[task_prompt] if task_prompt in i else i for i in results]), 200
    except Exception as e:
        logger.error(f"处理批量URL请求时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
