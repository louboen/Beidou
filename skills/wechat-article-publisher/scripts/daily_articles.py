#!/usr/bin/env python3
"""
每日文章批量生成工具
根据模板体系每日自动生成 3 篇文章供选择
"""

import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path(__file__).parent.parent
ARTICLES_DIR = WORKSPACE / "articles"
TEMPLATES_DIR = WORKSPACE / "templates"

# 内容库
CONTENT_LIBRARY = {
    "节气养生": {
        "选题": [
            {"title": "立春养生：做好这 3 点，全年少生病", "keywords": ["立春", "春季", "养生"]},
            {"title": "雨水时节：祛湿健脾正当时", "keywords": ["雨水", "祛湿", "脾胃"]},
            {"title": "惊蛰养生：防感冒、护肝脏", "keywords": ["惊蛰", "感冒", "养肝"]},
            {"title": "春分时节：阴阳平衡的关键", "keywords": ["春分", "平衡", "养生"]},
            {"title": "清明养生：踏青祭祖注意这些", "keywords": ["清明", "踏青", "保健"]},
            {"title": "谷雨时节：健脾祛湿养气血", "keywords": ["谷雨", "健脾", "气血"]},
        ],
        "模板": "templates/01_节气养生模板.html"
    },
    "中医食疗": {
        "选题": [
            {"title": "春季养肝茶：3 款简单有效的代茶饮", "keywords": ["养肝", "茶", "春季"]},
            {"title": "失眠怎么办？试试这 3 款安神汤", "keywords": ["失眠", "安神", "汤"]},
            {"title": "养胃粥谱：5 款家常粥养出好脾胃", "keywords": ["养胃", "粥", "脾胃"]},
            {"title": "补气养血：女性必喝的 3 款汤品", "keywords": ["补气", "养血", "女性"]},
            {"title": "降火祛痘：夏季清凉饮品推荐", "keywords": ["降火", "祛痘", "夏季"]},
            {"title": "补肾黑发：黑芝麻的 5 种吃法", "keywords": ["补肾", "黑发", "黑芝麻"]},
        ],
        "模板": "templates/02_中医食疗模板.html"
    },
    "穴位保健": {
        "选题": [
            {"title": "太冲穴：人体的出气筒，疏肝解郁", "keywords": ["太冲穴", "疏肝", "解郁"]},
            {"title": "足三里：长寿穴，每天按一按", "keywords": ["足三里", "长寿", "保健"]},
            {"title": "合谷穴：止痛要穴，缓解头痛牙痛", "keywords": ["合谷穴", "止痛", "头痛"]},
            {"title": "内关穴：护心穴，缓解心悸胸闷", "keywords": ["内关穴", "护心", "心悸"]},
            {"title": "涌泉穴：补肾安神，改善睡眠", "keywords": ["涌泉穴", "补肾", "睡眠"]},
            {"title": "肾俞穴：强腰补肾，缓解腰痛", "keywords": ["肾俞穴", "强腰", "腰痛"]},
        ],
        "模板": "templates/03_穴位保健模板.html"
    },
    "健康新闻": {
        "选题": [
            {"title": "2024 中国骨质疏松症流调结果发布", "keywords": ["骨质疏松", "流调", "数据"]},
            {"title": "新版高血压指南发布：诊断标准有变化", "keywords": ["高血压", "指南", "诊断"]},
            {"title": "糖尿病防治：中国专家提出新建议", "keywords": ["糖尿病", "防治", "专家"]},
            {"title": "流感高发季：疾控中心发布防控指南", "keywords": ["流感", "防控", "指南"]},
            {"title": "癌症早筛：这些人群需要定期检查", "keywords": ["癌症", "早筛", "检查"]},
            {"title": "医保新政：这些药品纳入报销范围", "keywords": ["医保", "药品", "报销"]},
        ],
        "模板": "templates/04_健康新闻模板.html"
    }
}

def generate_article_content(article_type, topic):
    """根据选题生成文章内容"""
    title = topic["title"]
    keywords = topic["keywords"]
    
    # 这里可以接入 AI 生成内容，目前使用占位符
    content = f"""
<!-- 文章内容需要根据选题填充 -->
<!-- 标题：{title} -->
<!-- 关键词：{', '.join(keywords)} -->
<!-- 类型：{article_type} -->

<p>[文章内容需要填充...]</p>
<p>建议：使用已有文章内容或手动编写</p>
"""
    return content

def create_daily_articles(date=None):
    """生成每日 3 篇文章"""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime("%Y-%m-%d")
    weekday = date.strftime("%A")
    
    # 每日文章类型轮换
    daily_types = [
        ["节气养生", "中医食疗", "穴位保健"],
        ["节气养生", "中医食疗", "健康新闻"],
        ["节气养生", "穴位保健", "健康新闻"],
        ["中医食疗", "穴位保健", "健康新闻"],
        ["节气养生", "中医食疗", "穴位保健"],
        ["节气养生", "中医食疗", "健康新闻"],
        ["节气养生", "穴位保健", "健康新闻"],
    ]
    
    # 根据星期几选择类型组合
    type_combination = daily_types[date.weekday() % len(daily_types)]
    
    print(f"📅 生成日期：{date_str} ({weekday})")
    print(f"📝 文章类型：{', '.join(type_combination)}")
    print("=" * 60)
    
    generated_articles = []
    
    for article_type in type_combination:
        # 随机选择一个选题
        content_lib = CONTENT_LIBRARY.get(article_type, {})
        topics = content_lib.get("选题", [])
        
        if not topics:
            print(f"⚠️  {article_type} 类型暂无选题")
            continue
        
        topic = random.choice(topics)
        title = topic["title"]
        
        # 生成文件名
        filename = f"{date_str}_{article_type}_{title[:10]}.html"
        filepath = ARTICLES_DIR / filename
        
        # 复制模板并填充内容
        template_path = WORKSPACE / content_lib.get("模板", "")
        
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
            
            # 替换标题和日期
            article_content = template_content.replace(
                "[节气名称] 养生：[核心主题]", 
                title
            ).replace(
                "[发布日期] · 节气养生",
                f"{date_str} · {article_type}"
            )
            
            # 保存文章
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(article_content)
            
            generated_articles.append({
                "type": article_type,
                "title": title,
                "filename": filename,
                "filepath": str(filepath)
            })
            
            print(f"✅ {article_type}: {title}")
            print(f"   文件：{filename}")
        else:
            print(f"❌ 模板不存在：{template_path}")
    
    print("=" * 60)
    print(f"📊 共生成 {len(generated_articles)} 篇文章")
    print("\n📋 文章列表:")
    for i, article in enumerate(generated_articles, 1):
        print(f"  {i}. 【{article['type']}】{article['title']}")
    
    # 保存生成记录
    record_file = WORKSPACE / "每日文章记录" / f"{date_str}.json"
    record_file.parent.mkdir(exist_ok=True)
    
    with open(record_file, "w", encoding="utf-8") as f:
        json.dump({
            "date": date_str,
            "articles": generated_articles
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 记录已保存：{record_file}")
    
    return generated_articles

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="每日文章批量生成工具")
    parser.add_argument("--date", type=str, default="", 
                       help="指定日期 (YYYY-MM-DD)，默认为明天")
    parser.add_argument("--days", type=int, default=1, 
                       help="生成多少天的文章 (1-7)")
    parser.add_argument("--list-topics", action="store_true",
                       help="列出所有可用选题")
    
    args = parser.parse_args()
    
    if args.list_topics:
        print("📚 内容库选题列表")
        print("=" * 60)
        for article_type, content in CONTENT_LIBRARY.items():
            print(f"\n【{article_type}】")
            for topic in content.get("选题", []):
                print(f"  • {topic['title']}")
        return
    
    # 确定起始日期
    if args.date:
        start_date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        start_date = datetime.now() + timedelta(days=1)  # 默认为明天
    
    # 生成指定天数的文章
    for i in range(args.days):
        current_date = start_date + timedelta(days=i)
        print(f"\n{'='*60}")
        print(f"第 {i+1} 天")
        print('='*60)
        create_daily_articles(current_date)

if __name__ == "__main__":
    main()
