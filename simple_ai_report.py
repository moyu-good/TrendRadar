# coding=utf-8
"""
简化版AI增强报告生成器
避免CSS样式冲突，专注于内容
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 导入MCP工具
from mcp_server.tools.analytics import AnalyticsTools
from mcp_server.tools.search_tools import SearchTools
from mcp_server.tools.data_query import DataQueryTools


class SimpleAIEnhancedReporter:
    """简化版AI增强新闻报告生成器"""
    
    def __init__(self, project_root: str = None):
        self.project_root = project_root or Path.cwd()
        self.analytics = AnalyticsTools(project_root)
        self.search = SearchTools(project_root)
        self.data_query = DataQueryTools(project_root)
    
    async def generate_simple_ai_report(self) -> Dict:
        """生成简化版AI增强报告"""
        print("🤖 正在生成AI增强版新闻分析报告...")
        
        report_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "basic_stats": {},
            "ai_insights": {},
            "recommendations": []
        }
        
        try:
            # 1. 获取基础数据
            print("📊 获取基础数据...")
            latest_news = await self._get_latest_news()
            report_data["basic_stats"] = {
                "total_news": len(latest_news),
                "platforms": list(set(news.get("platform", "") for news in latest_news)),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            # 2. AI分析 - 平台对比
            print("🔍 进行平台对比分析...")
            try:
                platform_compare = self.analytics.analyze_data_insights_unified(
                    insight_type="platform_compare",
                    topic="人工智能"
                )
                report_data["ai_insights"]["platform_comparison"] = platform_compare
            except Exception as e:
                print(f"平台对比分析失败: {e}")
                report_data["ai_insights"]["platform_comparison"] = {"success": False, "error": str(e)}

            # 3. AI分析 - 异常热度检测
            print("🚨 检测异常热度话题...")
            try:
                viral_topics = self.analytics.analyze_topic_trend_unified(
                    topic="热点",
                    analysis_type="viral",
                    threshold=2.5
                )
                report_data["ai_insights"]["viral_detection"] = viral_topics
            except Exception as e:
                print(f"异常热度检测失败: {e}")
                report_data["ai_insights"]["viral_detection"] = {"success": False, "error": str(e)}

            # 4. 生成智能推荐
            print("💡 生成智能推荐...")
            recommendations = await self._generate_recommendations(report_data)
            report_data["recommendations"] = recommendations

            print("✅ AI增强版报告生成完成！")
            return report_data

        except Exception as e:
            print(f"❌ AI报告生成失败: {str(e)}")
            return {"error": str(e), "basic_report": True}
    
    async def _get_latest_news(self, limit: int = 100) -> List[Dict]:
        """获取最新新闻数据"""
        try:
            result = self.data_query.get_latest_news(limit=limit, include_url=True)
            if isinstance(result, str):
                return json.loads(result).get("news", [])
            elif isinstance(result, dict):
                return result.get("news", [])
            else:
                return []
        except Exception as e:
            print(f"获取新闻数据失败: {e}")
            return []
    
    async def _generate_recommendations(self, report_data: Dict) -> List[Dict]:
        """基于AI分析生成智能推荐"""
        recommendations = []
        
        # 基于病毒检测生成推荐
        viral_data = report_data.get("ai_insights", {}).get("viral_detection", {})
        if viral_data and viral_data.get("success"):
            viral_topics = viral_data.get("viral_topics", [])
            for topic in viral_topics[:3]:
                recommendations.append({
                    "type": "热点关注",
                    "title": f"🔥 {topic.get('title', '未知话题')}",
                    "description": f"该话题热度突增{topic.get('growth_rate', 0)}倍，建议重点关注",
                    "priority": "high"
                })
        
        # 基于平台对比生成推荐
        platform_data = report_data.get("ai_insights", {}).get("platform_comparison", {})
        if platform_data and platform_data.get("success"):
            platforms = platform_data.get("platforms", [])
            if platforms:
                top_platform = platforms[0]
                recommendations.append({
                    "type": "平台策略",
                    "title": f"📈 {top_platform.get('name', '未知平台')}热度领先",
                    "description": f"该平台对目标话题关注度最高({top_platform.get('score', 0)}分)",
                    "priority": "medium"
                })
        
        return recommendations
    
    def generate_simple_html_report(self, ai_report: Dict) -> str:
        """生成简化版HTML报告"""
        basic_stats = ai_report.get("basic_stats", {})
        ai_insights = ai_report.get("ai_insights", {})
        recommendations = ai_report.get("recommendations", [])
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI增强版热点新闻分析</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #2c3e50; }}
        .timestamp {{ color: #666; font-size: 14px; }}
        
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        
        .insight-card {{ background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 15px 0; border-radius: 5px; }}
        .recommendation {{ background: #e8f5e8; border-left: 4px solid #27ae60; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .recommendation.high {{ border-left-color: #e74c3c; background: #fdf2f2; }}
        .recommendation.medium {{ border-left-color: #f39c12; background: #fef9e7; }}
        
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #ecf0f1; padding: 20px; border-radius: 5px; text-align: center; flex: 1; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI增强版热点新闻分析</h1>
            <div class="timestamp">{ai_report.get("timestamp", "")}</div>
        </div>
        
        <div class="section">
            <h2>📊 基础统计</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{basic_stats.get("total_news", 0)}</div>
                    <div class="stat-label">总新闻数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(basic_stats.get("platforms", []))}</div>
                    <div class="stat-label">监控平台</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔍 AI智能洞察</h2>"""
        
        # 添加平台对比分析
        platform_data = ai_insights.get("platform_comparison", {})
        if platform_data and platform_data.get("success"):
            html_content += '<div class="insight-card"><h3>📈 平台对比分析</h3>'
            platforms = platform_data.get("platforms", [])[:5]
            for platform in platforms:
                html_content += f'<div>• <strong>{platform.get("name", "")}</strong>: {platform.get("score", 0)}分 ({platform.get("news_count", 0)}条新闻)</div>'
            html_content += '</div>'
        
        # 添加异常热度检测
        viral_data = ai_insights.get("viral_detection", {})
        if viral_data and viral_data.get("success"):
            html_content += '<div class="insight-card"><h3>🚨 异常热度检测</h3>'
            viral_topics = viral_data.get("viral_topics", [])[:3]
            for topic in viral_topics:
                html_content += f'<div>• <strong>{topic.get("title", "")}</strong>: 热度突增{topic.get("growth_rate", 0):.1f}倍</div>'        
            html_content += '</div>'
        
        html_content += """</div>
        
        <div class="section">
            <h2>💡 智能推荐</h2>"""
        
        # 添加推荐内容
        for rec in recommendations:
            priority_class = rec.get("priority", "low")
            html_content += f'<div class="recommendation {priority_class}">'
            html_content += f'<h4>{rec.get("title", "")}</h4>'
            html_content += f'<p>{rec.get("description", "")}</p>'
            html_content += '</div>'
        
        if not recommendations:
            html_content += '<p>暂无推荐内容</p>'
        
        html_content += """
        </div>
    </div>
</body>
</html>"""
        
        return html_content


async def test_simple_ai_report():
    """测试简化版AI增强报告"""
    reporter = SimpleAIEnhancedReporter()
    
    print("🚀 开始生成简化版AI增强报告...")
    ai_report = await reporter.generate_simple_ai_report()
    
    if "error" not in ai_report:
        # 生成HTML报告
        html_content = reporter.generate_simple_html_report(ai_report)
        
        # 保存报告
        output_dir = Path("output/ai_enhanced")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = output_dir / f"simple_ai_report_{timestamp}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 简化版AI增强报告已生成: {html_file}")
        print(f"📊 报告包含 {len(ai_report.get('recommendations', []))} 个智能推荐")
        
        return html_content
    else:
        print(f"❌ 报告生成失败: {ai_report['error']}")
        return None


if __name__ == "__main__":
    # 运行测试
    result = asyncio.run(test_simple_ai_report())