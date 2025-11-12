# ☁️ TrendRadar云端部署解决方案

## 🎯 解决电脑关机问题的三种方案

### 方案一：Docker容器化部署（推荐）

#### 1. 安装Docker
```bash
# Windows
# 下载并安装Docker Desktop
# https://www.docker.com/products/docker-desktop

# Linux (Ubuntu/Debian)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# macOS
# 下载并安装Docker Desktop
# https://www.docker.com/products/docker-desktop
```

#### 2. 使用Docker Compose部署
```bash
# 克隆项目（如果还没克隆）
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar

# 使用本地Docker Compose配置
docker-compose -f docker-compose-local.yml up -d
```

#### 3. 验证部署
```bash
# 查看容器状态
docker ps

# 查看日志
docker logs trend-radar-local

# 进入容器
docker exec -it trend-radar-local bash
```

### 方案二：云服务器部署

#### 1. 选择云服务商
- **阿里云**：轻量应用服务器（约24元/月）
- **腾讯云**：云服务器CVM（约30元/月）
- **华为云**：弹性云服务器（约25元/月）
- **AWS**：EC2 t3.micro（约15美元/月）

#### 2. 服务器配置建议
- **操作系统**：Ubuntu 20.04 LTS
- **CPU**：1核
- **内存**：1GB
- **存储**：20GB SSD
- **带宽**：1Mbps

#### 3. 部署步骤
```bash
# 1. 连接服务器
ssh root@your_server_ip

# 2. 安装Docker
curl -fsSL https://get.docker.com | sh

# 3. 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. 克隆项目
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar

# 5. 配置环境变量
cp docker/.env.example docker/.env
# 编辑.env文件，填入你的配置

# 6. 启动服务
docker-compose up -d
```

### 方案三：GitHub Actions + 云函数（免费方案）

#### 1. Fork项目到你的GitHub
- 访问 https://github.com/sansan0/TrendRadar
- 点击右上角的 "Fork" 按钮

#### 2. 配置GitHub Secrets
在GitHub项目设置中添加以下Secrets：
```
EMAIL_FROM: 1249510763@qq.com
EMAIL_PASSWORD: nvynsqarwowkbace
EMAIL_TO: 1249510763@qq.com
EMAIL_SMTP_SERVER: smtp.qq.com
EMAIL_SMTP_PORT: 465
```

#### 3. 修改GitHub Actions工作流
编辑 `.github/workflows/crawler.yml` 文件，修改定时触发时间：
```yaml
on:
  schedule:
    # 日本时间9点 = UTC时间0点（需要考虑时差）
    - cron: '0 0 * * *'
  workflow_dispatch:  # 允许手动触发
```

#### 4. 启用Actions
- 进入GitHub项目的Actions标签页
- 启用工作流

## 🤖 AI分析功能详解

### 当前可用的AI分析工具

#### 1. 平台对比分析
```python
# 分析不同平台对特定话题的关注度
analytics.analyze_data_insights_unified(
    insight_type="platform_compare",
    topic="人工智能"
)
```

#### 2. 异常热度检测
```python
# 检测突然爆火的话题
analytics.analyze_topic_trend_unified(
    analysis_type="viral",
    threshold=2.5  # 热度突增倍数
)
```

#### 3. 关键词共现分析
```python
# 分析关键词同时出现的模式
analytics.analyze_data_insights_unified(
    insight_type="keyword_cooccur",
    min_frequency=2,
    top_n=15
)
```

#### 4. 话题趋势预测
```python
# 预测未来可能的热点
analytics.analyze_topic_trend_unified(
    analysis_type="predict",
    lookahead_hours=6,
    confidence_threshold=0.7
)
```

### AI增强版邮件报告

我已经为你创建了 `ai_enhanced_report.py`，它会生成包含以下内容的智能报告：

1. **基础统计**：总新闻数、监控平台数量
2. **AI智能洞察**：
   - 平台对比分析
   - 异常热度检测
   - 关键词共现模式
3. **智能推荐**：
   - 热点关注建议
   - 平台策略建议
   - 关键词组合建议

## 🚀 快速启动AI增强版

### 1. 测试AI增强版报告
```bash
# 运行AI增强版报告生成
C:\Users\12495\.local\bin\uv run python ai_enhanced_report.py
```

### 2. 修改定时任务使用AI版本
编辑 `run_daily.bat`：
```batch
@echo off
cd /d "D:\PROJECT\TrendRadar"
C:\Users\12495\.local\bin\uv run python ai_enhanced_report.py
```

### 3. 云端部署AI版本
在云端部署时，使用以下Docker Compose配置：
```yaml
environment:
  - ENABLE_CRAWLER=true
  - ENABLE_NOTIFICATION=true
  - REPORT_MODE=daily
  - PUSH_WINDOW_ENABLED=true
  - PUSH_WINDOW_START=08:00
  - PUSH_WINDOW_END=08:30
  - PUSH_WINDOW_ONCE_PER_DAY=true
  # ... 其他配置
```

## 💡 成本对比

| 方案 | 成本 | 可靠性 | 维护难度 | 推荐指数 |
|------|------|--------|----------|----------|
| Docker本地 | 免费 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 云服务器 | ¥25/月 | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| GitHub Actions | 免费 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🔧 故障排除

### 常见问题

1. **Docker启动失败**
   ```bash
   # 检查Docker服务
   sudo systemctl status docker
   
   # 重新启动Docker
   sudo systemctl restart docker
   ```

2. **邮件发送失败**
   - 检查QQ邮箱授权码是否正确
   - 确认邮箱SMTP服务已开启
   - 检查网络连接

3. **定时任务不执行**
   - 检查系统时间是否正确
   - 确认容器正在运行
   - 查看容器日志排查问题

### 监控和日志
```bash
# 查看容器日志
docker logs -f trend-radar-local

# 查看定时任务日志（在容器内）
docker exec -it trend-radar-local cat /var/log/cron.log
```

## 📞 技术支持

如果遇到问题，可以：
1. 查看项目GitHub Issues
2. 检查日志文件
3. 重新配置环境变量
4. 尝试重启容器或服务

**推荐方案**：使用云服务器部署，既稳定又便宜，每月只需25元左右！🚀