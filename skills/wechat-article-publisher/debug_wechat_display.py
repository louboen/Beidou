#!/usr/bin/env python3
"""
调试微信文章显示问题
分析为什么文章在微信平台显示为乱码
"""

import requests
import json
import re
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

def analyze_unicode_escape(text):
    """分析 Unicode 转义字符"""
    print("🔍 分析 Unicode 转义字符...")
    
    # 用户提供的乱码示例
    user_example = r"\u4e2d\u533b\u517b\u751f\u6d4b\u8bd5\u6587\u7ae0"
    print(f"用户示例: {user_example}")
    
    # 解码示例
    try:
        decoded = user_example.encode('ascii').decode('unicode_escape')
        print(f"解码后: {decoded}")
        print(f"字符数: {len(decoded)}")
    except Exception as e:
        print(f"解码失败: {e}")
    
    # 分析文本中的 Unicode 转义
    unicode_pattern = r'\\u[0-9a-fA-F]{4}'
    matches = re.findall(unicode_pattern, text)
    
    if matches:
        print(f"\n📊 在文本中发现 {len(matches)} 个 Unicode 转义字符")
        print("📋 前10个示例:")
        for i, match in enumerate(matches[:10]):
            try:
                decoded = match.encode('ascii').decode('unicode_escape')
                print(f"  {match} → '{decoded}'")
            except:
                print(f"  {match} → 解码失败")
    else:
        print("✅ 文本中没有发现 Unicode 转义字符")
    
    return matches

def test_content_encoding():
    """测试内容编码"""
    print("\n🔤 测试不同编码方式...")
    
    test_string = "中医养生测试文章"
    print(f"测试字符串: {test_string}")
    
    # 1. UTF-8 编码
    utf8_bytes = test_string.encode('utf-8')
    print(f"UTF-8 字节: {utf8_bytes}")
    print(f"UTF-8 十六进制: {utf8_bytes.hex()}")
    
    # 2. Unicode 转义
    unicode_escape = test_string.encode('unicode_escape').decode('ascii')
    print(f"Unicode 转义: {unicode_escape}")
    
    # 3. 尝试解码
    try:
        decoded = unicode_escape.encode('ascii').decode('unicode_escape')
        print(f"解码回: {decoded}")
        print(f"✅ 编码/解码成功")
    except Exception as e:
        print(f"❌ 解码失败: {e}")
    
    # 4. 测试微信可能的问题
    print("\n🔧 测试微信可能的问题...")
    
    # 模拟微信 API 可能的行为
    test_cases = [
        test_string,  # 原始字符串
        unicode_escape,  # Unicode 转义
        json.dumps(test_string),  # JSON 编码（带引号）
        json.dumps(test_string)[1:-1],  # JSON 编码（不带引号）
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}:")
        print(f"  输入: {repr(case)}")
        print(f"  长度: {len(case)} 字符")
        print(f"  字节: {len(case.encode('utf-8'))} 字节")
        
        # 检查是否包含 Unicode 转义
        if r'\u' in case:
            print(f"  ⚠️  包含 Unicode 转义字符")
            try:
                # 尝试解码
                if case.startswith('"') and case.endswith('"'):
                    decoded = json.loads(case)
                else:
                    decoded = case.encode('ascii').decode('unicode_escape')
                print(f"  可解码为: {decoded}")
            except:
                print(f"  ❌ 无法解码")

def check_draft_content(access_token, draft_media_id):
    """检查草稿内容"""
    print(f"\n📄 检查草稿内容: {draft_media_id[:30]}...")
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get"
    params = {'access_token': access_token}
    data = {'media_id': draft_media_id}
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        if 'news_item' in result:
            articles = result['news_item']
            print(f"📊 找到 {len(articles)} 篇文章")
            
            for i, article in enumerate(articles, 1):
                print(f"\n文章 {i}:")
                print(f"  标题: {article.get('title', 'N/A')}")
                print(f"  作者: {article.get('author', 'N/A')}")
                
                # 检查内容
                content = article.get('content', '')
                print(f"  内容长度: {len(content)} 字符")
                
                # 检查前200字符
                preview = content[:200].replace('\n', ' ')
                print(f"  内容预览: {preview}...")
                
                # 分析编码
                analyze_unicode_escape(content[:500])
                
        else:
            print(f"❌ 无法获取草稿内容: {result}")
            
    except Exception as e:
        print(f"❌ 检查草稿失败: {e}")

def create_test_draft_with_different_encodings(access_token):
    """使用不同编码创建测试草稿"""
    print("\n🎯 使用不同编码创建测试草稿...")
    
    test_contents = [
        {
            'name': '纯中文',
            'title': '测试文章1',
            'content': '<p>这是一篇纯中文测试文章。</p><p>中医养生测试。</p>'
        },
        {
            'name': '包含Unicode转义',
            'title': '测试文章2', 
            'content': r'<p>\u8fd9\u662f\u4e00\u7bc7\u5305\u542bUnicode\u8f6c\u4e49\u7684\u6d4b\u8bd5\u6587\u7ae0\u3002</p>'
        },
        {
            'name': 'JSON编码中文',
            'title': '测试文章3',
            'content': json.dumps('<p>这是一篇JSON编码的中文测试文章。</p>')[1:-1]
        }
    ]
    
    for test in test_contents:
        print(f"\n📋 测试: {test['name']}")
        print(f"📝 标题: {test['title']}")
        print(f"📄 内容: {test['content'][:100]}...")
        
        # 分析内容
        analyze_unicode_escape(test['content'])
        
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
            response = requests.post(url, params=params, json=data, timeout=30)
            result = response.json()
            
            print(f"📊 结果: {json.dumps(result, ensure_ascii=False)}")
            
            if 'media_id' in result:
                print(f"✅ 创建成功，草稿ID: {result['media_id'][:30]}...")
                # 立即检查内容
                check_draft_content(access_token, result['media_id'])
            else:
                print(f"❌ 创建失败")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("微信文章显示问题调试工具")
    print("=" * 60)
    
    # 1. 分析用户提供的乱码
    user_provided = r"\u4e2d\u533b\u517b\u751f\u6d4b\u8bd5\u6587\u7ae0\n\u8fd9\u662f\u4e00\u7bc7\u6d4b\u8bd5\u6587\u7ae0\uff0c\u9a8c\u8bc1\u4e2d\u6587\u663e\u793a\u662f\u5426\u6b63\u5e38\u3002\n\n\u4e2d\u533b\u8ba4\u4e3a\uff1a\u836f\u98df\u540c\u6e90\uff0c\u517b\u751f\u4e4b\u9053\u5728\u4e8e\u5e73\u8861\u3002"
    
    print("📋 用户提供的乱码内容:")
    print("-" * 40)
    print(user_provided)
    print("-" * 40)
    
    analyze_unicode_escape(user_provided)
    
    # 2. 测试编码
    test_content_encoding()
    
    # 3. 加载配置
    config = load_config()
    appid = config.get('WECHAT_APPID')
    appsecret = config.get('WECHAT_APPSECRET')
    
    if not appid or not appsecret:
        print("\n❌ 配置不完整，跳过 API 测试")
        return
    
    print(f"\n🔑 AppID: {appid}")
    
    # 4. 获取 access_token
    print("\n1️⃣ 获取 access_token...")
    token_result = get_access_token(appid, appsecret)
    
    if 'access_token' in token_result:
        access_token = token_result['access_token']
        print(f"✅ access_token 获取成功: {access_token[:20]}...")
    else:
        print(f"❌ 获取失败: {token_result}")
        return
    
    # 5. 检查之前创建的草稿
    print("\n2️⃣ 检查之前创建的草稿...")
    
    # 之前成功的草稿ID
    previous_drafts = [
        'K03y2eZTmx34znaim3BBR-FwWeDQIjrQ4Nj9QvltDm4gM97X0JiVJB7sRpst5XtD',  # 修复后文章
        'K03y2eZTmx34znaim3BBR4TY5gcsqko8i7jbdkf9XLK_DSkl4Nfl42LSH8xFQsKt',  # 简单测试文章
    ]
    
    for draft_id in previous_drafts:
        check_draft_content(access_token, draft_id)
    
    # 6. 创建不同编码的测试草稿
    print("\n3️⃣ 创建不同编码的测试草稿...")
    create_test_draft_with_different_encodings(access_token)
    
    print("\n" + "=" * 60)
    print("调试完成")
    print("=" * 60)
    
    print("\n💡 分析结论:")
    print("1. 用户看到的是 Unicode 转义字符，不是乱码")
    print("2. 这些字符可以正确解码为中文")
    print("3. 问题可能是微信平台的显示问题")
    print("4. 或者是我们发送的数据格式有问题")
    print("\n🔧 建议:")
    print("1. 检查微信草稿箱的实际显示")
    print("2. 尝试不同的内容格式")
    print("3. 验证微信 API 的编码要求")

if __name__ == "__main__":
    main()