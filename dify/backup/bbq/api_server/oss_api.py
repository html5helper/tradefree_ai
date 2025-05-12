import os
from datetime import datetime
from flask import request, jsonify
from tools.upload2oss import OSSUploader

# 初始化 OSS 上传器
uploader = OSSUploader(
    endpoint='https://oss-us-east-1.aliyuncs.com',  # 根据实际情况修改
    bucket_name='tradefree'  # 使用实际的bucket名称
)

def generate_oss_path(filename, folder_type='txt2img'):
    """生成OSS路径
    Args:
        filename: 原始文件名
        folder_type: 文件夹类型，默认为txt2img
    Returns:
        str: OSS完整路径
    """
    date_str = datetime.now().strftime('%Y%m%d')
    return f"comfyui/{date_str}/{folder_type}/{filename}"

def upload_file_to_oss_route():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
            
        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return jsonify({"error": "No selected files"}), 400

        # 获取文件夹类型参数
        folder_type = request.form.get('folder_type', 'txt2img')

        results = []
        for file in files:
            if file.filename == '':
                continue
                
            try:
                # 生成OSS路径
                oss_path = generate_oss_path(file.filename, folder_type)
                
                # 直接读取文件内容
                file_content = file.read()
                
                # 上传到OSS并获取URL
                url = uploader.upload_bytes(file_content, oss_path)
                
                results.append({
                    "success": True,
                    "filename": file.filename,
                    "url": url,
                    "oss_path": oss_path
                })
                        
            except Exception as e:
                results.append({
                    "success": False,
                    "filename": file.filename,
                    "error": str(e)
                })

        return jsonify({
            "success": True,
            "results": results
        })
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500