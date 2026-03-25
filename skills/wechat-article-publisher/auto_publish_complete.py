#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康科普文章自动生成并发布工具（完整版）
- 根据文章内容自动生成封面图片
- 每次使用新生成的封面
- 文章字数控制在 500-800 字
- 包含更新的医生介绍
"""

import os
import sys
import json
import random
import requests
from datetime import datetime
import subprocess

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
    ],
    "中医食疗": [
        {"title": "失眠怎么办", "subtitle": "食疗安神 改善睡眠", "color": "#5b6b9f"},
        {"title": "脾胃虚弱", "subtitle": "健脾养胃 易消化", "color": "#c9a959"},
    ],
    "穴位保健": [
        {"title": "内关穴", "subtitle": "宁心安神 缓解心悸", "color": "#b85c5c"},
        {"title": "足三里", "subtitle": "强身健体 延年益寿", "color": "#6b8f5b"},
    ]
}

def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {'grant_type': 'client_credential', 'appid': APPID, 'secret': APPSECRET}
    response = requests.get(url, params=params)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    raise Exception(f"获取 access_token 失败：{data}")

def generate_cover_html(title, subtitle, color):
    """生成封面图片 HTML"""
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>封面</title></head>
<body style="margin:0;display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif;">
<div class="cover" style="width:900px;height:500px;background:linear-gradient(135deg,{color} 0%,{adjust_color(color,30)} 50%,{adjust_color(color,50)} 100%);position:relative;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.5);">
<div class="circle" style="position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,0.1);top:-100px;right:-100px;"></div>
<div class="circle" style="position:absolute;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,0.1);bottom:-50px;left:-50px;"></div>
<div class="content" style="position:relative;z-index:10;text-align:center;padding-top:120px;color:white;text-shadow:2px 2px 4px rgba(0,0,0,0.6);">
<h1 class="title" style="font-size:52px;font-weight:bold;letter-spacing:6px;margin-bottom:20px;background:linear-gradient(180deg,#ffffff 0%,#e8f5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{title}</h1>
<h2 class="subtitle" style="font-size:30px;font-weight:300;letter-spacing:3px;margin-bottom:40px;opacity:0.95;">{subtitle}</h2>
<div style="width:200px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);margin:0 auto 30px;"></div>
<p class="footer" style="font-size:18px;opacity:0.85;letter-spacing:2px;">中医健康科普 · 娄伯恩医师</p>
</div>
</div>
</body>
</html>"""
    return html

def adjust_color(hex_color, percent):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = min(255, int(r * (100 + percent) / 100))
    g = min(255, int(g * (100 + percent) / 100))
    b = min(255, int(b * (100 + percent) / 100))
    return f"#{r:02x}{g:02x}{b:02x}"

def generate_cover_image(title, subtitle, color):
    """生成封面图片"""
    print(f"🎨 生成封面图片：{title}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.html")
    screenshot_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.png")
    
    # 保存 HTML
    html_content = generate_cover_html(title, subtitle, color)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 启动临时 HTTP 服务器
    print("启动 HTTP 服务器...")
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', '8889'], cwd=ASSETS_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import time
    time.sleep(2)
    
    try:
        # 使用 browser 工具截图
        from openclaw_tools import browser
        browser_action = {'action': 'open', 'targetUrl': f'http://localhost:8889/cover_{timestamp}.html', 'target': 'host'}
        result = browser.browser(**browser_action)
        target_id = result.get('targetId')
        if target_id:
            time.sleep(1)
            screenshot = browser.browser(action='screenshot', targetId=target_id, type='png')
            screenshot_path = screenshot.get('path', screenshot_path)
            print(f"✅ 封面图片已生成：{screenshot_path}")
            return screenshot_path
    except Exception as e:
        print(f"⚠️  浏览器截图失败：{e}")
    finally:
        server_proc.terminate()
    
    return None

def upload_cover_image(access_token, image_path):
    """上传封面图片到素材库"""
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, params=params, files=files)
    
    data = response.json()
    if 'media_id' in data:
        print(f"✅ 封面图片上传成功！MediaID: {data['media_id'][:50]}...")
        return data['media_id']
    else:
        print(f"❌ 封面图片上传失败：{data}")
        return None

def generate_article_content(topic_type, topic_info):
    """生成文章内容（500-800 字）"""
    if topic_type == "节气养生":
        return """
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">节气养生</strong></section>
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
                <p style="margin-bottom: 15px;">中医认为，顺应四时变化养生，可以达到事半功倍的效果。此时人体阳气逐渐升发，肝气旺盛，脾胃功能相对较弱。</p>
                <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，保持充足睡眠</p>
                <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃时令蔬菜</p>
                <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：适度运动，如散步、太极拳</p>
                <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
                <p style="margin-bottom: 15px;">• 山药薏米粥：健脾祛湿</p>
                <p style="margin-bottom: 15px;">• 菊花枸杞茶：清肝明目</p>
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 避免过度劳累，注意休息</p>
                <p style="margin-bottom: 15px;">• 注意保暖，防止受凉</p>
            </section>
        </section>
        """
    elif topic_type == "中医食疗":
        return """
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">中医食疗</strong></section>
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>🍲 食疗原理</strong></p>
                <p style="margin-bottom: 15px;">中医食疗讲究"药食同源"，通过日常饮食调理身体，安全有效。</p>
                <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
                <p style="margin-bottom: 15px;"><strong>酸枣仁莲子汤</strong></p>
                <p style="margin-bottom: 15px;">材料：酸枣仁 15g、莲子 20g、百合 15g</p>
                <p style="margin-bottom: 15px;">做法：所有材料煮 30 分钟，睡前温服</p>
                <p style="margin-bottom: 15px;">功效：养心安神，健脾益肾</p>
                <p style="margin-bottom: 15px;"><strong>桂圆红枣茶</strong></p>
                <p style="margin-bottom: 15px;">材料：桂圆肉 10g、红枣 5 枚、枸杞 10g</p>
                <p style="margin-bottom: 15px;">做法：沸水冲泡，代茶饮用</p>
                <p style="margin-bottom: 15px;">功效：补益心脾，养血安神</p>
                <p style="margin-bottom: 15px;"><strong>⚠️ 食用注意</strong></p>
                <p style="margin-bottom: 15px;">• 食疗需长期坚持</p>
                <p style="margin-bottom: 15px;">• 特殊人群请咨询医生</p>
            </section>
        </section>
        """
    else:
        return """
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">穴位保健</strong></section>
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📍 穴位介绍</strong></p>
                <p style="margin-bottom: 15px;">穴位按摩是中医传统保健方法，简单易学，安全有效。</p>
                <p style="margin-bottom: 15px;"><strong>🔍 穴位定位</strong></p>
                <p style="margin-bottom: 15px;">请参照标准穴位图准确定位</p>
                <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
                <p style="margin-bottom: 15px;">1. 用拇指指腹按压穴位</p>
                <p style="margin-bottom: 15px;">2. 力度以感觉酸胀为度</p>
                <p style="margin-bottom: 15px;">3. 每次按压 3-5 分钟</p>
                <p style="margin-bottom: 15px;"><strong>💡 保健功效</strong></p>
                <p style="margin-bottom: 15px;">• 疏通经络，调和气血</p>
                <p style="margin-bottom: 15px;">• 缓解疲劳，强身健体</p>
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 饭后 1 小时内不宜按摩</p>
                <p style="margin-bottom: 15px;">• 皮肤破损处禁止按摩</p>
            </section>
        </section>
        """

def create_doctor_section(doctor_img_url, qr_img_url):
    return f"""
    <section style="margin-top: 40px; padding: 20px; background-color: #f5f5f5; border-radius: 10px;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 16px; color: #2c5530;">👨‍⚕️ 医生介绍</strong></section>
        <section style="display: flex; justify-content: center; align-items: flex-start; margin-bottom: 20px;">
            <section style="flex: 0 0 150px; margin-right: 20px;"><img src="{doctor_img_url}" style="width: 150px; height: 200px; object-fit: cover; border-radius: 10px;"/></section>
            <section style="flex: 1; text-align: left; line-height: 1.8;">
                <p style="margin-bottom: 10px;"><strong>娄伯恩</strong> 主治医师</p>
                <p style="margin-bottom: 8px; font-size: 14px;">宋氏中医传承人 | 娄氏风湿病传承人</p>
                <p style="margin-bottom: 10px; font-size: 13px; color: #555;">出身于中医世家，毕业于河南中医学院中医骨伤系，曾在北京积水潭医院中医正骨科进修学习。临床中以虚、邪、瘀治痹理论为基础，中西医结合，辨证论治，在疼痛、骨伤、风湿病的诊治过程中积累丰富经验。任河南省中医药学会风湿病专业委员会委员，河南省中西医结合学会风湿病专业委员会委员，世界中联骨质疏松专业委员会理事，世界中联骨关节疾病专业委员会理事。</p>
                <p style="margin-bottom: 10px; font-size: 13px; color: #555;"><strong>擅长治疗</strong>：各类关节肌肉疼痛疾病，颈肩腰腿痛，骨折病，关节陈旧性损伤，风湿、类风湿、痛风关节炎。</p>
            </section>
        </section>
        <section style="text-align: center; margin-bottom: 20px;">
            <img src="{qr_img_url}" style="width: 150px; height: 150px;"/>
            <p style="font-size: 14px; color: #666; margin-top: 10px;">扫码添加微信 咨询健康问题</p>
        </section>
    </section>
    """

def create_hospital_section():
    return f"""
    <section style="margin-top: 30px; padding: 20px; background-color: #e8f4ea; border-radius: 10px;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 16px; color: #2c5530;">🏥 就诊信息</strong></section>
        <section style="line-height: 2; text-align: center;">
            <p style="margin-bottom: 10px;"><strong>医院名称</strong>：{HOSPITAL_INFO["name"]}</p>
            <p style="margin-bottom: 10px;"><strong>医院地址</strong>：{HOSPITAL_INFO["address"]}</p>
            <p style="margin-bottom: 10px;"><strong>咨询电话</strong>：{HOSPITAL_INFO["phone"]}</p>
        </section>
    </section>
    """

def get_image_urls(access_token):
    url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material"
    params = {'access_token': access_token}
    data = {'type': 'image', 'offset': 0, 'count': 20}
    response = requests.post(url, params=params, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    result = response.json()
    urls = {}
    if 'item' in result:
        for item in result['item']:
            if item.get('media_id') == DOCTOR_IMAGE_MEDIA_ID:
                urls['doctor'] = item.get('url', '')
            elif item.get('media_id') == QR_CODE_MEDIA_ID:
                urls['qr'] = item.get('url', '')
    return urls

def create_draft(access_token, title, content, doctor_img_url, qr_img_url, cover_media_id):
    url = "https://api.weixin.qq.com/cgi-bin/draft/add"
    full_content = f"""
    <section style="max-width: 100%; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', sans-serif;">
        {content}
        {create_doctor_section(doctor_img_url, qr_img_url)}
        {create_hospital_section()}
    </section>
    """
    data = {
        "articles": [{
            "title": title[:64],
            "author": "娄医",
            "digest": f"中医健康科普 - {title[:30]}",
            "content": full_content,
            "thumb_media_id": cover_media_id,
            "show_cover_pic": 1
        }]
    }
    params = {'access_token': access_token}
    response = requests.post(url, params=params, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'})
    return response.json()

def main():
    print("=" * 60)
    print("🚀 健康科普文章发布（自动生成封面）")
    print("=" * 60)
    
    # 1. 随机选择主题
    topic_type = random.choice(list(TOPIC_LIBRARY.keys()))
    topic_info = random.choice(TOPIC_LIBRARY[topic_type])
    
    print(f"\n📝 主题类型：{topic_type}")
    print(f"📰 文章标题：{topic_info['title']}")
    
    # 2. 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 3. 生成并上传封面图片
    print("\n🎨 生成封面图片...")
    # 使用 browser 工具生成封面
    import time
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cover_html = generate_cover_html(topic_info['title'], topic_info['subtitle'], topic_info['color'])
    html_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.html")
    cover_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.png")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(cover_html)
    
    # 启动 HTTP 服务器
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', '8891'], cwd=ASSETS_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    try:
        # 使用 browser 工具截图
        print("打开浏览器...")
        result = subprocess.run(
            ['openclaw', 'browser', 'open', '--url', f'http://localhost:8891/cover_{timestamp}.html', '--target', 'host'],
            capture_output=True, text=True, timeout=30
        )
        
        time.sleep(2)
        
        # 截图
        print("截图...")
        screenshot_result = subprocess.run(
            ['openclaw', 'browser', 'screenshot', '--type', 'png', '--output', cover_path],
            capture_output=True, text=True, timeout=30
        )
        
        if os.path.exists(cover_path):
            print(f"\n📤 上传封面图片...")
            cover_media_id = upload_cover_image(access_token, cover_path)
            if not cover_media_id:
                cover_media_id = DOCTOR_IMAGE_MEDIA_ID
        else:
            print("⚠️  截图失败，使用医生照片作为封面")
            cover_media_id = DOCTOR_IMAGE_MEDIA_ID
    except Exception as e:
        print(f"⚠️  生成封面失败：{e}")
        cover_media_id = DOCTOR_IMAGE_MEDIA_ID
    finally:
        server_proc.terminate()
    
    # 4. 生成文章内容
    print("\n✍️  生成文章内容...")
    content = generate_article_content(topic_type, topic_info)
    
    # 5. 获取图片 URL
    print("\n🖼️  获取图片 URL...")
    img_urls = get_image_urls(access_token)
    doctor_img_url = img_urls.get('doctor', '')
    qr_img_url = img_urls.get('qr', '')
    
    # 6. 创建草稿
    print("\n📤 发布到微信公众号草稿箱...")
    result = create_draft(access_token, topic_info['title'], content, doctor_img_url, qr_img_url, cover_media_id)
    
    # 7. 处理结果
    if 'media_id' in result:
        print("\n" + "=" * 60)
        print("✅ 发布成功！")
        print("=" * 60)
        print(f"📰 文章标题：{topic_info['title']}")
        print(f"🆔 草稿 ID: {result['media_id']}")
        print(f"🖼️  封面：已根据文章内容生成新封面")
        print(f"⏰ 发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📱 请登录微信公众平台预览并发布：")
        print("   https://mp.weixin.qq.com")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ 发布失败！")
        print("=" * 60)
        print(f"错误代码：{result.get('errcode', 'Unknown')}")
        print(f"错误信息：{result.get('errmsg', 'Unknown error')}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
