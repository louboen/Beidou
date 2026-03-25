#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成封面图片并上传到微信公众号素材库
"""

import os
import sys
import json
import requests
import subprocess
from datetime import datetime

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
ASSETS_DIR = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets"

def adjust_color(hex_color, percent):
    """调整颜色亮度"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = min(255, int(r * (100 + percent) / 100))
    g = min(255, int(g * (100 + percent) / 100))
    b = min(255, int(b * (100 + percent) / 100))
    return f"#{r:02x}{g:02x}{b:02x}"

def generate_cover_html(title, subtitle, color):
    """生成封面 HTML"""
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>封面</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}}
.cover{{width:900px;height:500px;background:linear-gradient(135deg,{color} 0%,{color1} 50%,{color2} 100%);position:relative;overflow:hidden}}
.circle{{position:absolute;border-radius:50%;background:rgba(255,255,255,0.1)}}
.circle1{{width:300px;height:300px;top:-100px;right:-100px}}
.circle2{{width:200px;height:200px;bottom:-50px;left:-50px}}
.content{{position:relative;z-index:10;text-align:center;padding-top:120px;color:white;text-shadow:2px 2px 4px rgba(0,0,0,0.6)}}
.title{{font-size:52px;font-weight:bold;letter-spacing:6px;margin-bottom:20px;background:linear-gradient(180deg,#fff 0%,#e8f5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.subtitle{{font-size:30px;font-weight:300;letter-spacing:3px;margin-bottom:40px;opacity:0.95}}
.divider{{width:200px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);margin:0 auto 30px}}
.footer{{font-size:18px;opacity:0.85;letter-spacing:2px}}
</style>
</head>
<body>
<div class="cover">
<div class="circle circle1"></div>
<div class="circle circle2"></div>
<div class="content">
<div class="title">{title}</div>
<div class="subtitle">{subtitle}</div>
<div class="divider"></div>
<div class="footer">中医健康科普 · 娄伯恩医师</div>
</div>
</div>
</body></html>""".format(
        color=color,
        color1=adjust_color(color, 30),
        color2=adjust_color(color, 50),
        title=title,
        subtitle=subtitle
    )
    return html

def get_access_token():
    """获取 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {'grant_type': 'client_credential', 'appid': APPID, 'secret': APPSECRET}
    response = requests.get(url, params=params)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    raise Exception(f"获取 access_token 失败：{data}")

def upload_image(access_token, image_path):
    """上传图片到素材库"""
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, params=params, files=files)
    
    data = response.json()
    if 'media_id' in data:
        print(f"✅ 封面上传成功！MediaID: {data['media_id'][:50]}...")
        return data['media_id']
    else:
        print(f"❌ 封面上传失败：{data}")
        return None

def main():
    if len(sys.argv) < 4:
        print("用法：python3 generate_cover.py <标题> <副标题> <颜色>")
        print("示例：python3 generate_cover.py '谷雨养生' '雨生百谷 祛湿健脾' '#2d6b45'")
        sys.exit(1)
    
    title = sys.argv[1]
    subtitle = sys.argv[2]
    color = sys.argv[3]
    
    print("=" * 60)
    print("🎨 生成封面图片")
    print("=" * 60)
    print(f"标题：{title}")
    print(f"副标题：{subtitle}")
    print(f"颜色：{color}")
    
    # 生成 HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.html")
    cover_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.png")
    
    print(f"\n📝 生成 HTML: {html_path}")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(generate_cover_html(title, subtitle, color))
    
    # 使用 browser 工具
    print("\n🌐 启动 HTTP 服务器...")
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', '8894'], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    import time
    time.sleep(2)
    
    try:
        print("📖 打开页面...")
        # 打开页面
        cmd1 = f"openclaw browser open --url 'http://localhost:8894/cover_{timestamp}.html' --target host"
        result1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out1, err1 = result1.communicate(timeout=30)
        
        time.sleep(2)
        
        print("📸 截图...")
        # 截图
        cmd2 = f"openclaw browser screenshot --type png --output '{cover_path}'"
        result2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2, err2 = result2.communicate(timeout=30)
        
        # 检查结果
        if os.path.exists(cover_path) and os.path.getsize(cover_path) > 0:
            print(f"\n✅ 封面图片已生成：{cover_path}")
            
            # 上传
            print("\n🔑 获取访问令牌...")
            access_token = get_access_token()
            
            print("\n📤 上传封面图片...")
            media_id = upload_image(access_token, cover_path)
            
            if media_id:
                print("\n" + "=" * 60)
                print("✅ 封面生成并上传成功！")
                print("=" * 60)
                print(f"MediaID: {media_id}")
                print(f"文件路径：{cover_path}")
                print("=" * 60)
                
                # 保存到配置文件
                config = {
                    "title": title,
                    "subtitle": subtitle,
                    "color": color,
                    "media_id": media_id,
                    "cover_path": cover_path,
                    "timestamp": timestamp
                }
                config_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.json")
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                print(f"\n💾 配置已保存：{config_path}")
                print(f"\n在发布脚本中使用：COVER_MEDIA_ID = \"{media_id}\"")
                return media_id
            else:
                print("❌ 上传失败")
                return None
        else:
            print(f"\n❌ 截图失败")
            print(f"文件存在：{os.path.exists(cover_path)}")
            if os.path.exists(cover_path):
                print(f"文件大小：{os.path.getsize(cover_path)} bytes")
            return None
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        return None
    finally:
        server_proc.terminate()

if __name__ == "__main__":
    media_id = main()
    sys.exit(0 if media_id else 1)
