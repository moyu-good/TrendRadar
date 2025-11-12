# 简化测试 - 验证GitHub Actions workflow配置
Write-Host "🚀 验证GitHub Actions配置" -ForegroundColor Green

# 检查关键文件
$files = @(
    ".github\workflows\daily-ai-report.yml",
    "config\config.yaml",
    "requirements.txt",
    "main.py"
)

Write-Host "`n📁 文件检查:" -ForegroundColor Yellow
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file" -ForegroundColor Red
    }
}

Write-Host "`n📋 配置概览:" -ForegroundColor Yellow
$config = Get-Content "config\config.yaml" -Raw
if ($config -match "notification:") { Write-Host "✅ 通知配置" -ForegroundColor Green }
if ($config -match "push_window:") { Write-Host "✅ 时间窗口配置" -ForegroundColor Green }
if ($config -match "platforms:") { Write-Host "✅ 平台配置" -ForegroundColor Green }

Write-Host "`n🎯 下一步:" -ForegroundColor Cyan
Write-Host "1. 推送代码到GitHub" -ForegroundColor White
Write-Host "2. 配置GitHub Secrets" -ForegroundColor White
Write-Host "3. 手动触发测试" -ForegroundColor White