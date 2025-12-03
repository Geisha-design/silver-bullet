# Silver_Bullet RPA项目

## 项目简介

Silver_Bullet 是一个自动化RPA（机器人流程自动化）项目，主要用于处理融易通系统的报关数据自动化操作。该项目能够自动登录系统、查询单证信息、下载清单文件、上传文件至第三方系统等功能。

## 功能特性

- 自动登录阿里巴巴融易通系统
- 查询出口清单信息
- 下载清单文件
- 自动登录EasyChina系统
- 上传文件到第三方系统
- 监控任务状态并下载处理后的文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

直接运行主程序：
```bash
python machongRPA.py
```

## 配置说明

项目中使用的账户信息已在代码中硬编码：
- 融易通系统账户：rongyitong002 / zzk995888zyk
- EasyChina系统账户：ryt / Zjport@123

## 项目结构

```
.
├── machongRPA.py       # 主程序文件
├── requirements.txt    # 依赖包列表
├── README.md           # 项目说明文档
├── downloaded_manifests/  # 下载的清单文件目录
├── downloaded_manifests_new/  # 新下载的清单文件目录
└── completed_manifests/   # 已完成处理的清单文件目录
```

## 核心功能模块

### alibaba()
处理阿里巴巴融易通系统的登录及清单查询下载功能。

### easyChina()
处理EasyChina系统的登录、文件上传和状态监控功能。

### parse_manifest_response()
解析融易通出口清单响应数据。

### query_manifest_download_url()
查询清单文件下载URL。

### download_file_from_url()
从URL下载文件并保存到指定目录。

### upload_file_to_third_party()
上传文件到第三方接口。

### check_task_status_easyChina()
检查任务状态。

## 注意事项

1. 项目需要网络连接以访问外部系统
2. 需要安装Chrome浏览器以支持WebPage操作
3. 账户信息硬编码在代码中，请注意安全问题
4. 项目会自动创建下载和处理文件的目录

## 许可证

MIT License