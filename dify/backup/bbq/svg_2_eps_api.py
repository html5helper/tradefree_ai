import os
from flask import Flask, request, jsonify
import cairosvg

app = Flask(__name__)
# 设置输出路径
OUTPUT_DIR = "/home/qinbinbin/ai_tools/dify/docker/volumes/certbot/www/svg"

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)