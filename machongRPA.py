# -*- coding: utf-8 -*-
"""
Silver_Bullet RPA自动化脚本
=========================

这是一个用于自动化处理融易通系统报关流程的RPA脚本，主要功能包括：
1. 自动登录阿里巴巴融易通系统
2. 查询并下载清单文件
3. 自动登录EasyChina系统
4. 上传文件并监控处理状态
5. 下载处理后的文件

注意事项：
- 需要安装Chrome浏览器以支持DrissionPage操作
- 账户信息硬编码在代码中，请注意安全问题
"""

import json
import os
import time
from urllib.parse import urlparse

from loguru import logger
from DrissionPage import WebPage, ChromiumOptions, SessionOptions
import random
import requests
import pandas as pd

# 系统配置常量
ALIBABA_LOGIN_URL = 'https://glp.aidc-dchain.com/login?redirectUrl=https%3A%2F%2Fglp.aidc-dchain.com%2FchinaExport%2F9610Export%2FdirectClearnce'
EASY_CHINA_LOGIN_URL = "http://192.168.8.35:10118/khi-front-declare/#/product-name-manage/goods-change"
ALIBABA_USERNAME = 'rongyitong002'
ALIBABA_PASSWORD = 'zzk995888zyk'
EASY_CHINA_USERNAME = 'ryt'
EASY_CHINA_PASSWORD = 'Zjport@123'


def exist(element):
    if element.is_exists:
        print("元素存在")
        url = element.attr("href")
    else:
        print("元素不存在")


def trNum(ele):
    tbody_element = ele
    tr_count = len(tbody_element.eles('tag:tr'))  # 使用标签选择器
    print(f"tr元素数量: {tr_count}")
    return tr_count


def randomSleep(min_seconds=3, max_seconds=5):
    """
    随机休眠一段时间
    
    Args:
        min_seconds (int): 最小休眠时间（秒）
        max_seconds (int): 最大休眠时间（秒）
    """
    # Generate a random integer representing sleep time (seconds)
    sleep_time = random.randint(min_seconds, max_seconds)
    logger.info(f"随机休眠 {sleep_time} 秒")
    # Let the program sleep for this random time
    time.sleep(sleep_time)

# 2025-10-23 14:03:11.204 | INFO     | __main__:alibaba:68 - {'x-hng': 'lang=zh-CN&domain=glp.aidc-dchain.com', 'isg': 'BN7eZXXhOvChzm4UeRZ_2GgeL3Ign6IZDZ9DvIhlRyEcq32F8C0CKyxYobenk5ox', 'locale': 'zh-cn', 'cn-gateway-useagent': 'pc', 'X-XSRF-TOKEN': '327ca485-3631-4ec1-bdad-f3b33770090e', 'SCMLOCALE': 'zh-cn', 'tfstk': 'gce-BMjLkiK-Lq8y2yfctz7kqsjcIsqPqzr6K20kOrUY5rgnO_Pov230584ha7VLMyaqZ4wLYpnQAySr-g504ukEdNbg9Oqz4Nx8zgQmdMZjKDey06T34uke0NbGIOqyv3vOw2MQRxgjj0MBF0aIljgqYDTSALsYcqujVpiBdmgjqDpWNyMCDogqAvi7RbsYcqoId2TkaO3RV0vLaJfB8QC-op9QH0h5iugXdmyx2b3_V8pBdhi-wVZSkaNdhUhLybeceFo8GlUq2yWwUYGLN5M7pNB-hlP0PmUCWB3b68yKs8Q9_4wr8PH7MZ9-dxnTvfVcAC30OoyxM8CMYmyuA8liCO8S-SqTpDeF8tUTVzFs18TR4n2gBuZXSVnHNiIvTBlS0AOlPUp3vIIIDVjr7BRETnoxSiQHTBl7Ym3G4dAeTXyP.', 'WDK_SESSID': 'f3986f31-2acc-427f-a127-20594ffac9bc', 'xlly_s': '1', 'cna': 'wa+AIa3VcU4CAT2ZlXJXRSsx'}
# 2025-10-23 14:03:41.577 | INFO     | __main__:alibaba:69 - {'x-hng': 'lang=zh-CN&domain=glp.aidc-dchain.com', 'hng': 'cn|zh_CN', 'cn-gateway-useagent': 'pc', 'isg': 'BDIyaXh4jrRdCrKI7bqLHCT6g34UwzZdUTs_wPwLXuXQj9KJ5FOGbTjtfysz5K71', 'SCMLOCALE': 'zh-cn', 'tfstk': 'gYloK16DAos_8F55EeVWESgN2VvxP7NQqDCLvWEe3orbeY3Jd62UmD0-93gz-kmSx4eK83intouGwYeLaBDnfcjKx2T78koExkHJHC3SPWNeX2A9641we1mjZWSKu7aLJXHA4C3SPZPeXhd96wvP6rmUYDyz3oz80zzrY8R2oyzd495rYq80corUT29ShE4Q0zPUTDu2oyZ4YUBFbkPUCj-QBIFXA_5riz2uj6Ect6YLr8qZzo4bljAQEluzm6-y7aWz0Pc2AgEIiqlzRmRAZW04-cVrnn5ox4ksAPoyigzoUV0TnXtNtrMqV-UoneW44Vr0aocBR6Zre2lLKb-NJulS2j2sOgxYvA3xa-mwDsmQKYkaaXxMggJP3ORXb6a2JjXCd8zboldZzGpKxjZpgEYcqqwzlPI9oEXC88zbo0LDogDYUratp', '_tb_token_': '19be0deb143e', 'xlly_s': '1', 'locale': 'zh-cn', 'global_sid': '1a491acb6ce114c36f194ae7671497ac', 'cna': 'wa+AIa3VcU4CAT2ZlXJXRSsx'}

def alibaba():
    """
    处理阿里巴巴融易通系统的登录及清单查询下载功能
    
    Returns:
        WebPage: WebPage对象
    """
    co = ChromiumOptions()
    co.existing_only(False)
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get(ALIBABA_LOGIN_URL)

    # 检查登录状态
    cookies = page.cookies()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    
    if cookie_dict.get('X-XSRF-TOKEN') is None:
        logger.info("开始登录阿里巴巴融易通系统")
        page.ele('xpath://*[@id="email"]').input(ALIBABA_USERNAME)
        page.ele('xpath://*[@id="password"]').input(ALIBABA_PASSWORD)
        randomSleep()
        page.ele('xpath://*[@id="member-user-auth-login"]').click()
        randomSleep()
        logger.info("阿里巴巴融易通系统登录成功")
        time.sleep(6)
    else:
        logger.info("阿里巴巴融易通系统已处于登录状态")

    time.sleep(2)
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    headers = {
        "Cookie": cookie_str
    }
    
    # 准备请求参数
    params = {
        "masterWayBill": "99930325330",
        "pageNum": 1,
        "pageSize": 10
    }

    try:
        response = requests.post(
            'https://gcep.aidc-dchain.com/coc/direct/export/manifest/list/search',
            headers=headers,
            json=params
        )
        logger.info(f"检查任务状态接口调用结果: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"响应内容: {result}")
            # 解析回执的保文
            status, manifest_code = parse_manifest_response(result)
            
            if manifest_code is not None:
                # 查询清单文件下载URL
                download_url = query_manifest_download_url(manifest_code, headers)
                if download_url:
                    logger.info(f"获取到下载URL: {download_url}")
                    # 下载文件到指定目录
                    save_directory = "./downloaded_manifests"
                    downloaded_file = download_file_from_url(download_url, save_directory, f"{manifest_code}.xlsx")
                    if downloaded_file:
                        logger.info(f"清单文件已保存到: {downloaded_file}")
                    else:
                        logger.error("文件下载失败")
                else:
                    logger.warning("未能获取到下载URL")
        else:
            logger.error(f"错误响应内容: {response.text}")
    except Exception as e:
        logger.error(f"调用接口时出错: {e}")

    return page


def parse_manifest_response(response_data):
    """
    解析融易通出口清单响应数据
    """
    if not response_data.get("success"):
        print("接口调用失败")
        return None

    data = response_data.get("data", {})
    manifest_list = data.get("list", [])

    if not manifest_list:
        print("未找到清单信息")
        return None

    # 获取第一个清单信息
    manifest = manifest_list[0]

    print(f"\n=== 出口清单信息解析结果 ===")


    print(f"清单编号: {manifest.get('manifestCode')}")

    print(f"当前状态: {manifest.get('status')}")
    print(f"业务线: {manifest.get('businessLine')}")
    print(f"申报类型: {manifest.get('declareType')}")
    print(f"运输方式: {manifest.get('transportType')} - 航班号: {manifest.get('flightNumber')}")
    print(f"总包裹数: {manifest.get('parcelCount')}")
    print(f"总重量: {manifest.get('totalWeight')}kg")
    print(f"总价值: {manifest.get('totalValue')}")
    print(f"创建时间: {manifest.get('createTime')}")
    print(f"海关清关时间: {manifest.get('customsCleaningTime')}")
    print(f"电商公司: {manifest.get('ecommerceFirmName')}")
    print(f"物流公司: {manifest.get('tmsCompanyName')}")
    print(f"货主: {manifest.get('ownerName')}")
    print(f"目的港: {manifest.get('destinationPortName')}")

    # 返回状态供其他函数使用
    return manifest.get('status'),manifest.get('manifestCode')


def query_manifest_download_url(manifest_code, headers):
    """
    查询清单文件下载URL

    Args:
        manifest_code (str): 清单编号
        headers (dict): 请求头，包含Cookie等信息

    Returns:
        str or None: 下载URL地址
    """
    # 准备请求参数
    params = {
        "manifestCode": manifest_code
    }

    try:
        response = requests.post(
            'https://gcep.aidc-dchain.com/coc/direct/export/manifest/list/queryOriginManifestUrl',
            headers=headers,
            json=params
        )
        print(f"查询清单下载URL接口调用结果: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"响应内容: {result}")

            # 解析响应数据获取下载URL
            if result.get("success"):
                # 根据实际响应结构调整URL提取逻辑
                download_url = result.get("data")  # 或者根据实际字段名称调整
                if download_url:
                    print(f"清单文件下载URL: {download_url}")
                    return download_url
                else:
                    print("未找到下载URL")
            else:
                print(f"接口调用失败: {result.get('message', '未知错误')}")
        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")

    return None


def download_file_from_url(url, save_directory, filename=None):
    """
    从URL下载文件并保存到指定目录
    
    Args:
        url (str): 文件下载链接
        save_directory (str): 保存文件的目录路径
        filename (str, optional): 保存的文件名，如果未提供则从URL中提取
    
    Returns:
        str or None: 下载成功返回保存的文件路径，失败返回None
    """
    try:
        # 确保保存目录存在
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            logger.info(f"创建目录: {save_directory}")
        
        # 如果没有提供文件名，从URL中提取
        if not filename:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            # 如果URL中没有文件名，使用默认名称
            if not filename:
                filename = "downloaded_file"
        
        # 完整的文件保存路径
        file_path = os.path.join(save_directory, filename)
        
        # 下载文件
        logger.info(f"开始下载文件: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        
        # 保存文件
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        logger.info(f"文件下载成功，保存路径: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"下载文件时出错: {e}")
        return None


def download_file_from_url_new(url, save_directory, filename=None , cookie_str =  None):
    """
    从URL下载文件并保存到指定目录

    Args:
        url (str): 文件下载链接
        save_directory (str): 保存文件的目录路径
        filename (str, optional): 保存的文件名，如果未提供则从URL中提取

    Returns:
        str or None: 下载成功返回保存的文件路径，失败返回None
    """
    try:
        # 确保保存目录存在
        import os
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            print(f"创建目录: {save_directory}")

        # 如果没有提供文件名，从URL中提取
        if not filename:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            # 如果URL中没有文件名，使用默认名称
            if not filename:
                filename = "downloaded_file_new"

        # 完整的文件保存路径
        file_path = os.path.join(save_directory, filename)

        # 下载文件
        print(f"开始下载文件: {url}")
        headerss = {
            "Cookie": cookie_str
        }
        response = requests.get(url, stream=True,headers= headerss)
        response.raise_for_status()  # 检查请求是否成功

        # 保存文件
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"文件下载成功，保存路径: {file_path}")
        return file_path

    except Exception as e:
        print(f"下载文件时出错: {e}")
        return None


# 192.168.8.35:10118/khi-front-declare，账号：ryt，密码：Zjport@123
def easyChina():
    """
    处理EasyChina系统的登录、文件上传和状态监控功能
    
    Returns:
        tuple: (WebPage对象, 状态码)
    """
    co = ChromiumOptions()
    co.existing_only(False)
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get(EASY_CHINA_LOGIN_URL)
    
    # 获取Cookie信息
    cookies = page.cookies(all_domains=True)
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    logger.info(f"当前Cookie信息: {cookie_dict}")
    logger.info('检查登录状态')
    time.sleep(5)

    # 检查是否已登录
    vflag = page.ele('xpath://*[@id="advanced_search"]/div/div[5]/div/div/div[1]/button', timeout=5)

    if not vflag:
        logger.info("开始登录EasyChina系统")
        time.sleep(5)
        page.ele('xpath://html/body/div/div/div/div/div/div[2]/div/div[2]/div/form/div[1]/div/div/input').input(EASY_CHINA_USERNAME)
        page.ele('xpath://*[@id="pane-tabCommon"]/form/div[2]/div/div/input').input(EASY_CHINA_PASSWORD)
        page.ele('xpath://*[@id="pane-tabCommon"]/form/div[3]/div/div[1]/div/input').input('6666')
        randomSleep()
        page.ele('xpath://*[@id="pane-tabCommon"]/form/div[4]/div').click()
        randomSleep()
        logger.info("EasyChina系统登录成功")
        page.get(EASY_CHINA_LOGIN_URL)
        
        logger.info('重新检查登录状态')
        cookies = page.cookies(all_domains=True)
        logger.info(f"登录后Cookie信息: {cookies}")
    else:
        logger.info("EasyChina系统已处于登录状态")
        cookies = page.cookies(all_domains=True)
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        logger.info(f"当前Cookie信息: {cookie_dict}")

    time.sleep(2)
    page.get(EASY_CHINA_LOGIN_URL)
    time.sleep(3)

    # 获取待处理文件路径并上传
    file_path = get_first_file_in_downloaded_manifests("./downloaded_manifests")
    if file_path:
        logger.info(f"找到待处理文件: {file_path}")
        upload_file_to_third_party(file_path, page)
    else:
        logger.warning("未找到待处理文件")
        return page, None

    # 监控任务状态
    cookies = page.cookies(all_domains=True)
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    
    while True:
        status, number_flag, file_name = check_task_status_easyChina(cookies, None)
        
        if status and status == "3":  # 处理成功
            logger.info(f"任务状态已变为: {status}，继续执行下一步")
            download_url = f"http://192.168.8.35:10118/khi-declare/declareGoodsChange/export?t=1761643111904&id={number_flag}&type=change&isBlobRequest=true"
            save_directory = "./downloaded_manifests_new"
            downloaded_file = download_file_from_url(
                download_url, save_directory, f"change{file_name}.xlsx")
            
            if downloaded_file:
                logger.info(f"清单文件已保存到: {downloaded_file}")
            else:
                logger.error("文件下载失败")
            break
            
        elif status and status == "4":  # 处理失败
            logger.error(f"任务状态已变为: {status}，转换失败")
            download_url = f"http://192.168.8.35:10118/khi-declare/declareGoodsChange/export?t=1761643111904&id={number_flag}&type=change&isBlobRequest=true"
            save_directory = "./downloaded_manifests_new"
            downloaded_file = download_file_from_url(
                download_url, save_directory, f"change{file_name}.xlsx")
            break
            
        else:
            logger.info("文件任务仍在处理中，等待15秒后重新检查...")
            time.sleep(15)  # 等待15秒后再次检查
            
    return page, status


def check_task_status_easyChina(cookies, task_id):
    """
    检查任务状态
    """
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    headers = {
        "Cookie": cookie_str
    }

    # 准备请求参数
    params = {
          "pageIndex": 1,
          "pageSize": 10,
          "createDateStart": "",
          "createDateEnd": ""
        }
    try:
        response = requests.post(
            'http://192.168.8.35:10118/khi-declare/declareGoodsChange/page',
            headers=headers,
            json=params
        )
        print(f"检查任务状态接口调用结果: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"响应内容: {result}")
            
            # 检查第一个data项的status是否等于3
            data_list = result.get("data", [])
            if data_list and len(data_list) > 0:
                first_data = data_list[0]
                status = first_data.get("status")
                numberflag = first_data.get("id")
                fileName = first_data.get("fileName")
                if status != "3":
                    print("解析中 仍未结束")
                    return status,numberflag,fileName
                elif status == "4":
                    print("解析失败，执行邮件预警模块")
                    return status,numberflag,fileName
                else:
                    print("解析成功，执行下载模块")
                    return status,numberflag,fileName

            # 解析回执的保文
            # return parse_task_status(result)
        else:
            print(f"错误响应内容: {response.text}")
    except Exception as e:
        print(f"调用接口时出错: {e}")

    return None,None,None


def upload_file_to_third_party(file_path, page):
    """
    上传文件到第三方接口
    
    Args:
        file_path (str): 要上传的文件路径
        page (WebPage): WebPage对象，用于获取Cookie信息
    """
    url = "http://192.168.8.35:10118/khi-declare/declareGoodsChange/import"
    cookies = page.cookies(all_domains=True)
    cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    
    headers = {
        'Cookie': cookie_str
    }
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return
    
    # 构造表单数据
    try:
        with open(file_path, 'rb') as f:
            files = {
                'files[]': (os.path.basename(file_path), f,
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            }
            data = {
                'customer': 'cainiao'
            }
            
            logger.info(f"正在上传文件: {file_path}")
            response = requests.post(url, files=files, data=data, headers=headers)
            
            logger.info(f"上传文件接口调用结果: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                logger.info(f"响应内容: {result}")
                
                # 创建completed_manifests文件夹（如果不存在）
                completed_dir = "./completed_manifests"
                if not os.path.exists(completed_dir):
                    os.makedirs(completed_dir)
                    logger.info(f"创建目录: {completed_dir}")

                # 移动文件到completed_manifests文件夹
                filename = os.path.basename(file_path)
                completed_file_path = os.path.join(completed_dir, filename)
                # 移动文件
                os.rename(file_path, completed_file_path)
                logger.info(f"文件已移动到: {completed_file_path}")
            else:
                logger.error(f"错误响应内容: {response.text}")
    except Exception as e:
        logger.error(f"调用上传文件接口时出错: {e}")


def init_database(db_path='excel_data.db'):
    """
    初始化SQLite数据库并创建表
    
    Args:
        db_path (str): 数据库文件路径
    """
    import sqlite3
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS excel_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            航班日期 TEXT,
            航班号 TEXT,
            车辆 TEXT,
            车净重 TEXT,
            司机 TEXT,
            电话 TEXT,
            白卡号 TEXT,
            线路 TEXT,
            票数 TEXT,
            件数 TEXT,
            重量 TEXT,
            主单号 TEXT,
            车牌号 TEXT,
            特殊渠道 TEXT,
            口岸检验 TEXT,
            更新日期 TEXT,
            更新人 TEXT,
            客服同学 TEXT,
            制单 TEXT,
            风险自查 TEXT,
            安检申报 TEXT,
            CCSP TEXT,
            体积 TEXT,
            计费重 TEXT,
            订舱 TEXT,
            现场同学 TEXT,
            现场文件需求 TEXT,
            交接单 TEXT,
            打单 TEXT,
            二维码 TEXT,
            品名清单 TEXT,
            申报单 TEXT,
            粉末保函 TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def parse_excel_data(file_path, db_path='excel_data.db'):
    """
    解析Excel文件中的所有数据并存储到SQLite数据库
    
    Args:
        file_path (str): Excel文件路径
        db_path (str): SQLite数据库文件路径
        
    Returns:
        int: 成功插入的记录数
    """
    try:
        # 初始化数据库
        init_database(db_path)
        
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 将NaN值替换为空字符串
        df = df.fillna('')
        
        # 连接数据库
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 插入数据
        inserted_count = 0
        for index, row in df.iterrows():
            row_data = (
                str(row.get('航班日期', '')),
                str(row.get('航班号', '')),
                str(row.get('车辆', '')),
                str(row.get('车净重', '')),
                str(row.get('司机', '')),
                str(row.get('电话', '')),
                str(row.get('白卡号', '')),
                str(row.get('线路', '')),
                str(row.get('票数', '')),
                str(row.get('件数', '')),
                str(row.get('重量', '')),
                str(row.get('主单号', '')).replace('-', ''),
                str(row.get('车牌号', '')),
                str(row.get('特殊渠道', '')),
                str(row.get('口岸检验', '')),
                str(row.get('更新日期', '')),
                str(row.get('更新人', '')),
                str(row.get('客服同学', '')),
                str(row.get('制单', '')),
                str(row.get('风险自查', '')),
                str(row.get('安检申报', '')),
                str(row.get('CCSP', '')),
                str(row.get('体积', '')),
                str(row.get('计费重', '')),
                str(row.get('订舱', '')),
                str(row.get('现场同学', '')),
                str(row.get('现场文件需求', '')),
                str(row.get('交接单', '')),
                str(row.get('打单', '')),
                str(row.get('二维码', '')),
                str(row.get('品名清单', '')),
                str(row.get('申报单', '')),
                str(row.get('粉末保函', ''))
            )
            
            # 插入数据到数据库
            cursor.execute('''
                INSERT INTO excel_data (
                    航班日期, 航班号, 车辆, 车净重, 司机, 电话, 白卡号, 线路, 票数, 件数, 重量, 
                    主单号, 车牌号, 特殊渠道, 口岸检验, 更新日期, 更新人, 客服同学, 制单, 风险自查, 
                    安检申报, CCSP, 体积, 计费重, 订舱, 现场同学, 现场文件需求, 交接单, 打单, 
                    二维码, 品名清单, 申报单, 粉末保函
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row_data)
            inserted_count += 1
        
        # 提交事务
        conn.commit()
        conn.close()
        
        logger.info(f"成功解析Excel文件，共{inserted_count}行数据已存储到数据库 {db_path}")
        return inserted_count
        
    except Exception as e:
        logger.error(f"解析Excel文件并存储到数据库时出错: {e}")
        return 0


def get_first_file_in_downloaded_manifests(directory="./downloaded_manifests"):
    """
    获取downloaded_manifests目录下第一个文件的路径
    
    Args:
        directory (str): 要搜索的目录路径，默认为"./downloaded_manifests"
        
    Returns:
        str or None: 第一个文件的完整路径，如果目录不存在或为空则返回None
    """
    # 检查目录是否存在
    if not os.path.exists(directory):
        logger.warning(f"目录 {directory} 不存在")
        return None
    
    # 获取目录下所有文件
    files = os.listdir(directory)
    
    # 过滤掉子目录，只保留文件
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    
    # 如果有文件，返回第一个文件的路径
    if files:
        first_file_path = os.path.join(directory, files[0])
        logger.info(f"找到第一个文件: {first_file_path}")
        return first_file_path
    else:
        logger.warning(f"目录 {directory} 中没有文件")
        return None


def fileReturn():
    """
    处理文件返回。99930325330
    """
    co = ChromiumOptions()
    co.existing_only(False)
    # co = ChromiumOptions().headless()
    so = SessionOptions()
    page = WebPage(chromium_options=co, session_or_options=so)
    page.get(
        'https://glp.aidc-dchain.com/login?redirectUrl=https%3A%2F%2Fglp.aidc-dchain.com%2FchinaExport%2F9610Export%2FdirectClearnce')

    # logger.info('第一次cookie状态检测')
    cookiea = page.cookies()
    dictionary = {cookie['name']: cookie['value'] for cookie in cookiea}
    cookiea = dictionary
    # logger.info(cookiea)
    # logger.info('Login status A')
    # logger.info(cookiea.get('X-XSRF-TOKEN'))
    if cookiea.get('X-XSRF-TOKEN') is None:
        logger.info("alibaba登陆中")
        page.ele('xpath://*[@id="email"]').input('rongyitong002')
        page.ele('xpath://*[@id="password"]').input('zzk995888zyk')
        randomSleep()
        page.ele('xpath://*[@id="member-user-auth-login"]').click()
        randomSleep()
        logger.info("alibaba登陆成功")

    else:
        # logger.info('Second cookie status detection')
        cookiea = page.cookies()
        # dictionary = {cookie['name']: cookie['value'] for cookie in cookiea}
        logger.info("alibaba验证已经为登陆状态")
    # tab = page.latest_tab
    """
        检查要求查询的单证信息状态
        """
    time.sleep(2)



if __name__ == '__main__':

    parse_excel_data('./CA融易通报关唯一模板.xlsx')

    #
    #
    # """
    # 主程序入口
    # """
    # logger.info("开始执行RPA自动化流程")
    #
    # # 执行EasyChina流程
    # page, status = easyChina()
    #
    # if status == "4":
    #     logger.error("文件处理失败")
    # elif status == "3":
    #     logger.info("文件处理成功，执行后续操作")
    #     # 这里可以添加后续操作
    # elif status is None:
    #     logger.warning("未获取到任务状态")
    # else:
    #     logger.info(f"任务状态: {status}")
