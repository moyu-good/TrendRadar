# 🆓 TrendRadar完全免费部署方案

## 🎯 免费方案总览

### ✅ 方案一：GitHub Actions（完全免费，推荐）
- **成本**：0元
- **可靠性**：⭐⭐⭐⭐
- **限制**：每月2000分钟执行时间
- **适用**：个人使用完全够用

### ✅ 方案二：本地+节能模式
- **成本**：0元
- **可靠性**：⭐⭐⭐
- **特点**：电脑开机时运行，智能节能

### ✅ 方案三：免费云服务组合
- **成本**：0元
- **可靠性**：⭐⭐⭐
- **组合**：多个免费服务搭配使用

---

## 🚀 方案一：GitHub Actions部署（重点推荐）

### 1. Fork项目到GitHub
```
1. 登录GitHub账号
2. 访问：https://github.com/sansan0/TrendRadar
3. 点击右上角"Fork"按钮
4. 等待Fork完成
```

### 2. 配置GitHub Secrets
在你的Fork项目中：
```
1. 点击 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加以下Secrets：
```

**需要添加的Secrets：**
```
EMAIL_FROM: 1249510763@qq.com
EMAIL_PASSWORD: nvynsqarwowkbace
EMAIL_TO: 1249510763@qq.com
EMAIL_SMTP_SERVER: smtp.qq.com
EMAIL_SMTP_PORT: 465
```

### 3. 创建GitHub Actions工作流
创建文件：`.github/workflows/ai-enhanced-cron.yml`

```yaml
name: 🤖 AI增强版每日热点推送

on:
  schedule:
    # 日本时间9点 = UTC时间0点
    - cron: '0 0 * * *'
  workflow_dispatch:  # 允许手动触发

jobs:
  trendradar-ai-report:
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 检出代码
      uses: actions/checkout@v3
      
    - name: 🐍 设置Python环境
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: 📦 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: 🔧 配置环境变量
      run: |
        echo "EMAIL_FROM=${{ secrets.EMAIL_FROM }}" >> $GITHUB_ENV
        echo "EMAIL_PASSWORD=${{ secrets.EMAIL_PASSWORD }}" >> $GITHUB_ENV
        echo "EMAIL_TO=${{ secrets.EMAIL_TO }}" >> $GITHUB_ENV
        echo "EMAIL_SMTP_SERVER=${{ secrets.EMAIL_SMTP_SERVER }}" >> $GITHUB_ENV
        echo "EMAIL_SMTP_PORT=${{ secrets.EMAIL_SMTP_PORT }}" >> $GITHUB_ENV
        
    - name: 🤖 生成AI增强版报告
      run: |
        python ai_enhanced_report.py
        
    - name: 📧 发送邮件报告
      run: |
        python send_ai_report_email.py
        
    - name: 📊 上传报告文件
      uses: actions/upload-artifact@v3
      with:
        name: ai-report-${{ github.run_number }}
        path: output/ai_enhanced/
        retention-days: 30
```

### 4. 创建邮件发送脚本
创建文件：`send_ai_report_email.py`

```python
# coding=utf-8
"""
AI报告邮件发送器
用于GitHub Actions环境
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime


def send_ai_report_email():
    """发送AI增强版报告邮件"""
    
    # 获取环境变量
    email_from = os.getenv('EMAIL_FROM')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_to = os.getenv('EMAIL_TO')
    smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.qq.com')
    smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '465'))
    
    if not all([email_from, email_password, email_to]):
        print("❌ 邮件配置不完整")
        return False
    
    # 查找最新的AI报告
    ai_report_dir = Path("output/ai_enhanced")
    if not ai_report_dir.exists():
        print("❌ AI报告目录不存在")
        return False
    
    # 获取最新的HTML报告
    html_files = list(ai_report_dir.glob("ai_report_*.html"))
    if not html_files:
        print("❌ 未找到AI报告文件")
        return False
    
    latest_report = max(html_files, key=lambda x: x.stat().st_mtime)
    
    try:
        # 读取报告内容
        with open(latest_report, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = f"🤖 AI增强版热点新闻分析 - {datetime.now().strftime('%Y年%m月%d日')}"
        
        # 邮件正文
        body = f"""
        <h2>🤖 AI增强版热点新闻分析</h2>
        <p>您好！这是由AI智能分析生成的新闻热点报告。</p>
        <p><strong>报告时间：</strong>{datetime.now().strftime('%Y年%m月%d日 %H:%M')}</p>
        
        <h3>📊 报告亮点：</h3>
        <ul>
        <li>✅ 平台对比分析 - 了解各平台关注度差异</li>
        <li>✅ 异常热度检测 - 发现突然爆火的话题</li>
        <li>✅ 关键词共现分析 - 洞察话题关联模式</li>
        <li>✅ 智能推荐 - 基于AI的个性化建议</li>
        </ul>
        
        <p>完整报告请查看附件，或使用浏览器打开HTML文件查看精美版式。</p>
        
        <hr>
        <p><small>此报告由TrendRadar AI自动生成，发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        """
        
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        # 添加HTML报告附件
        with open(latest_report, 'rb') as f:
            attachment = MIMEText(f.read(), 'html', 'utf-8')
            attachment.add_header('Content-Disposition', 'attachment', filename=latest_report.name)
            msg.attach(attachment)
        
        # 发送邮件
        print("📧 正在发送AI增强版报告邮件...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_from, email_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ AI增强版报告邮件发送成功！时间：{datetime.now().strftime('%H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False


if __name__ == "__main__":
    success = send_ai_report_email()
    exit(0 if success else 1)
```

### 5. 启用工作流
```
1. 进入你的Fork项目
2. 点击 Actions 标签页
3. 点击 "I understand my workflows, go ahead and enable them"
4. 工作流将在每天UTC时间0点（日本时间9点）自动运行
```

### 6. 手动测试
```
1. 进入 Actions 页面
2. 选择 "🤖 AI增强版每日热点推送"
3. 点击 "Run workflow"
4. 等待执行完成，检查邮箱
```

---

## 💡 方案二：本地智能节能模式

### 1. 创建智能启动脚本
创建文件：`smart_start.bat`

```batch
@echo off
echo 🧠 TrendRadar智能启动器
echo 当前时间：%date% %time%

:: 检查是否在工作日（周一到周五）
for /f "tokens=1 delims= " %%i in ('date /t') do set weekday=%%i

:: 工作日判断（中文系统）
if "%weekday%"=="周一" goto :workday
if "%weekday%"=="周二" goto :workday
if "%weekday%"=="周三" goto :workday
if "%weekday%"=="周四" goto :workday
if "%weekday%"=="周五" goto :workday

echo 📅 今天是周末，跳过执行
goto :end

:workday
echo 💼 工作日，继续执行...

:: 检查是否在早上8-9点（北京时间）
for /f "tokens=1,2 delims=:" %%i in ("%time%") do (
    set hour=%%i
    set minute=%%j
)

:: 去除前导空格
set hour=%hour: =%

:: 时间判断
if %hour% LSS 8 goto :too_early
if %hour% GTR 9 goto :too_late

echo ⏰ 时间合适（8-9点），开始执行TrendRadar...
cd /d "D:\PROJECT\TrendRadar"
C:\Users\12495\.local\bin\uv run python ai_enhanced_report.py
goto :end

:too_early
echo ⏰ 时间太早（%hour%点），跳过执行
goto :end

:too_late
echo ⏰ 时间太晚（%hour%点），跳过执行
goto :end

:end
echo ✅ 智能检查完成
pause
```

### 2. 添加到Windows启动项
```
1. 按 Win+R，输入 shell:startup
2. 将 smart_start.bat 复制到打开的文件夹
3. 这样每次开机都会智能检查是否运行
```

---

## 🌟 方案三：免费云服务组合

### 1. 免费服务清单

| 服务 | 免费额度 | 用途 |
|------|----------|------|
| GitHub Actions | 2000分钟/月 | 主要执行平台 |
| Vercel | 无限次部署 | Web界面展示 |
| Netlify | 100GB流量/月 | 报告托管 |
| Railway | 500小时/月 | 备选执行平台 |
| Render | 750小时/月 | 容器部署 |

### 2. Railway部署方案

#### Railway部署步骤：
```bash
# 1. 注册Railway账号
# https://railway.app

# 2. 创建新项目，连接GitHub
# 选择你的TrendRadar Fork项目

# 3. 配置环境变量
RAILWAY_AUTORUN=false
EMAIL_FROM=1249510763@qq.com
EMAIL_PASSWORD=nvynsqarwowkbace
EMAIL_TO=1249510763@qq.com
EMAIL_SMTP_SERVER=smtp.qq.com
EMAIL_SMTP_PORT=465

# 4. 创建cron任务
# Railway支持cron语法，设置为每天8点（北京时间）
0 8 * * *
```

### 3. Render部署方案

#### 创建`render.yaml`文件：
```yaml
services:
  - type: cron
    name: trendradar-ai-report
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python ai_enhanced_report.py && python send_ai_report_email.py
    schedule: "0 8 * * *"  # 北京时间8点
    envVars:
      - key: EMAIL_FROM
        value: 1249510763@qq.com
      - key: EMAIL_PASSWORD
        value: nvynsqarwowkbace
      - key: EMAIL_TO
        value: 1249510763@qq.com
      - key: EMAIL_SMTP_SERVER
        value: smtp.qq.com
      - key: EMAIL_SMTP_PORT
        value: "465"
```

---

## 🔄 方案切换指南

### 从本地切换到GitHub Actions：
```bash
# 1. 停用本地定时任务
schtasks /delete /tn "TrendRadar每日推送" /f

# 2. Fork项目到GitHub
# 3. 配置GitHub Secrets
# 4. 启用GitHub Actions
```

### 从GitHub Actions切换到Railway：
```bash
# 1. 禁用GitHub Actions工作流
# 2. 注册Railway账号
# 3. 部署到Railway
# 4. 配置cron任务
```

---

## 📊 免费方案对比

| 方案 | 成本 | 可靠性 | 技术门槛 | 推荐指数 |
|------|------|--------|----------|----------|
| GitHub Actions | 0元 | ⭐⭐⭐⭐ | 低 | ⭐⭐⭐⭐⭐ |
| 本地智能模式 | 0元 | ⭐⭐⭐ | 极低 | ⭐⭐⭐⭐ |
| Railway | 0元 | ⭐⭐⭐⭐ | 中 | ⭐⭐⭐⭐ |
| Render | 0元 | ⭐⭐⭐ | 中 | ⭐⭐⭐ |

---

## 🎯 我的推荐

**最佳免费方案组合：**

1. **主力**：GitHub Actions（完全免费，稳定可靠）
2. **备用**：本地智能模式（电脑开机时补充）
3. **备份**：Railway（GitHub Actions的补充）

**立即行动：**
```bash
# 第一步：Fork项目到GitHub
# 第二步：配置GitHub Secrets
# 第三步：测试运行
# 第四步：享受免费AI热点分析！
```

🎉 **完全免费，立即开始！**