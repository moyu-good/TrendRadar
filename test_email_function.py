# coding=utf-8
"""
邮件功能测试脚本
验证邮件配置和发送功能是否正常
"""

import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime


def test_email_config(config_path="config/test_config.yaml"):
    """测试邮件配置"""
    try:
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        email_config = config.get('email', {})
        sender_email = email_config.get('sender_email')
        sender_password = email_config.get('sender_password')
        recipient_email = email_config.get('recipient_email')
        smtp_server = email_config.get('smtp_server', 'smtp.qq.com')
        smtp_port = email_config.get('smtp_port', 587)
        
        print(f"发件人邮箱: {sender_email}")
        print(f"收件人邮箱: {recipient_email}")
        print(f"SMTP服务器: {smtp_server}:{smtp_port}")
        
        # 创建测试邮件 - 使用纯文本避免编码问题
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'TrendRadar AI增强报告测试'
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # 简单的文本内容
        text_content = """
TrendRadar AI增强报告测试

这是一封测试邮件，用于验证邮件发送功能是否正常。
如果收到此邮件，说明邮件配置正确！

发送测试时间: {timestamp}
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # HTML内容
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>AI增强报告测试</title>
        </head>
        <body>
            <h1>TrendRadar AI增强报告测试</h1>
            <p>这是一封测试邮件，用于验证邮件发送功能是否正常。</p>
            <p>如果收到此邮件，说明邮件配置正确！</p>
            <p>发送测试时间: {timestamp}</p>
        </body>
        </html>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # 添加纯文本和HTML版本
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        html_part = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # 发送邮件
        print("正在连接SMTP服务器...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # 启用调试模式
        print("正在启动TLS加密...")
        server.starttls()
        print("正在登录...")
        server.login(sender_email, sender_password)
        print("正在发送邮件...")
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print("✅ 测试邮件发送成功！")
        print("📧 请检查您的邮箱是否收到测试邮件")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ 邮箱认证失败: {e}")
        print("请检查您的QQ邮箱授权码是否正确")
        return False
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False


if __name__ == "__main__":
    print("🚀 开始测试邮件功能...")
    
    # 测试邮件配置
    success = test_email_config()
    
    if success:
        print("\n✅ 邮件功能测试完成！")
        print("接下来可以测试完整的AI报告发送功能")
    else:
        print("\n❌ 邮件功能测试失败！")
        print("请检查邮箱配置和网络连接")