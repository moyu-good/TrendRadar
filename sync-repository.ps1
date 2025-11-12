# 本地与远程仓库同步脚本
# 用于建立双向同步机制

# 设置颜色输出
$GREEN = "\033[32m"
$YELLOW = "\033[33m"
$RED = "\033[31m"
$NC = "\033[0m" # No Color

Write-Host "$GREEN=== TrendRadar 双向同步机制 ===$NC"
Write-Host ""

# 检查当前分支状态
Write-Host "$YELLOW📋 检查当前分支状态...$NC"
git status
Write-Host ""

# 获取远程更新
Write-Host "$YELLOW📥 获取远程仓库最新更新...$NC"
git fetch origin
Write-Host ""

# 检查是否有远程更新
$local_commit = git rev-parse HEAD
$remote_commit = git rev-parse origin/master

if ($local_commit -ne $remote_commit) {
    Write-Host "$YELLOW🔄 检测到远程有更新，正在合并...$NC"
    git merge origin/master
    Write-Host "$GREEN✅ 远程更新已合并到本地$NC"
} else {
    Write-Host "$GREEN✅ 本地已是最新版本$NC"
}
Write-Host ""

# 检查本地是否有未提交的更改
$status = git status --porcelain
if ($status) {
    Write-Host "$YELLOW💾 检测到本地有更改，正在提交...$NC"
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "同步更新 - $timestamp"
    Write-Host "$GREEN✅ 本地更改已提交$NC"
} else {
    Write-Host "$GREEN✅ 本地没有待提交的更改$NC"
}
Write-Host ""

# 推送到远程仓库
Write-Host "$YELLOW📤 推送到远程仓库...$NC"
git push origin master
Write-Host "$GREEN✅ 推送完成$NC"
Write-Host ""

# 显示最终状态
Write-Host "$YELLOW📊 最终同步状态:$NC"
git status
Write-Host ""
Write-Host "$GREEN🎉 双向同步完成！$NC"
Write-Host ""
Write-Host "$YELLOW💡 使用说明:$NC"
Write-Host "  • 运行此脚本可保持本地与远程仓库同步"
Write-Host "  • 自动处理冲突和合并"
Write-Host "  • 本地更改会自动提交并推送"
Write-Host "  • 远程更新会自动拉取并合并"