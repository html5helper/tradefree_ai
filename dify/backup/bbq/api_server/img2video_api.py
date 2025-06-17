import os
import cv2
import math
import requests
import json
import numpy as np
import glob

from PIL import Image
from urllib.parse import urlparse
from flask import request, jsonify
from moviepy import VideoFileClip, AudioFileClip
from moviepy.audio.fx import AudioLoop

from config import output_dir, default_audio_path

# output_dir = '/tmp'


class ImageToVideo:
    def __init__(self, size=(800, 800), fps=25, output_path="output.mp4"):
        self.size = size  # 宽, 高
        self.fps = fps
        self.output_path = output_path
        # 修改编码器为 avc1，这是 H.264 编码，具有更好的兼容性
        # self.fourcc = cv2.VideoWriter_fourcc(*'avc1')
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = None
        self.transition_frames = int(fps * 2)  # 增加转场帧数到2秒
        self.intro_duration = int(fps * 3)  # 片头持续3秒
        self.outro_duration = int(fps * 3)  # 片尾持续3秒
        self.static_duration = int(fps * 2)  # 每张图片静态显示2秒

    def __enter__(self):
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
        self.video_writer = cv2.VideoWriter(
            self.output_path, self.fourcc, self.fps, self.size
        )
        if not self.video_writer.isOpened():
            raise RuntimeError(f"无法创建视频文件：{self.output_path}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.video_writer:
            self.video_writer.release()

    def add_audio(self, audio_path, output_path=None):
        """为视频添加音效"""
        if output_path is None:
            output_path = self.output_path.replace(".mp4", "_with_audio.mp4")

        try:
            # 确保视频写入器已关闭
            if self.video_writer:
                self.video_writer.release()

            # 等待一小段时间确保文件写入完成
            import time

            time.sleep(1)

            # 检查视频文件是否存在且大小不为0
            if (
                not os.path.exists(self.output_path)
                or os.path.getsize(self.output_path) == 0
            ):
                raise RuntimeError(f"视频文件无效或为空：{self.output_path}")

            # 加载视频和音频
            video = VideoFileClip(self.output_path)
            audio = AudioFileClip(audio_path)

            # 如果音频长度不够，循环播放直到匹配视频长度
            if audio.duration < video.duration:
                audio = audio.with_effects([AudioLoop(duration=video.duration)])
            # 如果音频太长，裁剪到视频长度
            else:
                audio = audio.subclipped(0, video.duration)

            # 合并视频和音频
            final_video = video.with_audio(audio)
            # final_video.write_videofile(output_path, codec='libx264')
            final_video.write_videofile(
                output_path,
                codec="libx264",  # 视频编码
                audio_codec="aac",  # 强制使用 AAC 音频编码
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
                fps=24,
                audio_bitrate="192k",  # 提高音频码率（可选）
            )

            # 清理资源
            video.close()
            audio.close()
            final_video.close()

        except Exception as e:
            raise RuntimeError(f"添加音频时发生错误：{str(e)}")

    def read_and_resize(self, path):
        try:
            # 使用 PIL 打开并调整尺寸，确保格式一致性
            pil_img = Image.open(path).convert("RGB")
            pil_img = pil_img.resize(self.size, Image.LANCZOS)

            # 转换为 OpenCV 格式 (BGR)
            img = np.array(pil_img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            print(f"已加载图片: {path}, 尺寸: {img.shape}")
            return img
        except Exception as e:
            raise RuntimeError(f"处理图片失败: {path}, 错误: {str(e)}")

    def add_subtitle(self, img, text, font_scale=1, color=(0, 0, 0), thickness=2):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        x = (self.size[0] - text_size[0]) // 2
        y = self.size[1] - 30  # 距离底部30像素
        cv2.putText(img, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
        return img

    def add_static_frame(self, img, duration, subtitle=None):
        width, height = self.size
        for i in range(duration):
            # 创建光影遮罩
            mask = np.zeros((height, width), dtype=np.float32)
            # 光影位置
            light_position = int((width / duration) * i)
            # 光影宽度
            light_width = int(width * 0.2)
            # 计算光影的起始和结束位置
            start = max(0, light_position - light_width // 2)
            end = min(width, light_position + light_width // 2)
            # 创建渐变光影
            for x in range(start, end):
                distance = abs(x - light_position)
                intensity = 1 - (distance / (light_width / 2))
                mask[:, x] = intensity

            # 将遮罩扩展到三个通道
            mask = np.stack([mask] * 3, axis=-1)

            # 应用光影效果
            frame = img * (1 + mask * 0.5)  # 增强光影效果
            frame = np.clip(frame, 0, 255).astype(np.uint8)

            if subtitle:
                frame = self.add_subtitle(frame, subtitle)
            self.video_writer.write(frame)

    def create_intro(self):
        """创建片头动画"""
        # 创建黑色背景
        intro_frame = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        # 添加文字
        text = "Product Introduction"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (self.size[0] - text_size[0]) // 2
        text_y = (self.size[1] + text_size[1]) // 2

        # 淡入效果
        for i in range(self.intro_duration):
            frame = intro_frame.copy()
            alpha = min(1.0, i / (self.intro_duration * 0.3))  # 在前30%的时间内完成淡入
            cv2.putText(
                frame,
                text,
                (text_x, text_y),
                font,
                font_scale,
                (int(255 * alpha), int(255 * alpha), int(255 * alpha)),
                thickness,
            )
            self.video_writer.write(frame)

    def create_outro(self):
        """创建片尾动画"""
        # 创建黑色背景
        outro_frame = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        # 添加文字
        text = "Thank You"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (self.size[0] - text_size[0]) // 2
        text_y = (self.size[1] + text_size[1]) // 2

        # 淡出效果
        for i in range(self.outro_duration):
            frame = outro_frame.copy()
            alpha = 1.0 - min(
                1.0, i / (self.outro_duration * 0.7)
            )  # 在后70%的时间内完成淡出
            cv2.putText(
                frame,
                text,
                (text_x, text_y),
                font,
                font_scale,
                (int(255 * alpha), int(255 * alpha), int(255 * alpha)),
                thickness,
            )
            self.video_writer.write(frame)

    def add_transition(self, img1, img2, frames):
        """增强的过渡效果"""
        for i in range(frames):
            progress = i / frames
            # 使用缓动函数使过渡更平滑
            alpha = self.ease_in_out(progress)

            # 添加缩放效果
            scale = 1.0 + 0.1 * math.sin(progress * math.pi)
            h, w = img1.shape[:2]
            scaled_size = (int(w * scale), int(h * scale))

            # 缩放两张图片
            scaled_img1 = cv2.resize(img1, scaled_size)
            scaled_img2 = cv2.resize(img2, scaled_size)

            # 裁剪到原始尺寸
            start_x = (scaled_size[0] - w) // 2
            start_y = (scaled_size[1] - h) // 2
            scaled_img1 = scaled_img1[start_y : start_y + h, start_x : start_x + w]
            scaled_img2 = scaled_img2[start_y : start_y + h, start_x : start_x + w]

            # 混合图片
            transition = cv2.addWeighted(scaled_img1, 1 - alpha, scaled_img2, alpha, 0)
            self.video_writer.write(transition)

    def ease_in_out(self, x):
        """缓动函数，使过渡更平滑"""
        if x < 0.5:
            return 2 * x * x
        else:
            return 1 - pow(-2 * x + 2, 2) / 2

    def create_video(self, image_paths):
        # 添加片头
        self.create_intro()

        prev_img = None
        for i, path in enumerate(image_paths):
            if path.lower().endswith(".webp"):
                try:
                    gif = Image.open(path)
                    frame_count = 0
                    while True:
                        frame = gif.copy()
                        frame = frame.convert("RGB")
                        frame = frame.resize(self.size, Image.LANCZOS)
                        frame = np.array(frame)
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                        if prev_img is not None and frame_count == 0:
                            self.add_transition(prev_img, frame, self.transition_frames)
                        if frame_count == 0:
                            self.add_static_frame(
                                frame,
                                self.static_duration,
                                subtitle=f"Product Introduction {i}",
                            )
                        else:
                            self.video_writer.write(frame)

                        frame_count += 1
                        try:
                            gif.seek(frame_count)
                        except EOFError:
                            break
                    prev_img = frame
                except Exception as e:
                    print(f"处理动图 {path} 时出错: {e}")
            else:
                img = self.read_and_resize(path)
                if prev_img is not None:
                    self.add_transition(prev_img, img, self.transition_frames)
                self.add_static_frame(
                    img, self.static_duration, subtitle=f"Product Introduction {i}"
                )
                prev_img = img

        # 添加片尾
        self.create_outro()


def _parse_request_parameters():
    """解析请求参数"""
    size = tuple(map(int, request.form.get("size", "800,800").split(",")))
    fps = int(request.form.get("fps", "25"))
    run_id = request.form.get("run_id")
    input_directory = request.form.get("input_directory")

    return {
        "size": size,
        "fps": fps,
        "run_id": run_id,
        "input_directory": input_directory,
    }


def _collect_images_from_directory(input_directory):
    """从目录收集图片文件"""
    image_paths = []
    image_extensions = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.webp",
        "*.bmp",
        "*.tiff",
        "*.gif",
    ]

    for ext in image_extensions:
        pattern = os.path.join(input_directory, ext)
        image_paths.extend(glob.glob(pattern))
        # 同时搜索大写扩展名
        pattern_upper = os.path.join(input_directory, ext.upper())
        image_paths.extend(glob.glob(pattern_upper))

    # 按文件名排序确保顺序正确
    image_paths.sort()
    return image_paths


def _collect_images_from_upload(temp_dir):
    """从文件上传收集图片"""
    image_paths = []
    image_files = request.files.getlist("images")

    for i, image in enumerate(image_files):
        if image.filename:
            # 保持原始文件名和扩展名
            filename = f"{i:03d}_{image.filename}"
            image_path = os.path.join(temp_dir, filename)
            image.save(image_path)
            image_paths.append(image_path)

    return image_paths


def _get_filename_from_url(url, index):
    """从URL获取文件名"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if not filename or "." not in filename:
        # 根据Content-Type推断扩展名
        try:
            response = requests.head(url, timeout=10)
            content_type = response.headers.get("content-type", "")
            if "webp" in content_type:
                filename = f"image_{index}.webp"
            elif "png" in content_type:
                filename = f"image_{index}.png"
            elif "jpeg" in content_type or "jpg" in content_type:
                filename = f"image_{index}.jpg"
            else:
                filename = f"image_{index}.png"  # 默认
        except:
            filename = f"image_{index}.png"  # 默认

    return filename


def _collect_images_from_urls(temp_dir):
    """从URL收集图片"""
    image_paths = []
    image_urls_str = request.form.get("image_urls")

    try:
        image_urls = (
            json.loads(image_urls_str)
            if isinstance(image_urls_str, str)
            else image_urls_str
        )
    except:
        image_urls = (
            image_urls_str.split(",") if isinstance(image_urls_str, str) else []
        )

    for i, url in enumerate(image_urls):
        if url.strip():
            try:
                response = requests.get(url.strip(), timeout=30)
                response.raise_for_status()

                filename = _get_filename_from_url(url, i)
                # 添加序号前缀保持顺序
                filename = f"{len(image_paths):03d}_{filename}"
                image_path = os.path.join(temp_dir, filename)

                with open(image_path, "wb") as f:
                    f.write(response.content)
                image_paths.append(image_path)
            except Exception as e:
                print(f"下载图片失败 {url}: {e}")
                continue

    return image_paths


def _collect_all_images(params, temp_dir):
    """收集所有图片文件"""
    input_directory = params["input_directory"]

    # 处理目录输入的图片
    if input_directory and os.path.isdir(input_directory):
        image_paths = _collect_images_from_directory(input_directory)
        if not image_paths:
            raise ValueError(f"No valid images found in directory: {input_directory}")
        return image_paths, True  # 返回是否来自目录

    # 处理文件上传的图片
    elif "images" in request.files:
        return _collect_images_from_upload(temp_dir), False

    # 处理URL形式的图片
    elif "image_urls" in request.form:
        return _collect_images_from_urls(temp_dir), False

    else:
        raise ValueError(
            "No valid images provided. Please provide either 'input_directory', upload 'images', or provide 'image_urls'."
        )


def _process_audio(temp_dir, run_id, video_maker):
    """处理音频文件"""
    output_path = video_maker.output_path

    # 如果有音频文件
    if "audio" in request.files:
        audio_file = request.files["audio"]
        if audio_file.filename:
            audio_path = os.path.join(temp_dir, audio_file.filename)
            audio_file.save(audio_path)
            output_path_with_audio = os.path.join(
                output_dir, f"{run_id}_with_audio.mp4"
            )
            video_maker.add_audio(audio_path, output_path_with_audio)
            return output_path_with_audio
    else:
        output_path_with_audio = os.path.join(output_dir, f"{run_id}_with_audio.mp4")
        video_maker.add_audio(default_audio_path, output_path_with_audio)
        return output_path.replace(".mp4", "_no_audio.mp4")

    return output_path


def process_images_to_video_route():
    """处理图片转视频的主要接口"""
    try:
        # 1. 解析请求参数
        params = _parse_request_parameters()

        if not params["run_id"]:
            return jsonify({"error": "Missing 'run_id' parameter"}), 400

        # 2. 创建临时文件夹
        temp_dir = os.path.join(output_dir, "temp", params["run_id"])
        os.makedirs(temp_dir, exist_ok=True)

        # 3. 收集图片文件
        image_paths, from_directory = _collect_all_images(params, temp_dir)

        # 4. 如果不是从目录读取的图片，按文件名排序确保顺序正确
        if not from_directory:
            image_paths.sort()

        # 5. 设置输出视频路径
        output_path = os.path.join(output_dir, f"{params['run_id']}.mp4")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 6. 创建视频
        with ImageToVideo(
            size=params["size"], fps=params["fps"], output_path=output_path
        ) as video_maker:
            video_maker.create_video(image_paths)

            # 7. 处理音频
            final_output_path = _process_audio(temp_dir, params["run_id"], video_maker)

        return jsonify(
            {"video_path": final_output_path, "message": "Video created successfully"}
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# 使用示例：
if __name__ == "__main__":
    # 图片路径列表
    image_paths = [
        f"/Users/qinbinbin/Desktop/comfyui/xxx/a_0000{i}_.png" for i in range(1, 6)
    ]
    image_paths = (
        [
            f"/Users/qinbinbin/Desktop/comfyui/xxx/ComfyUI_27610_.webp",
        ]
        + image_paths
        + [
            f"/Users/qinbinbin/Desktop/comfyui/xxx/ComfyUI_27612_.webp",
        ]
    )

    # 使用上下文管理器创建视频
    with ImageToVideo() as video_maker:
        video_maker.create_video(image_paths)
        # 添加音效（需要提供音频文件路径）
        video_maker.add_audio(
            "/Users/qinbinbin/PycharmProjects/tradefree_ai/dify/backup/bbq/api_server/bgm.mp3"
        )

    print("视频生成完成！")
