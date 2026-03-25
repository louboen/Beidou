#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布工具 - 第二阶段（美化版）
- 中医文化元素封面
- 1500 字左右文章
- 3 张相关插图
"""

import os
import sys
import json
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

def get_access_token():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {'grant_type': 'client_credential', 'appid': APPID, 'secret': APPSECRET}
    response = requests.get(url, params=params)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    raise Exception("获取 access_token 失败")

def generate_cover_html(title, subtitle, theme_color):
    """生成含中医元素的封面 HTML"""
    
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>封面</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a1a;font-family:'Microsoft YaHei',sans-serif}
.cover{width:900px;height:500px;background:linear-gradient(135deg,%s 0%%,%s 50%%,%s 100%%);position:relative;overflow:hidden}
/* 太极图背景 */
.taiji{position:absolute;width:300px;height:300px;top:-50px;right:-50px;opacity:0.1;
background:radial-gradient(circle at 50%% 50%%,#fff 50%%,#000 50%%);
border-radius:50%%;animation:rotate 20s linear infinite}
@keyframes rotate{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
/* 草药装饰 */
.herb{position:absolute;width:100px;height:100px;opacity:0.15}
.herb1{top:50px;left:50px;transform:rotate(30deg)}
.herb2{bottom:80px;right:100px;transform:rotate(-45deg)}
.herb3{top:150px;left:100px;transform:rotate(60deg)}
.content{position:relative;z-index:10;text-align:center;padding-top:100px;color:white;text-shadow:2px 2px 4px rgba(0,0,0,0.6)}
.title{font-size:48px;font-weight:bold;letter-spacing:4px;margin-bottom:15px;
background:linear-gradient(180deg,#fff 0%%,#f0f0f0 100%%);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.subtitle{font-size:28px;font-weight:300;letter-spacing:2px;margin-bottom:30px;opacity:0.95}
.divider{width:150px;height:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);margin:0 auto 20px}
.footer{font-size:16px;opacity:0.85;letter-spacing:1px}
.tcm-badge{position:absolute;bottom:20px;right:20px;font-size:14px;opacity:0.3;
border:2px solid rgba(255,255,255,0.3);padding:5px 10px;border-radius:5px}
</style>
</head>
<body>
<div class="cover">
<div class="taiji"></div>
<div class="herb herb1">🌿</div>
<div class="herb herb2">🍃</div>
<div class="herb herb3">🌱</div>
<div class="content">
<div class="title">%s</div>
<div class="subtitle">%s</div>
<div class="divider"></div>
<div class="footer">中医健康科普 · 娄伯恩医师</div>
</div>
<div class="tcm-badge">中医文化</div>
</div>
</body></html>""" % (theme_color, adjust_color(theme_color, 20), adjust_color(theme_color, 40), title, subtitle)
    
    return html

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

def create_cover_image(title, subtitle, theme_color):
    """生成封面图片"""
    print("🎨 生成封面图片：%s" % title)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_filename = "cover_%s.html" % timestamp
    html_path = os.path.join(ASSETS_DIR, html_filename)
    
    html_content = generate_cover_html(title, subtitle, theme_color)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("📝 HTML 已保存：%s" % html_path)
    
    # 启动 HTTP 服务器
    server_proc = subprocess.Popen(['python3', '-m', 'http.server', '8910'], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    try:
        # 打开页面
        print("📖 打开页面...")
        cmd1 = "openclaw browser open --url 'http://localhost:8910/%s' --target host" % html_filename
        subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(timeout=30)
        time.sleep(2)
        
        # 截图
        print("📸 截图...")
        cmd2 = "openclaw browser screenshot --type png"
        subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(timeout=30)
        time.sleep(1)
        
        # 查找最新图片
        cover_files = glob.glob("/home/admin/.openclaw/media/browser/*.png")
        if cover_files:
            cover_path = max(cover_files, key=os.path.getctime)
            size = os.path.getsize(cover_path)
            print("✅ 封面图片已生成：%s" % cover_path)
            print("   文件大小：%d bytes" % size)
            
            if size < 10000:
                print("⚠️  文件大小异常，可能生成失败")
                return None
            
            return cover_path
        else:
            print("⚠️  未找到生成的图片")
            return None
    except Exception as e:
        print("⚠️  生成封面失败：%s" % e)
        return None
    finally:
        server_proc.terminate()

def generate_illustration_html(prompt, width=600, height=400, bg_color="#f5f5f5"):
    """生成插图 HTML"""
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>插图</title>
<style>
body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#1a1a1a}
.illustration{width:%dpx;height:%dpx;background:%s;position:relative;display:flex;justify-content:center;align-items:center}
.text{font-size:24px;color:#333;text-align:center;padding:20px}
</style>
</head>
<body>
<div class="illustration">
<div class="text">%s</div>
</div>
</body></html>""" % (width, height, bg_color, prompt)
    return html

def create_illustrations(article_type):
    """生成 3 张插图"""
    print("\n🎨 生成插图...")
    
    illustrations = []
    
    # 根据文章类型生成不同的插图提示
    if "风湿" in article_type:
        prompts = [
            ("中医理疗", "#e8f4ea"),
            ("草药调理", "#fff5e8"),
            ("针灸治疗", "#f0e8f4")
        ]
    else:
        prompts = [
            ("中草药", "#e8f4ea"),
            ("中医诊疗", "#fff5e8"),
            ("养生保健", "#f0e8f4")
        ]
    
    for i, (prompt, bg_color) in enumerate(prompts, 1):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = "illustration_%s_%d.html" % (timestamp, i)
        html_path = os.path.join(ASSETS_DIR, html_filename)
        
        html_content = generate_illustration_html(prompt, bg_color=bg_color)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 启动服务器
        server_proc = subprocess.Popen(['python3', '-m', 'http.server', '891%d' % i], cwd=ASSETS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        
        try:
            # 打开页面
            cmd1 = "openclaw browser open --url 'http://localhost:891%d/%s' --target host" % (i, html_filename)
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
                print("✅ 插图%d已生成：%s" % (i, prompt))
                illustrations.append((prompt, img_path))
        except Exception as e:
            print("⚠️  插图%d生成失败：%s" % (i, e))
            illustrations.append((prompt, None))
        finally:
            server_proc.terminate()
    
    return illustrations

def get_rheumatism_content():
    """生成春季风湿病治疗文章（1500 字左右）"""
    return """<section style="max-width: 100%; box-sizing: border-box;">
    <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 22px; color: #2c5530;">春季风湿病的治疗</strong></section>
    
    <section style="margin-bottom: 20px; line-height: 1.8;">
        <p style="margin-bottom: 15px;"><strong>📅 春季风湿病高发的原因</strong></p>
        <p style="margin-bottom: 15px;">春季是风湿病的高发季节，主要原因有以下几点：首先，春季气温变化较大，早晚温差明显，人体适应能力下降，容易受到风寒湿邪的侵袭。其次，春季雨水增多，空气湿度大，湿气容易困阻脾胃，导致气血运行不畅。第三，春季阳气初升，人体腠理疏松，外邪容易乘虚而入。最后，春季肝气旺盛，肝主筋，肝气不舒则筋脉失养，容易引发关节疼痛。</p>
        <p style="margin-bottom: 15px;">从中医角度来看，风湿病属于"痹证"范畴，主要由风、寒、湿三气杂至，合而为痹。《黄帝内经》云："风寒湿三气杂至，合而为痹也。其风气胜者为行痹，寒气胜者为痛痹，湿气胜者为着痹。"春季风湿病多以行痹和痛痹为主，表现为关节游走性疼痛、遇寒加重、得温则减等症状。</p>
        
        <p style="margin-bottom: 15px;"><strong>🔍 风湿病的中医辨证分型</strong></p>
        <p style="margin-bottom: 15px;"><strong>1. 风寒湿痹型</strong></p>
        <p style="margin-bottom: 15px;">症状：关节疼痛，游走不定，遇寒加重，得温则减，舌淡苔白，脉浮紧。此型多见于风湿病早期，外邪初犯，正气未虚。</p>
        <p style="margin-bottom: 15px;">治法：祛风散寒，除湿通络。</p>
        <p style="margin-bottom: 15px;">方药：防风汤加减。常用药物：防风 15g、羌活 12g、独活 12g、桂枝 10g、秦艽 12g、当归 12g、川芎 10g、甘草 6g。</p>
        
        <p style="margin-bottom: 15px;"><strong>2. 风湿热痹型</strong></p>
        <p style="margin-bottom: 15px;">症状：关节红肿热痛，活动受限，发热口渴，小便黄赤，舌红苔黄腻，脉滑数。此型多见于风湿病急性发作期。</p>
        <p style="margin-bottom: 15px;">治法：清热利湿，通络止痛。</p>
        <p style="margin-bottom: 15px;">方药：白虎加桂枝汤加减。常用药物：生石膏 30g（先煎）、知母 12g、桂枝 10g、黄柏 12g、苍术 12g、牛膝 12g、薏苡仁 30g、甘草 6g。</p>
        
        <p style="margin-bottom: 15px;"><strong>3. 肝肾亏虚型</strong></p>
        <p style="margin-bottom: 15px;">症状：关节疼痛日久，腰膝酸软，头晕耳鸣，神疲乏力，舌淡苔白，脉沉细。此型多见于风湿病后期，久病伤及肝肾。</p>
        <p style="margin-bottom: 15px;">治法：补益肝肾，强筋壮骨。</p>
        <p style="margin-bottom: 15px;">方药：独活寄生汤加减。常用药物：独活 12g、桑寄生 15g、杜仲 12g、牛膝 12g、细辛 3g、秦艽 12g、茯苓 12g、肉桂 6g、防风 10g、川芎 10g、党参 15g、当归 12g、白芍 12g、熟地黄 15g、甘草 6g。</p>
        
        <p style="margin-bottom: 15px;"><strong>💊 中医治疗方法</strong></p>
        <p style="margin-bottom: 15px;"><strong>1. 中药内服</strong></p>
        <p style="margin-bottom: 15px;">根据辨证分型选择合适的方剂，一般疗程为 2-4 周。服药期间注意观察病情变化，及时调整方药。同时配合饮食调理，忌食生冷、油腻、辛辣食物。</p>
        
        <p style="margin-bottom: 15px;"><strong>2. 中药外治</strong></p>
        <p style="margin-bottom: 15px;">• <strong>中药熏洗</strong>：用艾叶 30g、红花 15g、伸筋草 30g、透骨草 30g，煎水熏洗患处，每日 1-2 次，每次 20-30 分钟。可温经通络，祛风除湿。</p>
        <p style="margin-bottom: 15px;">• <strong>中药贴敷</strong>：用川乌、草乌、细辛、白芷等研末，用白酒或醋调成糊状，敷于患处，每日 1 次，每次 4-6 小时。可温经散寒，活血止痛。</p>
        <p style="margin-bottom: 15px;">• <strong>中药熨敷</strong>：用粗盐 500g 炒热，加入艾叶、红花、伸筋草等中药，装入布袋，熨敷患处，每日 1-2 次。可温经散寒，活血通络。</p>
        
        <p style="margin-bottom: 15px;"><strong>3. 针灸治疗</strong></p>
        <p style="margin-bottom: 15px;">取穴：阿是穴（痛点）、足三里、阳陵泉、阴陵泉、血海、梁丘、膝眼等。手法：平补平泻，留针 20-30 分钟，每日或隔日 1 次，10 次为一疗程。针灸可疏通经络，调和气血，缓解疼痛。</p>
        
        <p style="margin-bottom: 15px;"><strong>4. 推拿按摩</strong></p>
        <p style="margin-bottom: 15px;">在患处及周围穴位进行揉、按、推、拿等手法，每次 20-30 分钟，每日 1 次。可舒筋活络，缓解肌肉痉挛，改善关节活动度。</p>
        
        <p style="margin-bottom: 15px;"><strong>🌿 日常调护</strong></p>
        <p style="margin-bottom: 15px;">1. <strong>注意保暖</strong>：春季气温变化大，要注意及时增减衣物，特别是关节部位要保暖，避免受凉。</p>
        <p style="margin-bottom: 15px;">2. <strong>适度运动</strong>：选择温和的运动方式，如散步、太极拳、八段锦等，避免剧烈运动加重关节负担。运动前要做好热身活动。</p>
        <p style="margin-bottom: 15px;">3. <strong>饮食调理</strong>：多食用温性食物，如生姜、葱、蒜、羊肉等，少吃生冷、寒凉食物。可适当食用祛湿食物，如薏米、赤小豆、冬瓜等。</p>
        <p style="margin-bottom: 15px;">4. <strong>情志调节</strong>：保持心情舒畅，避免情绪波动。中医认为"肝主筋"，情志不舒会影响肝的疏泄功能，加重病情。</p>
        <p style="margin-bottom: 15px;">5. <strong>规律作息</strong>：保证充足睡眠，避免熬夜。睡眠充足有利于气血恢复，增强机体抗病能力。</p>
        
        <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
        <p style="margin-bottom: 15px;">• 风湿病是慢性病，治疗需要耐心，不可急于求成</p>
        <p style="margin-bottom: 15px;">• 遵医嘱用药，不可自行增减药量或停药</p>
        <p style="margin-bottom: 15px;">• 定期复诊，根据病情调整治疗方案</p>
        <p style="margin-bottom: 15px;">• 如出现关节红肿热痛加重、发热等情况，及时就医</p>
        <p style="margin-bottom: 15px;">• 孕妇、儿童及特殊人群请在医生指导下治疗</p>
    </section>
</section>"""

def upload_image(access_token, image_path):
    """上传图片到素材库"""
    print("📤 上传图片...")
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, params=params, files=files)
    
    data = response.json()
    if 'media_id' in data:
        print("✅ 上传成功！MediaID: %s" % data['media_id'][:50])
        return data['media_id']
    else:
        print("❌ 上传失败：%s" % data)
        return None

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

def create_draft(access_token, title, content, doctor_img_url, qr_img_url, cover_media_id, illustration_media_ids):
    """创建草稿"""
    url = "https://api.weixin.qq.com/cgi-bin/draft/add"
    
    # 在内容中插入插图
    content_with_images = insert_illustrations(content, illustration_media_ids)
    
    full_content = content_with_images + create_doctor_section(doctor_img_url, qr_img_url) + create_hospital_section()
    
    data = {
        "articles": [{
            "title": title[:64],
            "author": "娄医",
            "digest": "中医健康科普 - %s" % title[:30],
            "content": full_content,
            "thumb_media_id": cover_media_id,
            "show_cover_pic": 1
        }]
    }
    params = {'access_token': access_token}
    response = requests.post(url, params=params, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'})
    return response.json()

def insert_illustrations(content, illustration_media_ids):
    """在内容中插入插图"""
    # 找到合适的位置插入图片
    parts = content.split('</section>')
    
    # 在三个位置插入插图
    insert_positions = [3, 7, 11]  # 在第 3、7、11 个 section 后插入
    
    for i, media_id in enumerate(illustration_media_ids):
        if media_id and i < len(insert_positions):
            pos = insert_positions[i]
            if pos < len(parts):
                img_html = '<p style="text-align:center;margin:20px 0;"><img src="%s" style="max-width:100%%;height:auto;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);"/></p>' % media_id
                parts.insert(pos, img_html)
    
    return '</section>'.join(parts)

def create_doctor_section(doctor_img_url, qr_img_url):
    return """
    <section style="margin-top: 40px; padding: 20px; background-color: #f5f5f5; border-radius: 10px;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 16px; color: #2c5530;">👨‍⚕️ 医生介绍</strong></section>
        <section style="display: flex; justify-content: center; align-items: flex-start; margin-bottom: 20px;">
            <section style="flex: 0 0 150px; margin-right: 20px;"><img src="%s" style="width: 150px; height: 200px; object-fit: cover; border-radius: 10px;"/></section>
            <section style="flex: 1; text-align: left; line-height: 1.8;">
                <p style="margin-bottom: 10px;"><strong>娄伯恩</strong> 主治医师</p>
                <p style="margin-bottom: 8px; font-size: 14px;">宋氏中医传承人 | 娄氏风湿病传承人</p>
                <p style="margin-bottom: 10px; font-size: 13px; color: #555;">出身于中医世家，毕业于河南中医学院中医骨伤系，曾在北京积水潭医院中医正骨科进修学习。临床中以虚、邪、瘀治痹理论为基础，中西医结合，辨证论治，在疼痛、骨伤、风湿病的诊治过程中积累丰富经验。</p>
                <p style="margin-bottom: 10px; font-size: 13px; color: #555;"><strong>擅长治疗</strong>：各类关节肌肉疼痛疾病，颈肩腰腿痛，骨折病，关节陈旧性损伤，风湿、类风湿、痛风关节炎。</p>
            </section>
        </section>
        <section style="text-align: center; margin-bottom: 20px;">
            <img src="%s" style="width: 150px; height: 150px;"/>
            <p style="font-size: 14px; color: #666; margin-top: 10px;">扫码添加微信 咨询健康问题</p>
        </section>
    </section>
    """ % (doctor_img_url, qr_img_url)

def create_hospital_section():
    return """
    <section style="margin-top: 30px; padding: 20px; background-color: #e8f4ea; border-radius: 10px;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 16px; color: #2c5530;">🏥 就诊信息</strong></section>
        <section style="line-height: 2; text-align: center;">
            <p style="margin-bottom: 10px;"><strong>医院名称</strong>：%s</p>
            <p style="margin-bottom: 10px;"><strong>医院地址</strong>：%s</p>
            <p style="margin-bottom: 10px;"><strong>咨询电话</strong>：%s</p>
        </section>
    </section>
    """ % (HOSPITAL_INFO["name"], HOSPITAL_INFO["address"], HOSPITAL_INFO["phone"])

def count_chinese_chars(text):
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])

def main():
    print("=" * 60)
    print("🚀 微信公众号文章发布 - 第二阶段（美化版）")
    print("=" * 60)
    
    # 测试主题：春季风湿病的治疗
    title = "春季风湿病的治疗"
    subtitle = "中医辨证施治 标本兼治"
    theme_color = "#4a8f5a"  # 中医绿色
    
    print("\n📝 文章标题：%s" % title)
    print("🎨 主题颜色：%s" % theme_color)
    
    # 1. 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 2. 生成封面
    print("\n🎨 生成封面图片...")
    cover_path = create_cover_image(title, subtitle, theme_color)
    
    cover_media_id = DOCTOR_IMAGE_MEDIA_ID
    if cover_path:
        media_id = upload_image(access_token, cover_path)
        if media_id:
            cover_media_id = media_id
            print("\n✅ 封面已上传到素材库")
        else:
            print("\n⚠️  上传失败，使用医生照片")
    else:
        print("\n⚠️  生成失败，使用医生照片")
    
    # 3. 生成 3 张插图
    illustrations = create_illustrations("风湿病")
    illustration_media_ids = []
    
    for prompt, img_path in illustrations:
        if img_path:
            media_id = upload_image(access_token, img_path)
            illustration_media_ids.append(media_id if media_id else None)
        else:
            illustration_media_ids.append(None)
    
    # 4. 生成文章内容
    print("\n✍️  生成文章内容...")
    content = get_rheumatism_content()
    char_count = count_chinese_chars(content)
    print("📊 文章字数：%d 字" % char_count)
    
    # 5. 获取图片 URL
    print("\n🖼️  获取图片 URL...")
    img_urls = get_image_urls(access_token)
    doctor_img_url = img_urls.get('doctor', '')
    qr_img_url = img_urls.get('qr', '')
    
    # 6. 创建草稿
    print("\n📤 发布到微信公众号草稿箱...")
    result = create_draft(access_token, title, content, doctor_img_url, qr_img_url, cover_media_id, illustration_media_ids)
    
    # 7. 处理结果
    if 'media_id' in result:
        print("\n" + "=" * 60)
        print("✅ 发布成功！")
        print("=" * 60)
        print("📰 文章标题：%s" % title)
        print("🆔 草稿 ID: %s" % result['media_id'])
        print("📊 文章字数：%d 字" % char_count)
        print("🖼️  插图数量：%d 张" % len([x for x in illustration_media_ids if x]))
        print("⏰ 发布时间：%s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("\n📱 请登录微信公众平台预览：")
        print("   https://mp.weixin.qq.com")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ 发布失败！")
        print("=" * 60)
        print("错误代码：%s" % result.get('errcode', 'Unknown'))
        print("错误信息：%s" % result.get('errmsg', 'Unknown error'))
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
