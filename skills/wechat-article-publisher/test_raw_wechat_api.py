#!/usr/bin/env python3
"""
直接测试微信 API 的编码行为
发送原始数据，查看微信如何存储和返回
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

def test_different_encodings(access_token):
    """测试不同的编码方式"""
    print("🎯 测试不同的编码方式...")
    
    test_cases = [
        {
            'name': '纯UTF-8中文',
            'title': '测试文章',
            'content': '<p>这是一篇测试文章。</p>',
            'expected': '纯中文'
        },
        {
            'name': 'Unicode转义中文',
            'title': '测试文章',
            'content': r'<p>\u8fd9\u662f\u4e00\u7bc7\u6d4b\u8bd5\u6587\u7ae0\u3002</p>',
            'expected': 'Unicode转义'
        },
        {
            'name': '混合编码',
            'title': '测试文章',
            'content': r'<p>正常中文 \u548c Unicode\u8f6c\u4e49</p>',
            'expected': '混合'
        },
        {
            'name': 'HTML实体',
            'title': '测试文章',
            'content': '<p>这是一篇测试文章&amp;包含&amp;HTML实体。</p>',
            'expected': 'HTML实体'
        }
    ]
    
    for test in test_cases:
        print(f"\n📋 测试: {test['name']} ({test['expected']})")
        print(f"📝 内容: {repr(test['content'][:50])}...")
        
        # 创建草稿
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {'access_token': access_token}
        
        article = {
            'title': test['title'],
            'author': '测试',
            'digest': test['title'],
            'content': test['content'],
            'content_source_url': '',
            'thumb_media_id': '',  # 可能有问题，但用于测试
            'need_open_comment': 0,
            'only_fans_can_comment': 0
        }
        
        data = {'articles': [article]}
        
        try:
            # 发送原始 JSON
            json_str = json.dumps(data, ensure_ascii=False)
            print(f"📤 发送的JSON (前100字符): {json_str[:100]}...")
            print(f"📊 JSON长度: {len(json_str)} 字符")
            contains_unicode = '是' if '\\u' in json_str else '否'
            print(f"🔤 是否包含 \\u: {contains_unicode}")
            
            response = requests.post(url, params=params, json=data, timeout=30)
            result = response.json()
            
            print(f"📊 结果: {json.dumps(result, ensure_ascii=False)}")
            
            if 'media_id' in result:
                print(f"✅ 创建成功，草稿ID: {result['media_id'][:30]}...")
                
                # 立即获取并检查
                check_draft_content(access_token, result['media_id'])
            else:
                print(f"❌ 创建失败")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")

def check_draft_content(access_token, draft_media_id):
    """检查草稿内容"""
    print(f"  🔍 检查草稿内容...")
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get"
    params = {'access_token': access_token}
    data = {'media_id': draft_media_id}
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        if 'news_item' in result:
            article = result['news_item'][0]
            
            print(f"  📋 微信返回:")
            print(f"    标题: {repr(article.get('title', ''))}")
            print(f"    作者: {repr(article.get('author', ''))}")
            
            content = article.get('content', '')
            print(f"    内容前100字符: {repr(content[:100])}")
            
            # 分析编码
            analyze_content_encoding(content)
            
        else:
            print(f"  ❌ 无法获取草稿内容")
            
    except Exception as e:
        print(f"  ❌ 检查失败: {e}")

def analyze_content_encoding(content):
    """分析内容编码"""
    import re
    
    # 检查 Unicode 转义
    unicode_pattern = r'\\u[0-9a-fA-F]{4}'
    unicode_matches = re.findall(unicode_pattern, content[:500])
    
    # 检查 HTML 实体
    html_entity_pattern = r'&[a-zA-Z]+;'
    html_matches = re.findall(html_entity_pattern, content[:500])
    
    print(f"  🔤 编码分析:")
    print(f"    Unicode转义数量: {len(unicode_matches)}")
    print(f"    HTML实体数量: {len(html_matches)}")
    
    if unicode_matches:
        print(f"    Unicode示例: {unicode_matches[:3]}")
        # 尝试解码
        try:
            decoded = unicode_matches[0].encode('latin-1').decode('unicode_escape')
            print(f"    解码示例: {unicode_matches[0]} → '{decoded}'")
        except:
            print(f"    无法解码示例")
    
    # 检查是否包含中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content[:200])
    print(f"    中文字符数量: {len(chinese_chars)}")
    
    if chinese_chars:
        print(f"    中文示例: {chinese_chars[:5]}")

def test_with_ensure_ascii(access_token):
    """测试 ensure_ascii 参数的影响"""
    print("\n🔧 测试 ensure_ascii 参数...")
    
    test_content = '<p>这是一篇测试文章。</p>'
    
    # 测试 ensure_ascii=True (默认)
    data_true = {'articles': [{
        'title': '测试标题',
        'author': '测试',
        'digest': '测试',
        'content': test_content,
        'content_source_url': '',
        'thumb_media_id': '',
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }]}
    
    json_true = json.dumps(data_true, ensure_ascii=True)
    json_false = json.dumps(data_true, ensure_ascii=False)
    
    print(f"📊 ensure_ascii=True 的JSON (前100字符):")
    print(f"  {json_true[:100]}...")
    print(f"  长度: {len(json_true)} 字符")
    contains_unicode_true = '是' if '\\u' in json_true else '否'
    print(f"  包含 \\u: {contains_unicode_true}")
    
    print(f"\n📊 ensure_ascii=False 的JSON (前100字符):")
    print(f"  {json_false[:100]}...")
    print(f"  长度: {len(json_false)} 字符")
    contains_unicode_false = '是' if '\\u' in json_false else '否'
    print(f"  包含 \\u: {contains_unicode_false}")
    
    # 测试发送 ensure_ascii=False
    print(f"\n🎯 测试发送 ensure_ascii=False 的JSON...")
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {'access_token': access_token}
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    try:
        response = requests.post(
            url, 
            params=params, 
            data=json_false.encode('utf-8'),
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        print(f"📊 结果: {json.dumps(result, ensure_ascii=False)}")
        
        if 'media_id' in result:
            print(f"✅ 创建成功，草稿ID: {result['media_id'][:30]}...")
            check_draft_content(access_token, result['media_id'])
        else:
            print(f"❌ 创建失败")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("微信 API 编码行为测试")
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
    
    # 3. 测试不同的编码方式
    test_different_encodings(access_token)
    
    # 4. 测试 ensure_ascii 参数
    test_with_ensure_ascii(access_token)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n💡 关键发现:")
    print("1. requests 的 json 参数默认使用 ensure_ascii=True")
    print("2. 这会导致中文被转换为 Unicode 转义")
    print("3. 微信 API 可能直接存储了这些转义字符")
    print("4. 微信前端可能无法正确解码")
    print("\n🔧 解决方案:")
    print("1. 使用 ensure_ascii=False")
    print("2. 或者手动编码 JSON 字符串")
    print("3. 设置正确的 Content-Type 头")

if __name__ == "__main__":
    main()