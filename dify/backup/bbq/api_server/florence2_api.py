import requests
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from flask import request, jsonify

from config import device, torch_dtype, model_path

# 初始化模型在 CPU 上
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch_dtype, trust_remote_code=True).to("cpu")
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)


def process_image(image, task_prompt, text_input=None):
    global model
    # 将模型移动到 GPU
    if torch.cuda.is_available():
        model = model.to(device)

    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
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
    # 将模型移回 CPU 以释放 GPU 资源
    if torch.cuda.is_available():
        model = model.to("cpu")
        torch.cuda.empty_cache()  # 清空 GPU 缓存

    return parsed_answer


def process_image_api_route():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        image_file = request.files['image']
        image = Image.open(image_file.stream)
        task_prompt = request.form.get('task_prompt', '<MORE_DETAILED_CAPTION>')
        text_input = request.form.get('text_input')

        result = process_image(image, task_prompt, text_input)
        return result[task_prompt]
    except Exception as e:
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
                response = requests.get(url, stream=True)
                response.raise_for_status()
                image = Image.open(response.raw)
                result = process_image(image, task_prompt, text_input)
                results.append(result)
            except Exception as e:
                results.append({"error": f"Error processing {url}: {str(e)}"})

        return jsonify([i[task_prompt] for i in results]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
