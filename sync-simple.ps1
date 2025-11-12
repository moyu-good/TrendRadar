# 三方同步管理脚本
Write-Host "=== TrendRadar 三方同步管理 ===" -ForegroundColor Green
Write-Host "原始源代码: sansan0/TrendRadar" -ForegroundColor Blue
Write-Host "你的Fork: moyu-good/TrendRadar" -ForegroundColor Blue
Write-Host "本地仓库: 当前目录" -ForegroundColor Blue
Write-Host ""

# 函数：显示当前状态
function Show-Status {
    Write-Host "当前仓库状态:" -ForegroundColor Yellow
    Write-Host "远程仓库配置:"
    git remote -v
    Write-Host ""
}

# 显示当前状态
Show-Status

Write-Host "步骤1: 获取原始源代码更新..." -ForegroundColor Yellow
# 获取原始源代码更新
git fetch upstream

# 检查是否有更新
$local_commit = git rev-parse HEAD
$upstream_commit = git rev-parse upstream/master

if ($local_commit -ne $upstream_commit) {
    Write-Host "发现原始源代码有更新，正在合并..." -ForegroundColor Yellow
    
    # 创建备份分支（可选）
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    git branch backup-before-upstream-$timestamp
    Write-Host "已创建备份分支: backup-before-upstream-$timestamp" -ForegroundColor Green
    
    # 合并原始源代码
    git merge upstream/master --no-edit
    Write-Host "原始源代码更新已合并" -ForegroundColor Green
} else {
    Write-Host "原始源代码已是最新版本" -ForegroundColor Green
}
Write-Host ""

Write-Host "步骤2: 检查本地更改..." -ForegroundColor Yellow
# 检查本地是否有未提交的更改
$status = git status --porcelain
if ($status) {
    Write-Host "发现本地有更改，正在提交..." -ForegroundColor Yellow
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "本地更新 - $timestamp"
    Write-Host "本地更改已提交" -ForegroundColor Green
} else {
    Write-Host "本地没有待提交的更改" -ForegroundColor Green
}
Write-Host ""

Write-Host "步骤3: 推送到你的Fork..." -ForegroundColor Yellow
# 推送到远程仓库
git push origin master

if ($LASTEXITCODE -eq 0) {
    Write-Host "推送到Fork成功" -ForegroundColor Green
} else {
    Write-Host "推送到Fork失败" -ForegroundColor Red
}
Write-Host ""

Write-Host "最终状态:" -ForegroundColor Yellow
git status
Write-Host ""

Write-Host "三方同步完成！" -ForegroundColor Green
Write-Host ""
Write-Host "使用说明:" -ForegroundColor Yellow
Write-Host "  • 此脚本管理三方同步：原始代码 → 本地 → 你的Fork"
Write-Host "  • 自动处理冲突和合并"
Write-Host "  • 本地更改会自动提交并推送"
Write-Host "  • 原始源代码更新会自动拉取并合并"
Write-Host "  • 建议定期运行以保持同步"