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
    # logger.info(f"p元素数量: {tr_count}")
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

    # logger.info(left_top[0]+100)
    # cv = left_top[0]-50
    # cv2 =  left_top[1]+100
    # 绘制红色边框（边框宽度为5像素）
    border_width = 4
    # draw.rectangle([left_top[0]-50, left_top[1]+100, right_bottom[0]+200, right_bottom[1]+200],
    #                outline="red", width=border_width)
    #
    # draw.rectangle([left_top[0]-50, left_top[1]+100, right_bottom[0]+200, right_bottom[1]+200],
    #                outline="red", width=border_width)


    draw.rectangle([left_top[0]+200, left_top[1]+600, right_bottom[0]+550, right_bottom[1]+700],
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
        # logger.info(f"轨迹文本: {text}")
        
        # 检查文本是否匹配预定义的轨迹
        if is_matching_tracking(text):
            time_zone = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]').attr("data-date")
            # logger.info(f"时间: {time_zone}")
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
    earliest_item = min(matching_items, key=lambda x: x['time'] if x['time'] else "")
    return earliest_item


def classify_and_save_image_by_time_relation(page, finallyelement, earliest_match, marked_image_path, package_number=None):
    """
    根据签收时间和其它轨迹时间的关系对图片进行分类存储
    
    1. 如果没有其他轨迹的操作时间晚于签收时间，归类到"签收后无轨迹"文件夹
    2. 如果有其他轨迹的操作时间等于签收时间，归类到"与签收时间一致"文件夹
    3. 如果有其他轨迹的操作时间晚于签收时间，归类到"签收后有新轨迹"文件夹
    """
    # 获取签收时间
    sign_time = earliest_match['time']
    sign_index = earliest_match['index']
    
    # 收集所有在签收时间之前的轨迹信息
    all_tracks = []
    for i in range(1, trNum(finallyelement)+1):
        # 只处理签收元素之前的元素
        if i >= sign_index:
            break
            
        time_zone = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]').attr("data-date")
        element = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]/p')
        text = element.text

        # 只添加在签收时间之后的轨迹
        if time_zone and time_zone >= sign_time:
            all_tracks.append({
                'index': i,
                'text': text,
                'time': time_zone
            })

    
    # 判断时间关系
    has_later_track = False
    has_ealer_track = False
    has_same_time_track = False
    
    for track in all_tracks:
        if track['time'] < sign_time:
            has_later_track = True
        elif track['time'] == sign_time:
            has_same_time_track = True

    # 检查是否存在签收时间之后的轨迹（在签收元素之后的元素中）
    for i in range(sign_index+1, trNum(finallyelement)+1):
        time_zone = page.ele(f'xpath://*[@id="content-"]/ul/li[{i}]').attr("data-date")
        # logger.info(time_zone)
        # logger.info(sign_time)
        if time_zone and time_zone < sign_time:
            has_ealer_track = True
            break

    if sign_index == 1:
        has_ealer_track = False
        logger.info("没有其他轨迹")
    else:
        logger.info(f"有其他轨迹，关系为：{has_later_track}, {has_same_time_track}, {has_ealer_track}")

    
    # 创建对应的文件夹在data目录下
    folder_name = ""
    if has_ealer_track and not has_same_time_track:
        folder_name = "签收后有新轨迹"
    elif has_same_time_track:
        folder_name = "与签收时间一致"
    else:
        folder_name = "签收后无轨迹"
    
    # 确保data目录下的文件夹存在
    data_folder_path = os.path.join("data", folder_name)
    os.makedirs(data_folder_path, exist_ok=True)
    
    # 确定文件名
    if package_number:
        filename = f"{package_number}.png"
    else:
        filename = os.path.basename(marked_image_path)
        
    # 移动标记图片到data目录下的对应文件夹
    import shutil
    destination_path = os.path.join(data_folder_path, filename)
    shutil.move(marked_image_path, destination_path)
    
    logger.info(f"图片已分类保存至: {destination_path}")


def log_error_package(package_number):
    """
    将出错的package_number记录到errorNumber.txt文件中
    
    Args:
        package_number (str): 出错的包裹号
    """
    try:
        with open("errorNumber.txt", "a", encoding="utf-8") as f:
            f.write(f"{package_number}\n")
        logger.info(f"已将包裹号 {package_number} 记录到 errorNumber.txt")
    except Exception as e:
        logger.info(f"记录错误包裹号时出错: {e}")


def main(key, package_number=None):
    try:
        co = ChromiumOptions()
        co.existing_only(False)
        co.set_argument('--window-size', '1920,1080')
        so = SessionOptions()
        page = WebPage(chromium_options=co, session_or_options=so)
        page.get("https://www.servientrega.com.ec/Tracking/?guia="+key+"&tipo=GUIA#thumb")


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

            element.get_screenshot(f"element_{index}_screenshotsaika.png",)


            # 使用corners获取元素的四个角坐标
            corners = element.rect.corners
            logger.info(f"元素坐标: {corners}")
            
            # 在完整页面截图上对目标元素添加红色边框和文字标注
            if package_number:
                output_path = f"{package_number}_tracking_element_{index}_marked.png"
            else:
                output_path = f"tracking_element_{index}_marked.png"
                
            add_red_border_to_element(screenshot_path, output_path, corners, "签收轨迹")
            logger.info(f"已保存标记截图: {output_path}")
            
            # 根据时间关系对图片进行分类存储
            classify_and_save_image_by_time_relation(page, finallyelement, earliest_match, output_path, package_number)
        else:
            logger.info("未找到匹配的轨迹")
    except Exception as e:
        logger.info(f"处理运单 {key} 时发生错误: {e}")
        if package_number:
            log_error_package(package_number)
        raise  # 重新抛出异常以便上层处理


def extract_waybill_numbers(file_path):
    """
    从Excel文件中提取所有运单号和对应的包裹号

    Args:
        file_path (str): Excel文件路径

    Returns:
        list: 包含字典的列表，每个字典包含'waybill_number'(运单号)和'package_number'(包裹号)
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)

        # 查找可能包含运单号的列
        waybill_data = []

        # 常见的运单号和包裹号列名
        waybill_columns = ['主单号', '运单号', 'Waybill Number', 'Tracking Number',
                          'Tracking No', '运单编号', '快递单号', '物流单号']
        package_columns = ['包裹号', '包裹编号', 'Package Number', 'Package No']

        waybill_col = None
        package_col = None

        # 查找运单号列
        for col in waybill_columns:
            if col in df.columns:
                waybill_col = col
                break

        # 查找包裹号列
        for col in package_columns:
            if col in df.columns:
                package_col = col
                break

        # 如果找到了运单号列
        if waybill_col:
            # 获取运单号和包裹号（如果存在）
            for index, row in df.iterrows():
                waybill_number = str(row[waybill_col]).replace('-', '').replace(' ', '')
                
                # 获取包裹号（如果存在对应的列）
                package_number = None
                if package_col and package_col in df.columns:
                    package_number = str(row[package_col]).replace(' ', '')
                
                waybill_data.append({
                    'waybill_number': waybill_number,
                    'package_number': package_number
                })

        # 如果没找到明确的运单号列，则尝试启发式查找
        if not waybill_data:
            # 遍历所有列，查找符合运单号格式的数据
            for index, row in df.iterrows():
                for col in df.columns:
                    value = str(row[col]).replace('-', '').replace(' ', '')
                    # 启发式判断：运单号通常为8-20位的数字或字母数字组合
                    if 8 <= len(value) <= 20 and value.isalnum():
                        # 可能是运单号
                        waybill_data.append({
                            'waybill_number': value,
                            'package_number': None  # 没有明确的包裹号列
                        })
                        break  # 每行只取一个可能的运单号

        logger.info(f"成功提取 {len(waybill_data)} 个运单记录")
        return waybill_data

    except Exception as e:
        logger.error(f"提取运单号时出错: {e}")
        return []

if __name__ == '__main__':

    matching_items =  [{'time': '31/10/2025 15:58 PM'},{'time': '28/10/2025 10:52 AM'}]


    #     ({
    #
    #     'time': time_zone
    # }))
    #

    # earliest_item = min(matching_items, key=lambda x: x['time'] if x['time'] else "")
    # logger.info(earliest_item)
    # main('RL100419617BQ', 'BG-25061552FTMA8FJW')



    waybill_data = extract_waybill_numbers("./副本需要截图的包裹【已签收，但无签收轨迹，最新节点非闭环节点丢件罚单】.xlsx")
    for item in waybill_data:
        waybill_number = item['waybill_number']
        package_number = item['package_number']
        main(waybill_number, package_number)
    #     # time.sleep(1)


