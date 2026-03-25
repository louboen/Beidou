#!/usr/bin/env python3
"""
微信公众号文章发布工具
尝试使用已有图片或创建无封面图片的草稿
"""

import requests
import json
import sys
import os
from typing import Optional, Dict, List

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
WECHAT_API_BASE = "https://api.weixin.qq.com"

def get_access_token() -> Optional[str]:
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

def get_existing_images(access_token: str, count: int = 10) -> List[Dict]:
    """获取已有的图片素材"""
    print(f"获取已有的图片素材 (最多{count}张)...")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/material/batchget_material"
    params = {"access_token": access_token}
    
    data = {
        "type": "image",
        "offset": 0,
        "count": count
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "item" in result:
            images = []
            for item in result["item"]:
                images.append({
                    "media_id": item.get("media_id"),
                    "name": item.get("name", "未命名"),
                    "update_time": item.get("update_time"),
                    "url": item.get("url")
                })
            print(f"✅ 获取到 {len(images)} 张图片")
            return images
        else:
            print(f"❌ 获取图片素材失败: {result}")
            return []
            
    except Exception as e:
        print(f"❌ 获取图片素材时出错: {e}")
        return []

def create_draft_without_cover(access_token: str, article: Dict) -> Optional[str]:
    """创建无封面图片的草稿（尝试）"""
    print("尝试创建无封面图片的草稿...")
    
    # 尝试不提供 thumb_media_id
    article_without_cover = article.copy()
    if "thumb_media_id" in article_without_cover:
        del article_without_cover["thumb_media_id"]
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [article_without_cover]
    }
    
    try:
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
            return None
            
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        return None

def create_draft_with_existing_image(access_token: str, article: Dict, image_media_id: str) -> Optional[str]:
    """使用已有图片创建草稿"""
    print(f"使用已有图片创建草稿 (media_id: {image_media_id[:30]}...)")
    
    article_with_cover = article.copy()
    article_with_cover["thumb_media_id"] = image_media_id
    article_with_cover["show_cover_pic"] = 1
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [article_with_cover]
    }
    
    try:
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
            return None
            
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        return None

def create_test_article() -> Dict:
    """创建测试文章"""
    return {
        "title": "测试文章",
        "author": "测试",
        "digest": "测试摘要",
        "content": "<p>测试内容</p>",
        "content_source_url": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }

def create_actual_article() -> Dict:
    """创建实际文章"""
    return {
        "title": "春季中医养生",
        "author": "娄医生",
        "digest": "春季养生正当时，中医养生指南。",
        "content": """
            <h1>春季中医养生</h1>
            
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
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号文章发布工具")
    print("=" * 60)
    
    # 获取 access_token
    print("1. 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        sys.exit(1)
    
    print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
    
    # 获取已有图片
    print("\n2. 获取已有图片素材...")
    existing_images = get_existing_images(access_token, 5)
    
    if existing_images:
        print(f"\n📷 可用图片:")
        for i, img in enumerate(existing_images, 1):
            print(f"  {i}. {img['name']}")
            print(f"     media_id: {img['media_id'][:30]}...")
            print(f"     更新时间: {img.get('update_time', '未知')}")
            if i < len(existing_images):
                print()
    
    # 创建测试文章
    print("\n3. 创建测试文章...")
    test_article = create_test_article()
    
    # 尝试无封面图片
    print("\n4. 尝试无封面图片创建草稿...")
    draft_id = create_draft_without_cover(access_token, test_article)
    
    if draft_id:
        print(f"\n✅ 成功创建无封面图片的草稿!")
        print(f"   草稿 ID: {draft_id}")
    else:
        print(f"\n❌ 无封面图片创建失败，尝试使用已有图片...")
        
        if existing_images:
            # 使用第一张图片
            first_image = existing_images[0]
            print(f"\n5. 使用已有图片创建草稿: {first_image['name']}")
            draft_id = create_draft_with_existing_image(access_token, test_article, first_image["media_id"])
            
            if draft_id:
                print(f"\n✅ 成功使用已有图片创建草稿!")
                print(f"   草稿 ID: {draft_id}")
                print(f"   使用图片: {first_image['name']}")
            else:
                print(f"\n❌ 使用已有图片创建也失败。")
                print(f"   可能原因:")
                print(f"   1. 图片格式不符合封面要求")
                print(f"   2. API 权限限制")
                print(f"   3. 微信公众号配置问题")
        else:
            print(f"\n❌ 没有可用的图片素材。")
            print(f"   建议:")
            print(f"   1. 登录微信公众平台上传合适的封面图片")
            print(f"   2. 图片尺寸: 900x500 像素")
            print(f"   3. 图片格式: JPG/PNG")
            print(f"   4. 文件大小: 不超过 2MB")
    
    # 如果测试成功，创建实际文章
    if draft_id:
        print("\n6. 创建实际中医养生文章...")
        actual_article = create_actual_article()
        
        if existing_images:
            # 使用第一张图片
            first_image = existing_images[0]
            actual_draft_id = create_draft_with_existing_image(access_token, actual_article, first_image["media_id"])
            
            if actual_draft_id:
                print(f"\n✅ 中医养生文章创建成功!")
                print(f"   草稿 ID: {actual_draft_id}")
                print(f"   文章标题: {actual_article['title']}")
                print(f"   使用图片: {first_image['name']}")
            else:
                print(f"\n⚠️  中医养生文章创建失败，但测试文章成功。")
        else:
            print(f"\n⚠️  没有可用图片，无法创建实际文章。")
    
    print("\n" + "=" * 60)
    print("发布工具完成")
    print("=" * 60)
    
    # 提供后续步骤
    print("\n🎯 后续步骤:")
    print("1. 登录微信公众平台 (https://mp.weixin.qq.com)")
    print("2. 进入'内容与互动' -> '草稿箱'")
    print("3. 查看创建的草稿")
    print("4. 添加或更换封面图片")
    print("5. 预览并发布")
    
    print("\n💡 建议:")
    print("1. 在微信公众平台手动上传合适的封面图片")
    print("2. 封面图片尺寸: 900x500 像素")
    print("3. 使用 write_wechat_article.py 创建更多文章")
    print("4. 使用生成的 HTML 文件内容")

if __name__ == "__main__":
    main()