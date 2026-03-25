#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成文章配图（封面 +3 张插图）
"""

import os
import sys
import subprocess
import time
import glob

ASSETS_DIR = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets"

def generate_html(content, width, height, bg_color, elements):
    """生成 HTML"""
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>图片</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}
.canvas{width:%dpx;height:%dpx;background:%s;position:relative;overflow:hidden}
%s
</style>
</head>
<body>
<div class="canvas">
%s
</div>
</body></html>""" % (width, height, bg_color, elements['css'], elements['html'])
    return html

def create_cover():
    """生成封面图片"""
    print("\n🎨 生成封面图片...")
    
    elements = {
        'css': """
.taiji{position:absolute;width:200px;height:200px;top:30px;right:30px;opacity:0.15;
background:radial-gradient(circle at 50%% 50%%,#fff 50%%,#000 50%%);border-radius:50%%}
.herb{position:absolute;font-size:80px;opacity:0.2}
.herb1{top:80px;left:50px;transform:rotate(30deg)}
.herb2{bottom:100px;right:80px;transform:rotate(-45deg)}
.herb3{top:150px;left:120px;transform:rotate(60deg)}
.acupuncture{position:absolute;font-size:60px;opacity:0.15;bottom:80px;left:80px}
.content{position:relative;z-index:10;text-align:center;padding-top:120px;color:white;text-shadow:2px 2px 4px rgba(0,0,0,0.6)}
.title{font-size:44px;font-weight:bold;letter-spacing:3px;margin-bottom:15px}
.subtitle{font-size:26px;font-weight:300;letter-spacing:2px;margin-bottom:30px;opacity:0.95}
.divider{width:150px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);margin:0 auto 20px}
.footer{font-size:16px;opacity:0.85;letter-spacing:1px}
.tcm-badge{position:absolute;bottom:20px;right:20px;font-size:14px;opacity:0.3;
border:2px solid rgba(255,255,255,0.3);padding:5px 10px;border-radius:5px}
""",
        'html': """
<div class="taiji"></div>
<div class="herb herb1">🌿</div>
<div class="herb herb2">🍃</div>
<div class="herb herb3">🌱</div>
<div class="acupuncture">📍</div>
<div class="content">
<div class="title">春季风湿病的治疗</div>
<div class="subtitle">中医辨证施治 标本兼治</div>
<div class="divider"></div>
<div class="footer">中医健康科普 · 娄伯恩医师</div>
</div>
<div class="tcm-badge">中医文化</div>
"""
    }
    
    html_content = generate_html(elements, 900, 500, "linear-gradient(135deg,#4a8f5a 0%,#6ab87a 50%,#8ad49a 100%)", elements)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "cover_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    return html_path, timestamp

def create_illustration_1():
    """生成插图 1：中医理疗"""
    print("\n🎨 生成插图 1：中医理疗...")
    
    elements = {
        'css': """
.content{position:absolute;top:50%%;left:50%%;transform:translate(-50%%,-50%%);text-align:center}
.icon{font-size:120px;margin-bottom:20px}
.title{font-size:32px;font-weight:bold;color:#333}
""",
        'html': """
<div class="content">
<div class="icon">💆</div>
<div class="title">中医理疗</div>
</div>
"""
    }
    
    html_content = generate_html(elements, 600, 400, "linear-gradient(135deg,#e8f4ea 0%,#c8e4cc 100%)", elements)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "illustration1_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    return html_path, timestamp

def create_illustration_2():
    """生成插图 2：草药调理"""
    print("\n🎨 生成插图 2：草药调理...")
    
    elements = {
        'css': """
.content{position:absolute;top:50%%;left:50%%;transform:translate(-50%%,-50%%);text-align:center}
.icon{font-size:120px;margin-bottom:20px}
.title{font-size:32px;font-weight:bold;color:#333}
""",
        'html': """
<div class="content">
<div class="icon">🌿</div>
<div class="title">草药调理</div>
</div>
"""
    }
    
    html_content = generate_html(elements, 600, 400, "linear-gradient(135deg,#fff5e8 0%,#ffe8c8 100%)", elements)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "illustration2_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    return html_path, timestamp

def create_illustration_3():
    """生成插图 3：针灸治疗"""
    print("\n🎨 生成插图 3：针灸治疗...")
    
    elements = {
        'css': """
.content{position:absolute;top:50%%;left:50%%;transform:translate(-50%%,-50%%);text-align:center}
.icon{font-size:120px;margin-bottom:20px}
.title{font-size:32px;font-weight:bold;color:#333}
""",
        'html': """
<div class="content">
<div class="icon">📍</div>
<div class="title">针灸治疗</div>
</div>
"""
    }
    
    html_content = generate_html(elements, 600, 400, "linear-gradient(135deg,#f0e8f4 0%,#e0d8e4 100%)", elements)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, "illustration3_%s.html" % timestamp)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📝 HTML 已保存：%s" % html_path)
    return html_path, timestamp

def screenshot_html(html_path, port):
    """截图 HTML 页面"""
    # 启动 HTTP 服务器
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', str(port)], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    try:
        # 打开页面
        html_filename = os.path.basename(html_path)
        cmd1 = "openclaw browser open --url 'http://localhost:%d/%s' --target host" % (port, html_filename)
        subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(timeout=30)
        time.sleep(2)
        
        # 截图
        cmd2 = "openclaw browser screenshot --type png"
        subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(timeout=30)
        time.sleep(1)
        
        # 查找最新图片
        img_files = glob.glob("/home/admin/.openclaw/media/browser/*.png")
        if img_files:
            img_path = max(img_files, key=os.path.getctime)
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
    print("🎨 生成文章配图")
    print("=" * 60)
    
    images = {}
    
    # 生成封面
    html_path, ts = create_cover()
    img_path = screenshot_html(html_path, 8920)
    if img_path:
        images['cover'] = img_path
    
    # 生成插图 1
    html_path, ts = create_illustration_1()
    img_path = screenshot_html(html_path, 8921)
    if img_path:
        images['illustration1'] = img_path
    
    # 生成插图 2
    html_path, ts = create_illustration_2()
    img_path = screenshot_html(html_path, 8922)
    if img_path:
        images['illustration2'] = img_path
    
    # 生成插图 3
    html_path, ts = create_illustration_3()
    img_path = screenshot_html(html_path, 8923)
    if img_path:
        images['illustration3'] = img_path
    
    # 输出结果
    print("\n" + "=" * 60)
    print("✅ 图片生成完成")
    print("=" * 60)
    for name, path in images.items():
        print("%s: %s" % (name, path))
    print("=" * 60)
    
    # 保存配置
    import json
    config = {
        'article_title': '春季风湿病的治疗',
        'images': {k: os.path.basename(v) for k, v in images.items()},
        'status': 'pending_confirmation'
    }
    config_path = os.path.join(ASSETS_DIR, 'images_config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print("\n💾 配置已保存：%s" % config_path)

if __name__ == "__main__":
    main()
