#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成文章配图 - 修复版
"""

import os
import sys
import subprocess
import time
import glob

ASSETS_DIR = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets"

def create_cover():
    """生成封面图片"""
    print("\n🎨 生成封面图片...")
    
    html_content = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>春季风湿病的治疗</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}
.cover{width:900px;height:500px;background:linear-gradient(135deg,#4a8f5a 0%,#6ab87a 50%,#8ad49a 100%);position:relative;overflow:hidden}
.taiji{position:absolute;width:200px;height:200px;top:30px;right:30px;opacity:0.15;background:radial-gradient(circle at 50% 50%,#fff 50%,#000 50%);border-radius:50%}
.herb{position:absolute;font-size:80px;opacity:0.2}
.herb1{top:80px;left:50px;transform:rotate(30deg)}
.herb2{bottom:100px;right:80px;transform:rotate(-45deg)}
.herb3{top:150px;left:120px;transform:rotate(60deg)}
.content{position:relative;z-index:10;text-align:center;padding-top:120px;color:white;text-shadow:2px 2px 4px rgba(0,0,0,0.6)}
.title{font-size:44px;font-weight:bold;letter-spacing:3px;margin-bottom:15px}
.subtitle{font-size:26px;font-weight:300;letter-spacing:2px;margin-bottom:30px;opacity:0.95}
.divider{width:150px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);margin:0 auto 20px}
.footer{font-size:16px;opacity:0.85;letter-spacing:1px}
</style>
</head>
<body>
<div class="cover">
<div class="taiji"></div>
<div class="herb herb1">🌿</div>
<div class="herb herb2">🍃</div>
<div class="herb herb3">🌱</div>
<div class="content">
<div class="title">春季风湿病的治疗</div>
<div class="subtitle">中医辨证施治 标本兼治</div>
<div class="divider"></div>
<div class="footer">中医健康科普 · 娄伯恩医师</div>
</div>
</div>
</body></html>"""
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "cover_fixed_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    print("   标题：春季风湿病的治疗")
    return html_path, timestamp

def create_illustration_1():
    """生成插图 1：中医理疗"""
    print("\n🎨 生成插图 1：中医理疗...")
    
    html_content = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>中医理疗</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}
.canvas{width:600px;height:400px;background:linear-gradient(135deg,#e8f4ea 0%,#c8e4cc 100%);position:relative;display:flex;justify-content:center;align-items:center}
.icon{font-size:120px;margin-bottom:20px}
.title{font-size:32px;font-weight:bold;color:#333}
</style>
</head>
<body>
<div class="canvas">
<div style="text-align:center">
<div class="icon">💆</div>
<div class="title">中医理疗</div>
</div>
</div>
</body></html>"""
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "ill1_fixed_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    return html_path, timestamp

def create_illustration_2():
    """生成插图 2：草药调理"""
    print("\n🎨 生成插图 2：草药调理...")
    
    html_content = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>草药调理</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}
.canvas{width:600px;height:400px;background:linear-gradient(135deg,#fff5e8 0%,#ffe8c8 100%);position:relative;display:flex;justify-content:center;align-items:center}
.icon{font-size:120px;margin-bottom:20px}
.title{font-size:32px;font-weight:bold;color:#333}
</style>
</head>
<body>
<div class="canvas">
<div style="text-align:center">
<div class="icon">🌿</div>
<div class="title">草药调理</div>
</div>
</div>
</body></html>"""
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "ill2_fixed_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    return html_path, timestamp

def create_illustration_3():
    """生成插图 3：针灸治疗"""
    print("\n🎨 生成插图 3：针灸治疗...")
    
    html_content = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>针灸治疗</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}
.canvas{width:600px;height:400px;background:linear-gradient(135deg,#f0e8f4 0%,#e0d8e4 100%);position:relative;display:flex;justify-content:center;align-items:center}
.icon{font-size:120px;margin-bottom:20px}
.title{font-size:32px;font-weight:bold;color:#333}
</style>
</head>
<body>
<div class="canvas">
<div style="text-align:center">
<div class="icon">📍</div>
<div class="title">针灸治疗</div>
</div>
</div>
</body></html>"""
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "ill3_fixed_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    return html_path, timestamp

def screenshot_html(html_path, port):
    """截图 HTML 页面"""
    # 启动 HTTP 服务器
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', str(port)], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)
    
    try:
        # 打开页面
        html_filename = os.path.basename(html_path)
        url = 'http://localhost:%d/%s' % (port, html_filename)
        print("   打开 URL: %s" % url)
        
        # 使用 browser 工具打开
        from openclaw.tools import browser
        result = browser.browser(action='open', targetUrl=url, target='host')
        target_id = result.get('targetId')
        
        if not target_id:
            print("⚠️  打开页面失败")
            return None
        
        time.sleep(3)
        
        # 截图
        print("   截图...")
        screenshot = browser.browser(action='screenshot', targetId=target_id, type='png')
        img_path = screenshot.get('path')
        
        if img_path and os.path.exists(img_path):
            size = os.path.getsize(img_path)
            print("✅ 图片已生成：%s" % img_path)
            print("   文件大小：%d bytes" % size)
            
            if size < 10000:
                print("⚠️  文件大小异常")
                return None
            
            return img_path
        else:
            print("⚠️  未找到生成的图片")
            return None
    except Exception as e:
        print("⚠️  截图失败：%s" % e)
        return None
    finally:
        server_proc.terminate()

def main():
    print("=" * 60)
    print("🎨 重新生成文章配图（修复版）")
    print("=" * 60)
    
    images = {}
    
    # 生成封面
    html_path, ts = create_cover()
    img_path = screenshot_html(html_path, 8930)
    if img_path:
        images['cover'] = img_path
    
    # 生成插图 1
    html_path, ts = create_illustration_1()
    img_path = screenshot_html(html_path, 8931)
    if img_path:
        images['illustration1'] = img_path
    
    # 生成插图 2
    html_path, ts = create_illustration_2()
    img_path = screenshot_html(html_path, 8932)
    if img_path:
        images['illustration2'] = img_path
    
    # 生成插图 3
    html_path, ts = create_illustration_3()
    img_path = screenshot_html(html_path, 8933)
    if img_path:
        images['illustration3'] = img_path
    
    # 输出结果
    print("\n" + "=" * 60)
    print("✅ 图片生成完成")
    print("=" * 60)
    for name, path in images.items():
        print("%s: %s" % (name, path))
    print("=" * 60)

if __name__ == "__main__":
    main()
