#!/usr/bin/env python3
"""
测试简单文章发布，排除编码问题
"""

import requests
import json
import os
from pathlib import Path

def load_config():
    """加载配置"""
    env_path = Path('.env')
    config = {}
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"').strip("'")
    return config

def get_access_token(appid, appsecret):
    """获取 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': appid,
        'secret': appsecret
    }
    
    response = requests.get(url, params=params, timeout=10)
    return response.json()

def create_simple_html_content():
    """创建简单的 HTML 内容"""
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>简单测试</title>
</head>
<body>
    <h1>中医食疗养生方测试</h1>
    <p>这是一篇测试文章，检查中文显示是否正常。</p>
    <p>中医食疗养生方：药食同源，食物不仅可以充饥，还能调理身体。</p>
    <h2>食疗原则</h2>
    <ul>
        <li>因人制宜：寒性体质多吃温性食物</li>
        <li>因时制宜：春季养肝，多吃绿色蔬菜</li>
        <li>因地制宜：根据地域特点选择食物</li>
    </ul>
    <p>作者：娄医</p>
</body>
</html>"""

def test_draft_with_simple_content():
    """测试简单内容发布"""
    print("=" * 60)
    print("简单文章发布测试")
    print("=" * 60)
    
    # 1. 加载配置
    config = load_config()
    appid = config.get('WECHAT_APPID')
    appsecret = config.get('WECHAT_APPSECRET')
    
    if not appid or not appsecret:
        print("❌ 配置不完整")
        return
    
    print(f"🔑 AppID: {appid}")
    
    # 2. 获取 access_token
    print("\n1️⃣ 获取 access_token...")
    token_result = get_access_token(appid, appsecret)
    
    if 'access_token' in token_result:
        access_token = token_result['access_token']
        print(f"✅ access_token 获取成功: {access_token[:20]}...")
    else:
        print(f"❌ 获取失败: {token_result}")
        return
    
    # 3. 测试不同标题长度
    test_cases = [
        {
            'title': '测试',
            'author': '娄医',
            'description': '最短标题'
        },
        {
            'title': '中医食疗',
            'author': '娄医',
            'description': '4字标题'
        },
        {
            'title': '中医食疗养生方',
            'author': '娄医',
            'description': '7字标题'
        },
        {
            'title': '春季中医养生指南与食疗方案',
            'author': '娄医',
            'description': '长标题'
        },
        {
            'title': '中医食疗养生方：药食同源的健康之道与实践方法指南',
            'author': '娄医',
            'description': '超长标题'
        }
    ]
    
    # 4. 创建简单内容
    simple_content = create_simple_html_content()
    print(f"\n📄 测试内容长度: {len(simple_content)} 字符")
    print(f"📋 内容预览: {simple_content[:100]}...")
    
    # 5. 测试每个标题
    print("\n2️⃣ 测试不同标题长度...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试 {i}: {test_case['description']}")
        print(f"📝 标题: {test_case['title']}")
        print(f"📏 标题长度: {len(test_case['title'])} 字符")
        
        # 准备请求
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {'access_token': access_token}
        
        article = {
            'title': test_case['title'],
            'author': test_case['author'],
            'digest': f'{test_case["title"][:30]}...' if len(test_case['title']) > 30 else test_case['title'],
            'content': simple_content,
            'content_source_url': '',
            'thumb_media_id': '',  # 不使用封面
            'need_open_comment': 0,
            'only_fans_can_comment': 0
        }
        
        data = {'articles': [article]}
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            result = response.json()
            
            print(f"📊 结果: {json.dumps(result, ensure_ascii=False)}")
            
            if 'media_id' in result:
                print(f"✅ 发布成功!")
                print(f"🆔 草稿ID: {result['media_id'][:30]}...")
            else:
                print(f"❌ 发布失败")
                
                # 分析错误
                errcode = result.get('errcode')
                errmsg = result.get('errmsg', '')
                
                print(f"🔍 错误分析:")
                print(f"  错误代码: {errcode}")
                print(f"  错误信息: {errmsg}")
                
                if errcode == 45003:
                    print(f"  💡 标题长度限制: 可能超过64字符或字节限制")
                    print(f"  📏 当前标题字节数: {len(test_case['title'].encode('utf-8'))} 字节")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        # 避免频率限制
        if i < len(test_cases):
            print("⏳ 等待2秒...")
            import time
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

def check_actual_article():
    """检查实际文章的问题"""
    print("\n🔍 检查实际文章...")
    
    article_file = 'articles/auto_中医食疗_养生食谱.html'
    
    if os.path.exists(article_file):
        with open(article_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 文章: {article_file}")
        print(f"📏 文件大小: {len(content)} 字符")
        print(f"📊 字节大小: {len(content.encode('utf-8'))} 字节")
        
        # 检查标题
        import re
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            title = title_match.group(1)
            print(f"📝 HTML 标题: {title}")
            print(f"📏 标题长度: {len(title)} 字符")
            print(f"📊 标题字节: {len(title.encode('utf-8'))} 字节")
        
        # 检查前200字符
        print(f"\n📋 内容前200字符:")
        print("-" * 40)
        print(content[:200])
        print("-" * 40)
        
        # 检查是否有特殊字符
        print(f"\n🔤 字符检查:")
        for i, char in enumerate(content[:100]):
            if ord(char) > 127:  # 非ASCII字符
                print(f"  位置 {i}: '{char}' (U+{ord(char):04X})")
    
    else:
        print(f"❌ 文章文件不存在: {article_file}")

def main():
    """主函数"""
    print("🚀 简单文章发布测试")
    print()
    
    # 测试简单内容
    test_draft_with_simple_content()
    
    # 检查实际文章
    check_actual_article()
    
    print("\n💡 建议:")
    print("1. 使用简单标题测试")
    print("2. 检查文章内容编码")
    print("3. 逐步增加复杂度")
    print("4. 验证每个步骤")

if __name__ == "__main__":
    main()