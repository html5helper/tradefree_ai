#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
生成产品图片脚本
实现以下步骤：
1. 调用Dify API生成四宫格动作图
2. 拆分四宫格图片
3. 移除背景
4. 上传图片至OSS
"""

import os
import sys
import argparse
import requests
import io
import uuid
from datetime import datetime
from PIL import Image
from typing import List, Dict, Any, Optional, Tuple
import logging

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入相关模块
from dify_exec_workflow import nanobanana_workflow, x4_workflow
from image_split import split_image, remove_background

from tools.upload2oss import OSSUploader

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ProductImageGenerator:
    """产品图片生成器"""

    def __init__(self, output_dir: str = "output"):
        """初始化产品图片生成器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        self.oss_uploader = OSSUploader(
            endpoint="https://oss-cn-shenzhen.aliyuncs.com",  # 根据实际情况修改
            bucket_name="tradefree-images",  # 使用实际的bucket名称
        )

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

    def generate_action_image(self, image_path: str, prompt: str) -> str:
        """调用Dify API生成四宫格动作图

        Args:
            image_path: 输入图片路径
            prompt: 提示词，描述要生成的四宫格图片内容

        Returns:
            str: 生成的图片路径
        """
        logger.info(f"开始生成四宫格动作图，输入图片：{image_path}")

        try:
            # 使用x4_workflow生成四宫格图片
            result = nanobanana_workflow(
                imgs=[image_path],
                query=prompt,
            )

            # 检查结果
            if not result:
                raise Exception("生成四宫格图片失败，未返回图片URL")

            # 下载生成的图片
            image_url = result
            response = requests.get(image_url)
            if response.status_code != 200:
                raise Exception(f"下载生成的图片失败，状态码：{response.status_code}")

            # 保存图片
            run_id = str(uuid.uuid4())
            output_path = os.path.join(self.output_dir, f"{run_id}_grid.jpg")
            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.info(f"成功生成四宫格动作图：{output_path}")
            return output_path

        except Exception as e:
            logger.error(f"生成四宫格动作图失败：{str(e)}")
            raise

    def split_grid_image(self, grid_image_path: str) -> List[str]:
        """拆分四宫格图片

        Args:
            grid_image_path: 四宫格图片路径

        Returns:
            List[str]: 拆分后的图片路径列表
        """
        logger.info(f"开始拆分四宫格图片：{grid_image_path}")

        try:
            # 获取文件名（不含扩展名）
            base_name = os.path.splitext(os.path.basename(grid_image_path))[0]

            # 拆分图片
            output_dir = os.path.join(self.output_dir, f"{base_name}_split")
            os.makedirs(output_dir, exist_ok=True)

            # 调用split_image函数拆分图片
            split_paths = split_image(
                grid_image_path,
                output_dir,
                split_mode="4",  # 2x2四宫格
                remove_bg=True,
            )

            logger.info(f"成功拆分四宫格图片，共{len(split_paths)}张：{split_paths}")
            return output_dir

        except Exception as e:
            logger.error(f"拆分四宫格图片失败：{str(e)}")
            raise

    # def remove_backgrounds(self, image_paths: List[str]) -> List[str]:
    #     """移除图片背景

    #     Args:
    #         image_paths: 图片路径列表

    #     Returns:
    #         List[str]: 处理后的图片路径列表
    #     """
    #     logger.info(f"开始移除{len(image_paths)}张图片的背景")

    #     result_paths = []
    #     for i, image_path in enumerate(image_paths):
    #         try:
    #             # 获取文件名（不含扩展名）
    #             base_name = os.path.splitext(os.path.basename(image_path))[0]

    #             # 设置输出路径
    #             output_path = os.path.join(self.output_dir, f"{base_name}_nobg.png")

    #             # 调用remove_background函数移除背景
    #             remove_background(image_path, output_path)

    #             result_paths.append(output_path)
    #             logger.info(f"成功移除背景 [{i+1}/{len(image_paths)}]：{output_path}")

    #         except Exception as e:
    #             logger.error(f"移除背景失败 [{i+1}/{len(image_paths)}]：{str(e)}")
    #             # 继续处理下一张图片
    #             continue

    #     return result_paths

    def upload_to_oss(self, image_dir: str) -> List[str]:
        """上传图片至OSS

        Args:
            image_dir: 图片目录

        Returns:
            List[str]: OSS URL列表
        """
        logger.info(f"开始上传{len(image_dir)}张图片至OSS")

        oss_urls = []
        # 遍历文件夹image_dir，并将下面所有的文件上传至oss
        image_paths = []
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                image_paths.append(os.path.join(root, file))

        date_str = datetime.now().strftime("%Y%m%d")

        for i, image_path in enumerate(image_paths):
            try:
                # 获取文件名
                file_name = os.path.basename(image_path)
                # 生成 OSS 路径
                # oss_path = f"comfyui/{date_str}/img2square/{run_id}/{output_filename}"
                oss_path = f"product/{date_str}/{file_name}"

                # 上传到OSS
                oss_url = self.oss_uploader.upload_file(image_path, oss_path)

                oss_urls.append(oss_url)
                logger.info(f"成功上传图片至OSS [{i+1}/{len(image_paths)}]：{oss_url}")

            except Exception as e:
                logger.error(f"上传图片至OSS失败 [{i+1}/{len(image_paths)}]：{str(e)}")
                # 继续处理下一张图片
                continue

        return oss_urls

    def process(
        self, image_path: str, prompt: str, num_images: int = 1
    ) -> Dict[str, Any]:
        """处理图片生成流程

        Args:
            image_path: 输入图片路径
            prompt: 提示词
            num_images: 生成图片数量

        Returns:
            Dict[str, Any]: 处理结果
        """
        logger.info(
            f"开始处理图片生成流程，输入图片：{image_path}，生成数量：{num_images}"
        )

        result = {
            "grid_images": [],
            "split_images": [],
            "nobg_images": [],
            "oss_urls": [],
        }

        try:
            # 生成多张四宫格图片
            for i in range(num_images):
                logger.info(f"生成第{i+1}/{num_images}张四宫格图片")

                # 1. 生成四宫格动作图
                grid_image_path = self.generate_action_image(image_path, prompt)
                result["grid_images"].append(grid_image_path)

                # 2. 拆分四宫格图片
                split_paths = self.split_grid_image(grid_image_path)
                result["split_images"].extend(split_paths)

                # # 3. 移除背景
                # nobg_paths = self.remove_backgrounds(split_paths)
                # result["nobg_images"].extend(nobg_paths)

                # # 4. 上传至OSS
                oss_urls = self.upload_to_oss(split_paths)
                result["oss_urls"].extend(oss_urls)

            logger.info("图片生成流程处理完成")
            return result

        except Exception as e:
            logger.error(f"图片生成流程处理失败：{str(e)}")
            return result


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="生成产品图片")
    parser.add_argument("--image", "-i", required=True, help="输入图片路径")
    parser.add_argument(
        "--prompt", "-p", required=True, help="提示词，描述要生成的四宫格图片内容"
    )
    parser.add_argument(
        "--num", "-n", type=int, default=1, help="生成图片数量，默认为1"
    )
    parser.add_argument(
        "--output", "-o", default="output", help="输出目录，默认为'output'"
    )
    args = parser.parse_args()

    # 检查输入图片是否存在
    # if not os.path.isfile(args.image):
    #     logger.error(f"输入图片不存在：{args.image}")
    #     return 1

    # 创建产品图片生成器
    generator = ProductImageGenerator(output_dir=args.output)

    # 处理图片生成流程
    result = generator.process(args.image, args.prompt, args.num)

    # 打印结果
    logger.info(f"生成了{len(result['grid_images'])}张四宫格图片")
    logger.info(f"拆分了{len(result['split_images'])}张子图片")
    logger.info(f"处理了{len(result['nobg_images'])}张无背景图片")
    logger.info(f"上传了{len(result['oss_urls'])}张图片至OSS")

    # 打印OSS URL
    if result["oss_urls"]:
        logger.info("OSS URL列表：")
        for url in result["oss_urls"]:
            print(url)

    return 0


if __name__ == "__main__":
    sys.exit(main())
