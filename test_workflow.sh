#!/bin/bash
# 测试GitHub Actions workflow配置

echo "🚀 测试GitHub Actions workflow配置..."

# 检查必需文件是否存在
echo "📁 检查必需文件..."

files=(
    ".github/workflows/daily-ai-report.yml"
    ".github/workflows/ai-enhanced-daily.yml"
    "config/config.yaml"
    "requirements.txt"
    "main.py"
    "send_ai_report_email.py"
    "simple_ai_report.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
    fi
done

# 检查workflow语法
echo ""
echo "🔍 检查workflow语法..."
if command -v yq &> /dev/null; then
    yq eval '.github/workflows/daily-ai-report.yml' > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ daily-ai-report.yml 语法正确"
    else
        echo "❌ daily-ai-report.yml 语法错误"
    fi
else
    echo "⚠️  未安装yq，跳过语法检查"
fi

# 检查Python依赖
echo ""
echo "📦 检查Python依赖..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 可用"
    
    # 创建临时环境测试依赖
    echo "测试依赖安装..."
    pip install -r requirements.txt --dry-run 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ 依赖包看起来正常"
    else
        echo "⚠️  依赖包可能有问题"
    fi
else
    echo "❌ Python3 不可用"
fi

# 检查配置文件格式
echo ""
echo "⚙️  检查配置文件..."
if command -v python3 &> /dev/null; then
    python3 -c "
import yaml
try:
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    print('✅ config.yaml 格式正确')
    
    # 检查必要的配置项
    required_keys = ['notification', 'platforms']
    for key in required_keys:
        if key in config:
            print(f'✅ 找到 {key} 配置')
        else:
            print(f'⚠️  缺少 {key} 配置')
            
except Exception as e:
    print(f'❌ config.yaml 格式错误: {e}')
"
fi

echo ""
echo "🎯 测试完成！"
echo ""
echo "📋 下一步操作："
echo "1. 将代码推送到GitHub"
echo "2. 在GitHub仓库中配置Secrets："
echo "   - SENDER_EMAIL: 您的发件邮箱"
echo "   - SENDER_PASSWORD: 您的邮箱授权码"
echo "   - RECIPIENT_EMAIL: 接收报告的邮箱"
echo "3. 手动触发workflow测试"
echo "4. 等待定时任务自动运行"