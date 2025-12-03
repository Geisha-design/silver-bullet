# API 文档

本文档描述了 Silver_Bullet 项目的主要函数和类。

## 主要函数

### `alibaba()`

处理阿里巴巴融易通系统的登录及清单查询下载功能。

**功能：**
- 自动登录阿里巴巴融易通系统
- 查询指定运单号的清单信息
- 解析响应数据并下载清单文件

**参数：**
无

**返回值：**
- `page` - WebPage 对象

---

### `easyChina()`

处理 EasyChina 系统的登录、文件上传和状态监控功能。

**功能：**
- 自动登录 EasyChina 系统
- 上传清单文件到第三方系统
- 监控任务处理状态
- 下载处理后的文件

**参数：**
无

**返回值：**
- `page` - WebPage 对象
- `status` - 任务状态

---

### `parse_manifest_response(response_data)`

解析融易通出口清单响应数据。

**参数：**
- `response_data` - API 响应数据（字典格式）

**返回值：**
- `status` - 清单状态
- `manifestCode` - 清单编号

---

### `query_manifest_download_url(manifest_code, headers)`

查询清单文件下载 URL。

**参数：**
- `manifest_code` - 清单编号
- `headers` - HTTP 请求头

**返回值：**
- 成功时返回下载 URL 字符串
- 失败时返回 None

---

### `download_file_from_url(url, save_directory, filename)`

从 URL 下载文件并保存到指定目录。

**参数：**
- `url` - 文件下载链接
- `save_directory` - 保存文件的目录路径
- `filename` - 保存的文件名（可选）

**返回值：**
- 成功时返回保存的文件路径
- 失败时返回 None

---

### `upload_file_to_third_party(file_path, page)`

上传文件到第三方接口。

**参数：**
- `file_path` - 要上传的文件路径
- `page` - WebPage 对象，用于获取 Cookie 信息

**返回值：**
无

---

### `check_task_status_easyChina(cookies, task_id)`

检查任务状态。

**参数：**
- `cookies` - Cookie 信息
- `task_id` - 任务 ID（可选）

**返回值：**
- `status` - 任务状态
- `numberflag` - 任务编号
- `fileName` - 文件名

---

### `parse_excel_data(file_path)`

解析 Excel 文件中的所有数据。

**参数：**
- `file_path` - Excel 文件路径

**返回值：**
- 包含每行数据字典的列表

---

### `get_first_file_in_downloaded_manifests(directory)`

获取指定目录下第一个文件的路径。

**参数：**
- `directory` - 目录路径

**返回值：**
- 第一个文件的完整路径，如果目录不存在或为空则返回 None

---

### `randomSleep()`

随机休眠一段时间（3-5秒）。

**参数：**
无

**返回值：**
无

---

### `trNum(ele)`

计算 tbody 元素中 tr 元素的数量。

**参数：**
- `ele` - tbody 元素

**返回值：**
- tr 元素数量

---

## 辅助函数

### `exist(element)`

检查元素是否存在。

**参数：**
- `element` - 要检查的元素

**返回值：**
无