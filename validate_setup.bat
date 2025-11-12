@echo off
echo 🚀 验证GitHub Actions配置...
echo.

echo 📁 检查关键文件:
if exist ".github\workflows\daily-ai-report.yml" echo ✅ daily-ai-report.yml
if exist ".github\workflows\ai-enhanced-daily.yml" echo ✅ ai-enhanced-daily.yml
if exist "config\config.yaml" echo ✅ config.yaml
if exist "requirements.txt" echo ✅ requirements.txt
if exist "main.py" echo ✅ main.py
echo.

echo 📋 检查配置:
findstr "notification:" config\config.yaml >nul && echo ✅ 通知配置 || echo ⚠️ 通知配置
findstr "push_window:" config\config.yaml >nul && echo ✅ 时间窗口 || echo ⚠️ 时间窗口
findstr "platforms:" config\config.yaml >nul && echo ✅ 平台配置 || echo ⚠️ 平台配置
echo.

echo 🎯 下一步操作:
echo 1. 推送代码到GitHub
echo 2. 配置GitHub Secrets:
echo    - SENDER_EMAIL: 您的发件邮箱
echo    - SENDER_PASSWORD: 您的邮箱授权码
echo    - RECIPIENT_EMAIL: 接收报告的邮箱
echo 3. 手动触发workflow测试
echo.
echo ✅ 配置验证完成！
pause