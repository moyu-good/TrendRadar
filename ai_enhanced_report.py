# coding=utf-8
"""
AI增强版报告生成器
整合MCP服务器的AI分析功能，生成更智能的新闻分析报告
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


class AIEnhancedReporter:
    """AI增强版新闻报告生成器"""
    
    def __init__(self, project_root: str = None):
        self.project_root = project_root or Path.cwd()
        self.analytics = AnalyticsTools(project_root)
        self.search = SearchTools(project_root)
        self.data_query = DataQueryTools(project_root)
    
    async def generate_ai_enhanced_report(self) -> Dict:
        """生成AI增强版报告"""
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
            platform_compare = self.analytics.analyze_data_insights_unified(
                insight_type="platform_compare",
                topic="人工智能"  # 可以动态调整关键词
            )
            report_data["ai_insights"]["platform_comparison"] = platform_compare
            
            # 3. AI分析 - 异常热度检测
            print("🚨 检测异常热度话题...")
            viral_topics = self.analytics.analyze_topic_trend_unified(
                topic="热点",
                analysis_type="viral",
                threshold=2.5
            )
            report_data["ai_insights"]["viral_detection"] = viral_topics
            
            # 4. AI分析 - 关键词共现
            print("🔗 分析关键词共现模式...")
            keyword_cooccur = self.analytics.analyze_data_insights_unified(
                insight_type="keyword_cooccur",
                min_frequency=2,
                top_n=15
            )
            report_data["ai_insights"]["keyword_patterns"] = keyword_cooccur
            
            # 5. 智能推荐
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
            # 使用数据查询工具获取最新新闻
            result = self.data_query.get_latest_news(limit=limit, include_url=True)
            if isinstance(result, str):
                # 解析JSON字符串结果
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
                    "priority": "high",
                    "action": "immediate_attention"
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
                    "priority": "medium",
                    "action": "focus_platform"
                })
        
        # 基于关键词模式生成推荐
        keyword_data = report_data.get("ai_insights", {}).get("keyword_patterns", {})
        if keyword_data and keyword_data.get("success"):
            patterns = keyword_data.get("cooccurrence_patterns", [])
            for pattern in patterns[:2]:
                keywords = pattern.get("keywords", [])
                if len(keywords) >= 2:
                    recommendations.append({
                        "type": "关键词组合",
                        "title": f"🔗 {' + '.join(keywords[:3])}",
                        "description": f"这些关键词经常同时出现({pattern.get('frequency', 0)}次)，可能存在关联话题",
                        "priority": "low",
                        "action": "explore_combination"
                    })
        
        return recommendations
    
    def generate_html_report(self, ai_report: Dict) -> str:
        """生成HTML格式的AI增强报告"""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI增强版热点新闻分析</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #2c3e50; margin-bottom: 10px; }
        .timestamp { color: #7f8c8d; font-size: 14px; }
        
        .section { margin-bottom: 30px; }
        .section h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        
        .insight-card { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 15px 0; border-radius: 8px; }
        .recommendation { background: #e8f5e8; border-left: 4px solid #27ae60; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .recommendation.high { border-left-color: #e74c3c; background: #fdf2f2; }
        .recommendation.medium { border-left-color: #f39c12; background: #fef9e7; }
        
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #ecf0f1; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 24px; font-weight: bold; color: #2c3e50; }
        .stat-label { color: #7f8c8d; font-size: 14px; }
        
        .keyword-tag { display: inline-block; background: #3498db; color: white; padding: 4px 8px; border-radius: 4px; margin: 2px; font-size: 12px; }
        .platform-score { background: #95a5a6; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI增强版热点新闻分析</h1>
            <div class="timestamp">{timestamp}</div>
        </div>
        
        <div class="section">
            <h2>📊 基础统计</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_news}</div>
                    <div class="stat-label">总新闻数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{platform_count}</div>
                    <div class="stat-label">监控平台</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔍 AI智能洞察</h2>
            {ai_insights_html}
        </div>
        
        <div class="section">
            <h2>💡 智能推荐</h2>
            {recommendations_html}
        </div>
    </div>
</body>
</html>
        """
        
        # 生成AI洞察HTML
        ai_insights_html = self._generate_ai_insights_html(ai_report.get("ai_insights", {}))
        
        # 生成推荐HTML
        recommendations_html = self._generate_recommendations_html(ai_report.get("recommendations", []))
        
        # 填充模板
        basic_stats = ai_report.get("basic_stats", {})
        html_content = html_template.format(
            timestamp=ai_report.get("timestamp", ""),
            total_news=basic_stats.get("total_news", 0),
            platform_count=len(basic_stats.get("platforms", [])),
            ai_insights_html=ai_insights_html,
            recommendations_html=recommendations_html
        )
        
        return html_content
    
    def _generate_ai_insights_html(self, ai_insights: Dict) -> str:
        """生成AI洞察HTML"""
        html_parts = []
        
        # 平台对比分析
        platform_data = ai_insights.get("platform_comparison", {})
        if platform_data and platform_data.get("success"):
            html_parts.append('<div class="insight-card">')
            html_parts.append('<h3>📈 平台对比分析</h3>')
            platforms = platform_data.get("platforms", [])[:5]
            for platform in platforms:
                html_parts.append(f'<div>• <strong>{platform.get("name", "")}</strong>: '
                                f'<span class="platform-score">{platform.get("score", 0)}分</span> '
                                f'({platform.get("news_count", 0)}条新闻)</div>')
            html_parts.append('</div>')
        
        # 异常热度检测
        viral_data = ai_insights.get("viral_detection", {})
        if viral_data and viral_data.get("success"):
            html_parts.append('<div class="insight-card">')
            html_parts.append('<h3>🚨 异常热度检测</h3>')
            viral_topics = viral_data.get("viral_topics", [])[:3]
            for topic in viral_topics:
                html_parts.append(f'<div>• <strong>{topic.get("title", "")}</strong>: '
                                f'热度突增{topic.get("growth_rate", 0):.1f}倍</div>')
            html_parts.append('</div>')
        
        # 关键词共现分析
        keyword_data = ai_insights.get("keyword_patterns", {})
        if keyword_data and keyword_data.get("success"):
            html_parts.append('<div class="insight-card">')
            html_parts.append('<h3>🔗 关键词共现模式</h3>')
            patterns = keyword_data.get("cooccurrence_patterns", [])[:5]
            for pattern in patterns:
                keywords = pattern.get("keywords", [])
                if keywords:
                    keyword_tags = ' '.join([f'<span class="keyword-tag">{k}</span>' for k in keywords[:3]])
                    html_parts.append(f'<div>• {keyword_tags} (出现{pattern.get("frequency", 0)}次)</div>')
            html_parts.append('</div>')
        
        return '\n'.join(html_parts) if html_parts else '<p>暂无AI洞察数据</p>'
    
    def _generate_recommendations_html(self, recommendations: List[Dict]) -> str:
        """生成推荐HTML"""
        if not recommendations:
            return '<p>暂无推荐内容</p>'
        
        html_parts = []
        for rec in recommendations:
            priority_class = rec.get("priority", "low")
            html_parts.append(f'<div class="recommendation {priority_class}">')
            html_parts.append(f'<h4>{rec.get("title", "")}</h4>')
            html_parts.append(f'<p>{rec.get("description", "")}</p>')
            html_parts.append('</div>')
        
        return '\n'.join(html_parts)


async def test_ai_enhanced_report():
    """测试AI增强版报告"""
    reporter = AIEnhancedReporter()
    
    print("🚀 开始生成AI增强版报告...")
    ai_report = await reporter.generate_ai_enhanced_report()
    
    if "error" not in ai_report:
        # 生成HTML报告
        html_content = reporter.generate_html_report(ai_report)
        
        # 保存报告
        output_dir = Path("output/ai_enhanced")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = output_dir / f"ai_report_{timestamp}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ AI增强版报告已生成: {html_file}")
        print(f"📊 报告包含 {len(ai_report.get('recommendations', []))} 个智能推荐")
        
        return str(html_file)
    else:
        print(f"❌ 报告生成失败: {ai_report['error']}")
        return None


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_ai_enhanced_report())