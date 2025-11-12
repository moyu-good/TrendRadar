# 🚀 GitHub Actions 免费部署完整指南

## 📋 部署步骤

### 1️⃣ Fork 项目到您的GitHub账户

1. 访问 [https://github.com/sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)
2. 点击右上角的 "⭐ Star" 支持项目（可选）
3. 点击右上角的 "🍴 Fork" 按钮
4. 选择您的个人账户作为目标

### 2️⃣ 配置 GitHub Secrets

在您的Fork仓库中，按以下步骤操作：

1. 点击 `Settings` 标签页
2. 在左侧菜单中选择 `Secrets and variables` → `Actions`
3. 点击 `New repository secret` 按钮
4. 添加以下必需的secrets：

#### 必需参数：
- `SENDER_EMAIL`: `1249510763@qq.com` (您的QQ邮箱)
- `SENDER_PASSWORD`: `nvynsqarwowkbace` (您的QQ邮箱授权码)
- `RECIPIENT_EMAIL`: `1249510763@qq.com` (接收报告的邮箱)

#### 可选参数：
- `SMTP_SERVER`: `smtp.qq.com` (默认)
- `SMTP_PORT`: `587` (默认)

### 3️⃣ 上传配置文件

1. 在您的Fork仓库中，点击 `Add file` → `Upload files`
2. 上传以下文件到仓库根目录：
   - `.github/workflows/ai-enhanced-cron.yml` (已创建)
   - `send_ai_report_email.py` (已创建)
   - `simple_ai_report.py` (已创建)
   - `config/test_config.yaml` (已创建)

### 4️⃣ 验证部署

#### 手动触发测试
1. 进入 `Actions` 标签页
2. 选择 `AI增强趋势报告定时发送` 工作流
3. 点击 `Run workflow` → `Run workflow`
4. 等待执行完成（约2-3分钟）

#### 检查执行结果
- ✅ 绿色勾号：执行成功
- ❌ 红色叉号：执行失败，点击查看日志
- 🟡 黄色圆圈：正在执行

### 5️⃣ 设置通知（可选）

1. 进入 `Settings` → `Notifications`
2. 配置邮件通知，当工作流失败时接收提醒

## 📧 邮件效果预览

您将收到包含以下内容的AI增强报告：

```
主题：🤖 AI热点分析 11月13日 - 智能新闻洞察

内容：
📊 基础统计
• 总新闻数: 156条
• 监控平台: 微博、知乎、GitHub、V2EX

🔍 AI智能洞察
• 平台对比分析
• 异常热度检测
• 关键词共现模式

💡 智能推荐
• 热点关注建议
• 平台策略建议
```

## ⚙️ 定时设置

默认设置：
- ⏰ 发送时间：每天 UTC 00:00 (日本时间 9:00 AM)
- 📅 发送频率：每天一次
- 🌍 时区：Asia/Tokyo

如需修改时间，编辑 `.github/workflows/ai-enhanced-cron.yml` 中的 cron 表达式：
```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 00:00 = 日本时间 9:00 AM
```

## 🔧 故障排查

### 常见问题

#### 1. 邮件发送失败
- ✅ 检查QQ邮箱授权码是否正确
- ✅ 确认SMTP服务已开启
- ✅ 验证邮箱地址拼写

#### 2. 工作流执行失败
- ✅ 检查Secrets配置是否完整
- ✅ 查看Actions日志获取详细错误信息
- ✅ 确认所有必需文件已上传

#### 3. 没有收到邮件
- ✅ 检查垃圾邮件文件夹
- ✅ 验证邮箱地址是否正确
- ✅ 查看GitHub Actions执行状态

### 查看日志
1. 进入 `Actions` 标签页
2. 点击具体的工作流运行记录
3. 展开失败的步骤查看详细日志

## 📊 免费额度说明

GitHub Actions 免费额度（每月）：
- ⏱️ 2000 分钟运行时间（足够使用）
- 📦 500MB 存储空间
- 🚫 无并发限制（公共仓库）

本工作流每次运行约消耗 2-3 分钟，完全在免费额度内。

## 🎯 成功验证

完成部署后，您将：
- ✅ 每天自动收到AI增强版热点新闻分析
- ✅ 包含智能洞察和推荐
- ✅ 完全免费，无需服务器
- ✅ 即使电脑关机也能正常接收

## 📞 技术支持

如遇到问题：
1. 查看GitHub Actions日志
2. 检查邮箱配置
3. 验证网络连接
4. 重新运行工作流测试

---

**🎉 恭喜！您已成功配置免费的AI增强新闻分析服务！**

每天上午9点（日本时间），您将收到最新的AI分析热点报告。