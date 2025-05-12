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
            print("[Error] 请求中未包含文件字段 'files'")
            return jsonify({"error": "Missing 'files' field in request"}), 400
            
        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            print("[Error] 文件列表为空或文件名为空")
            return jsonify({"error": "Empty file list or invalid filenames"}), 400

        # 获取文件夹类型参数
        folder_type = request.form.get('folder_type')
        if not folder_type:
            print("[Error] 缺少必需的 folder_type 参数")
            return jsonify({"error": "Missing required folder_type parameter"}), 400

        print(f"[Info] 开始处理上传请求，folder_type: {folder_type}, 文件数量: {len(files)}")

        results = []
        for file in files:
            if file.filename == '':
                continue
                
            try:
                print(f"[Info] 处理文件: {file.filename}")
                # 生成OSS路径
                oss_path = generate_oss_path(file.filename, folder_type)
                
                # 直接读取文件内容
                try:
                    file_content = file.read()
                    if not file_content:
                        raise ValueError("Empty file content")
                except Exception as e:
                    print(f"[Error] 读取文件内容失败: {str(e)}")
                    raise
                
                # 上传到OSS并获取URL
                try:
                    url = uploader.upload_bytes(file_content, oss_path)
                    print(f"[Info] 文件上传成功: {oss_path}")
                except Exception as e:
                    print(f"[Error] OSS上传失败: {str(e)}")
                    raise
                
                results.append({
                    "success": True,
                    "filename": file.filename,
                    "url": url,
                    "oss_path": oss_path
                })
                        
            except Exception as e:
                error_msg = f"处理文件失败: {str(e)}"
                print(f"[Error] {error_msg}")
                results.append({
                    "success": False,
                    "filename": file.filename,
                    "error": error_msg
                })

        print(f"[Info] 请求处理完成，成功: {sum(1 for r in results if r.get('success'))}/{len(results)}")
        return jsonify({
            "success": True,
            "results": results
        })
                
    except Exception as e:
        error_msg = f"请求处理失败: {str(e)}"
        print(f"[Error] {error_msg}")
        return jsonify({"error": error_msg}), 500