import os
import cv2
from PIL import Image
import numpy as np
from flask import request, jsonify
from moviepy import VideoFileClip, AudioFileClip

# from config import output_dir
output_dir = '/tmp'


class ImageToVideo:
    def __init__(self, size=(800, 800), fps=25, output_path='output.mp4'):
        self.size = size  # 宽, 高
        self.fps = fps
        self.output_path = output_path
        # 修改编码器为 avc1，这是 H.264 编码，具有更好的兼容性
        self.fourcc = cv2.VideoWriter_fourcc(*'avc1')
        self.video_writer = None
        self.transition_frames = int(fps * 1.5)  # 转场帧数

    def __enter__(self):
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
        self.video_writer = cv2.VideoWriter(self.output_path, self.fourcc, self.fps, self.size)
        if not self.video_writer.isOpened():
            raise RuntimeError(f"无法创建视频文件：{self.output_path}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.video_writer:
            self.video_writer.release()

    def add_audio(self, audio_path, output_path=None):
        """为视频添加音效"""
        if output_path is None:
            output_path = self.output_path.replace('.mp4', '_with_audio.mp4')

        try:
            # 确保视频写入器已关闭
            if self.video_writer:
                self.video_writer.release()

            # 等待一小段时间确保文件写入完成
            import time
            time.sleep(1)

            # 检查视频文件是否存在且大小不为0
            if not os.path.exists(self.output_path) or os.path.getsize(self.output_path) == 0:
                raise RuntimeError(f"视频文件无效或为空：{self.output_path}")

            # 加载视频和音频
            video = VideoFileClip(self.output_path)
            audio = AudioFileClip(audio_path)

            # 如果音频长度不够，循环播放直到匹配视频长度
            if audio.duration < video.duration:
                audio = audio.loop(duration=video.duration)
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
                audio_bitrate="192k"  # 提高音频码率（可选）
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
            pil_img = Image.open(path).convert('RGB')
            pil_img = pil_img.resize(self.size, Image.LANCZOS)

            # 转换为 OpenCV 格式 (BGR)
            img = np.array(pil_img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            print(f"已加载图片: {path}, 尺寸: {img.shape}")
            return img
        except Exception as e:
            raise RuntimeError(f"处理图片失败: {path}, 错误: {str(e)}")

    def add_static_frame(self, img, duration):
        for _ in range(duration):
            self.video_writer.write(img)

    def add_transition(self, img1, img2, frames):
        for i in range(frames):
            alpha = i / frames
            transition = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
            self.video_writer.write(transition)

    def create_video(self, image_paths):
        # 读取所有图片
        images = [self.read_and_resize(path) for path in image_paths]

        # 验证所有图片尺寸一致
        expected_shape = (self.size[1], self.size[0], 3)  # OpenCV 使用 (高, 宽, 通道)
        for i, img in enumerate(images):
            if img.shape != expected_shape:
                raise ValueError(f"图片 {image_paths[i]} 尺寸异常: {img.shape}")

        # 第一张图片静态显示
        self.add_static_frame(images[0], self.fps)

        # 添加所有转场
        for i in range(len(images) - 1):
            self.add_transition(images[i], images[i + 1], self.transition_frames)

        # 最后一张图片静态显示
        self.add_static_frame(images[-1], self.fps * 2)

def process_images_to_video_route():
    # 检查请求中是否包含文件
    if 'images' not in request.files:
        return jsonify({"error": "Missing 'images' in the request"}), 400

    # 获取所有图片文件
    image_files = request.files.getlist('images')
    if not image_files:
        return jsonify({"error": "No images uploaded"}), 400

    # 获取参数
    size = tuple(map(int, request.form.get('size', '800,800').split(',')))
    fps = int(request.form.get('fps', '25'))
    run_id = request.form.get('run_id')

    if not run_id:
        return jsonify({"error": "Missing 'run_id' parameter"}), 400

    try:
        # 创建临时文件夹存储上传的图片
        temp_dir = os.path.join(output_dir, 'temp', run_id)
        os.makedirs(temp_dir, exist_ok=True)

        # 保存上传的图片
        image_paths = []
        for image in image_files:
            if image.filename:
                image_path = os.path.join(temp_dir, image.filename)
                image.save(image_path)
                image_paths.append(image_path)

        # 设置输出视频路径
        output_path = os.path.join(output_dir, f"{run_id}.mp4")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 创建视频
        with ImageToVideo(size=size, fps=fps, output_path=output_path) as video_maker:
            video_maker.create_video(image_paths)

        # 如果有音频文件
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file.filename:
                audio_path = os.path.join(temp_dir, audio_file.filename)
                audio_file.save(audio_path)
                output_path_with_audio = os.path.join(output_dir, f"{run_id}_with_audio.mp4")
                video_maker.add_audio(audio_path, output_path_with_audio)
                output_path = output_path_with_audio

        return jsonify({
            "video_path": output_path,
            "message": "Video created successfully"
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# 使用示例：
if __name__ == '__main__':
    # 图片路径列表
    image_paths = [f'/Users/qinbinbin/Desktop/comfyui/xxx/a_0000{i}_.png' for i in range(1, 6)]

    # 使用上下文管理器创建视频
    with ImageToVideo() as video_maker:
        video_maker.create_video(image_paths)
        # 添加音效（需要提供音频文件路径）
        video_maker.add_audio('/Users/qinbinbin/Downloads/no-copyright-music-corporate-background-334863.mp3')

    print("视频生成完成！")
