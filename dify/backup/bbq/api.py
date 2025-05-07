import os
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from flask import Flask, request, jsonify
import cairosvg

app = Flask(__name__)

# 设置输出路径
OUTPUT_DIR = "/home/qinbinbin/ai_tools/dify/docker/volumes/certbot/www/svg"

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_path = "/home/qinbinbin/ai_tools/ComfyUI/models/florence2/large"
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)


def process_image(image, task_prompt, text_input=None):
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
    return parsed_answer


@app.route('/convert_svg_to_eps', methods=['POST'])
def convert_svg_to_eps():
    # 检查请求中是否包含文件
    if 'svg_file' not in request.files:
        return jsonify({"error": "Missing 'svg_file' in the request"}), 400

    svg_file = request.files['svg_file']
    if svg_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 获取 run_id 参数
    run_id = request.form.get('run_id')
    if not run_id:
        return jsonify({"error": "Missing 'run_id' parameter"}), 400

    try:
        # 读取 SVG 文件内容
        svg_content = svg_file.read()

        # 生成 EPS 文件路径，以 run_id 命名
        eps_filename = os.path.join(OUTPUT_DIR, f"{run_id}.eps")
        os.makedirs(os.path.dirname(eps_filename), exist_ok=True)

        # 将 SVG 转换为 EPS
        cairosvg.svg2eps(bytestring=svg_content, write_to=eps_filename)

        return jsonify({"eps_name": f"{run_id}.eps"})
    except Exception as e:
        return jsonify({"error": f"An error occurred during conversion: {str(e)}"}), 500


@app.route('/process_image', methods=['POST'])
def process_image_api():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        image_file = request.files['image']
        image = Image.open(image_file.stream)
        task_prompt = request.form.get('task_prompt', '<MORE_DETAILED_CAPTION>')
        text_input = request.form.get('text_input')

        result = process_image(image, task_prompt, text_input)
        return jsonify({"parsed_answer": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
