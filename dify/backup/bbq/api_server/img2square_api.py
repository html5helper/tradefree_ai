from PIL import Image
import os
import requests
import json
import uuid
import random
import time
import logging
import shutil
from urllib.parse import urlparse
from flask import request, jsonify
from config import output_dir

# 定义输出目录
# output_dir = os.environ.get("OUTPUT_DIR", "/tmp")

# 常用User-Agent列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux i686; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

# 常用Referer列表
REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.baidu.com/",
    "https://www.yahoo.com/",
    "https://www.instagram.com/",
    "https://www.pinterest.com/",
    "https://www.twitter.com/",
    "https://www.facebook.com/",
]


def get_random_headers():
    """生成随机请求头"""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Referer": random.choice(REFERERS),
    }
    return headers


def convert_to_square(image_path, output_path=None, background_color=(255, 255, 255)):
    """
    将图片转换为正方形，通过添加白色边框
    如果图片已经是正方形，则直接返回原图路径

    参数:
        image_path: 输入图片路径
        output_path: 输出图片路径（如果为None，则覆盖原文件）
        background_color: 背景颜色，默认为白色 (R,G,B)
    返回:
        str: 处理后的图片路径
    异常:
        IOError: 图片文件不存在或无法读取
        ValueError: 图片格式不支持或参数错误
    """
    try:
        # 检查输入文件是否存在
        if not os.path.exists(image_path):
            raise IOError(f"输入文件不存在: {image_path}")

        # 打开原始图片
        try:
            original_image = Image.open(image_path)
            # 检查图片格式
            format = original_image.format
            logging.info(f"处理图片: {image_path}, 格式: {format}")

            # 转换为RGB模式（处理RGBA、CMYK等格式）
            if original_image.mode != "RGB":
                logging.info(f"转换图片模式: {original_image.mode} -> RGB")
                original_image = original_image.convert("RGB")
        except Exception as e:
            raise ValueError(f"无法打开或处理图片: {e}")

        # 获取原始图片尺寸
        width, height = original_image.size
        logging.info(f"图片尺寸: {width}x{height}")

        # 检查图片是否已经是正方形
        if width == height:
            logging.info(f"图片已经是正方形，无需转换: {image_path} ({width}x{height})")
            # 如果指定了输出路径且与输入不同，则复制文件
            return "xxx"

        # 确定正方形边长（取长宽中较大的值）
        square_size = max(width, height)

        # 创建新的正方形图片
        square_image = Image.new("RGB", (square_size, square_size), background_color)

        # 计算粘贴位置（居中）
        paste_position = ((square_size - width) // 2, (square_size - height) // 2)

        # 将原始图片粘贴到新图片中心
        square_image.paste(original_image, paste_position)

        # 保存结果
        if output_path is None:
            output_path = image_path

        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 保存图片，尝试保持原始格式
        try:
            if format and format.lower() in ["jpeg", "jpg"]:
                square_image.save(output_path, format=format, quality=95)
            elif format and format.lower() == "png":
                square_image.save(output_path, format=format, optimize=True)
            elif format and format.lower() == "webp":
                square_image.save(output_path, format=format, quality=95)
            else:
                # 默认使用JPEG格式
                square_image.save(output_path, format="JPEG", quality=95)

            logging.info(
                f"已转换: {image_path} -> {output_path} ({width}x{height} -> {square_size}x{square_size})"
            )
        except Exception as e:
            logging.error(f"保存图片失败: {e}")
            raise IOError(f"保存图片失败: {e}")
        finally:
            # 关闭图片对象，释放内存
            if original_image:
                original_image.close()
            if square_image:
                square_image.close()

        return output_path

    except Exception as e:
        logging.error(f"转换图片失败: {e}")
        raise


def _get_filename_from_url(url, index):
    """
    从URL获取文件名

    参数:
        url: 图片URL
        index: 图片索引，用于生成默认文件名

    返回:
        str: 文件名
    """
    try:
        # 解析URL获取文件名
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        logging.debug(f"从URL解析的文件名: {filename}")

        if not filename or "." not in filename:
            logging.info(f"URL {url} 没有有效的文件名，尝试从Content-Type推断")
            # 根据Content-Type推断扩展名
            try:
                # 使用随机请求头
                headers = get_random_headers()
                # 添加重试机制
                max_retries = 3
                retry_count = 0

                while retry_count < max_retries:
                    try:
                        logging.debug(f"发送HEAD请求到 {url}")
                        response = requests.head(url, headers=headers, timeout=10)
                        response.raise_for_status()
                        break
                    except (
                        requests.exceptions.RequestException,
                        requests.exceptions.HTTPError,
                    ) as e:
                        retry_count += 1
                        if retry_count >= max_retries:
                            logging.warning(f"获取文件类型失败 {url}: {e}")
                            raise
                        # 指数退避策略
                        sleep_time = 2**retry_count + random.uniform(0, 1)
                        logging.info(
                            f"重试获取文件类型 {url}, 等待 {sleep_time:.2f} 秒..."
                        )
                        time.sleep(sleep_time)
                        # 更换请求头
                        headers = get_random_headers()

                content_type = response.headers.get("content-type", "")
                logging.info(f"URL {url} 的Content-Type: {content_type}")

                if "png" in content_type:
                    filename = f"image_{index}.png"
                elif "jpeg" in content_type or "jpg" in content_type:
                    filename = f"image_{index}.jpg"
                elif "webp" in content_type:
                    filename = f"image_{index}.webp"
                elif "gif" in content_type:
                    filename = f"image_{index}.gif"
                elif "svg" in content_type:
                    filename = f"image_{index}.svg"
                elif "tiff" in content_type:
                    filename = f"image_{index}.tiff"
                elif "bmp" in content_type:
                    filename = f"image_{index}.bmp"
                else:
                    logging.warning(
                        f"未知的Content-Type: {content_type}，使用默认jpg格式"
                    )
                    filename = f"image_{index}.jpg"  # 默认

                logging.info(f"根据Content-Type推断的文件名: {filename}")
            except Exception as e:
                logging.error(f"获取文件类型失败 {url}: {e}")
                filename = f"image_{index}.jpg"  # 默认
                logging.info(f"使用默认文件名: {filename}")

        return filename
    except Exception as e:
        logging.error(f"处理URL文件名时出错: {e}")
        return f"image_{index}.jpg"  # 出错时使用默认文件名


def _collect_images_from_urls(image_urls, temp_dir):
    """
    从URL收集图片

    参数:
        image_urls: 图片URL列表
        temp_dir: 临时目录路径，用于保存下载的图片

    返回:
        list: 下载成功的图片路径列表
    """
    image_paths = []
    total_urls = len(image_urls)

    logging.info(f"开始从{total_urls}个URL下载图片到{temp_dir}")

    # 确保临时目录存在
    if not os.path.exists(temp_dir):
        try:
            os.makedirs(temp_dir, exist_ok=True)
            logging.info(f"创建临时目录: {temp_dir}")
        except Exception as e:
            logging.error(f"创建临时目录失败: {e}")
            raise IOError(f"创建临时目录失败: {e}")

    for i, url in enumerate(image_urls):
        if not url or not url.strip():
            logging.warning(f"跳过空URL，索引: {i}")
            continue

        url = url.strip()
        logging.info(f"处理URL [{i+1}/{total_urls}]: {url}")

        # 使用随机请求头
        headers = get_random_headers()
        # 添加重试机制
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # 添加随机延迟，避免请求过于频繁
                if i > 0:  # 第一个请求不延迟
                    delay = random.uniform(1, 3)  # 随机1-3秒延迟
                    logging.info(f"请求延迟 {delay:.2f} 秒...")
                    time.sleep(delay)

                # 使用随机请求头发送请求
                logging.debug(f"发送GET请求到 {url}")
                response = requests.get(url, headers=headers, timeout=30, stream=True)
                response.raise_for_status()

                # 获取文件名
                filename = _get_filename_from_url(url, i)
                # 添加序号前缀保持顺序
                filename = f"{i:03d}_{filename}"
                image_path = os.path.join(temp_dir, filename)

                # 使用流式下载，减少内存占用
                file_size = 0
                with open(image_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            file_size += len(chunk)

                # 验证文件是否有效
                if file_size == 0:
                    logging.warning(f"下载的文件为空: {image_path}")
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    raise ValueError("下载的文件为空")

                # 尝试打开图片验证格式
                try:
                    with Image.open(image_path) as img:
                        img_format = img.format
                        img_size = img.size
                        logging.info(
                            f"图片格式: {img_format}, 尺寸: {img_size[0]}x{img_size[1]}"
                        )
                except Exception as e:
                    logging.warning(f"下载的文件不是有效图片: {e}")
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    raise ValueError(f"下载的文件不是有效图片: {e}")

                image_paths.append(image_path)
                logging.info(f"成功下载图片: {url} -> {image_path} ({file_size} 字节)")
                break  # 成功下载，跳出重试循环

            except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
            ) as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logging.error(f"下载图片失败 {url}: {e}")
                    break  # 达到最大重试次数，放弃此图片

                # 指数退避策略
                sleep_time = 2**retry_count + random.uniform(0, 1)
                logging.info(f"重试下载图片 {url}, 等待 {sleep_time:.2f} 秒...")
                time.sleep(sleep_time)
                # 更换请求头
                headers = get_random_headers()
            except ValueError as e:
                # 已经在上面处理了文件删除
                logging.error(f"图片验证失败 {url}: {e}")
                break
            except Exception as e:
                logging.error(f"下载图片失败 {url}: {e}")
                # 清理可能部分下载的文件
                if "image_path" in locals() and os.path.exists(image_path):
                    os.remove(image_path)
                    logging.info(f"删除部分下载的文件: {image_path}")
                break  # 其他异常，放弃此图片

    logging.info(f"图片下载完成，成功: {len(image_paths)}/{total_urls}")
    return image_paths


def process_images_to_square_route():
    """
    处理图片转正方形的API接口

    接收图片URL列表，将图片转换为正方形并返回处理后的图片路径

    请求参数:
        image_urls: 图片URL列表，可以是JSON数组字符串或逗号分隔的URL列表
        run_id: 任务ID，用于标识本次请求，如不提供则自动生成
        background_color: 背景颜色，格式为"R,G,B"，默认为"255,255,255"(白色)

    返回:
        JSON对象，包含处理后的图片路径列表、数量和状态信息
    """
    request_start_time = time.time()
    logging.info("收到图片转正方形请求")

    try:
        # 获取请求参数
        run_id = request.form.get("run_id", str(uuid.uuid4()))
        logging.info(f"任务ID: {run_id}")

        # 解析背景颜色
        try:
            background_color_str = request.form.get("background_color", "255,255,255")
            background_color = tuple(map(int, background_color_str.split(",")))
            # 验证RGB值范围
            if (
                any(c < 0 or c > 255 for c in background_color)
                or len(background_color) != 3
            ):
                raise ValueError(
                    f"无效的背景颜色值: {background_color_str}，应为'R,G,B'格式且值在0-255范围内"
                )
            logging.info(f"背景颜色: {background_color}")
        except ValueError as e:
            logging.error(f"背景颜色参数错误: {e}")
            return (
                jsonify({"error": f"Invalid background_color parameter: {str(e)}"}),
                400,
            )

        # 创建临时文件夹
        temp_dir = os.path.join(output_dir, "temp", run_id)
        try:
            os.makedirs(temp_dir, exist_ok=True)
            logging.info(f"创建临时目录: {temp_dir}")
        except Exception as e:
            logging.error(f"创建临时目录失败: {e}")
            return (
                jsonify({"error": f"Failed to create temporary directory: {str(e)}"}),
                500,
            )

        # 处理图片URL列表
        image_urls_str = request.form.get("image_urls")
        if not image_urls_str:
            logging.error("缺少'image_urls'参数")
            return jsonify({"error": "Missing 'image_urls' parameter"}), 400

        # 尝试解析JSON或逗号分隔的URL列表
        try:
            if isinstance(image_urls_str, str):
                if image_urls_str.strip().startswith(
                    "["
                ) and image_urls_str.strip().endswith("]"):
                    # 尝试解析JSON数组
                    image_urls = json.loads(image_urls_str)
                    logging.info(f"从JSON解析URL列表，包含{len(image_urls)}个URL")
                else:
                    # 尝试按逗号分隔
                    image_urls = [
                        url.strip() for url in image_urls_str.split(",") if url.strip()
                    ]
                    logging.info(
                        f"从逗号分隔字符串解析URL列表，包含{len(image_urls)}个URL"
                    )
            else:
                image_urls = image_urls_str
                logging.info(f"直接使用提供的URL列表，包含{len(image_urls)}个URL")
        except Exception as e:
            logging.error(f"解析image_urls参数失败: {e}")
            return (
                jsonify({"error": f"Failed to parse image_urls parameter: {str(e)}"}),
                400,
            )

        if not image_urls:
            logging.error("未提供有效的图片URL")
            return jsonify({"error": "No valid image URLs provided"}), 400

        # 下载图片
        logging.info(f"开始下载{len(image_urls)}个URL的图片")
        try:
            image_paths = _collect_images_from_urls(image_urls, temp_dir)
        except Exception as e:
            logging.error(f"下载图片过程中发生错误: {e}")
            return jsonify({"error": f"Error during image download: {str(e)}"}), 500

        if not image_paths:
            logging.error("未能从提供的URL下载任何图片")
            return (
                jsonify(
                    {"error": "Failed to download any images from the provided URLs"}
                ),
                400,
            )

        # 转换为正方形并保存
        logging.info(f"开始处理{len(image_paths)}张图片转为正方形")
        output_urls = []
        for i, image_path in enumerate(image_paths):
            try:
                # 生成输出文件名
                # output_filename = f"square_{i:03d}_{os.path.basename(image_path)}"
                output_filename = f"square_{os.path.basename(image_path)}"
                output_path = os.path.join(output_dir, run_id, output_filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                logging.info(
                    f"处理图片 [{i+1}/{len(image_paths)}]: {image_path} -> {output_path}"
                )

                # 转换为正方形
                converted_path = convert_to_square(
                    image_path, output_path, background_color
                )
                if converted_path == "xxx":
                    output_urls.append(image_urls[i])
                else:
                    output_urls.append(
                        f"http://dify.html5core.com/svg/{run_id}/{output_filename}"
                    )
            except Exception as e:
                logging.error(f"处理图片失败 {image_path}: {e}")
                continue

        if not output_urls:
            logging.error("未能将任何图片转换为正方形")
            return jsonify({"error": "Failed to convert any images to square"}), 500

        # 计算处理时间
        process_time = time.time() - request_start_time
        logging.info(
            f"请求处理完成，共处理{len(output_urls)}张图片，耗时{process_time:.2f}秒"
        )
        return jsonify(
            {
                "image_paths": output_urls,
                "count": len(output_urls),
                "process_time_seconds": round(process_time, 2),
                "message": "Images converted to square successfully",
            }
        )

    except ValueError as e:
        logging.error(f"参数错误: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"处理请求时发生错误: {e}", exc_info=True)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        # 清理临时文件夹
        try:
            shutil.rmtree(temp_dir)
            logging.info(f"已删除临时目录: {temp_dir}")
        except Exception as e:
            logging.error(f"删除临时目录失败: {e}")


# 使用示例：
if __name__ == "__main__":
    # 示例用法1：转换单个图片
    convert_to_square("/Users/qinbinbin/Desktop/tttt.jpg", "output.jpg")

    # 示例用法2：批量转换文件夹中的所有图片
    # batch_convert_to_square("input_images", "output_images")

    # 如果你想使用其他背景颜色，例如黑色
    # convert_to_square("input.jpg", background_color=(0, 0, 0))
