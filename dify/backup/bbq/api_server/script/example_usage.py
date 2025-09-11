#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片分割示例脚本
用法：python example_usage.py [图片路径] [输出目录] [分割模式] [是否移除背景]
分割模式：4 表示四宫格，9 表示九宫格，默认为 4
是否移除背景：0 表示不移除，1 表示移除，默认为 0
"""

import sys
import os
from image_split import split_image

def main():
    # 解析命令行参数
    if len(sys.argv) < 2:
        print("用法：python example_usage.py [图片路径] [输出目录] [分割模式] [是否移除背景]")
        print("分割模式：4 表示四宫格，9 表示九宫格，默认为 4")
        print("是否移除背景：0 表示不移除，1 表示移除，默认为 0")
        return
    
    # 获取图片路径
    image_path = sys.argv[1]
    
    # 获取输出目录（可选）
    output_dir = None
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # 获取分割模式（可选）
    split_mode = "4"
    if len(sys.argv) > 3:
        split_mode = sys.argv[3]
    
    # 获取是否移除背景（可选）
    remove_bg = False
    if len(sys.argv) > 4:
        remove_bg = sys.argv[4] == "1"
    
    # 定义日志回调函数
    def log_callback(message):
        print(message)
    
    # 调用分割函数
    success, message, output_paths = split_image(image_path, output_dir, split_mode, remove_bg, log_callback)
    
    # 输出结果
    print(message)
    if success:
        print("分割后的文件路径:")
        for path in output_paths:
            print(f"  - {path}")

if __name__ == "__main__":
    main()