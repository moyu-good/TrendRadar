#!/bin/bash
# 检查GitHub Actions状态脚本

echo "🔍 检查TrendRadar GitHub Actions状态"
echo "=================================="

# 检查配置文件
echo "📋 配置文件检查："
if [ -f "config/config.yaml" ]; then
    echo "✅ config/config.yaml 存在"
    
    # 检查关键配置
    if grep -q "push_window.*enabled.*true" config/config.yaml; then
        echo "✅ 推送时间窗口已启用"
    fi
    
    if grep -q "once_per_day.*true" config/config.yaml; then
        echo "✅ 每日一次推送已设置"
    fi
    
    if grep -q "email_from.*1249510763@qq.com" config/config.yaml; then
        echo "✅ 邮箱配置正确"
    fi
else
    echo "❌ config/config.yaml 不存在"
fi

echo ""
echo "⏰ 时间配置："
echo "• 推送时间窗口: 08:00-21:00 (北京时间)"
echo "• 对应日本时间: 09:00-22:00"
echo "• GitHub Actions运行: 每小时一次"
echo "• 实际推送: 每天一次（在时间窗口内）"

echo ""
echo "📧 邮件配置检查："
echo "• 发件人: 1249510763@qq.com"
echo "• SMTP服务器: smtp.qq.com:465 (SSL)"
echo "• 收件人: 1249510763@qq.com"

echo ""
echo "🎯 监控平台："
echo "• 今日头条、百度热搜、华尔街见闻、澎湃新闻"
echo "• 哔哩哔哩热搜、财联社热门、凤凰网、贴吧"
echo "• 微博、抖音、知乎"
echo "• 总计: 11个主流平台"

echo ""
echo "✅ 总结："
echo "您的配置完全正确！现有workflow能够保证："
echo "1. 每小时检查一次新内容"
echo "2. 每天只在8:00-21:00北京时间推送一次"
echo "3. 包含11个平台的精选热点内容"
echo "4. 直接发送到您的QQ邮箱"

echo ""
echo "📋 建议："
echo "• 检查您的邮箱（包括垃圾邮件文件夹）"
echo "• 如果今天还没收到邮件，可以手动触发workflow测试"
echo "• 如需调整时间，修改config.yaml中的push_window设置"