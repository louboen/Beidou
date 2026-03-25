#!/usr/bin/env python3
"""
微信公众号文章写作工具
创建中医养生相关的微信公众号文章
"""

import os
import sys
import json
import datetime
from typing import Dict, List, Optional

def create_article_template(topic: str = "中医养生") -> Dict:
    """创建文章模板"""
    
    templates = {
        "中医养生": {
            "title": "春季中医养生指南",
            "author": "娄医生",
            "digest": "春季养生正当时，中医教你如何顺应时节调养身体。",
            "content": """<h1>春季中医养生指南</h1>

<h2>一、春季养生原则</h2>
<p>春季是万物复苏的季节，中医认为春季对应肝脏，肝主疏泄，喜条达而恶抑郁。春季养生应遵循以下原则：</p>

<h3>1. 顺应自然</h3>
<ul>
<li><strong>早睡早起</strong>：顺应阳气生发，晚上11点前入睡，早上6-7点起床</li>
<li><strong>适当运动</strong>：选择散步、太极拳、八段锦等温和运动</li>
<li><strong>保持心情舒畅</strong>：避免生气、抑郁，保持乐观心态</li>
</ul>

<h3>2. 饮食调养</h3>
<ul>
<li><strong>多吃绿色蔬菜</strong>：菠菜、芹菜、西兰花、韭菜等</li>
<li><strong>适量酸味食物</strong>：柠檬、山楂、醋（助肝气疏泄）</li>
<li><strong>少吃油腻辛辣</strong>：避免加重肝脏负担</li>
</ul>

<h2>二、春季养生食谱</h2>

<h3>1. 枸杞菊花茶</h3>
<p><strong>材料</strong>：枸杞10克，菊花5克，冰糖适量</p>
<p><strong>做法</strong>：沸水冲泡，代茶饮用</p>
<p><strong>功效</strong>：清肝明目，缓解眼疲劳</p>

<h3>2. 菠菜猪肝汤</h3>
<p><strong>材料</strong>：菠菜200克，猪肝100克，姜片适量</p>
<p><strong>做法</strong>：
<ol>
<li>猪肝切片，用清水浸泡30分钟去血水</li>
<li>菠菜洗净切段</li>
<li>锅中加水烧开，放入姜片、猪肝煮至变色</li>
<li>加入菠菜，煮1-2分钟即可</li>
</ol>
</p>
<p><strong>功效</strong>：补血养肝，改善视力</p>

<h3>3. 山药红枣粥</h3>
<p><strong>材料</strong>：山药100克，红枣10枚，大米50克</p>
<p><strong>做法</strong>：所有材料洗净，加水煮粥</p>
<p><strong>功效</strong>：健脾养胃，补气养血</p>

<h2>三、穴位保健</h2>

<h3>1. 太冲穴</h3>
<p><strong>位置</strong>：足背第一、二跖骨结合部前方凹陷处</p>
<p><strong>按摩方法</strong>：用拇指按压，每次5-10分钟，每日2次</p>
<p><strong>功效</strong>：疏肝理气，缓解压力</p>

<h3>2. 肝俞穴</h3>
<p><strong>位置</strong>：背部第九胸椎棘突下旁开1.5寸</p>
<p><strong>按摩方法</strong>：让他人帮忙按摩或使用按摩器</p>
<p><strong>功效</strong>：调理肝脏功能</p>

<h3>3. 足三里</h3>
<p><strong>位置</strong>：膝盖外侧凹陷下3寸</p>
<p><strong>按摩方法</strong>：拇指按压，有酸胀感为宜</p>
<p><strong>功效</strong>：健脾和胃，增强免疫力</p>

<h2>四、春季养生小贴士</h2>

<ol>
<li><strong>晨起梳头</strong>：用木梳从前额梳到后颈，促进头部血液循环</li>
<li><strong>睡前泡脚</strong>：用温水泡脚15分钟，加入艾叶或生姜效果更佳</li>
<li><strong>常笑养生</strong>：笑能宣肺，促进气血运行</li>
<li><strong>适度运动</strong>：春季宜"广步于庭"，不宜剧烈运动</li>
<li><strong>注意保暖</strong>：春季温差大，注意"春捂秋冻"</li>
</ol>

<hr>

<div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0;">
<p style="margin: 0; color: #666; font-size: 14px;">
<strong>温馨提示</strong>：本文仅供参考，如有不适请及时就医。养生贵在坚持，持之以恒方能见效。
</p>
</div>

<p style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
发布时间：{date} | 作者：{author} | 文章来源：中医娄伯恩微信公众号
</p>"""
        },
        "中医食疗": {
            "title": "中医食疗养生方",
            "author": "娄医生",
            "digest": "药食同源，中医食疗养生方助您健康生活。",
            "content": """<h1>中医食疗养生方</h1>

<h2>一、食疗原则</h2>
<p>中医认为"药食同源"，食物不仅可以充饥，还能调理身体。食疗应遵循以下原则：</p>

<h3>1. 因人制宜</h3>
<ul>
<li><strong>寒性体质</strong>：多吃温性食物，如姜、葱、羊肉</li>
<li><strong>热性体质</strong>：多吃凉性食物，如西瓜、绿豆、苦瓜</li>
<li><strong>虚性体质</strong>：多吃补益食物，如山药、红枣、枸杞</li>
</ul>

<h3>2. 因时制宜</h3>
<ul>
<li><strong>春季</strong>：养肝，多吃绿色蔬菜</li>
<li><strong>夏季</strong>：养心，多吃红色食物</li>
<li><strong>秋季</strong>：养肺，多吃白色食物</li>
<li><strong>冬季</strong>：养肾，多吃黑色食物</li>
</ul>

<h2>二、常见病症食疗方</h2>

<h3>1. 感冒初期</h3>
<p><strong>姜枣茶</strong></p>
<p><strong>材料</strong>：生姜3片，红枣5枚，红糖适量</p>
<p><strong>做法</strong>：水煎代茶饮</p>
<p><strong>功效</strong>：散寒解表，适用于风寒感冒</p>

<h3>2. 咳嗽有痰</h3>
<p><strong>梨膏糖</strong></p>
<p><strong>材料</strong>：雪梨1个，川贝母3克，冰糖适量</p>
<p><strong>做法</strong>：雪梨去核，填入川贝母和冰糖，蒸熟食用</p>
<p><strong>功效</strong>：润肺止咳，化痰平喘</p>

<h3>3. 失眠多梦</h3>
<p><strong>百合莲子粥</strong></p>
<p><strong>材料</strong>：百合30克，莲子30克，大米50克</p>
<p><strong>做法</strong>：所有材料洗净，加水煮粥</p>
<p><strong>功效</strong>：养心安神，改善睡眠</p>

<h2>三、四季养生食疗</h2>

<h3>春季养肝食疗</h3>
<ul>
<li><strong>菠菜猪肝汤</strong>：补血养肝</li>
<li><strong>枸杞菊花茶</strong>：清肝明目</li>
<li><strong>芹菜炒香干</strong>：平肝降压</li>
</ul>

<h3>夏季养心食疗</h3>
<ul>
<li><strong>绿豆汤</strong>：清热解毒</li>
<li><strong>西瓜汁</strong>：生津止渴</li>
<li><strong>苦瓜炒蛋</strong>：清心降火</li>
</ul>

<h3>秋季养肺食疗</h3>
<ul>
<li><strong>银耳莲子羹</strong>：润肺止咳</li>
<li><strong>蜂蜜柚子茶</strong>：化痰止咳</li>
<li><strong>白萝卜汤</strong>：理气化痰</li>
</ul>

<h3>冬季养肾食疗</h3>
<ul>
<li><strong>黑豆排骨汤</strong>：补肾强骨</li>
<li><strong>核桃芝麻糊</strong>：补肾乌发</li>
<li><strong>羊肉汤</strong>：温补肾阳</li>
</ul>

<hr>

<div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0;">
<p style="margin: 0; color: #666; font-size: 14px;">
<strong>食疗注意事项</strong>：
<ol style="margin: 10px 0; padding-left: 20px;">
<li>食疗不能代替药物治疗</li>
<li>长期坚持才能见效</li>
<li>如有不适请及时就医</li>
<li>根据自身体质选择食疗方</li>
</ol>
</p>
</div>

<p style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
发布时间：{date} | 作者：{author} | 文章来源：中医娄伯恩微信公众号
</p>"""
        },
        "穴位保健": {
            "title": "常用穴位保健指南",
            "author": "娄医生",
            "digest": "掌握常用穴位，自我保健更轻松。",
            "content": """<h1>常用穴位保健指南</h1>

<h2>一、头部穴位</h2>

<h3>1. 百会穴</h3>
<p><strong>位置</strong>：头顶正中，两耳尖连线中点</p>
<p><strong>功效</strong>：提神醒脑，改善头痛、失眠</p>
<p><strong>按摩方法</strong>：用中指按压，顺时针揉按3-5分钟</p>

<h3>2. 太阳穴</h3>
<p><strong>位置</strong>：眉梢与外眼角之间向后约1寸凹陷处</p>
<p><strong>功效</strong>：缓解头痛、眼疲劳</p>
<p><strong>按摩方法</strong>：用拇指按压，轻轻揉动</p>

<h3>3. 风池穴</h3>
<p><strong>位置</strong>：后颈部，枕骨下两侧凹陷处</p>
<p><strong>功效</strong>：缓解颈椎病、头痛、感冒</p>
<p><strong>按摩方法</strong>：用拇指按压，有酸胀感为宜</p>

<h2>二、上肢穴位</h2>

<h3>1. 合谷穴</h3>
<p><strong>位置</strong>：手背第一、二掌骨之间，约平第二掌骨中点</p>
<p><strong>功效</strong>：缓解头痛、牙痛、感冒</p>
<p><strong>按摩方法</strong>：用拇指按压对侧合谷穴</p>

<h3>2. 内关穴</h3>
<p><strong>位置</strong>：前臂掌侧，腕横纹上2寸</p>
<p><strong>功效</strong>：缓解心悸、失眠、胃痛</p>
<p><strong>按摩方法</strong>：用拇指按压，有酸麻感为宜</p>

<h3>3. 劳宫穴</h3>
<p><strong>位置</strong>：手掌心，握拳时中指尖处</p>
<p><strong>功效</strong>：清心火，安神定志</p>
<p><strong>按摩方法</strong>：用拇指按压另一手掌心</p>

<h2>三、下肢穴位</h2>

<h3>1. 足三里</h3>
<p><strong>位置</strong>：膝盖外侧凹陷下3寸</p>
<p><strong>功效</strong>：健脾和胃，增强免疫力</p>
<p><strong>按摩方法</strong>：用拇指按压，有酸胀感为宜</p>

<h3>2. 三阴交</h3>
<p><strong>位置</strong>：内踝尖上3寸，胫骨内侧缘后方</p>
<p><strong>功效</strong>：调理妇科病，改善失眠</p>
<p><strong>按摩方法</strong>：用拇指按压，女性经期避免按压</p>

<h3>3. 涌泉穴</h3>
<p><strong>位置</strong>：足底前1/3凹陷处</p>
<p><strong>功效</strong>：补肾益精，改善失眠</p>
<p><strong>按摩方法</strong>：睡前用手掌搓热涌泉穴</p>

<h2>四、腹部穴位</h2>

<h3>1. 中脘穴</h3>
<p><strong>位置</strong>：腹部正中线，脐上4寸</p>
<p><strong>功效</strong>：调理脾胃，改善消化不良</p>
<p><strong>按摩方法</strong>：用手掌顺时针按摩</p>

<h3>2. 关元穴</h3>
<p><strong>位置</strong>：腹部正中线，脐下3寸</p>
<p><strong>功效</strong>：补肾固精，改善疲劳</p>
<p><strong>按摩方法</strong>：用手掌轻轻按压</p>

<h2>五、穴位按摩注意事项</h2>

<ol>
<li><strong>力度适中</strong>：以有酸胀感为宜，避免过度用力</li>
<li><strong>持之以恒</strong>：每天坚持按摩才能见效</li>
<li><strong>避开伤口</strong>：皮肤破损处避免按摩</li>
<li><strong>特殊人群</strong>：孕妇、重病患者需在医生指导下进行</li>
<li><strong>最佳时间</strong>：早晨起床后、晚上睡前为佳</li>
</ol>

<hr>

<div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0;">
<p style="margin: 0; color: #666; font-size: 14px;">
<strong>温馨提示</strong>：穴位按摩是辅助保健方法，不能代替药物治疗。如有严重疾病，请及时就医。
</p>
</div>

<p style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
发布时间：{date} | 作者：{author} | 文章来源：中医娄伯恩微信公众号
</p>"""
        }
    }
    
    if topic in templates:
        template = templates[topic].copy()
        # 替换日期和作者
        current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
        template["content"] = template["content"].format(date=current_date, author=template["author"])
        return template
    else:
        # 返回默认模板
        default = templates["中医养生"].copy()
        current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
        default["content"] = default["content"].format(date=current_date, author=default["author"])
        return default

def save_article_to_file(article: Dict, filename: Optional[str] = None) -> str:
    """保存文章到文件"""
    if not filename:
        # 生成文件名
        title = article["title"].replace(" ", "_").replace("/", "_")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wechat_article_{title}_{timestamp}.md"
    
    # 创建Markdown格式
    gen_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 处理HTML内容转换为Markdown
    processed_content = article['content']
    processed_content = processed_content.replace('<h1>', '# ').replace('</h1>', '')
    processed_content = processed_content.replace('<h2>', '## ').replace('</h2>', '')
    processed_content = processed_content.replace('<h3>', '### ').replace('</h3>', '')
    processed_content = processed_content.replace('<p>', '').replace('</p>', '\n\n')
    processed_content = processed_content.replace('<ul>', '').replace('</ul>', '')
    processed_content = processed_content.replace('<li>', '* ').replace('</li>', '')
    processed_content = processed_content.replace('<ol>', '').replace('</ol>', '')
    processed_content = processed_content.replace('<strong>', '**').replace('</strong>', '**')
    processed_content = processed_content.replace('<em>', '*').replace('</em>', '*')
    processed_content = processed_content.replace('<hr>', '---')
    processed_content = processed_content.replace('<div style="', '').replace('</div>', '')
    processed_content = processed_content.replace('style="', '').replace('"', '')
    
    md_content = f"""# {article['title']}

**作者**: {article['author']}

**摘要**: {article['digest']}

---

{processed_content}

**生成时间**: {gen_time}
**文章类型**: 微信公众号文章
**目标公众号**: 中医娄伯恩
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    return filename

def save_html_article(article: Dict, filename: Optional[str] = None) -> str:
    """保存HTML格式文章"""
    if not filename:
        title = article["title"].replace(" ", "_").replace("/", "_")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wechat_article_{title}_{timestamp}.html"
    
    current_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .tip-box {{
            background-color: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #4CAF50;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .author {{
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        .digest {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <h1>{article['title']}</h1>
    
    <div class="author">
        <strong>作者</strong>: {article['author']}
    </div>
    
    <div class="digest">
        {article['digest']}
    </div>
    
    {article['content']}
    
    <div class="footer">
        <p>发布时间: {current_time}</p>
        <p>文章来源: 中医娄伯恩微信公众号</p>
        <p>© 2026 中医娄伯恩 版权所有</p>
    </div>
</body>
</html>'''
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return filename

def list_article_topics() -> List[str]:
    """列出可用的文章主题"""
    return ["中医养生", "中医食疗", "穴位保健"]

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号文章写作工具")
    parser.add_argument("--topic", choices=list_article_topics(), default="中医养生", help="文章主题")
    parser.add_argument("--list-topics", action="store_true", help="列出可用主题")
    parser.add_argument("--output-md", help="输出Markdown文件路径")
    parser.add_argument("--output-html", help="输出HTML文件路径")
    parser.add_argument("--preview", action="store_true", help="预览文章内容")
    
    args = parser.parse_args()
    
    if args.list_topics:
        print("可用文章主题:")
        for topic in list_article_topics():
            print(f"  - {topic}")
        return
    
    # 创建文章
    print(f"创建文章: {args.topic}")
    article = create_article_template(args.topic)
    
    # 预览
    if args.preview:
        print("\n" + "="*60)
        print(f"标题: {article['title']}")
        print(f"作者: {article['author']}")
        print(f"摘要: {article['digest']}")
        print("="*60)
        
        # 显示前500字符内容
        content_preview = article['content'].replace('<h1>', '\n# ').replace('</h1>', '\n')
        content_preview = content_preview.replace('<h2>', '\n## ').replace('</h2>', '\n')
        content_preview = content_preview.replace('<h3>', '\n### ').replace('</h3>', '\n')
        content_preview = content_preview.replace('<p>', '').replace('</p>', '\n')
        content_preview = content_preview[:500] + "..." if len(content_preview) > 500 else content_preview
        print(f"\n内容预览:\n{content_preview}")
        print("="*60)
    
    # 保存文件
    if args.output_md:
        md_file = save_article_to_file(article, args.output_md)
        print(f"✅ Markdown文件已保存: {md_file}")
    
    if args.output_html:
        html_file = save_html_article(article, args.output_html)
        print(f"✅ HTML文件已保存: {html_file}")
    
    if not args.output_md and not args.output_html and not args.preview:
        # 默认保存两种格式
        md_file = save_article_to_file(article)
        html_file = save_html_article(article)
        print(f"✅ 文章创建完成!")
        print(f"   Markdown文件: {md_file}")
        print(f"   HTML文件: {html_file}")
        print(f"\n📋 文章信息:")
        print(f"   标题: {article['title']} ({len(article['title'])}字符)")
        print(f"   作者: {article['author']} ({len(article['author'])}字符)")
        print(f"   摘要: {article['digest']} ({len(article['digest'])}字符)")
        print(f"   内容长度: {len(article['content'])}字符")
        
        # 检查限制
        print(f"\n🔍 微信公众号限制检查:")
        if len(article['title']) <= 64:
            print(f"   ✅ 标题长度符合要求 (≤64字符)")
        else:
            print(f"   ❌ 标题长度超出限制: {len(article['title'])} > 64")
        
        if len(article['digest']) <= 120:
            print(f"   ✅ 摘要长度符合要求 (≤120字符)")
        else:
            print(f"   ❌ 摘要长度超出限制: {len(article['digest'])} > 120")
        
        if len(article['author']) <= 8:
            print(f"   ✅ 作者长度符合要求 (≤8字符)")
        else:
            print(f"   ❌ 作者长度超出限制: {len(article['author'])} > 8")
        
        print(f"\n💡 使用建议:")
        print(f"   1. 登录微信公众平台 (https://mp.weixin.qq.com)")
        print(f"   2. 使用HTML文件内容创建文章")
        print(f"   3. 添加合适的封面图片")
        print(f"   4. 预览并发布")

if __name__ == "__main__":
    main()