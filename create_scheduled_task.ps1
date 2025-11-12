# 创建TrendRadar定时任务
# 日本时间早9点 = 北京时间早8点

$TaskName = "TrendRadar每日推送"
$Description = "每天早上8点（北京时间）运行TrendRadar并发送邮件推送"
$ScriptPath = "D:\PROJECT\TrendRadar\run_daily.bat"

# 创建批处理文件
$BatchContent = @"
@echo off
cd /d "D:\PROJECT\TrendRadar"
C:\Users\12495\.local\bin\uv run python main.py
"@

$BatchContent | Out-File -FilePath $ScriptPath -Encoding ASCII

# 创建触发器（每天上午8点）
$Trigger = New-ScheduledTaskTrigger -Daily -At 08:00

# 创建操作
$Action = New-ScheduledTaskAction -Execute $ScriptPath

# 创建设置
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 注册任务
try {
    Register-ScheduledTask -TaskName $TaskName -Description $Description -Trigger $Trigger -Action $Action -Settings $Settings -Force
    Write-Host "✅ 定时任务创建成功！" -ForegroundColor Green
    Write-Host "📅 任务名称: $TaskName" -ForegroundColor Yellow
    Write-Host "⏰ 执行时间: 每天上午8点（北京时间/日本时间早9点）" -ForegroundColor Yellow
    Write-Host "📧 将发送到: 1249510763@qq.com" -ForegroundColor Yellow
} catch {
    Write-Host "❌ 创建定时任务失败: $($_.Exception.Message)" -ForegroundColor Red
}