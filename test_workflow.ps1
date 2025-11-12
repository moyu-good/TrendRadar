# PowerShell测试脚本 - 验证GitHub Actions workflow配置

Write-Host "🚀 测试GitHub Actions workflow配置..." -ForegroundColor Green

# 检查必需文件
Write-Host "`n📁 检查必需文件..." -ForegroundColor Yellow

$requiredFiles = @(
    ".github\workflows\daily-ai-report.yml",
    ".github\workflows\ai-enhanced-daily.yml",
    "config\config.yaml",
    "requirements.txt",
    "main.py",
    "send_ai_report_email.py",
    "simple_ai_report.py"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file 存在" -ForegroundColor Green
    } else {
        Write-Host "❌ $file 不存在" -ForegroundColor Red
        $allFilesExist = $false
    }
}

# 检查Python环境
Write-Host "`n🐍 检查Python环境..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python 可用" -ForegroundColor Green
    $pythonVersion = python --version
    Write-Host "   版本: $pythonVersion" -ForegroundColor Gray
} else {
    Write-Host "❌ Python 不可用" -ForegroundColor Red
}

# 检查配置文件格式
Write-Host "`n⚙️  检查配置文件..." -ForegroundColor Yellow
try {
    $configContent = Get-Content "config\config.yaml" -Raw
    Write-Host "✅ config.yaml 可读取" -ForegroundColor Green
    
    # 检查关键配置项
    if ($configContent -match "notification:") {
        Write-Host "✅ 找到 notification 配置" -ForegroundColor Green
    } else {
        Write-Host "⚠️  可能缺少 notification 配置" -ForegroundColor Yellow
    }
    
    if ($configContent -match "platforms:") {
        Write-Host "✅ 找到 platforms 配置" -ForegroundColor Green
    } else {
        Write-Host "⚠️  可能缺少 platforms 配置" -ForegroundColor Yellow
    }
    
    if ($configContent -match "push_window:") {
        Write-Host "✅ 找到 push_window 配置" -ForegroundColor Green
    } else {
        Write-Host "⚠️  可能缺少 push_window 配置" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ 无法读取 config.yaml: $($_.Exception.Message)" -ForegroundColor Red
}

# 检查workflow文件
Write-Host "`n🔧 检查workflow文件..." -ForegroundColor Yellow
$workflowFiles = @(
    ".github\workflows\daily-ai-report.yml",
    ".github\workflows\ai-enhanced-daily.yml"
)

foreach ($workflow in $workflowFiles) {
    if (Test-Path $workflow) {
        try {
            $workflowContent = Get-Content $workflow -Raw
            Write-Host "✅ $workflow 存在且可读" -ForegroundColor Green
            
            # 检查关键元素
            if ($workflowContent -match "schedule:") {
                Write-Host "   ✅ 包含定时触发器" -ForegroundColor Gray
            }
            if ($workflowContent -match "workflow_dispatch:") {
                Write-Host "   ✅ 支持手动触发" -ForegroundColor Gray
            }
            if ($workflowContent -match "secrets\.") {
                Write-Host "   ✅ 使用Secrets配置" -ForegroundColor Gray
            }
        } catch {
            Write-Host "⚠️  $workflow 存在但无法读取: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    }
}

# 检查依赖文件
Write-Host "`n📦 检查依赖文件..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    try {
        $reqContent = Get-Content "requirements.txt"
        Write-Host "✅ requirements.txt 存在" -ForegroundColor Green
        Write-Host "   依赖包数量: $($reqContent.Count)" -ForegroundColor Gray
        
        $keyPackages = @("requests", "pytz", "pyyaml", "fastmcp")
        foreach ($package in $keyPackages) {
            if ($reqContent -match $package) {
                Write-Host "   ✅ 找到 $package" -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host "⚠️  无法读取 requirements.txt" -ForegroundColor Yellow
    }
}

# 总体评估
Write-Host "`n📊 总体评估:" -ForegroundColor Cyan
if ($allFilesExist) {
    Write-Host "✅ 基础文件检查通过！" -ForegroundColor Green
} else {
    Write-Host "❌ 缺少必需文件，请检查部署" -ForegroundColor Red
}

Write-Host "`n📋 下一步操作建议:" -ForegroundColor Yellow
Write-Host "1. 将代码推送到GitHub" -ForegroundColor White
Write-Host "2. 在GitHub仓库中配置Secrets:" -ForegroundColor White
Write-Host "   - SENDER_EMAIL: 您的发件邮箱" -ForegroundColor Gray
Write-Host "   - SENDER_PASSWORD: 您的邮箱授权码" -ForegroundColor Gray
Write-Host "   - RECIPIENT_EMAIL: 接收报告的邮箱" -ForegroundColor Gray
Write-Host "3. 手动触发workflow测试" -ForegroundColor White
Write-Host "4. 等待明天自动运行验证" -ForegroundColor White

Write-Host "`n🎯 测试完成！" -ForegroundColor Green