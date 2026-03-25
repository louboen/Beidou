#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传医生照片和二维码到微信公众号素材库
"""

import os
import sys
import json
import requests

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"

# 图片路径
DOCTOR_PHOTO_PATH = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets/doctor_photo.jpg"
QR_CODE_PATH = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets/qr_code.jpg"

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
    print("📤 上传医生照片和二维码到微信公众号素材库")
    print("=" * 60)
    
    # 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 上传医生照片
    print("\n📸 上传医生照片...")
    doctor_media_id = upload_permanent_image(access_token, DOCTOR_PHOTO_PATH, "医生照片")
    
    # 上传二维码
    print("\n📱 上传微信二维码...")
    qr_media_id = upload_permanent_image(access_token, QR_CODE_PATH, "微信二维码")
    
    # 保存结果
    if doctor_media_id and qr_media_id:
        print("\n" + "=" * 60)
        print("✅ 全部上传成功！")
        print("=" * 60)
        
        # 保存到配置文件
        config = {
            "doctor_image_media_id": doctor_media_id,
            "qr_code_media_id": qr_media_id,
            "upload_time": "2026-03-20 08:06"
        }
        
        config_path = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets/media_ids.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 配置已保存到：{config_path}")
        print("\n请在发布脚本中更新以下 MediaID：")
        print(f"   DOCTOR_IMAGE_MEDIA_ID = \"{doctor_media_id}\"")
        print(f"   QR_CODE_MEDIA_ID = \"{qr_media_id}\"")
        print("=" * 60)
        
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ 上传失败，请检查错误信息")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
