# 安装指南

本指南将帮助您安装和设置 Silver_Bullet 项目。

## 系统要求

- Python 3.8 或更高版本
- Chrome 浏览器（用于 DrissionPage）
- 稳定的网络连接

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd Silver_Bullet
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装 ChromeDriver

DrissionPage 需要 Chrome 浏览器支持。首次运行时，DrissionPage 会自动下载匹配的 ChromeDriver。

如果自动下载失败，请手动从 [ChromeDriver 官网](https://chromedriver.chromium.org/) 下载对应版本。

## 验证安装

安装完成后，可以通过以下命令验证：

```bash
python -c "import DrissionPage; print('DrissionPage 安装成功')"
python -c "import pandas; print('pandas 安装成功')"
```

## 故障排除

### 1. 依赖安装失败

尝试升级 pip 后重新安装：

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. ChromeDriver 问题

确保 Chrome 浏览器已安装并可以正常启动。

### 3. 权限问题

在 Linux/macOS 系统上，可能需要给脚本添加执行权限：

```bash
chmod +x machongRPA.py
```