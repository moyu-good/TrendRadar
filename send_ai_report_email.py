# coding=utf-8
"""
AI增强版报告邮件发送器
结合AI分析功能，发送智能新闻报告到指定邮箱
"""

import asyncio
import smtplib
import os
import yaml
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Optional

from simple_ai_report import SimpleAIEnhancedReporter


class AIEmailSender:
    """AI增强版邮件发送器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_logging()
        self.reporter = SimpleAIEnhancedReporter()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        try:
            print(f"正在加载配置文件: {self.config_path}")
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                print(f"配置文件加载成功，包含email配置: {'email' in config}")
                if 'email' in config:
                    email_config = config['email']
                    print(f"邮件配置 - sender_email: {bool(email_config.get('sender_email'))}")
                    print(f"邮件配置 - sender_password: {bool(email_config.get('sender_password'))}")
                    print(f"邮件配置 - recipient_email: {bool(email_config.get('recipient_email'))}")
                return config
        except FileNotFoundError:
            print(f"❌ 配置文件不存在: {self.config_path}")
            return self._create_default_config()
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> dict:
        """创建默认配置"""
        return {
            'email': {
                'smtp_server': 'smtp.qq.com',
                'smtp_port': 587,
                'sender_email': os.getenv('SENDER_EMAIL', ''),
                'sender_password': os.getenv('SENDER_PASSWORD', ''),
                'recipient_email': os.getenv('RECIPIENT_EMAIL', '')
            },
            'ai_analysis': {
                'enabled': True,
                'summary_length': 800,
                'include_trends': True,
                'include_insights': True,
                'include_predictions': True
            },
            'logging': {
                'level': 'INFO',
                'file': 'trendradar.log'
            }
        }
    
    def _setup_logging(self):
        """设置日志"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_file = log_config.get('file', 'trendradar.log')
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def generate_ai_report(self) -> Optional[str]:
        """生成AI增强版报告"""
        try:
            self.logger.info("开始生成AI增强版报告...")
            
            # 生成AI报告
            ai_report = await self.reporter.generate_simple_ai_report()
            
            if "error" in ai_report:
                self.logger.error(f"AI报告生成失败: {ai_report['error']}")
                return None
            
            # 生成HTML报告
            html_content = self.reporter.generate_simple_html_report(ai_report)
            
            self.logger.info(f"✅ AI增强版报告生成完成，包含{len(ai_report.get('recommendations', []))}个智能推荐")
            return html_content
            
        except Exception as e:
            self.logger.error(f"AI报告生成异常: {e}")
            return None
    
    def send_email(self, subject: str, html_content: str) -> bool:
        """发送邮件"""
        email_config = self.config.get('email', {})
        
        smtp_server = email_config.get('smtp_server', 'smtp.qq.com')
        smtp_port = email_config.get('smtp_port', 587)
        sender_email = email_config.get('sender_email')
        sender_password = email_config.get('sender_password')
        recipient_email = email_config.get('recipient_email')
        use_ssl = email_config.get('use_ssl', True)
        
        if not all([sender_email, sender_password, recipient_email]):
            self.logger.error("❌ 邮件配置不完整，请检查邮箱设置")
            return False
        
        try:
            self.logger.info(f"正在发送邮件到 {recipient_email}...")
            
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email
            
            # 添加纯文本和HTML内容
            text_content = f"AI增强版热点新闻分析报告\n\n请查看HTML版本以获得更好的阅读体验。\n\n发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            html_part = MIMEText(html_content, 'html', 'utf-8')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # 连接SMTP服务器并发送
            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()  # 启用TLS加密
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            
            self.logger.info(f"✅ 邮件发送成功: {subject}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            self.logger.error("❌ 邮箱认证失败，请检查授权码是否正确")
            return False
        except Exception as e:
            self.logger.error(f"❌ 邮件发送失败: {e}")
            return False
    
    async def send_ai_enhanced_report(self) -> bool:
        """发送AI增强版报告邮件"""
        try:
            # 生成AI报告
            html_content = await self.generate_ai_report()
            if not html_content:
                self.logger.error("无法生成AI报告")
                return False
            
            # 生成邮件主题
            now = datetime.now()
            subject = f"🤖 AI热点分析 {now.strftime('%m月%d日')} - 智能新闻洞察"
            
            # 发送邮件
            success = self.send_email(subject, html_content)
            
            if success:
                # 保存本地副本
                self._save_local_copy(html_content, now)
            
            return success
            
        except Exception as e:
            self.logger.error(f"AI报告邮件发送异常: {e}")
            return False
    
    def _save_local_copy(self, html_content: str, timestamp: datetime):
        """保存本地副本"""
        try:
            output_dir = Path("output/ai_emails")
            output_dir.mkdir(exist_ok=True)
            
            filename = f"ai_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.html"
            file_path = output_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"📁 本地副本已保存: {file_path}")
            
        except Exception as e:
            self.logger.warning(f"无法保存本地副本: {e}")


async def main():
    """主函数"""
    import sys
    print("🚀 启动AI增强版邮件发送器...")
    
    # 检查命令行参数
    config_path = "config/config.yaml"  # 默认路径
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        print(f"使用配置文件: {config_path}")
    
    sender = AIEmailSender(config_path)
    
    # 发送AI增强版报告
    success = await sender.send_ai_enhanced_report()
    
    if success:
        print("✅ AI增强版报告邮件发送完成！")
    else:
        print("❌ AI增强版报告邮件发送失败！")
        return 1
    
    return 0


if __name__ == "__main__":
    # 运行异步主函数
    result = asyncio.run(main())
    exit(result)