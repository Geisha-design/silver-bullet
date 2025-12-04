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

def add_text_to_image(image_path, output_path, text="签收轨迹"):
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

def add_red_border_and_text(image_path, output_path, text="签收轨迹"):
    """
    给图片添加红色边框和文字标注
    """
    # 打开图片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # 添加红色边框
    width, height = image.size
    border_width = 5
    draw.rectangle([0, 0, width-1, height-1], outline="red", width=border_width)
    
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


def add_red_border_to_element(image_path, output_path, corners, text="签收轨迹"):
    """
    给整个页面截图中的特定元素添加红色边框和文字标注
    :param image_path: 页面截图路径
    :param output_path: 输出图片路径
    :param corners: 元素的四个角坐标 [(左上), (右上), (右下), (左下)]
    :param text: 标注文字
    """
    # 打开图片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # 从corners获取边界坐标
    # corners格式: [(左上x, 左上y), (右上x, 右上y), (右下x, 右下y), (左下x, 左下y)]
    left_top = corners[0]
    right_bottom = corners[2]

    print("逆空虫洞")
    print(left_top[0]+100)
    cv = left_top[0]-50
    cv2 =  left_top[1]+100
    # 绘制红色边框（边框宽度为5像素）
    border_width = 4
    draw.rectangle([cv, left_top[1]+100, right_bottom[0]+200, right_bottom[1]+200],
                   outline="red", width=border_width)
    
    # 设置字体和大小（根据系统调整字体路径）
    try:
        font = ImageFont.truetype("simhei.ttf", 36)  # 尝试使用黑体字体
    except:
        font = ImageFont.load_default()  # 如果找不到字体则使用默认字体

    # 获取文字尺寸
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 计算文字位置（元素右下角）
    x = right_bottom[0] - text_width - 20
    y = right_bottom[1] - text_height - 20

    # 添加红色文字
    draw.text((x, y), text, fill=(255, 0, 0), font=font)

    # 保存结果
    image.save(output_path)


def find_earliest_matching_tracking(page, finallyelement):
    """
    查找时间最早的匹配轨迹
    """
    matching_items = []
    
    for i in range(1, trNum(finallyelement)+1):
        element = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]/p')
        text = element.text
        # 暂时注释掉
        # print(f"轨迹文本: {text}")
        
        # 检查文本是否匹配预定义的轨迹
        if is_matching_tracking(text):
            time_zone = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]').attr("data-date")
            print(f"时间: {time_zone}")
            matching_items.append({
                'index': i,
                'element': element,
                'text': text,
                'time': time_zone
            })
    
    # 如果没有匹配项，返回None
    if not matching_items:
        return None
    
    # 根据时间找出最早的匹配项
    # 这里假设时间格式是可以直接比较的字符串
    earliest_item = max(matching_items, key=lambda x: x['time'] if x['time'] else "")
    return earliest_item


def classify_and_save_image_by_time_relation(page, finallyelement, earliest_match, marked_image_path):
    """
    根据签收时间和其它轨迹时间的关系对图片进行分类存储
    
    1. 如果没有其他轨迹的操作时间晚于签收时间，归类到"签收后无轨迹"文件夹
    2. 如果有其他轨迹的操作时间等于签收时间，归类到"与签收时间一致"文件夹
    3. 如果有其他轨迹的操作时间晚于签收时间，归类到"签收后有新轨迹"文件夹
    """
    # 获取签收时间
    sign_time = earliest_match['time']
    
    # 收集所有轨迹的时间信息
    all_tracks = []
    for i in range(1, trNum(finallyelement)+1):
        time_zone = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]').attr("data-date")
        element = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]/p')
        text = element.text
        
        if time_zone:
            all_tracks.append({
                'index': i,
                'text': text,
                'time': time_zone
            })
    
    # 判断时间关系
    has_later_track = False
    has_same_time_track = False
    
    for track in all_tracks:
        if track['time'] < sign_time:
            has_later_track = True
        elif track['time'] == sign_time and track['index'] != earliest_match['index']:
            has_same_time_track = True
    
    # 创建对应的文件夹
    if has_later_track:
        folder_name = "签收后有新轨迹"
    elif has_same_time_track:
        folder_name = "与签收时间一致"
    else:
        folder_name = "签收后无轨迹"
    
    # 确保文件夹存在
    os.makedirs(folder_name, exist_ok=True)
    
    # 移动标记图片到对应文件夹
    import shutil
    filename = os.path.basename(marked_image_path)
    destination_path = os.path.join(folder_name, filename)
    shutil.move(marked_image_path, destination_path)
    
    print(f"图片已分类保存至: {destination_path}")


def main(key):
    co = ChromiumOptions()
    co.existing_only(False)
    co.set_argument('--window-size', '1920,1080')
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get("https://www.servientrega.com.ec/Tracking/?guia="+key+"&tipo=GUIA#thumb")

    # 设置窗口大小以确保截图的一致性
    # page.set.window_size()

    # 之后用于获取所有下属节点标签
    finallyelement = page.ele('xpath://*[@id="content-"]/ul')
    
    # 查找时间最早的匹配轨迹
    earliest_match = find_earliest_matching_tracking(page, finallyelement)
    
    if earliest_match:
        # 先对整个页面进行截图，使用固定视口大小确保一致性
        screenshot_path = f"full_page_screenshot.png"
        page.get_screenshot(screenshot_path, full_page=True)
        
        # 获取匹配元素的位置信息
        index = earliest_match['index']
        element = page.ele(f'xpath://*[@id="content-"]/ul/li[{index}]')

        element.get_screenshot(f"element_{index}_screenshotsaika.png")


        # 使用corners获取元素的四个角坐标
        corners = element.rect.corners
        print(f"元素坐标: {corners}")
        
        # 在完整页面截图上对目标元素添加红色边框和文字标注
        output_path = f"tracking_element_{index}_marked.png"
        add_red_border_to_element(screenshot_path, output_path, corners, "签收轨迹")
        print(f"已保存标记截图: {output_path}")
        
        # 根据时间关系对图片进行分类存储
        classify_and_save_image_by_time_relation(page, finallyelement, earliest_match, output_path)
    else:
        print("未找到匹配的轨迹")


def extract_waybill_numbers(file_path):
    """
    从Excel文件中提取所有运单号并存储到列表中

    Args:
        file_path (str): Excel文件路径

    Returns:
        list: 包含所有运单号的列表
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)

        # 查找可能包含运单号的列
        waybill_numbers = []

        # 常见的运单号列名
        possible_columns = ['主单号', '运单号', 'Waybill Number', 'Tracking Number',
                            'Tracking No', '运单编号', '快递单号', '物流单号']

        # 检查是否有明确的运单号列
        for col in possible_columns:
            if col in df.columns:
                # 获取该列的所有非空值，并清理数据
                column_values = df[col].dropna().astype(str).tolist()
                # 清理可能的格式字符（如横线）
                cleaned_values = [str(value).replace('-', '').replace(' ', '') for value in column_values]
                waybill_numbers.extend(cleaned_values)
                break

        # 如果没找到明确的列，则尝试启发式查找
        if not waybill_numbers:
            # 遍历所有列，查找符合运单号格式的数据
            for col in df.columns:
                # 获取该列的所有非空值
                values = df[col].dropna().astype(str).tolist()
                # 启发式判断：运单号通常为8-20位的数字或字母数字组合
                for value in values:
                    cleaned_value = str(value).replace('-', '').replace(' ', '')
                    if 8 <= len(cleaned_value) <= 20 and cleaned_value.isalnum():
                        # 可能是运单号
                        waybill_numbers.append(cleaned_value)

        # 去除重复项
        waybill_numbers = list(set(waybill_numbers))

        logger.info(f"成功提取 {len(waybill_numbers)} 个运单号")
        return waybill_numbers

    except Exception as e:
        logger.error(f"提取运单号时出错: {e}")
        return []
if __name__ == '__main__':
    # cc = extract_waybill_numbers("./需要截图的包裹【已签收，但无签收轨迹，最新节点非闭环节点丢件罚单】.xlsx")
    # print(cc)
    main('RL100474746BQ')

