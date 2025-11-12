# 三方同步管理脚本
# 管理原始源代码、你的Fork和本地仓库的同步

$GREEN = "\033[32m"
$YELLOW = "\033[33m"
$RED = "\033[31m"
$BLUE = "\033[34m"
$NC = "\033[0m" # No Color

Write-Host "$GREEN=== TrendRadar 三方同步管理 ===$NC"
Write-Host "${BLUE}原始源代码: sansan0/TrendRadar${NC}"
Write-Host "${BLUE}你的Fork: moyu-good/TrendRadar${NC}"
Write-Host "${BLUE}本地仓库: 当前目录${NC}"
Write-Host ""

# 函数：显示当前状态
function Show-Status {
    Write-Host "${YELLOW}📊 当前仓库状态:${NC}"
    Write-Host "远程仓库配置:"
    git remote -v
    Write-Host ""
    
    Write-Host "分支状态:"
    git status
    Write-Host ""
}

# 函数：同步原始源代码
function Sync-Upstream {
    Write-Host "$YELLOW🔄 正在同步原始源代码更新...$NC"
    
    # 获取原始源代码更新
    git fetch upstream
    
    # 检查是否有更新
    $local_commit = git rev-parse HEAD
    $upstream_commit = git rev-parse upstream/master
    
    if ($local_commit -ne $upstream_commit) {
        Write-Host "$GREEN发现原始源代码有更新，正在合并...$NC"
        
        # 创建备份分支（可选）
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        git branch backup-before-upstream-$timestamp
        Write-Host "$GREEN已创建备份分支: backup-before-upstream-$timestamp$NC"
        
        # 合并原始源代码
        git merge upstream/master --no-edit
        Write-Host "$GREEN✅ 原始源代码更新已合并$NC"
    } else {
        Write-Host "$GREEN✅ 原始源代码已是最新版本$NC"
    }
}

# 函数：推送到你的Fork
function Push-To-Fork {
    Write-Host "$YELLOW📤 正在推送到你的Fork...$NC"
    
    git push origin master
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "$GREEN✅ 推送到Fork成功$NC"
    } else {
        Write-Host "$RED❌ 推送到Fork失败$NC"
    }
}

# 函数：处理本地更改
function Handle-Local-Changes {
    Write-Host "$YELLOW💾 检查本地更改...$NC"
    
    $status = git status --porcelain
    if ($status) {
        Write-Host "$YELLOW发现本地有更改，正在提交...$NC"
        git add .
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "本地更新 - $timestamp"
        Write-Host "$GREEN✅ 本地更改已提交$NC"
        return $true
    } else {
        Write-Host "$GREEN✅ 本地没有待提交的更改$NC"
        return $false
    }
}

# 主流程
Write-Host "$YELLOW🔍 步骤1: 检查当前状态$NC"
Show-Status

Write-Host "$YELLOW🔍 步骤2: 处理本地更改$NC"
$has_changes = Handle-Local-Changes

Write-Host "$YELLOW🔍 步骤3: 同步原始源代码$NC"
Sync-Upstream

Write-Host "$YELLOW🔍 步骤4: 推送到你的Fork$NC"
Push-To-Fork

Write-Host "$YELLOW🔍 步骤5: 最终状态检查$NC"
Show-Status

Write-Host "$GREEN🎉 三方同步完成！$NC"
Write-Host ""
Write-Host "$YELLOW💡 使用说明:$NC"
Write-Host "  • 此脚本管理三方同步：原始代码 → 本地 → 你的Fork"
Write-Host "  • 自动处理冲突和合并"
Write-Host "  • 本地更改会自动提交并推送"
Write-Host "  • 原始源代码更新会自动拉取并合并"
Write-Host "  • 建议定期运行以保持同步"
Write-Host ""
Write-Host "$YELLOW🔧 其他有用命令:$NC"
Write-Host "  查看原始源代码更新: git log upstream/master --oneline"
Write-Host "  查看你的Fork更新: git log origin/master --oneline"
Write-Host "  手动同步原始代码: git fetch upstream && git merge upstream/master"
Write-Host "  手动推送到Fork: git push origin master"