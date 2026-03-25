#!/usr/bin/env python3
"""
创建微信公众号测试草稿
"""

import requests
import json
import sys

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
WECHAT_API_BASE = "https://api.weixin.qq.com"

def get_access_token():
    """获取 access_token"""
    url = f"{WECHAT_API_BASE}/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "access_token" in data:
            return data["access_token"]
        else:
            print(f"❌ access_token 获取失败: {data}")
            return None
            
    except Exception as e:
        print(f"❌ 获取 access_token 时出错: {e}")
        return None

def create_test_draft(access_token):
    """创建测试草稿"""
    print("创建测试草稿...")
    
    # 测试文章内容
    test_article = {
        "title": "OpenClaw 微信公众号发布测试",
        "author": "中医娄伯恩",
        "digest": "这是通过 OpenClaw AI 助手自动发布的测试文章，验证微信公众号 API 集成功能。",
        "content": """
            <h1>OpenClaw 微信公众号发布测试</h1>
            
            <p>这是一篇通过 <strong>OpenClaw AI 助手</strong> 自动发布的测试文章。</p>
            
            <h2>测试目的</h2>
            <ul>
                <li>验证微信公众号 API 集成功能</li>
                <li>测试自动发布流程</li>
                <li>确认草稿创建权限</li>
            </ul>
            
            <h2>技术架构</h2>
            <p>使用微信公众号官方 API，通过 AppID 和 AppSecret 进行认证。</p>
            
            <h2>发布时间</h2>
            <p>2026年3月18日 14:10</p>
            
            <h2>发布工具</h2>
            <p>OpenClaw AI 助手 + 微信公众号发布技能</p>
            
            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                注意：此文章仅用于测试目的，将在测试完成后删除。
            </p>
        """,
        "content_source_url": "https://openclaw.ai",
        "thumb_media_id": "",  # 如果没有封面图片，留空
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [test_article]
    }
    
    try:
        print("发送创建草稿请求...")
        response = requests.post(url, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "media_id" in result:
            print(f"\n✅ 草稿创建成功!")
            print(f"   媒体 ID: {result['media_id']}")
            return result["media_id"]
        elif "errcode" in result and result["errcode"] == 0:
            print(f"\n✅ 草稿创建成功!")
            if "media_id" in result:
                print(f"   媒体 ID: {result['media_id']}")
            return True
        else:
            print(f"\n❌ 草稿创建失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_draft_list(access_token):
    """获取草稿列表"""
    print("\n获取草稿列表...")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/batchget"
    params = {"access_token": access_token}
    
    data = {
        "offset": 0,
        "count": 10,
        "no_content": 1  # 不返回内容，只返回基本信息
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "item" in result:
            print(f"✅ 获取到 {len(result['item'])} 篇草稿:")
            for i, item in enumerate(result["item"], 1):
                print(f"  {i}. {item.get('title', '无标题')} (ID: {item.get('media_id', '未知')})")
            return result["item"]
        else:
            print(f"❌ 获取草稿列表失败: {result}")
            return []
            
    except Exception as e:
        print(f"❌ 获取草稿列表时出错: {e}")
        return []

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号草稿创建测试")
    print("=" * 60)
    
    # 获取 access_token
    print("1. 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        sys.exit(1)
    
    print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
    
    # 先查看现有草稿
    get_draft_list(access_token)
    
    # 创建测试草稿
    print("\n2. 创建测试草稿...")
    media_id = create_test_draft(access_token)
    
    if media_id:
        # 再次查看草稿列表确认
        print("\n3. 验证草稿创建...")
        drafts = get_draft_list(access_token)
        
        if drafts:
            print(f"\n✅ 测试完成! 草稿已成功创建到微信公众号。")
            print(f"   请登录微信公众平台查看草稿箱。")
        else:
            print(f"\n⚠️  草稿可能创建成功，但获取列表失败。")
            print(f"   请登录微信公众平台查看草稿箱确认。")
    else:
        print(f"\n❌ 草稿创建失败。")
        print(f"   可能原因:")
        print(f"   1. API 权限不足")
        print(f"   2. 内容格式不符合要求")
        print(f"   3. 网络或服务器问题")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()