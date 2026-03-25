#!/usr/bin/env python3
"""
创建最小化的微信公众号草稿
符合所有限制：
1. 标题：64字符以内
2. 摘要：120字符以内
3. 作者：8字符以内
4. 必须有封面图片
"""

import requests
import json
import sys

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
WECHAT_API_BASE = "https://api.weixin.qq.com"

# 永久图片 media_id（从之前测试获取）
PERMANENT_IMAGE_MEDIA_ID = "K03y2eZTmx34znaim3BBR05xm8XZ3Lek78z_tzFm6n_AK8a61hRKxD1DC3V62CRH"

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

def create_minimal_draft(access_token, thumb_media_id):
    """创建最小化的草稿（符合所有限制）"""
    print("创建最小化草稿...")
    
    # 最小化的内容
    short_title = "测试"  # 2字符
    short_author = "测试"  # 2字符
    short_digest = "测试文章"  # 4字符
    
    print(f"标题: '{short_title}' ({len(short_title)}字符)")
    print(f"作者: '{short_author}' ({len(short_author)}字符)")
    print(f"摘要: '{short_digest}' ({len(short_digest)}字符)")
    
    # 最简单的文章内容
    article = {
        "title": short_title,
        "author": short_author,
        "digest": short_digest,
        "content": "<p>测试内容</p>",
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
        "show_cover_pic": 1  # 显示封面图片
    }
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [article]
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
            print(f"   错误代码: {result.get('errcode', '未知')}")
            print(f"   错误信息: {result.get('errmsg', '未知')}")
            
            # 分析常见错误
            error_analysis = {
                45003: "标题长度超出限制（64字符以内）",
                45004: "摘要长度超出限制（120字符以内）",
                45110: "作者长度超出限制（8字符以内）",
                40007: "封面图片 media_id 无效",
                40001: "access_token 无效或已过期",
                40002: "API 权限不足"
            }
            
            errcode = result.get('errcode')
            if errcode in error_analysis:
                print(f"   💡 分析: {error_analysis[errcode]}")
            
            return False
            
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_actual_draft(access_token, thumb_media_id):
    """创建实际可用的草稿"""
    print("创建实际草稿...")
    
    # 实际可用的内容
    title = "春季养肝指南"  # 6字符
    author = "娄医生"  # 3字符
    digest = "春季养肝正当时，中医养生小贴士。"  # 15字符
    
    print(f"标题: '{title}' ({len(title)}字符)")
    print(f"作者: '{author}' ({len(author)}字符)")
    print(f"摘要: '{digest}' ({len(digest)}字符)")
    
    # 实际的文章内容
    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": """
            <h1>春季养肝指南</h1>
            
            <p>春季是养肝的最佳时机，中医认为肝主疏泄，喜条达而恶抑郁。</p>
            
            <h2>养生要点</h2>
            <ul>
                <li>多吃绿色蔬菜</li>
                <li>早睡早起</li>
                <li>保持心情舒畅</li>
            </ul>
            
            <h2>养生食谱</h2>
            <h3>枸杞菊花茶</h3>
            <p>枸杞10克，菊花5克，沸水冲泡。</p>
            
            <p style="color: #666; font-size: 14px;">
                发布时间：2026年3月18日
            </p>
        """,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
        "show_cover_pic": 1  # 显示封面图片
    }
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [article]
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
                print(f"  {i}. {item.get('title', '无标题')}")
                print(f"     媒体 ID: {item.get('media_id', '未知')}")
                print(f"     更新时间: {item.get('update_time', '未知')}")
                if i < len(result["item"]):
                    print()
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
    print("微信公众号最小化草稿创建测试")
    print(f"封面图片 media_id: {PERMANENT_IMAGE_MEDIA_ID[:30]}...")
    print("=" * 60)
    
    # 获取 access_token
    print("1. 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        sys.exit(1)
    
    print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
    
    # 先查看现有草稿
    print("\n2. 查看现有草稿...")
    existing_drafts = get_draft_list(access_token)
    
    # 创建最小化草稿
    print("\n3. 创建最小化草稿...")
    media_id = create_minimal_draft(access_token, PERMANENT_IMAGE_MEDIA_ID)
    
    if media_id:
        # 等待一下让服务器处理
        import time
        print("\n等待3秒让服务器处理...")
        time.sleep(3)
        
        # 再次查看草稿列表确认
        print("\n4. 验证草稿创建...")
        new_drafts = get_draft_list(access_token)
        
        if new_drafts:
            new_count = len(new_drafts) - len(existing_drafts) if existing_drafts else len(new_drafts)
            if new_count > 0:
                print(f"\n✅ 最小化测试完成! 成功创建 {new_count} 篇草稿。")
                
                # 尝试创建实际草稿
                print("\n5. 创建实际草稿...")
                actual_media_id = create_actual_draft(access_token, PERMANENT_IMAGE_MEDIA_ID)
                
                if actual_media_id:
                    print(f"\n✅ 实际草稿创建成功!")
                    print(f"   请登录微信公众平台查看草稿箱。")
                else:
                    print(f"\n⚠️  实际草稿创建失败，但最小化测试成功。")
            else:
                print(f"\n⚠️  草稿可能创建成功，但未在列表中显示。")
        else:
            print(f"\n⚠️  无法获取草稿列表，但创建请求可能已成功。")
    else:
        print(f"\n❌ 最小化草稿创建失败。")
        print(f"   可能原因:")
        print(f"   1. media_id 无效或已过期")
        print(f"   2. API 权限限制")
        print(f"   3. 微信公众号配置问题")
        
        print(f"\n💡 建议:")
        print(f"   1. 检查 media_id 是否有效（可能已过期）")
        print(f"   2. 重新上传图片获取新的 media_id")
        print(f"   3. 检查微信公众号API权限设置")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    # 提供后续步骤
    print("\n🎯 后续步骤:")
    print("1. 登录微信公众平台 (https://mp.weixin.qq.com)")
    print("2. 进入'内容与互动' -> '草稿箱'")
    print("3. 查看测试文章")
    print("4. 检查API权限设置")
    print("5. 如有问题，重新上传图片获取新的 media_id")

if __name__ == "__main__":
    main()