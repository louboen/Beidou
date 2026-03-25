#!/usr/bin/env python3
"""
使用临时图片素材创建草稿
临时素材有效期为3天，但可能更容易成功
"""

import requests
import json
import sys
import base64

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

def upload_temp_image(access_token):
    """上传临时图片素材"""
    print("上传临时图片素材...")
    
    # 创建一个简单的 PNG 图片
    png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    image_data = base64.b64decode(png_base64)
    
    # 保存为文件
    with open("temp_test.png", "wb") as f:
        f.write(image_data)
    
    # 上传临时素材
    url = f"{WECHAT_API_BASE}/cgi-bin/media/upload"
    params = {
        "access_token": access_token,
        "type": "image"
    }
    
    try:
        with open("temp_test.png", "rb") as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if "media_id" in result:
                print(f"\n✅ 临时图片上传成功!")
                print(f"   媒体 ID: {result['media_id']}")
                print(f"   类型: {result.get('type', '未知')}")
                print(f"   创建时间: {result.get('created_at', '未知')}")
                return result["media_id"]
            else:
                print(f"\n❌ 临时图片上传失败: {result}")
                return None
                
    except Exception as e:
        print(f"❌ 上传临时图片时出错: {e}")
        return None
    finally:
        # 清理临时文件
        import os
        if os.path.exists("temp_test.png"):
            os.remove("temp_test.png")

def create_draft_with_temp_image(access_token, temp_media_id):
    """使用临时图片创建草稿"""
    print(f"\n使用临时图片创建草稿 (media_id: {temp_media_id[:30]}...)")
    
    # 最小化的内容
    title = "测试文章"
    author = "测试"
    digest = "测试摘要"
    
    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": "<p>测试内容</p>",
        "content_source_url": "",
        "thumb_media_id": temp_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
        "show_cover_pic": 1
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
            return True
        else:
            print(f"\n❌ 草稿创建失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("使用临时图片素材测试")
    print("=" * 60)
    
    # 获取 access_token
    print("1. 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        sys.exit(1)
    
    print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
    
    # 上传临时图片
    print("\n2. 上传临时图片素材...")
    temp_media_id = upload_temp_image(access_token)
    
    if not temp_media_id:
        print("❌ 临时图片上传失败，测试终止")
        sys.exit(1)
    
    # 使用临时图片创建草稿
    print("\n3. 使用临时图片创建草稿...")
    draft_media_id = create_draft_with_temp_image(access_token, temp_media_id)
    
    if draft_media_id:
        print(f"\n✅ 测试成功! 草稿已创建。")
        print(f"   临时图片 media_id: {temp_media_id}")
        print(f"   草稿 media_id: {draft_media_id}")
        print(f"\n💡 注意: 临时素材有效期为3天")
    else:
        print(f"\n❌ 草稿创建失败。")
        print(f"   可能原因:")
        print(f"   1. 临时图片格式不符合要求")
        print(f"   2. API 权限限制")
        print(f"   3. 微信公众号配置问题")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()