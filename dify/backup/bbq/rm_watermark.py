import cv2
import numpy as np


def remove_watermark(image_path):
    # 读取图片
    image = cv2.imread(image_path)
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 对灰度图进行阈值处理，这里假设水印颜色较浅
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    # 查找轮廓
    contours, _ = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 创建掩码
    mask = np.zeros_like(gray)
    for contour in contours:
        cv2.drawContours(mask, [contour], -1, 255, -1)
    # 使用inpaint函数去除水印
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    return result


# 调用函数
image_path = '/Users/qinbinbin/Downloads/1.webp'
result = remove_watermark(image_path)
# 保存处理后的图片
cv2.imwrite('/Users/qinbinbin/Downloads/water.jpg', result)
