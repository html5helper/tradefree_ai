import requests
import torch
import traceback
import io
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from flask import request, jsonify
from config import device, torch_dtype, model_path

# 启动时一次性加载模型到合适 device
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)

def process_image(image, task_prompt, text_input=None):
    # prompt 拼接优化
    prompt = task_prompt if text_input is None else task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        num_beams=3
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(generated_text, task=task_prompt,
                                                      image_size=(image.width, image.height))
    return parsed_answer

def process_image_api_route():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        image_file = request.files['image']
        image = Image.open(image_file.stream).convert('RGB')
        task_prompt = request.form.get('task_prompt', '<MORE_DETAILED_CAPTION>')
        text_input = request.form.get('text_input')
        result = process_image(image, task_prompt, text_input)
        return result[task_prompt]
    except Exception as e:
        traceback.print_exc()  # 输出详细错误堆栈到 gunicorn 日志
        return jsonify({"error": str(e)}), 500


def process_image_urls_api_route():
    try:
        data = request.get_json()
        if 'url_list' not in data:
            return jsonify({"error": "Missing 'url_list' in the request"}), 400

        url_list = data['url_list']
        task_prompt = data.get('task_prompt', '<MORE_DETAILED_CAPTION>')
        text_input = data.get('text_input')
        results = []
        for url in url_list:
            try:
                # 增加重试次数和超时设置
                session = requests.Session()
                session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
                session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
                
                response = session.get(url, timeout=(5, 10))  # 连接超时5秒，读取超时10秒
                response.raise_for_status()
                
                image = Image.open(io.BytesIO(response.content)).convert('RGB')
                result = process_image(image, task_prompt, text_input)
                results.append(result)
            except requests.exceptions.RequestException as e:
                # 更详细的错误信息
                error_msg = f"Error processing {url}: {str(e)}"
                if isinstance(e, requests.exceptions.ConnectionError):
                    error_msg = f"Connection failed for {url}: {str(e)}"
                elif isinstance(e, requests.exceptions.Timeout):
                    error_msg = f"Timeout while processing {url}: {str(e)}"
                elif isinstance(e, requests.exceptions.HTTPError):
                    error_msg = f"HTTP error for {url}: {str(e)}"
                results.append({"error": error_msg})
            except Exception as e:
                results.append({"error": f"Unexpected error processing {url}: {str(e)}"})

        return jsonify([i[task_prompt] if task_prompt in i else i for i in results]), 200
    except Exception as e:
        traceback.print_exc()  # 输出详细错误堆栈到 gunicorn 日志
        return jsonify({"error": str(e)}), 500
