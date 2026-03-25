#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传封面图片到微信公众号素材库
"""

import os
import sys
import json
import requests

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"

# 封面图片路径（刚刚生成的）
COVER_PATH = "/home/admin/.openclaw/media/browser/dffb4e6f-e1e6-4f4e-95b9-5dfb6446c851.png"

def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {'grant_type': 'client_credential', 'appid': APPID, 'secret': APPSECRET}
    response = requests.get(url, params=params)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    raise Exception(f"获取 access_token 失败：{data}")

def upload_image(access_token, image_path):
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, params=params, files=files)
    
    data = response.json()
    if 'media_id' in data:
        print(f"✅ 封面上传成功！")
        print(f"MediaID: {data['media_id']}")
        print(f"URL: {data.get('url', 'N/A')}")
        return data['media_id']
    else:
        print(f"❌ 封面上传失败：{data}")
        return None

def main():
    print("=" * 60)
    print("📤 上传封面图片到微信公众号素材库")
    print("=" * 60)
    
    if not os.path.exists(COVER_PATH):
        print(f"❌ 文件不存在：{COVER_PATH}")
        sys.exit(1)
    
    print(f"封面路径：{COVER_PATH}")
    print(f"文件大小：{os.path.getsize(COVER_PATH)} bytes")
    
    # 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 上传
    print("\n📤 上传封面图片...")
    media_id = upload_image(access_token, COVER_PATH)
    
    if media_id:
        print("\n" + "=" * 60)
        print("✅ 上传成功！")
        print("=" * 60)
        
        # 保存配置
        config = {
            "cover_media_id": media_id,
            "cover_path": COVER_PATH,
            "description": "谷雨养生封面"
        }
        config_path = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets/latest_cover.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 配置已保存：{config_path}")
        print(f"\n在发布脚本中使用：COVER_MEDIA_ID = \"{media_id}\"")
        print("=" * 60)
        return media_id
    else:
        print("\n" + "=" * 60)
        print("❌ 上传失败")
        print("=" * 60)
        return None

if __name__ == "__main__":
    media_id = main()
    sys.exit(0 if media_id else 1)
