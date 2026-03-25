#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康科普文章自动生成并发布工具（最终版）
- 根据文章内容自动生成封面图片
- 每次使用新生成的封面
- 文章字数控制在 800 字左右
- 包含更新的医生介绍
"""

import os
import sys
import json
import random
import requests
from datetime import datetime
import subprocess
import time

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
    """生成封面图片 HTML"""
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
<html><head><meta charset="utf-8"><title>封面</title></head>
<body style="margin:0;display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif;">
<div style="width:900px;height:500px;background:linear-gradient(135deg,{color} 0%,{color1} 50%,{color2} 100%);position:relative;overflow:hidden;">
<div style="position:absolute;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,0.1);top:-100px;right:-100px;"></div>
<div style="position:absolute;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,0.1);bottom:-50px;left:-50px;"></div>
<div style="position:relative;z-index:10;text-align:center;padding-top:120px;color:white;text-shadow:2px 2px 4px rgba(0,0,0,0.6);">
<h1 style="font-size:52px;font-weight:bold;letter-spacing:6px;margin-bottom:20px;background:linear-gradient(180deg,#ffffff 0%,#e8f5e9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{title}</h1>
<h2 style="font-size:30px;font-weight:300;letter-spacing:3px;margin-bottom:40px;opacity:0.95;">{subtitle}</h2>
<div style="width:200px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);margin:0 auto 30px;"></div>
<p style="font-size:18px;opacity:0.85;letter-spacing:2px;">中医健康科普 · 娄伯恩医师</p>
</div>
</div>
</body></html>""".format(color=color, color1=adjust_color(color, 30), color2=adjust_color(color, 50), title=title, subtitle=subtitle)
    return html

def generate_cover_with_browser(title, subtitle, color):
    """使用浏览器生成封面图片（Python 3.6 兼容）"""
    print(f"🎨 生成封面图片：{title}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.html")
    cover_path = os.path.join(ASSETS_DIR, f"cover_{timestamp}.png")
    
    # 保存 HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(generate_cover_html(title, subtitle, color))
    
    # 启动 HTTP 服务器
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', '8893'], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    try:
        # 使用 browser 工具打开页面并截图
        print("打开页面...")
        open_result = subprocess.Popen(
            ['openclaw', 'browser', 'open', '--url', f'http://localhost:8893/cover_{timestamp}.html', '--target', 'host'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        open_out, open_err = open_result.communicate(timeout=30)
        
        time.sleep(2)
        
        # 截图
        print("截图...")
        screenshot_result = subprocess.Popen(
            ['openclaw', 'browser', 'screenshot', '--type', 'png', '--output', cover_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        screenshot_out, screenshot_err = screenshot_result.communicate(timeout=30)
        
        if os.path.exists(cover_path) and os.path.getsize(cover_path) > 0:
            print(f"✅ 封面图片已生成：{cover_path}")
            return cover_path
        else:
            print("⚠️  截图失败")
            return None
    except Exception as e:
        print(f"⚠️  生成封面失败：{e}")
        return None
    finally:
        server_proc.terminate()

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
    """生成文章内容（800 字左右）"""
    if topic_type == "节气养生":
        return """
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">节气养生</strong></section>
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
                <p style="margin-bottom: 15px;">中医认为，顺应四时变化养生，可以达到事半功倍的效果。此时人体阳气逐渐升发，肝气旺盛，脾胃功能相对较弱，容易出现湿气困脾的情况。谷雨时节降雨增多，空气湿度大，外湿容易侵袭人体，导致脾胃运化功能失常，出现食欲不振、疲倦乏力等症状。此时养生应以健脾祛湿、疏肝理气为主，为夏季的健康打下基础。</p>
                
                <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，保持充足睡眠。建议晚上 11 点前入睡，早上 6-7 点起床，顺应自然界阳气升发的规律。午间可适当小憩 15-30 分钟，但不宜过长，以免影响夜间睡眠。保持室内通风干燥，避免潮湿环境。衣物要适时增减，防止受凉感冒。</p>
                <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃时令蔬菜。推荐食用山药、薏米、赤小豆等健脾祛湿的食材，少吃生冷、油腻、甜食，以免加重脾胃负担。可适当食用辛温发散的食物，如葱、姜、蒜等，帮助阳气升发。多喝温水，促进新陈代谢。早餐要营养丰富，午餐要吃饱，晚餐要清淡适量。</p>
                <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：适度运动，如散步、太极拳、八段锦等。运动可以促进气血运行，帮助排出体内湿气，但不宜过度出汗，以免耗伤阳气。建议每天运动 30-60 分钟，以微微出汗为度。运动后及时擦干汗水，避免受凉。可选择在早晨或傍晚运动，避开中午高温时段。</p>
                <p style="margin-bottom: 15px;">4. <strong>情志调节</strong>：保持心情舒畅，避免情绪波动。中医认为"怒伤肝"，情绪不稳定会影响肝的疏泄功能。可通过听音乐、读书、与朋友聊天等方式调节情绪，保持乐观心态。培养兴趣爱好，如养花、书法、绘画等，陶冶情操，放松身心。</p>
                
                <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
                <p style="margin-bottom: 15px;">• <strong>山药薏米粥</strong>：山药 30g、薏米 20g、大米 50g，煮粥食用，健脾祛湿。适合脾胃虚弱、湿气重者</p>
                <p style="margin-bottom: 15px;">• <strong>赤小豆冬瓜汤</strong>：赤小豆 30g、冬瓜 200g，煮汤饮用，利水消肿。适合水肿、小便不利者</p>
                <p style="margin-bottom: 15px;">• <strong>菊花枸杞茶</strong>：菊花 5g、枸杞 10g，沸水冲泡，清肝明目。适合眼睛干涩、肝火旺盛者</p>
                <p style="margin-bottom: 15px;">• <strong>陈皮普洱茶</strong>：陈皮 5g、普洱茶 3g，沸水冲泡，理气健脾。适合消化不良、腹胀者</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 避免过度劳累，注意休息，劳逸结合</p>
                <p style="margin-bottom: 15px;">• 注意保暖，尤其是早晚温差大时，防止受凉感冒</p>
                <p style="margin-bottom: 15px;">• 如有不适症状，及时就医，不要自行用药</p>
                <p style="margin-bottom: 15px;">• 过敏体质者避免接触花粉等过敏原</p>
                <p style="margin-bottom: 15px;">• 慢性病患者要按时服药，定期复查</p>
            </section>
        </section>
        """
    elif topic_type == "中医食疗":
        return """
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">节气养生</strong></section>
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
                <p style="margin-bottom: 15px;">中医认为，顺应四时变化养生，可以达到事半功倍的效果。此时人体阳气逐渐升发，肝气旺盛，脾胃功能相对较弱，容易出现湿气困脾的情况。谷雨时节降雨增多，空气湿度大，外湿容易侵袭人体，导致脾胃运化功能失常，出现食欲不振、疲倦乏力等症状。</p>
                
                <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，保持充足睡眠。建议晚上 11 点前入睡，早上 6-7 点起床，顺应自然界阳气升发的规律。午间可适当小憩 15-30 分钟，但不宜过长，以免影响夜间睡眠。保持室内通风干燥，避免潮湿环境。</p>
                <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃时令蔬菜。推荐食用山药、薏米、赤小豆等健脾祛湿的食材，少吃生冷、油腻、甜食，以免加重脾胃负担。可适当食用辛温发散的食物，如葱、姜、蒜等，帮助阳气升发。多喝温水，促进新陈代谢。</p>
                <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：适度运动，如散步、太极拳、八段锦等。运动可以促进气血运行，帮助排出体内湿气，但不宜过度出汗，以免耗伤阳气。建议每天运动 30-60 分钟，以微微出汗为度。运动后及时擦干汗水，避免受凉。</p>
                <p style="margin-bottom: 15px;">4. <strong>情志调节</strong>：保持心情舒畅，避免情绪波动。中医认为"怒伤肝"，情绪不稳定会影响肝的疏泄功能。可通过听音乐、读书、与朋友聊天等方式调节情绪，保持乐观心态。</p>
                
                <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
                <p style="margin-bottom: 15px;">• <strong>山药薏米粥</strong>：山药 30g、薏米 20g、大米 50g，煮粥食用，健脾祛湿</p>
                <p style="margin-bottom: 15px;">• <strong>赤小豆冬瓜汤</strong>：赤小豆 30g、冬瓜 200g，煮汤饮用，利水消肿</p>
                <p style="margin-bottom: 15px;">• <strong>菊花枸杞茶</strong>：菊花 5g、枸杞 10g，沸水冲泡，清肝明目</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 避免过度劳累，注意休息，劳逸结合</p>
                <p style="margin-bottom: 15px;">• 注意保暖，尤其是早晚温差大时，防止受凉感冒</p>
                <p style="margin-bottom: 15px;">• 如有不适症状，及时就医，不要自行用药</p>
                <p style="margin-bottom: 15px;">• 过敏体质者避免接触花粉等过敏原</p>
            </section>
        </section>
        """
    elif topic_type == "中医食疗":
        return """
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">中医食疗</strong></section>
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>🍲 食疗原理</strong></p>
                <p style="margin-bottom: 15px;">中医食疗讲究"药食同源"，通过日常饮食调理身体，安全有效。食物具有四气五味，合理搭配可以达到预防疾病、强身健体的目的。失眠多与心脾两虚、肝火扰心等因素有关，通过食疗可以调理脏腑功能，改善睡眠质量。食疗的优势在于副作用小，易于坚持，适合长期调理。现代研究也证实，许多食物中含有调节神经系统的营养成分，如色氨酸、镁、钙等，有助于改善睡眠。</p>
                
                <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
                
                <p style="margin-bottom: 15px;"><strong>食谱一：酸枣仁莲子汤</strong></p>
                <p style="margin-bottom: 15px;">材料：酸枣仁 15g、莲子 20g、百合 15g、冰糖适量</p>
                <p style="margin-bottom: 15px;">做法：酸枣仁捣碎，莲子去心，百合洗净。所有材料放入锅中，加水适量，大火煮沸后转小火煮 30 分钟，加入冰糖调味即可。睡前 1 小时温服，连续服用 2-4 周可见效。酸枣仁可提前炒制，增强安神效果。</p>
                <p style="margin-bottom: 15px;">功效：养心安神，健脾益肾。适合心脾两虚、心悸失眠者食用。酸枣仁具有显著的镇静安神作用，莲子补脾益肾，百合清心安神，三者合用效果更佳。此方对于入睡困难、多梦易醒者尤为适宜。</p>
                
                <p style="margin-bottom: 15px;"><strong>食谱二：桂圆红枣茶</strong></p>
                <p style="margin-bottom: 15px;">材料：桂圆肉 10g、红枣 5 枚、枸杞 10g、红糖适量</p>
                <p style="margin-bottom: 15px;">做法：桂圆肉、红枣（去核）、枸杞洗净，放入茶壶中，沸水冲泡，加盖焖 15 分钟，加入红糖调味即可。每日下午饮用，不宜晚上饮用，以免兴奋神经影响睡眠。可反复冲泡 2-3 次，最后将桂圆肉和红枣吃掉。</p>
                <p style="margin-bottom: 15px;">功效：补益心脾，养血安神。适合气血不足、失眠健忘者饮用。桂圆肉补心脾、益气血，红枣健脾益气，枸杞滋补肝肾，适合女性调理气血。此方对于面色萎黄、心悸怔忡者效果显著。</p>
                
                <p style="margin-bottom: 15px;"><strong>食谱三：小米南瓜粥</strong></p>
                <p style="margin-bottom: 15px;">材料：小米 50g、南瓜 100g、红枣 3 枚</p>
                <p style="margin-bottom: 15px;">做法：小米洗净，南瓜去皮切块，红枣去核。所有材料放入锅中，加水适量，大火煮沸后转小火煮 40 分钟至粥稠即可。晚餐食用，有助于安神助眠。可根据个人口味加入适量蜂蜜或冰糖调味。</p>
                <p style="margin-bottom: 15px;">功效：健脾和胃，安神助眠。适合脾胃虚弱、睡眠不佳者食用。小米含有丰富的色氨酸，有助于合成褪黑素，改善睡眠质量。南瓜富含膳食纤维，有助于肠道健康。此方老少皆宜，尤其适合老年人和儿童。</p>
                
                <p style="margin-bottom: 15px;"><strong>食谱四：核桃芝麻糊</strong></p>
                <p style="margin-bottom: 15px;">材料：核桃仁 30g、黑芝麻 20g、糯米 50g、白糖适量</p>
                <p style="margin-bottom: 15px;">做法：核桃仁、黑芝麻炒香，糯米洗净。所有材料放入料理机中，加水打成糊状，倒入锅中煮沸，加入白糖调味即可。早餐或下午食用，可补充营养，改善睡眠。</p>
                <p style="margin-bottom: 15px;">功效：补肾益精，养血安神。适合肾精不足、失眠健忘者食用。核桃仁补肾益智，黑芝麻滋补肝肾，糯米健脾养胃，三者合用可改善脑力疲劳，提高睡眠质量。</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 食用注意</strong></p>
                <p style="margin-bottom: 15px;">• 食疗需长期坚持，不可急于求成，一般建议连续食用 2-4 周</p>
                <p style="margin-bottom: 15px;">• 孕妇、儿童及特殊人群请在医生指导下食用</p>
                <p style="margin-bottom: 15px;">• 食疗不能替代药物治疗，如失眠严重请及时就医</p>
                <p style="margin-bottom: 15px;">• 避免晚餐过饱，睡前不宜饮茶、咖啡等刺激性饮品</p>
                <p style="margin-bottom: 15px;">• 保持规律作息，创造良好的睡眠环境</p>
                <p style="margin-bottom: 15px;">• 糖尿病患者慎用含糖食疗方，可改用代糖</p>
            </section>
        </section>
        """
    else:  # 穴位保健
        return """
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">穴位保健</strong></section>
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📍 穴位介绍</strong></p>
                <p style="margin-bottom: 15px;">穴位按摩是中医传统保健方法，简单易学，安全有效。通过刺激特定穴位，可以疏通经络、调和气血，达到防病治病的目的。穴位按摩的优势在于无需药物、无副作用，适合日常保健。坚持按摩可以增强体质，预防疾病，提高生活质量。现代研究表明，穴位按摩可以调节神经系统、内分泌系统和免疫系统功能，具有广泛的保健作用。</p>
                
                <p style="margin-bottom: 15px;"><strong>🔍 穴位定位</strong></p>
                <p style="margin-bottom: 15px;">内关穴位于前臂掌侧，腕横纹上 2 寸（约三横指），掌长肌腱与桡侧腕屈肌腱之间。取穴时，手掌向上，从腕横纹向上量三横指，在两筋之间按压，有酸胀感即是。可先找到腕横纹，再向上量取，反复按压确认酸胀点。每个人的穴位位置可能略有差异，以按压有酸胀感为准。</p>
                
                <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>指按法</strong>：用拇指指腹按压穴位，其余四指托住前臂，固定手腕。按压力度要均匀，不可忽轻忽重。可先轻轻按压，逐渐加力，找到最舒适的力度。</p>
                <p style="margin-bottom: 15px;">2. <strong>力度</strong>：以感觉酸胀为度，不可用力过猛，以免损伤组织。力度应由轻到重，逐渐加力，让身体适应刺激。老年人和儿童力度要适当减轻。</p>
                <p style="margin-bottom: 15px;">3. <strong>时间</strong>：每次按压 3-5 分钟，每日 2-3 次，早晚各一次为宜。可在睡前按摩，有助于改善睡眠。也可在感到心悸、胸闷时随时按压缓解症状。坚持按摩 2-4 周可见明显效果。</p>
                <p style="margin-bottom: 15px;">4. <strong>呼吸</strong>：按压时缓慢深呼吸，放松身心，效果更佳。吸气时放松，呼气时按压，配合呼吸节奏进行。深呼吸可以帮助放松肌肉，增强按摩效果。</p>
                <p style="margin-bottom: 15px;">5. <strong>配穴</strong>：可配合神门穴、心俞穴等，增强安神效果。神门穴位于腕部，心俞穴位于背部，配合使用效果更佳。也可配合足三里、三阴交等穴位，调理全身气血。</p>
                
                <p style="margin-bottom: 15px;"><strong>💡 保健功效</strong></p>
                <p style="margin-bottom: 15px;">• <strong>宁心安神</strong>：缓解心悸、胸闷、失眠、焦虑等症状。适合工作压力大、精神紧张的人群。对于考试焦虑、面试紧张等情况也有缓解作用。</p>
                <p style="margin-bottom: 15px;">• <strong>和胃降逆</strong>：改善恶心、呕吐、胃痛、呃逆等胃部不适。适合胃肠功能紊乱者。对于晕车、孕吐等情况也有一定缓解作用。</p>
                <p style="margin-bottom: 15px;">• <strong>疏通经络</strong>：缓解上肢疼痛、麻木、活动不利等症状。适合长期伏案工作者。对于鼠标手、键盘手等职业病有预防作用。</p>
                <p style="margin-bottom: 15px;">• <strong>预防保健</strong>：日常按摩可强身健体，预防心血管疾病。适合中老年人日常保健。对于高血压、冠心病等慢性病患者，可作为辅助保健方法。</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 饭后 1 小时内不宜按摩，以免影响消化功能</p>
                <p style="margin-bottom: 15px;">• 孕妇慎用，某些穴位可能引起子宫收缩</p>
                <p style="margin-bottom: 15px;">• 皮肤破损、感染处禁止按摩，以免加重感染</p>
                <p style="margin-bottom: 15px;">• 如有严重不适，立即停止并就医，不要强行按摩</p>
                <p style="margin-bottom: 15px;">• 按摩前后喝温水，促进新陈代谢</p>
                <p style="margin-bottom: 15px;">• 保持指甲修剪整齐，避免划伤皮肤</p>
                <p style="margin-bottom: 15px;">• 冬季按摩注意保暖，避免受凉</p>
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
    """统计中文字符数"""
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
    
    # 2. 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 3. 生成并上传封面图片
    print("\n🎨 生成封面图片...")
    cover_path = generate_cover_with_browser(topic_info['title'], topic_info['subtitle'], topic_info['color'])
    
    cover_media_id = DOCTOR_IMAGE_MEDIA_ID  # 默认使用医生照片
    if cover_path:
        print("\n📤 上传封面图片...")
        uploaded_media_id = upload_cover_image(access_token, cover_path)
        if uploaded_media_id:
            cover_media_id = uploaded_media_id
            print("✅ 使用新生成的封面")
        else:
            print("⚠️  上传失败，使用医生照片作为封面")
    else:
        print("⚠️  生成失败，使用医生照片作为封面")
    
    # 4. 生成文章内容
    print("\n✍️  生成文章内容...")
    content = generate_article_content(topic_type, topic_info)
    char_count = count_chinese_chars(content)
    print(f"📊 文章字数：约{char_count}字（目标 800 字左右）")
    
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
