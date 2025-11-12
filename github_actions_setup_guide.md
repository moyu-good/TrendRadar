# GitHub Actions 配置指南

## 设置步骤

### 1. Fork 仓库到您的GitHub账户
1. 访问 https://github.com/sansan0/TrendRadar
2. 点击右上角的 "Fork" 按钮
3. 选择您的账户作为目标

### 2. 配置 GitHub Secrets
在您的Fork仓库中，前往：
Settings → Secrets and variables → Actions → New repository secret

需要添加以下secrets：

#### 必需参数：
- `SENDER_EMAIL`: 发送方邮箱地址 (例如: 1249510763@qq.com)
- `SENDER_PASSWORD`: QQ邮箱授权码 (不是QQ密码！)
- `RECIPIENT_EMAIL`: 接收方邮箱地址 (例如: 1249510763@qq.com)

#### 可选参数（如需自定义）：
- `SMTP_SERVER`: SMTP服务器地址 (默认: smtp.qq.com)
- `SMTP_PORT`: SMTP端口 (默认: 587)

### 3. 获取QQ邮箱授权码
1. 登录QQ邮箱网页版
2. 进入 设置 → 账户 → POP3/SMTP服务
3. 点击 "生成授权码"
4. 按提示发送短信验证
5. 将获得的授权码作为 `SENDER_PASSWORD` secret

### 4. 验证配置
配置完成后，您可以：
1. 手动触发工作流测试（Actions → AI增强趋势报告定时发送 → Run workflow）
2. 等待第二天UTC 00:00自动运行（日本时间9:00 AM）

### 5. 监控执行状态
- 在Actions标签页查看执行历史
- 点击具体运行记录查看详细日志
- 下载日志文件进行故障排查

### 6. 修改时间设置（可选）
如需修改发送时间，编辑 `.github/workflows/ai-enhanced-cron.yml` 文件：
```yaml
schedule:
  - cron: '0 0 * * *'  # 修改这里的cron表达式
```

### 注意事项
- GitHub Actions免费额度：每月2000分钟，足够此用途
- 日志文件保留7天后自动删除
- 如收不到邮件，请检查垃圾邮件文件夹
- 确保QQ邮箱的SMTP服务已开启