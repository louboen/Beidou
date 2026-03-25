#!/usr/bin/env python3
"""
微信公众号官方 API 发布工具
使用 AppID 和 AppSecret 直接发布文章到草稿箱
"""

import os
import sys
import json
import requests
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# 配置
WECHAT_API_BASE = "https://api.weixin.qq.com"

def load_env():
    """从.env 文件加载配置"""
    env_path = Path(__file__).parent.parent / ".env"
    config = {}
    
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip().strip('"').strip("'")
    
    return config

def get_access_token(appid: str, appsecret: str) -> Optional[str]:
    """获取 access_token"""
    url = f"{WECHAT_API_BASE}/cgi-bin/token"
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

def upload_image(access_token: str, image_source: str) -> Optional[str]:
    """上传图片获取 media_id（支持本地路径或 URL）"""
    url = f"{WECHAT_API_BASE}/cgi-bin/material/add_material"
    params = {
        "access_token": access_token,
        "type": "image"
    }
    
    try:
        # 判断是 URL 还是本地路径
        if image_source.startswith('http://') or image_source.startswith('https://'):
            # 下载网络图片
            response = requests.get(image_source, timeout=30)
            response.raise_for_status()
            files = {'media': ('image.jpg', response.content, 'image/jpeg')}
        else:
            # 本地文件
            with open(image_source, 'rb') as f:
                files = {'media': f}
        
        response = requests.post(url, params=params, files=files, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "media_id" in result:
            return result["media_id"]
        else:
            print(f"❌ 上传图片失败：{result}")
            return None
    except Exception as e:
        print(f"❌ 上传图片时出错：{e}")
        return None

def create_draft(access_token: str, article: Dict) -> Optional[Dict]:
    """创建草稿"""
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {
        "access_token": access_token
    }
    
    data = {
        "articles": [article]
    }
    
    try:
        # 确保 JSON 编码时保留中文，不使用 ASCII 转义
        import json
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        response = requests.post(url, params=params, data=json_data, headers={'Content-Type': 'application/json; charset=utf-8'}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ 创建草稿失败：{e}")
        return None

def parse_markdown_title(content: str) -> str:
    """从 Markdown 内容提取标题（微信限制：标题最多 64 字节）"""
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            # 微信按字节计算，中文占 3 字节，确保不超过 64 字节
            while len(title.encode('utf-8')) > 64 and len(title) > 0:
                title = title[:-1]
            return title
    return "Untitled"

def parse_html_title(content: str) -> str:
    """从 HTML 内容提取标题"""
    import re
    # 优先从<title>标签提取
    match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        while len(title.encode('utf-8')) > 64 and len(title) > 0:
            title = title[:-1]
        return title
    
    # 其次从<h1>标签提取
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        while len(title.encode('utf-8')) > 64 and len(title) > 0:
            title = title[:-1]
        return title
    
    return "Untitled"

def parse_markdown_content(content: str) -> str:
    """简单转换 Markdown 为 HTML"""
    # 这里做简单的转换，实际使用可以引入 markdown 库
    html = content
    
    # 转换标题
    html = html.replace('\n# ', '\n<h1>').replace('\n', '</h1>\n', 1)
    html = html.replace('\n## ', '\n<h2>').replace('\n', '</h2>\n', 1)
    html = html.replace('\n### ', '\n<h3>').replace('\n', '</h3>\n', 1)
    
    # 转换粗体
    import re
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 转换换行
    html = html.replace('\n\n', '</p><p>')
    html = html.replace('\n', '<br>')
    
    return f"<p>{html}</p>"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号官方 API 发布工具")
    parser.add_argument("--markdown", type=str, help="Markdown 文件路径")
    parser.add_argument("--html", type=str, help="HTML 文件路径")
    parser.add_argument("--title", type=str, help="文章标题")
    parser.add_argument("--author", type=str, default="娄医生", help="作者")
    parser.add_argument("--digest", type=str, help="摘要")
    parser.add_argument("--cover", type=str, help="封面图片路径")
    parser.add_argument("--content-format", type=str, default="html", choices=["html", "markdown"], help="内容格式")
    
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
    
    # 获取 access_token
    print("\n1️⃣ 获取 access_token...")
    access_token = get_access_token(appid, appsecret)
    if not access_token:
        sys.exit(1)
    print(f"✅ access_token 获取成功：{access_token[:20]}...")
    
    # 读取内容
    print("\n2️⃣ 读取文章内容...")
    if args.markdown:
        content_path = Path(args.markdown)
        content_format = "markdown"
    elif args.html:
        content_path = Path(args.html)
        content_format = "html"
    else:
        print("❌ 请指定 --markdown 或 --html 文件")
        sys.exit(1)
    
    if not content_path.exists():
        print(f"❌ 文件不存在：{content_path}")
        sys.exit(1)
    
    # 读取文件，确保正确处理 UTF-8 编码
    with open(content_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    
    # 确保内容是 Unicode 字符串，不是转义序列
    # 如果检测到 \u 转义序列，需要解码
    if r'\u' in content:
        print("⚠️  检测到 Unicode 转义序列，正在解码...")
        try:
            content = content.encode('utf-8').decode('unicode_escape')
        except:
            pass
    
    print(f"✅ 读取成功：{content_path.name} ({len(content)} 字符)")
    
    # 提取标题
    title = args.title
    if not title:
        if content_format == "markdown":
            title = parse_markdown_title(content)
        else:
            title = parse_html_title(content)
    print(f"📝 标题：{title}")
    
    # 转换内容
    if content_format == "markdown":
        html_content = parse_markdown_content(content)
    else:
        # 对于 HTML 文件，提取 body 内容，去除 head 和 html 标签
        import re
        # 尝试提取 body 内容
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if body_match:
            html_content = body_match.group(1)
        else:
            # 如果没有 body 标签，去除 html/head/DOCTYPE 等标签
            html_content = content
            html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content, flags=re.IGNORECASE)
            html_content = re.sub(r'<html[^>]*>', '', html_content, flags=re.IGNORECASE)
            html_content = re.sub(r'</html>', '', html_content, flags=re.IGNORECASE)
            html_content = re.sub(r'<head[^>]*>.*?</head>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # 清理可能的 BOM 和异常字符
        html_content = html_content.replace('\ufeff', '').replace('\ufffd', '')
    
    # 调试：检查内容长度
    print(f"📄 内容长度：{len(html_content)} 字符 / {len(html_content.encode('utf-8'))} 字节")
    if len(html_content.encode('utf-8')) > 20000:
        print("⚠️  内容可能超限（微信限制 20000 字节），将截断")
        # 简单截断
        while len(html_content.encode('utf-8')) > 20000 and len(html_content) > 0:
            html_content = html_content[:-1]
    
    # 上传封面图片
    thumb_media_id = None
    if args.cover and args.cover != "skip":
        # 检查是 URL 还是本地文件
        is_url = args.cover.startswith('http://') or args.cover.startswith('https://')
        if is_url or Path(args.cover).exists():
            print("\n3️⃣ 上传封面图片...")
            thumb_media_id = upload_image(access_token, args.cover)
            if thumb_media_id:
                print(f"✅ 封面上传成功：{thumb_media_id}")
            else:
                print("⚠️  封面上传失败，将使用默认封面")
        else:
            print(f"\n⚠️  封面文件不存在：{args.cover}")
    else:
        print("\n⚠️  未指定封面图片，微信将使用默认处理")
    
    # 摘要（微信限制：128 字节）
    digest = args.digest or f"{title} - 来自{config.get('WECHAT_ACCOUNT_NAME', '公众号')}"
    while len(digest.encode('utf-8')) > 128 and len(digest) > 0:
        digest = digest[:-1]
    
    # 作者（微信限制：8 字节）
    author = args.author or "娄医生"
    while len(author.encode('utf-8')) > 8 and len(author) > 0:
        author = author[:-1]
    
    print(f"✍️  作者：{author}")
    print(f"📋 摘要：{digest[:50]}...")
    
    # 构建文章数据
    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": html_content,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "show_cover_pic": 1,
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    # 创建草稿
    print("\n4️⃣ 创建草稿...")
    result = create_draft(access_token, article)
    
    if result:
        # 微信 API 成功响应：返回 media_id，没有 errcode 或 errcode=0
        # 失败响应：返回 errcode != 0
        if "errcode" in result:
            if result["errcode"] == 0:
                media_id = result.get("media_id", "unknown")
                print(f"\n✅ 草稿创建成功！")
                print(f"📄 MediaID: {media_id}")
                print(f"📝 标题：{title}")
                print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\n👉 请登录微信公众平台预览并发布：https://mp.weixin.qq.com")
            else:
                print(f"\n❌ 创建草稿失败：{result}")
                sys.exit(1)
        elif "media_id" in result:
            # 成功响应，没有 errcode 字段
            media_id = result.get("media_id", "unknown")
            print(f"\n✅ 草稿创建成功！")
            print(f"📄 MediaID: {media_id}")
            print(f"📝 标题：{title}")
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
