# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import yaml

def test_email():
    # 读取配置
    config_path = Path("config/config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    email_config = config['notification']['webhooks']
    
    # 邮件配置
    smtp_server = email_config['email_smtp_server']
    smtp_port = int(email_config['email_smtp_port'])
    email_from = email_config['email_from']
    email_password = email_config['email_password']
    email_to = email_config['email_to']
    
    print(f"测试邮件配置:")
    print(f"SMTP服务器: {smtp_server}:{smtp_port}")
    print(f"发件人: {email_from}")
    print(f"收件人: {email_to}")
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "TrendRadar邮件测试"
        
        body = """
        <h2>🎯 TrendRadar邮件测试</h2>
        <p>这是一封测试邮件，用于验证邮件推送功能是否正常。</p>
        <p>如果你收到这封邮件，说明配置成功！</p>
        <hr>
        <p><small>发送时间：2025年11月12日</small></p>
        """
        
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        # 发送邮件
        print("正在连接SMTP服务器...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        print("正在登录...")
        server.login(email_from, email_password)
        print("正在发送邮件...")
        server.send_message(msg)
        server.quit()
        
        print("✅ 邮件发送成功！请检查你的邮箱。")
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    test_email()