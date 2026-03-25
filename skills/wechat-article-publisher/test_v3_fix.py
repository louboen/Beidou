#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 v3 修复版本 - 验证编码问题彻底解决
"""

import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

APPID = os.getenv('WECHAT_APPID')
APPSECRET = os.getenv('WECHAT_APPSECRET')

def get_access_token():
    """获取 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': APPID,
        'secret': APPSECRET
    }
    response = requests.get(url, params=params)
    result = response.json()
    if 'access_token' in result:
        return result['access_token']
    raise Exception(f"获取 access_token 失败：{result}")

def test_encoding_fix():
    """测试编码修复"""
    print("="*60)
    print("测试 v3 编码修复")
    print("="*60)
    
    # 测试数据
    test_title = "中医食疗养生方"
    test_content = "<p>这是一篇测试文章，包含中文：春季养生、食疗、穴位保健。</p>"
    
    # 🔧 正确方式
    print("\n✅ 正确方式 (ensure_ascii=False + data 参数):")
    data_correct = {
        "articles": [{
            "title": test_title,
            "content": test_content
        }]
    }
    json_correct = json.dumps(data_correct, ensure_ascii=False)
    print(f"  JSON: {json_correct[:100]}...")
    has_unicode = '\\u' in json_correct
    print(f"  包含 \\u: {'是' if has_unicode else '否'}")
    
    # ❌ 错误方式
    print("\n❌ 错误方式 (json 参数，默认 ensure_ascii=True):")
    data_wrong = {
        "articles": [{
            "title": test_title,
            "content": test_content
        }]
    }
    json_wrong = json.dumps(data_wrong, ensure_ascii=True)
    print(f"  JSON: {json_wrong[:100]}...")
    has_unicode_wrong = '\\u' in json_wrong
    print(f"  包含 \\u: {'是' if has_unicode_wrong else '否'}")
    
    print("\n" + "="*60)
    print("结论：必须使用 ensure_ascii=False")
    print("="*60)

def test_real_publish():
    """测试实际发布"""
    print("\n" + "="*60)
    print("测试实际发布")
    print("="*60)
    
    try:
        access_token = get_access_token()
        print("✅ access_token 获取成功")
        
        # 创建测试文章
        test_article = {
            "articles": [{
                "title": "v3 编码修复测试",
                "author": "娄医",
                "digest": "测试 ensure_ascii=False 修复效果",
                "content": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>v3 编码修复测试</title>
</head>
<body>
    <h1>🎉 v3 编码修复测试</h1>
    <p>这是一篇测试文章，用于验证编码修复是否生效。</p>
    <h2>测试内容</h2>
    <ul>
        <li>中医养生</li>
        <li>食疗保健</li>
        <li>穴位按摩</li>
    </ul>
    <p><strong>预期结果：</strong>所有中文正常显示，无 Unicode 转义字符。</p>
</body>
</html>
                """,
                "thumb_media_id": "",
                "show_cover_pic": 0
            }]
        }
        
        # 🔧 关键修复：使用 ensure_ascii=False + data 参数
        json_data = json.dumps(test_article, ensure_ascii=False)
        
        print(f"\n📤 发送数据:")
        print(f"  标题：'v3 编码修复测试'")
        has_unicode_data = '\\u' in json_data
        print(f"  包含 \\u: {'是' if has_unicode_data else '否'}")
        
        # 发送到微信
        url = "https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {'access_token': access_token}
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        
        print(f"\n🚀 发送请求...")
        response = requests.post(
            url,
            params=params,
            data=json_data.encode('utf-8'),  # 🔧 手动编码为 UTF-8
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        print(f"\n📊 发布结果：{json.dumps(result, ensure_ascii=False)}")
        
        if 'errcode' in result and result['errcode'] == 0:
            draft_id = result.get('media_id', '未知')
            print(f"\n🎉 发布成功!")
            print(f"🆔 草稿 ID: {draft_id}")
            print(f"\n请前往微信草稿箱检查显示效果：")
            print(f"https://mp.weixin.qq.com")
            return draft_id
        else:
            print(f"\n❌ 发布失败：{result}")
            return None
            
    except Exception as e:
        print(f"\n❌ 异常：{e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """主函数"""
    # 1. 测试编码
    test_encoding_fix()
    
    # 2. 测试发布
    draft_id = test_real_publish()
    
    if draft_id:
        print("\n" + "="*60)
        print("✅ 测试完成！")
        print("="*60)
        print(f"\n请检查微信草稿箱:")
        print(f"文章标题：v3 编码修复测试")
        print(f"草稿 ID: {draft_id}")
        print(f"\n确认事项:")
        print(f"1. 标题是否显示正常中文")
        print(f"2. 内容是否显示正常中文")
        print(f"3. 无 \\uXXXX 格式的乱码")

if __name__ == '__main__':
    main()
