import os
import subprocess
import tempfile
from flask import request, jsonify
from config import output_dir

def convert_svg_to_cmyk_pdf_route():
    """
    将SVG文件转换为CMYK PDF文件的API接口
    支持文件上传和文件路径两种输入方式
    """
    try:
        svg_content = None
        svg_filename = None
        
        # 检查是否有文件上传
        if 'svg_file' in request.files:
            svg_file = request.files['svg_file']
            if svg_file.filename != '':
                svg_content = svg_file.read()
                svg_filename = svg_file.filename
        
        # 检查是否提供了文件路径
        svg_path = request.form.get('svg_path')
        if svg_path and os.path.exists(svg_path):
            with open(svg_path, 'rb') as f:
                svg_content = f.read()
            svg_filename = os.path.basename(svg_path)
        
        # 如果既没有文件上传也没有有效路径
        if not svg_content:
            return jsonify({
                "error": "请提供SVG文件（通过文件上传'svg_file'或文件路径'svg_path'）"
            }), 400
        
        # 获取run_id参数，如果没有则使用文件名
        run_id = request.form.get('run_id')
        if not run_id:
            if svg_filename:
                run_id = os.path.splitext(svg_filename)[0]
            else:
                run_id = "converted_svg"
        
        # 检查依赖
        if not _check_dependencies():
            return jsonify({
                "error": "缺少必要依赖：请安装inkscape和ghostscript"
            }), 500
        
        # 执行转换
        result = _convert_svg_to_cmyk_pdf(svg_content, run_id)
        
        if result['success']:
            return jsonify({
                "success": True,
                "pdf_path": result['pdf_path'],
                "pdf_name": result['pdf_name']
            })
        else:
            return jsonify({
                "error": f"转换失败: {result['error']}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"处理请求时发生错误: {str(e)}"
        }), 500

def _check_dependencies():
    """
    检查必要的依赖是否已安装
    """
    try:
        # 检查inkscape
        subprocess.run(['inkscape', '--version'], 
                      capture_output=True, check=True)
        
        # 检查ghostscript
        subprocess.run(['gs', '--version'], 
                      capture_output=True, check=True)
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def _convert_svg_to_cmyk_pdf(svg_content, run_id):
    """
    执行SVG到CMYK PDF的转换
    """
    try:
        # 创建临时文件保存SVG内容
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.svg', delete=False) as svg_temp:
            svg_temp.write(svg_content)
            svg_temp_path = svg_temp.name
        
        # 定义输出路径
        pdf_temp_path = os.path.join(output_dir, f"{run_id}_temp.pdf")
        pdf_cmyk_path = os.path.join(output_dir, f"{run_id}_CMYK.pdf")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # 第一步：使用inkscape将SVG转换为PDF
            inkscape_cmd = [
                'inkscape',
                svg_temp_path,
                '--export-type=pdf',
                f'--export-filename={pdf_temp_path}'
            ]
            
            result = subprocess.run(inkscape_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            # 第二步：使用ghostscript将PDF转换为CMYK
            # CMYK配置文件路径（可选）
            cmyk_profile = "/home/qinbinbin/ai_tools/comfyui/tmp/ISOcoated_v2_300_eci.icc"
            
            gs_cmd = [
                'gs',
                '-sDEVICE=pdfwrite',
                '-dProcessColorModel=/DeviceCMYK',
                f'-sOutputFile={pdf_cmyk_path}',
                '-dPreserveOverprintSettings=true',
                '-dNOPAUSE',
                '-dBATCH',
                '-dSAFER'
            ]
            
            # 如果CMYK配置文件存在，添加到命令中
            if os.path.exists(cmyk_profile):
                gs_cmd.insert(-4, f'-sDefaultCMYKProfile={cmyk_profile}')
            
            gs_cmd.append(pdf_temp_path)
            
            result = subprocess.run(gs_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            # 清理临时文件
            if os.path.exists(pdf_temp_path):
                os.remove(pdf_temp_path)
            
            return {
                'success': True,
                'pdf_path': pdf_cmyk_path,
                'pdf_name': f"{run_id}_CMYK.pdf"
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f"命令执行失败: {e.stderr if e.stderr else str(e)}"
            }
        
        finally:
            # 清理SVG临时文件
            if os.path.exists(svg_temp_path):
                os.remove(svg_temp_path)
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }