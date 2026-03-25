#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康科普文章发布工具 - 新流程
1. 生成封面图片
2. 发送给用户确认
3. 用户确认后再发布
"""

import os
import sys
import json
import random
import requests
from datetime import datetime
import time
import subprocess
import glob

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
ASSETS_DIR = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets"

# 图片素材 ID
DOCTOR_IMAGE_MEDIA_ID = "K03y2eZTmx34znaim3BBRy-hW8MwrIRYoS1C9TYHWzs-KFA98jdCEYv-hPoYqtep"
QR_CODE_MEDIA_ID = "K03y2eZTmx34znaim3BBR8vT0SAOIjvDpXukxrl6NjB0b1C_Z9D_ummnCemdfcSN"

# 医院信息
HOSPITAL_INFO = {
    "name": "郑州金庚中医康复医院",
    "address": "郑州市中牟县芦医庙大街与象湖南路交叉口",
    "phone": "0371-68216120"
}

# 文章主题库
TOPIC_LIBRARY = {
    "节气养生": [
        {"title": "谷雨养生", "subtitle": "雨生百谷 祛湿健脾", "color": "#2d6b45"},
        {"title": "清明养生", "subtitle": "踏青祭祖 养肝护阳", "color": "#4a8f5a"},
        {"title": "立夏养生", "subtitle": "养心安神 防暑降温", "color": "#b85c5c"},
    ],
    "中医食疗": [
        {"title": "失眠怎么办", "subtitle": "食疗安神 改善睡眠", "color": "#5b6b9f"},
        {"title": "脾胃虚弱", "subtitle": "健脾养胃 易消化", "color": "#c9a959"},
        {"title": "春季养肝", "subtitle": "疏肝理气 调畅情志", "color": "#6b8f5b"},
    ],
    "穴位保健": [
        {"title": "内关穴", "subtitle": "宁心安神 缓解心悸", "color": "#b85c5c"},
        {"title": "足三里", "subtitle": "强身健体 延年益寿", "color": "#6b8f5b"},
        {"title": "太冲穴", "subtitle": "疏肝解郁 消气止痛", "color": "#8b5c8b"},
    ]
}

def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {'grant_type': 'client_credential', 'appid': APPID, 'secret': APPSECRET}
    response = requests.get(url, params=params)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    raise Exception("获取 access_token 失败：%s" % data)

def adjust_color(hex_color, percent):
    """调整颜色亮度"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = min(255, int(r * (100 + percent) / 100))
    g = min(255, int(g * (100 + percent) / 100))
    b = min(255, int(b * (100 + percent) / 100))
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def generate_cover_html(title, subtitle, color):
    """生成封面 HTML"""
    color1 = adjust_color(color, 30)
    color2 = adjust_color(color, 50)
    
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>封面</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}
.cover{width:900px;height:500px;background:linear-gradient(135deg,%s 0%%,%s 50%%,%s 100%%);position:relative;overflow:hidden}
.circle{position:absolute;border-radius:50%%;background:rgba(255,255,255,0.1)}
.circle1{width:300px;height:300px;top:-100px;right:-100px}
.circle2{width:200px;height:200px;bottom:-50px;left:-50px}
.content{position:relative;z-index:10;text-align:center;padding-top:120px;color:white;text-shadow:2px 2px 4px rgba(0,0,0,0.6)}
.title{font-size:52px;font-weight:bold;letter-spacing:6px;margin-bottom:20px;background:linear-gradient(180deg,#fff 0%%,#e8f5e9 100%%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.subtitle{font-size:30px;font-weight:300;letter-spacing:3px;margin-bottom:40px;opacity:0.95}
.divider{width:200px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);margin:0 auto 30px}
.footer{font-size:18px;opacity:0.85;letter-spacing:2px}
</style>
</head>
<body>
<div class="cover">
<div class="circle circle1"></div>
<div class="circle circle2"></div>
<div class="content">
<div class="title">%s</div>
<div class="subtitle">%s</div>
<div class="divider"></div>
<div class="footer">中医健康科普 · 娄伯恩医师</div>
</div>
</div>
</body></html>""" % (color, color1, color2, title, subtitle)
    
    return html

def create_cover_image(title, subtitle, color):
    """生成封面图片并返回路径"""
    print("🎨 生成封面图片：%s" % title)
    
    # 生成 HTML 文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_filename = "cover_%s.html" % timestamp
    html_path = os.path.join(ASSETS_DIR, html_filename)
    
    # 生成 HTML 内容
    html_content = generate_cover_html(title, subtitle, color)
    
    # 保存 HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("📝 HTML 已保存：%s" % html_path)
    
    # 验证 HTML 内容
    if title in html_content:
        print("✅ 标题已正确写入 HTML")
    else:
        print("❌ 标题未写入 HTML")
        return None
    
    # 使用 browser 工具生成图片
    print("\n🌐 使用 browser 工具生成图片...")
    
    # 启动 HTTP 服务器
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', '8901'], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    try:
        # 打开页面
        print("📖 打开页面...")
        cmd1 = "openclaw browser open --url 'http://localhost:8901/%s' --target host" % html_filename
        subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(timeout=30)
        time.sleep(2)
        
        # 截图
        print("📸 截图...")
        cmd2 = "openclaw browser screenshot --type png"
        subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(timeout=30)
        time.sleep(1)
        
        # 查找最新生成的图片
        cover_files = glob.glob("/home/admin/.openclaw/media/browser/*.png")
        if cover_files:
            cover_path = max(cover_files, key=os.path.getctime)
            print("✅ 封面图片已生成：%s" % cover_path)
            print("   文件大小：%d bytes" % os.path.getsize(cover_path))
            return cover_path
        else:
            print("⚠️  未找到生成的图片")
            return None
    except Exception as e:
        print("⚠️  生成封面失败：%s" % e)
        return None
    finally:
        server_proc.terminate()

def main():
    print("=" * 60)
    print("🎨 生成封面图片（待确认流程）")
    print("=" * 60)
    
    # 1. 随机选择主题
    topic_type = random.choice(list(TOPIC_LIBRARY.keys()))
    topic_info = random.choice(TOPIC_LIBRARY[topic_type])
    
    print("\n📝 主题类型：%s" % topic_type)
    print("📰 文章标题：%s" % topic_info['title'])
    print("🎨 封面颜色：%s" % topic_info['color'])
    
    # 2. 生成封面图片
    print("\n🎨 生成封面图片...")
    cover_path = create_cover_image(topic_info['title'], topic_info['subtitle'], topic_info['color'])
    
    if not cover_path:
        print("\n❌ 封面生成失败")
        return
    
    # 3. 输出信息，等待用户确认
    print("\n" + "=" * 60)
    print("✅ 封面图片已生成，请确认：")
    print("=" * 60)
    print("📰 文章标题：%s" % topic_info['title'])
    print("🎨 封面副标题：%s" % topic_info['subtitle'])
    print("🖼️  封面路径：%s" % cover_path)
    print("=" * 60)
    print("\n📌 下一步：")
    print("1. 检查封面图片是否正确")
    print("2. 确认无误后，运行发布脚本")
    print("=" * 60)
    
    # 保存配置供发布脚本使用
    config = {
        "topic_type": topic_type,
        "title": topic_info['title'],
        "subtitle": topic_info['subtitle'],
        "color": topic_info['color'],
        "cover_path": cover_path,
        "status": "pending_confirmation"
    }
    config_path = os.path.join(ASSETS_DIR, "pending_publish.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print("\n💾 配置已保存：%s" % config_path)

if __name__ == "__main__":
    main()
