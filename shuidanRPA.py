import json
import os
import time
from urllib.parse import urlparse
from loguru import logger
from DrissionPage import WebPage, ChromiumOptions, SessionOptions
import random
import requests
import pandas as pd

from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path, output_path, text="你很好啊"):
    # 打开图片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 设置字体和大小（根据系统调整字体路径）
    try:
        font = ImageFont.truetype("simhei.ttf", 36)  # 尝试使用黑体字体
    except:
        font = ImageFont.load_default()  # 如果找不到字体则使用默认字体

    # 获取文字尺寸
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 图片尺寸
    img_width, img_height = image.size

    # 计算文字位置（右下角）
    x = img_width - text_width - 10
    y = img_height - text_height - 10

    # 添加红色文字
    draw.text((x, y), text, fill=(255, 0, 0), font=font)

    # 保存结果
    image.save(output_path)

# 使用示例
# add_text_to_image('screenshot.png', 'output.png')

# 定义需要匹配的轨迹文本
TRACKING_TEXTS = [
    "Reportado Entregado en Agencia",
    "Reportado Entregado en App",
    "Certificacion de Prueba de Entrega",
    "Entrega Digitalizada en Centro Logistico"
]

def is_matching_tracking(text):
    """
    检查文本是否与预定义的轨迹之一模糊匹配
    """
    for tracking_text in TRACKING_TEXTS:
        # 使用简单的包含检查进行模糊匹配
        if tracking_text in text:
            return True
    return False

def trNum(ele):
    tbody_element = ele
    tr_count = len(tbody_element.eles('tag:p'))  # 使用标签选择器
    print(f"p元素数量: {tr_count}")
    return tr_count

def main():
    co = ChromiumOptions()
    co.existing_only(False)
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get("https://www.servientrega.com.ec/Tracking/?guia=RL102368484BQ&tipo=GUIA#thumb")

    # 之后用于获取所有下属节点标签
    finallyelement = page.ele('xpath://*[@id="content-"]/ul')
    trNum(finallyelement)

    for i in range(1, trNum(finallyelement)+1):
        element = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]/p')
        text = element.text
        print(text)
        
        # 检查文本是否匹配预定义的轨迹
        if is_matching_tracking(text):
            # 截图该元素并保存
            screenshot_path = f"tracking_element_{i}.png"
            element.get_screenshot(screenshot_path)
            
            # 在截图上添加文字"你很好啊"
            output_path = f"tracking_element_{i}_marked.png"
            add_text_to_image(screenshot_path, output_path, "签收轨迹")
            print(f"已保存标记截图: {output_path}")

    # page.ele('xpath://*[@id="content-"]/ul/li[1]/p')

# //*[@id="content-"]/ul/li[3]/p
if __name__ == '__main__':
    main()