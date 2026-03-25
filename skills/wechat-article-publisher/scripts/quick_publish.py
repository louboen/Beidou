#!/usr/bin/env python3
"""
微信公众号文章快速发布工具
用于日常中医养生内容的快速发布
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# 配置
SCRIPT_DIR = Path(__file__).parent
ENV_FILE = SCRIPT_DIR / ".env"

def load_env():
    """加载环境变量"""
    config = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip().strip('"').strip("'")
    return config

def get_access_token(appid, appsecret):
    """获取 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": appsecret
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "access_token" in data:
            return data["access_token"]
        else:
            print(f"❌ 获取 access_token 失败：{data}")
            return None
    except Exception as e:
        print(f"❌ 获取 access_token 时出错：{e}")
        return None

def upload_image(access_token, image_path):
    """上传图片"""
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {"access_token": access_token, "type": "image"}
    
    try:
        if image_path.startswith('http://') or image_path.startswith('https://'):
            response = requests.get(image_path, timeout=30)
            response.raise_for_status()
            files = {'media': ('image.jpg', response.content, 'image/jpeg')}
        else:
            with open(image_path, 'rb') as f:
                files = {'media': f}
        
        response = requests.post(url, params=params, files=files, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "url" in result:
            return result["url"]
        else:
            print(f"❌ 上传图片失败：{result}")
            return None
    except Exception as e:
        print(f"❌ 上传图片时出错：{e}")
        return None

def create_draft(access_token, article):
    """创建草稿"""
    url = "https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    try:
        import json
        json_data = json.dumps({"articles": [article]}, ensure_ascii=False).encode('utf-8')
        response = requests.post(url, params=params, data=json_data, 
                                headers={'Content-Type': 'application/json; charset=utf-8'}, 
                                timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 创建草稿失败：{e}")
        return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号文章快速发布工具")
    parser.add_argument("--title", type=str, required=True, help="文章标题")
    parser.add_argument("--content", type=str, required=True, help="文章内容文件路径")
    parser.add_argument("--cover", type=str, default="https://picsum.photos/900/500", help="封面图片 URL 或路径")
    parser.add_argument("--author", type=str, default="娄医生", help="作者")
    parser.add_argument("--digest", type=str, help="摘要（可选）")
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_env()
    appid = config.get("WECHAT_APPID")
    appsecret = config.get("WECHAT_APPSECRET")
    
    if not appid or not appsecret:
        print("❌ 配置错误：请在.env 文件中设置 WECHAT_APPID 和 WECHAT_APPSECRET")
        sys.exit(1)
    
    print(f"📱 公众号：{config.get('WECHAT_ACCOUNT_NAME', '未知')}")
    print(f"🔑 AppID: {appid}")
    print(f"📝 标题：{args.title}")
    
    # 获取 access_token
    print("\n1️⃣ 获取 access_token...")
    access_token = get_access_token(appid, appsecret)
    if not access_token:
        sys.exit(1)
    print(f"✅ access_token 获取成功")
    
    # 读取内容
    print("\n2️⃣ 读取文章内容...")
    content_path = Path(args.content)
    if not content_path.exists():
        print(f"❌ 文件不存在：{content_path}")
        sys.exit(1)
    
    with open(content_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    
    print(f"✅ 读取成功：{len(content)} 字符")
    
    # 上传封面
    print("\n3️⃣ 上传封面图片...")
    cover_url = upload_image(access_token, args.cover)
    if cover_url:
        print(f"✅ 封面上传成功")
    else:
        print("⚠️  封面上传失败，使用默认")
        cover_url = ""
    
    # 摘要
    digest = args.digest or f"{args.title} - 来自中医娄伯恩"
    digest = digest[:120]
    
    # 构建文章数据
    article = {
        "title": args.title,
        "author": args.author,
        "digest": digest,
        "content": content,
        "content_source_url": "",
        "thumb_media_id": cover_url,
        "show_cover_pic": 1,
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    # 创建草稿
    print("\n4️⃣ 创建草稿...")
    result = create_draft(access_token, article)
    
    if result:
        if "errcode" in result:
            if result["errcode"] == 0:
                media_id = result.get("media_id", "unknown")
                print(f"\n✅ 草稿创建成功！")
                print(f"📄 MediaID: {media_id}")
                print(f"📝 标题：{args.title}")
                print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\n👉 请登录微信公众平台预览并发布：https://mp.weixin.qq.com")
            else:
                print(f"\n❌ 创建草稿失败：{result}")
                sys.exit(1)
        elif "media_id" in result:
            media_id = result.get("media_id", "unknown")
            print(f"\n✅ 草稿创建成功！")
            print(f"📄 MediaID: {media_id}")
            print(f"📝 标题：{args.title}")
            print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"\n👉 请登录微信公众平台预览并发布：https://mp.weixin.qq.com")
        else:
            print(f"\n❌ 创建草稿失败：{result}")
            sys.exit(1)
    else:
        print("\n❌ 创建草稿失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
