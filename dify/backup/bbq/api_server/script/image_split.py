import os
from pathlib import Path
from PIL import Image
import numpy as np

# 导入rembg库用于背景移除
try:
    import rembg
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("警告: rembg库未安装，背景移除功能将不可用。请运行 'pip install rembg' 安装。")

def remove_background(img, log_callback=None):
    """移除图片背景
    
    Args:
        img (PIL.Image): 输入图片对象
        log_callback (callable, optional): 日志回调函数
        
    Returns:
        PIL.Image: 移除背景后的图片对象，如果rembg不可用则返回原图
    """
    if not REMBG_AVAILABLE:
        if log_callback:
            log_callback("警告: rembg库未安装，无法移除背景。请运行 'pip install rembg' 安装。")
        return img
    
    try:
        # 确保图片为RGBA模式以支持透明背景
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 使用rembg移除背景
        result = rembg.remove(img)
        
        if log_callback:
            log_callback("成功移除图片背景")
        
        return result
    except Exception as e:
        if log_callback:
            log_callback(f"移除背景失败: {str(e)}")
        return img

def split_image(image_path, output_dir=None, split_mode="4", remove_bg=False, log_callback=None):
    """分割单张图片（支持四宫格和九宫格）
    
    Args:
        image_path (str): 输入图片的文件路径
        output_dir (str, optional): 输出目录路径，默认为与输入图片相同的目录
        split_mode (str, optional): 分割模式，"4"表示四宫格，"9"表示九宫格，默认为"4"
        remove_bg (bool, optional): 是否移除背景，默认为False
        log_callback (callable, optional): 日志回调函数，用于输出日志信息
        
    Returns:
        tuple: (成功标志, 消息, 分割后的文件路径列表)
    """
    try:
        # 处理输出目录
        if output_dir is None:
            output_dir = os.path.dirname(image_path)
            
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取文件名（不含扩展名）作为基础名
        filename_base = Path(image_path).stem
        
        # 获取原图文件扩展名
        original_ext = Path(image_path).suffix.lower()
        # 映射文件扩展名到PIL格式
        format_map = {
            '.jpg': 'JPEG', '.jpeg': 'JPEG',
            '.png': 'PNG', '.bmp': 'BMP',
            '.tiff': 'TIFF', '.tif': 'TIFF'
        }
        output_format = format_map.get(original_ext, 'PNG')
        
        # 存储分割后的文件路径
        output_paths = []
        
        with Image.open(image_path) as img:
            # 如果需要移除背景，先处理背景移除
            if remove_bg:
                if log_callback:
                    log_callback(f"正在移除 {filename_base} 的背景...")
                img = remove_background(img, log_callback)
            
            # 获取原图尺寸
            width, height = img.size
            original_width, original_height = width, height
            
            # 根据分割模式处理图片尺寸
            if split_mode == "9":
                # 九宫格需要正方形图片
                if width != height:
                    if log_callback:
                        log_callback(f"警告: {filename_base} 不是正方形图片 ({width}x{height})，九宫格分割需要裁剪为正方形")
                    # 取较小的尺寸作为正方形边长
                    size = min(width, height)
                    # 居中裁剪为正方形
                    left = (width - size) // 2
                    top = (height - size) // 2
                    img = img.crop((left, top, left + size, top + size))
                    width = height = size
                    
            else:
                # 四宫格保持原图完整性，不进行裁剪
                if width != height and log_callback:
                    log_callback(f"信息: {filename_base} 为长图 ({width}x{height})，四宫格分割将保持完整性")
            
            # 根据分割模式确定网格大小
            if split_mode == "9":
                grid_size = 3
                mode_name = "九宫格"
                # 九宫格使用均匀分割
                sub_width = width // grid_size
                sub_height = height // grid_size
                
                # 生成分割位置
                positions = []
                for row in range(grid_size):
                    for col in range(grid_size):
                        left = col * sub_width
                        top = row * sub_height
                        right = left + sub_width
                        bottom = top + sub_height
                        positions.append((left, top, right, bottom))
            else:
                mode_name = "四宫格"
                # 四宫格使用十字风格分割，以中心点为基准
                center_x = width // 2
                center_y = height // 2
                
                # 四宫格分割位置（十字风格）
                positions = [
                    (0, 0, center_x, center_y),              # 左上
                    (center_x, 0, width, center_y),         # 右上
                    (0, center_y, center_x, height),        # 左下
                    (center_x, center_y, width, height)     # 右下
                ]
            
            # 保存子图
            for i, pos in enumerate(positions, 1):
                sub_img = img.crop(pos)
                output_filename = f"{filename_base}_{i}{original_ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                # 保存时保持原格式
                if output_format == 'JPEG':
                    # JPEG不支持透明度，需要转换为RGB
                    if sub_img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', sub_img.size, (255, 255, 255))
                        background.paste(sub_img, mask=sub_img.split()[-1] if sub_img.mode == 'RGBA' else None)
                        sub_img = background
                    sub_img.save(output_path, output_format, quality=95)
                else:
                    sub_img.save(output_path, output_format)
                
                # 添加到输出路径列表
                output_paths.append(output_path)
            
            return True, f"成功分割: {filename_base} ({mode_name})", output_paths
            
    except Exception as e:
        error_msg = f"分割失败 {Path(image_path).stem}: {str(e)}"
        return False, error_msg, []