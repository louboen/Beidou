#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康科普文章自动生成并发布工具（封面生成整合版）
- 使用 browser 工具生成封面图片
- 每次根据文章内容生成新封面
- 文章字数控制在 800 字左右
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
    raise Exception(f"获取 access_token 失败：{data}")

def generate_cover_html(title, subtitle, color):
    """生成封面 HTML"""
    def adjust_color(hex_color, percent):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = min(255, int(r * (100 + percent) / 100))
        g = min(255, int(g * (100 + percent) / 100))
        b = min(255, int(b * (100 + percent) / 100))
        return f"#{r:02x}{g:02x}{b:02x}"
    
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

def generate_and_upload_cover(title, subtitle, color, access_token):
    """生成封面并上传到素材库"""
    print(f"🎨 生成封面图片：{title}")
    
    # 生成 HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_filename = f"cover_{timestamp}.html"
    html_path = os.path.join(ASSETS_DIR, html_filename)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(generate_cover_html(title, subtitle, color))
    
    # 启动 HTTP 服务器
    print("🌐 启动 HTTP 服务器...")
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', '8897'], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    try:
        # 打开页面
        print("📖 打开页面...")
        cmd1 = f"openclaw browser open --url 'http://localhost:8897/{html_filename}' --target host"
        result1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out1, err1 = result1.communicate(timeout=30)
        
        time.sleep(2)
        
        # 截图
        print("📸 截图...")
        cmd2 = "openclaw browser screenshot --type png"
        result2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2, err2 = result2.communicate(timeout=30)
        
        # 查找最新生成的图片
        cover_files = glob.glob("/home/admin/.openclaw/media/browser/*.png")
        if cover_files:
            cover_path = max(cover_files, key=os.path.getctime)
        else:
            cover_path = None
        
        if not cover_path or not os.path.exists(cover_path):
            print("⚠️  截图失败")
            return None
        
        print(f"✅ 封面图片已生成：{cover_path}")
        
        # 上传到素材库
        print("📤 上传封面图片...")
        url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
        params = {'access_token': access_token, 'type': 'image'}
        
        with open(cover_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files)
        
        data = response.json()
        if 'media_id' in data:
            media_id = data['media_id']
            print(f"✅ 封面上传成功！MediaID: {media_id[:50]}...")
            return media_id
        else:
            print(f"❌ 封面上传失败：{data}")
            return None
            
    except Exception as e:
        print(f"⚠️  生成封面失败：{e}")
        return None
    finally:
        server_proc.terminate()

def generate_article_content(topic_type, topic_info):
    """生成文章内容 - 根据具体标题生成对应内容"""
    title = topic_info['title']
    subtitle = topic_info['subtitle']
    
    if topic_type == "节气养生":
        if "谷雨" in title or "谷雨" in subtitle:
            return get_guyu_content()
        elif "清明" in title or "清明" in subtitle:
            return get_qingming_content()
        elif "立夏" in title or "立夏" in subtitle:
            return get_lixia_content()
        else:
            return get_generic_seasonal_content()
    elif topic_type == "中医食疗":
        if "脾胃" in title or "脾胃" in subtitle:
            return get_sipiwei_content()
        elif "失眠" in title or "失眠" in subtitle:
            return get_shimian_content()
        elif "养肝" in title or "养肝" in subtitle:
            return get_yanggan_content()
        else:
            return get_generic_food_therapy_content()
    else:  # 穴位保健
        if "内关" in title or "内关" in subtitle:
            return get_neiguan_content()
        elif "足三里" in title or "足三里" in subtitle:
            return get_zusanli_content()
        elif "太冲" in title or "太冲" in subtitle:
            return get_taichong_content()
        else:
            return get_generic_acupoint_content()

def get_guyu_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">谷雨养生</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
            <p style="margin-bottom: 15px;">谷雨是春季的最后一个节气，此时降雨增多，空气湿度大，故有"雨生百谷"之说。中医认为，谷雨时节阳气逐渐升发，肝气旺盛，脾胃功能相对较弱，容易出现湿气困脾的情况。此时养生应以健脾祛湿、疏肝理气为主，为夏季的健康打下基础。</p>
            <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
            <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，保持充足睡眠。建议晚上 11 点前入睡，早上 6-7 点起床，顺应自然界阳气升发的规律。午间可适当小憩 15-30 分钟。保持室内通风干燥，避免潮湿环境。</p>
            <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃时令蔬菜。推荐食用山药、薏米、赤小豆等健脾祛湿的食材，少吃生冷、油腻、甜食。可适当食用辛温发散的食物，如葱、姜、蒜等，帮助阳气升发。</p>
            <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：适度运动，如散步、太极拳、八段锦等。运动可以促进气血运行，帮助排出体内湿气，但不宜过度出汗。建议每天运动 30-60 分钟，以微微出汗为度。</p>
            <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
            <p style="margin-bottom: 15px;">• <strong>山药薏米粥</strong>：山药 30g、薏米 20g、大米 50g，煮粥食用，健脾祛湿</p>
            <p style="margin-bottom: 15px;">• <strong>赤小豆冬瓜汤</strong>：赤小豆 30g、冬瓜 200g，煮汤饮用，利水消肿</p>
            <p style="margin-bottom: 15px;">• <strong>菊花枸杞茶</strong>：菊花 5g、枸杞 10g，沸水冲泡，清肝明目</p>
            <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
            <p style="margin-bottom: 15px;">• 避免过度劳累，注意休息</p>
            <p style="margin-bottom: 15px;">• 注意保暖，防止受凉感冒</p>
        </section>
    </section>
    """

def get_qingming_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">清明养生</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
            <p style="margin-bottom: 15px;">清明时节，气温转暖，草木萌发，万物欣欣向荣。此时人体阳气也开始升发，肝气旺盛。清明是祭祖扫墓的时节，情绪容易波动，更要注意情志调养。</p>
            <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
            <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，适当午休</p>
            <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡为主，多吃绿色蔬菜</p>
            <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：踏青、放风筝、散步</p>
            <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
            <p style="margin-bottom: 15px;">• 菊花茶：清肝明目</p>
            <p style="margin-bottom: 15px;">• 菠菜：养血润燥</p>
            <p style="margin-bottom: 15px;">• 荠菜：清热解毒</p>
        </section>
    </section>
    """

def get_lixia_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">立夏养生</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
            <p style="margin-bottom: 15px;">立夏是夏季的第一个节气，标志着夏天的开始。此时气温逐渐升高，人体阳气外发，心气渐旺，容易出现心烦、失眠、出汗多等症状。中医认为"夏气与心气相通"，立夏养生应以养心安神、防暑降温为主，为安然度夏打下基础。</p>
            <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
            <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：晚睡早起，中午适当午休。建议晚上 11 点左右入睡，早上 6 点起床。午间小憩 15-30 分钟，有助于养心安神。保持室内通风，温度适宜，避免贪凉受寒。</p>
            <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃清热解暑的食物。推荐食用冬瓜、黄瓜、苦瓜、绿豆等，少吃辛辣、油腻、烧烤类食物。适当食用酸味食物，如山楂、柠檬等，有助于敛汗生津。</p>
            <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：选择温和的运动，如散步、太极拳、游泳等。避免在烈日下剧烈运动，最好在清晨或傍晚进行。运动后及时补充水分，但不要立即饮用冰水。</p>
            <p style="margin-bottom: 15px;">4. <strong>情志调节</strong>：保持心情舒畅，避免情绪激动。中医认为"心主神明"，情绪波动会影响心脏功能。可通过听音乐、练书法、养花种草等方式陶冶情操，静心养神。</p>
            <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
            <p style="margin-bottom: 15px;">• <strong>绿豆汤</strong>：绿豆 50g，加水煮汤，清热解毒，消暑止渴</p>
            <p style="margin-bottom: 15px;">• <strong>莲子百合粥</strong>：莲子 20g、百合 15g、大米 50g，煮粥食用，养心安神</p>
            <p style="margin-bottom: 15px;">• <strong>酸梅汤</strong>：乌梅 10g、山楂 15g、甘草 5g，煮水代茶饮，生津止渴</p>
            <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
            <p style="margin-bottom: 15px;">• 避免长时间待在空调房，适当出汗有助于排湿</p>
            <p style="margin-bottom: 15px;">• 不要贪食冷饮，以免损伤脾胃</p>
            <p style="margin-bottom: 15px;">• 注意防暑降温，避免中暑</p>
        </section>
    </section>
    """

def get_generic_seasonal_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">节气养生</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
            <p style="margin-bottom: 15px;">中医认为，顺应四时变化养生，可以达到事半功倍的效果。</p>
            <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
            <p style="margin-bottom: 15px;">1. 起居调养：早睡早起</p>
            <p style="margin-bottom: 15px;">2. 饮食调理：清淡饮食</p>
            <p style="margin-bottom: 15px;">3. 运动保健：适度运动</p>
        </section>
    </section>
    """

def get_sipiwei_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">脾胃调理</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>🍲 脾胃重要性</strong></p>
            <p style="margin-bottom: 15px;">中医认为"脾胃为后天之本"，脾胃功能好坏直接影响消化吸收和气血生化。脾主运化，胃主受纳，两者共同完成食物的消化吸收，将营养物质输送到全身。现代人饮食不规律、工作压力大、熬夜多，很容易出现脾胃虚弱的情况，表现为食欲不振、疲倦乏力、大便溏稀、面色萎黄等症状。长期脾胃虚弱还会影响免疫力，导致容易感冒、体质下降。</p>
            
            <p style="margin-bottom: 15px;"><strong>🔍 脾胃虚弱的表现</strong></p>
            <p style="margin-bottom: 15px;">• 食欲不振，吃一点就饱</p>
            <p style="margin-bottom: 15px;">• 疲倦乏力，精神不振</p>
            <p style="margin-bottom: 15px;">• 大便溏稀，或便秘与腹泻交替</p>
            <p style="margin-bottom: 15px;">• 面色萎黄，唇色淡白</p>
            <p style="margin-bottom: 15px;">• 舌淡胖，边有齿痕</p>
            
            <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
            
            <p style="margin-bottom: 15px;"><strong>食谱一：山药莲子粥</strong></p>
            <p style="margin-bottom: 15px;">材料：山药 30g、莲子 20g、小米 50g、红枣 3 枚</p>
            <p style="margin-bottom: 15px;">做法：山药去皮切块，莲子去心，小米洗净，红枣去核。所有材料放入锅中，加水适量，大火煮沸后转小火煮 30 分钟即可。可加入适量冰糖调味。</p>
            <p style="margin-bottom: 15px;">功效：健脾养胃，安神助眠。适合脾胃虚弱、食欲不振、失眠多梦者食用。山药性平味甘，归脾、肺、肾经，具有补脾养胃、生津益肺的功效。莲子补脾止泻、养心安神。小米健脾和胃、补虚损。三者合用，健脾养胃效果更佳。</p>
            
            <p style="margin-bottom: 15px;"><strong>食谱二：陈皮白术茶</strong></p>
            <p style="margin-bottom: 15px;">材料：陈皮 5g、白术 10g、茯苓 10g、甘草 3g</p>
            <p style="margin-bottom: 15px;">做法：所有材料洗净，放入茶壶中，沸水冲泡，加盖焖 15 分钟即可。代茶饮用，可反复冲泡 2-3 次。也可加水煎煮 20 分钟，效果更佳。</p>
            <p style="margin-bottom: 15px;">功效：健脾益气，祛湿化痰。适合脾虚湿重、腹胀便溏者饮用。陈皮理气健脾、燥湿化痰。白术健脾益气、燥湿利水。茯苓利水渗湿、健脾宁心。甘草补脾益气、调和诸药。此方为经典的健脾祛湿方剂。</p>
            
            <p style="margin-bottom: 15px;"><strong>食谱三：南瓜小米粥</strong></p>
            <p style="margin-bottom: 15px;">材料：南瓜 100g、小米 50g、红糖适量</p>
            <p style="margin-bottom: 15px;">做法：南瓜去皮切块，小米洗净。所有材料放入锅中，加水适量，大火煮沸后转小火煮 40 分钟至粥稠，加入红糖调味。早餐或晚餐食用均可。</p>
            <p style="margin-bottom: 15px;">功效：健脾和胃，补中益气。适合脾胃虚弱、消化不良者食用。南瓜性温味甘，归脾、胃经，具有补中益气、消炎止痛的功效。小米健脾和胃、补虚损，是传统的养胃佳品。此粥老少皆宜，尤其适合老年人和儿童。</p>
            
            <p style="margin-bottom: 15px;"><strong>食谱四：党参黄芪炖鸡</strong></p>
            <p style="margin-bottom: 15px;">材料：党参 15g、黄芪 20g、鸡肉 200g、姜片 3 片、盐适量</p>
            <p style="margin-bottom: 15px;">做法：鸡肉洗净切块，党参、黄芪洗净。所有材料放入炖盅，加水适量，隔水炖 2 小时，加盐调味即可。每周食用 1-2 次。</p>
            <p style="margin-bottom: 15px;">功效：补气健脾，增强免疫力。适合脾气虚弱、体虚易感冒者食用。党参补中益气、健脾益肺。黄芪补气固表、利尿托毒。鸡肉温中益气、补精填髓。此汤补气效果显著，适合体质虚弱者调理。</p>
            
            <p style="margin-bottom: 15px;"><strong>⚠️ 饮食注意</strong></p>
            <p style="margin-bottom: 15px;">• 少吃生冷、油腻、辛辣刺激食物，以免损伤脾胃</p>
            <p style="margin-bottom: 15px;">• 规律饮食，细嚼慢咽，七分饱为宜，不要暴饮暴食</p>
            <p style="margin-bottom: 15px;">• 保持心情舒畅，避免思虑过度，中医认为"思伤脾"</p>
            <p style="margin-bottom: 15px;">• 适当运动，促进脾胃运化，但不宜过度劳累</p>
            <p style="margin-bottom: 15px;">• 注意腹部保暖，避免受凉</p>
        </section>
    </section>
    """

def get_shimian_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">失眠调理</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>🍲 失眠原因</strong></p>
            <p style="margin-bottom: 15px;">中医认为失眠多与心脾两虚、肝火扰心等因素有关。现代生活节奏快、压力大，很多人都有睡眠问题。</p>
            <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
            <p style="margin-bottom: 15px;">• 酸枣仁莲子汤：养心安神</p>
            <p style="margin-bottom: 15px;">• 桂圆红枣茶：补益心脾</p>
            <p style="margin-bottom: 15px;">• 小米南瓜粥：安神助眠</p>
        </section>
    </section>
    """

def get_yanggan_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">春季养肝</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>🍲 养肝重要性</strong></p>
            <p style="margin-bottom: 15px;">中医认为"春气与肝气相通"，春季是养肝护肝的最佳时节。肝主疏泄，调畅气机，肝气舒畅则全身气血调和。现代人工作压力大、熬夜多，很容易出现肝气郁结、肝火旺盛的情况，表现为情绪烦躁、眼睛干涩、胁肋胀痛等症状。</p>
            <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
            <p style="margin-bottom: 15px;"><strong>食谱一：菊花枸杞茶</strong></p>
            <p style="margin-bottom: 15px;">材料：菊花 5g、枸杞 10g、决明子 10g</p>
            <p style="margin-bottom: 15px;">做法：所有材料洗净，放入茶壶中，沸水冲泡，加盖焖 15 分钟即可。代茶饮用，可反复冲泡 2-3 次。</p>
            <p style="margin-bottom: 15px;">功效：清肝明目，滋补肝肾。适合肝火旺盛、眼睛干涩者饮用。</p>
            <p style="margin-bottom: 15px;"><strong>食谱二：菠菜猪肝汤</strong></p>
            <p style="margin-bottom: 15px;">材料：菠菜 200g、猪肝 100g、姜片 3 片</p>
            <p style="margin-bottom: 15px;">做法：菠菜洗净切段，猪肝切片用料酒腌制 10 分钟。锅中加水烧开，放入姜片和猪肝，煮至猪肝变色，加入菠菜烫熟，加盐调味即可。</p>
            <p style="margin-bottom: 15px;">功效：养血补肝，滋阴润燥。适合肝血不足、面色萎黄者食用。</p>
            <p style="margin-bottom: 15px;"><strong>食谱三：玫瑰山楂茶</strong></p>
            <p style="margin-bottom: 15px;">材料：玫瑰花 5g、山楂 10g、陈皮 5g</p>
            <p style="margin-bottom: 15px;">做法：所有材料洗净，沸水冲泡，加盖焖 10 分钟即可。代茶饮用。</p>
            <p style="margin-bottom: 15px;">功效：疏肝理气，活血化瘀。适合肝气郁结、情绪不畅者饮用。</p>
            <p style="margin-bottom: 15px;"><strong>⚠️ 饮食注意</strong></p>
            <p style="margin-bottom: 15px;">• 少吃辛辣、油腻、烧烤类食物</p>
            <p style="margin-bottom: 15px;">• 戒烟限酒，避免损伤肝脏</p>
            <p style="margin-bottom: 15px;">• 保持心情舒畅，避免生气发怒</p>
        </section>
    </section>
    """

def get_generic_food_therapy_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">中医食疗</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>🍲 食疗原理</strong></p>
            <p style="margin-bottom: 15px;">中医食疗讲究"药食同源"。</p>
            <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
            <p style="margin-bottom: 15px;">• 食疗方一</p>
            <p style="margin-bottom: 15px;">• 食疗方二</p>
        </section>
    </section>
    """

def get_neiguan_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">内关穴</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📍 穴位定位</strong></p>
            <p style="margin-bottom: 15px;">内关穴位于前臂掌侧，腕横纹上 2 寸。</p>
            <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
            <p style="margin-bottom: 15px;">用拇指按压 3-5 分钟</p>
            <p style="margin-bottom: 15px;"><strong>💡 功效</strong></p>
            <p style="margin-bottom: 15px;">宁心安神，缓解心悸</p>
        </section>
    </section>
    """

def get_zusanli_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">足三里</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📍 穴位定位</strong></p>
            <p style="margin-bottom: 15px;">足三里位于小腿外侧，犊鼻穴下 3 寸（约四横指），胫骨前嵴外一横指处。取穴时，屈膝，找到膝盖外侧凹陷处（犊鼻穴），向下量四横指，再向外侧量一横指，按压有酸胀感即是。</p>
            <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
            <p style="margin-bottom: 15px;">1. 用拇指指腹按压穴位，其余四指托住小腿</p>
            <p style="margin-bottom: 15px;">2. 力度以感觉酸胀为度，不可用力过猛</p>
            <p style="margin-bottom: 15px;">3. 每次按压 3-5 分钟，每日 2-3 次</p>
            <p style="margin-bottom: 15px;">4. 可配合艾灸，效果更佳</p>
            <p style="margin-bottom: 15px;"><strong>💡 保健功效</strong></p>
            <p style="margin-bottom: 15px;">• 健脾和胃，调理消化系统</p>
            <p style="margin-bottom: 15px;">• 补中益气，增强免疫力</p>
            <p style="margin-bottom: 15px;">• 通经活络，缓解下肢疼痛</p>
            <p style="margin-bottom: 15px;">• 延年益寿，是著名的长寿穴</p>
            <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
            <p style="margin-bottom: 15px;">• 饭后 1 小时内不宜按摩</p>
            <p style="margin-bottom: 15px;">• 孕妇慎用</p>
        </section>
    </section>
    """

def get_taichong_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">太冲穴</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📍 穴位定位</strong></p>
            <p style="margin-bottom: 15px;">太冲穴位于足背侧，第 1、2 跖骨结合部之前的凹陷处。取穴时，从大脚趾和二脚趾之间的缝隙向上推，推到骨头前方的凹陷处，按压有酸胀感即是。</p>
            <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
            <p style="margin-bottom: 15px;">1. 用拇指指腹按压穴位</p>
            <p style="margin-bottom: 15px;">2. 力度以感觉酸胀为度</p>
            <p style="margin-bottom: 15px;">3. 每次按压 3-5 分钟，每日 2-3 次</p>
            <p style="margin-bottom: 15px;"><strong>💡 保健功效</strong></p>
            <p style="margin-bottom: 15px;">• 疏肝解郁，缓解情绪烦躁</p>
            <p style="margin-bottom: 15px;">• 清肝明目，改善眼睛干涩</p>
            <p style="margin-bottom: 15px;">• 平息肝风，缓解头痛眩晕</p>
            <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
            <p style="margin-bottom: 15px;">• 孕妇慎用</p>
            <p style="margin-bottom: 15px;">• 皮肤破损处禁止按摩</p>
        </section>
    </section>
    """

def get_generic_acupoint_content():
    return """
    <section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">穴位保健</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📍 穴位介绍</strong></p>
            <p style="margin-bottom: 15px;">穴位按摩是中医传统保健方法。</p>
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

def count_chinese_chars(text):
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])

def main():
    print("=" * 60)
    print("🚀 健康科普文章发布（自动生成封面）")
    print("=" * 60)
    
    # 1. 随机选择主题
    topic_type = random.choice(list(TOPIC_LIBRARY.keys()))
    topic_info = random.choice(TOPIC_LIBRARY[topic_type])
    
    print(f"\n📝 主题类型：{topic_type}")
    print(f"📰 文章标题：{topic_info['title']}")
    print(f"🎨 封面颜色：{topic_info['color']}")
    
    # 2. 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 3. 生成并上传封面
    print("\n🎨 生成封面图片...")
    cover_media_id = generate_and_upload_cover(
        topic_info['title'],
        topic_info['subtitle'],
        topic_info['color'],
        access_token
    )
    
    if not cover_media_id:
        print("⚠️  封面生成失败，使用医生照片作为封面")
        cover_media_id = DOCTOR_IMAGE_MEDIA_ID
    
    # 4. 生成文章内容（根据标题匹配）
    print("\n✍️  生成文章内容...")
    content = generate_article_content(topic_type, topic_info)
    char_count = count_chinese_chars(content)
    print(f"📊 文章字数：约{char_count}字")
    
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
        print(f"📊 文章字数：约{char_count}字")
        print(f"🖼️  封面：已根据文章内容生成")
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
