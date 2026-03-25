#!/usr/bin/env python3
"""
上传测试图片到微信公众号
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

def create_test_image():
    """创建测试图片（使用 base64 编码的简单图片）"""
    print("创建测试图片...")
    
    # 创建一个简单的 PNG 图片（1x1 像素的绿色点）
    # 这是一个最小的有效 PNG 文件
    png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    # 保存为文件
    image_data = base64.b64decode(png_base64)
    with open("test_image.png", "wb") as f:
        f.write(image_data)
    
    print("✅ 测试图片创建完成: test_image.png")
    return "test_image.png"

def upload_image(access_token, image_path):
    """上传图片到微信公众号"""
    print(f"上传图片: {image_path}")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/media/upload"
    params = {
        "access_token": access_token,
        "type": "image"
    }
    
    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if "media_id" in result:
                print(f"\n✅ 图片上传成功!")
                print(f"   媒体 ID: {result['media_id']}")
                print(f"   创建时间: {result.get('created_at', '未知')}")
                return result["media_id"]
            else:
                print(f"\n❌ 图片上传失败: {result}")
                return None
                
    except Exception as e:
        print(f"❌ 上传图片时出错: {e}")
        import traceback
        traceback.print_exc()
        return None

def upload_permanent_image(access_token, image_path):
    """上传永久图片素材"""
    print(f"上传永久图片素材: {image_path}")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/material/add_material"
    params = {
        "access_token": access_token,
        "type": "image"
    }
    
    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if "media_id" in result:
                print(f"\n✅ 永久图片上传成功!")
                print(f"   媒体 ID: {result['media_id']}")
                print(f"   URL: {result.get('url', '未知')}")
                return result["media_id"]
            else:
                print(f"\n❌ 永久图片上传失败: {result}")
                return None
                
    except Exception as e:
        print(f"❌ 上传永久图片时出错: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号图片上传测试")
    print("=" * 60)
    
    # 获取 access_token
    print("1. 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        sys.exit(1)
    
    print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
    
    # 创建测试图片
    print("\n2. 创建测试图片...")
    image_path = create_test_image()
    
    # 上传临时图片
    print("\n3. 上传临时图片...")
    media_id = upload_image(access_token, image_path)
    
    if media_id:
        print(f"\n✅ 临时图片上传成功，media_id: {media_id}")
        
        # 尝试上传永久图片
        print("\n4. 上传永久图片素材...")
        permanent_media_id = upload_permanent_image(access_token, image_path)
        
        if permanent_media_id:
            print(f"\n✅ 永久图片上传成功，media_id: {permanent_media_id}")
            print(f"\n📋 测试结果:")
            print(f"   临时图片 media_id: {media_id}")
            print(f"   永久图片 media_id: {permanent_media_id}")
            print(f"\n💡 使用建议:")
            print(f"   草稿封面需要使用永久图片素材的 media_id")
        else:
            print(f"\n⚠️  永久图片上传失败，但临时图片可用")
            print(f"   临时图片 media_id: {media_id}")
            print(f"   注意: 临时素材有效期为 3 天")
    else:
        print(f"\n❌ 图片上传失败")
        print(f"   可能原因:")
        print(f"   1. API 权限不足")
        print(f"   2. 图片格式不符合要求")
        print(f"   3. 图片大小超过限制")
        print(f"   4. 网络或服务器问题")
    
    # 清理临时文件
    import os
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"\n🗑️  已清理临时文件: {image_path}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()