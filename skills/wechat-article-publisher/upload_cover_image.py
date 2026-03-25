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

# 封面图片路径
COVER_IMAGE_PATH = "/home/admin/.openclaw/media/browser/be38f71e-17ca-4ee7-a08f-c7b6189af568.png"

def get_access_token():
    """获取微信公众号 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': APPID,
        'secret': APPSECRET
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        raise Exception(f"获取 access_token 失败：{data}")

def upload_permanent_image(access_token, image_path, title):
    """上传永久图片素材"""
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, params=params, files=files)
    
    data = response.json()
    if 'media_id' in data:
        print(f"✅ {title} 上传成功！")
        print(f"   MediaID: {data['media_id']}")
        print(f"   URL: {data.get('url', 'N/A')}")
        return data['media_id']
    else:
        print(f"❌ {title} 上传失败！")
        print(f"   错误代码：{data.get('errcode', 'Unknown')}")
        print(f"   错误信息：{data.get('errmsg', 'Unknown error')}")
        return None

def main():
    print("=" * 60)
    print("📤 上传封面图片到微信公众号素材库")
    print("=" * 60)
    
    # 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 上传封面图片
    print("\n🖼️  上传封面图片...")
    cover_media_id = upload_permanent_image(access_token, COVER_IMAGE_PATH, "谷雨养生封面")
    
    # 保存结果
    if cover_media_id:
        print("\n" + "=" * 60)
        print("✅ 上传成功！")
        print("=" * 60)
        
        # 保存到配置文件
        config_path = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets/cover_media_id.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({
                "cover_media_id": cover_media_id,
                "article_title": "谷雨养生：雨生百谷，祛湿健脾",
                "upload_time": "2026-03-20 08:16"
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 配置已保存到：{config_path}")
        print(f"\n请在发布脚本中使用以下 MediaID：")
        print(f"   COVER_MEDIA_ID = \"{cover_media_id}\"")
        print("=" * 60)
        
        return cover_media_id
    else:
        print("\n" + "=" * 60)
        print("❌ 上传失败，请检查错误信息")
        print("=" * 60)
        return None

if __name__ == "__main__":
    main()
