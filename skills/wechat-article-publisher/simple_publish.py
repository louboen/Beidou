#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康科普文章发布工具 - 简化版
策略：使用医生照片作为统一封面，避免封面匹配问题
"""

import os
import sys
import json
import random
import requests
from datetime import datetime

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"

# 图片素材 ID - 统一使用医生照片作为封面
COVER_MEDIA_ID = "K03y2eZTmx34znaim3BBRy-hW8MwrIRYoS1C9TYHWzs-KFA98jdCEYv-hPoYqtep"
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
        {"title": "谷雨养生", "content_func": "get_guyu_content"},
        {"title": "清明养生", "content_func": "get_qingming_content"},
        {"title": "立夏养生", "content_func": "get_lixia_content"},
    ],
    "中医食疗": [
        {"title": "失眠怎么办", "content_func": "get_shimian_content"},
        {"title": "脾胃虚弱", "content_func": "get_sipiwei_content"},
        {"title": "春季养肝", "content_func": "get_yanggan_content"},
    ],
    "穴位保健": [
        {"title": "内关穴", "content_func": "get_neiguan_content"},
        {"title": "足三里", "content_func": "get_zusanli_content"},
        {"title": "太冲穴", "content_func": "get_taichong_content"},
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

# 内容生成函数
def get_guyu_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">谷雨养生</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
            <p style="margin-bottom: 15px;">谷雨是春季的最后一个节气，此时降雨增多，空气湿度大，故有"雨生百谷"之说。中医认为，谷雨时节阳气逐渐升发，肝气旺盛，脾胃功能相对较弱，容易出现湿气困脾的情况。</p>
            <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
            <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，保持充足睡眠</p>
            <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃时令蔬菜</p>
            <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：适度运动，如散步、太极拳</p>
            <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
            <p style="margin-bottom: 15px;">• 山药薏米粥：健脾祛湿</p>
            <p style="margin-bottom: 15px;">• 赤小豆冬瓜汤：利水消肿</p>
            <p style="margin-bottom: 15px;">• 菊花枸杞茶：清肝明目</p>
        </section>
    </section>"""

def get_qingming_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">清明养生</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
            <p style="margin-bottom: 15px;">清明时节，气温转暖，草木萌发，万物欣欣向荣。此时人体阳气也开始升发，肝气旺盛。</p>
            <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
            <p style="margin-bottom: 15px;">1. 起居调养：早睡早起</p>
            <p style="margin-bottom: 15px;">2. 饮食调理：清淡为主</p>
            <p style="margin-bottom: 15px;">3. 运动保健：踏青、散步</p>
        </section>
    </section>"""

def get_lixia_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">立夏养生</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
            <p style="margin-bottom: 15px;">立夏是夏季的第一个节气，标志着夏天的开始。此时气温逐渐升高，人体阳气外发，心气渐旺。</p>
            <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
            <p style="margin-bottom: 15px;">1. 起居调养：晚睡早起</p>
            <p style="margin-bottom: 15px;">2. 饮食调理：清淡解暑</p>
            <p style="margin-bottom: 15px;">3. 运动保健：温和运动</p>
        </section>
    </section>"""

def get_sipiwei_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">脾胃调理</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>🍲 脾胃重要性</strong></p>
            <p style="margin-bottom: 15px;">中医认为"脾胃为后天之本"，脾胃功能好坏直接影响消化吸收和气血生化。</p>
            <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
            <p style="margin-bottom: 15px;">• 山药莲子粥：健脾养胃</p>
            <p style="margin-bottom: 15px;">• 陈皮白术茶：健脾益气</p>
            <p style="margin-bottom: 15px;">• 南瓜小米粥：健脾和胃</p>
        </section>
    </section>"""

def get_shimian_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">失眠调理</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>🍲 失眠原因</strong></p>
            <p style="margin-bottom: 15px;">中医认为失眠多与心脾两虚、肝火扰心等因素有关。</p>
            <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
            <p style="margin-bottom: 15px;">• 酸枣仁莲子汤：养心安神</p>
            <p style="margin-bottom: 15px;">• 桂圆红枣茶：补益心脾</p>
        </section>
    </section>"""

def get_yanggan_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">春季养肝</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>🍲 养肝重要性</strong></p>
            <p style="margin-bottom: 15px;">中医认为"春气与肝气相通"，春季是养肝护肝的最佳时节。</p>
            <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
            <p style="margin-bottom: 15px;">• 菊花枸杞茶：清肝明目</p>
            <p style="margin-bottom: 15px;">• 菠菜猪肝汤：养血补肝</p>
        </section>
    </section>"""

def get_neiguan_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">内关穴</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📍 穴位定位</strong></p>
            <p style="margin-bottom: 15px;">内关穴位于前臂掌侧，腕横纹上 2 寸。</p>
            <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
            <p style="margin-bottom: 15px;">用拇指按压 3-5 分钟</p>
        </section>
    </section>"""

def get_zusanli_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">足三里</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📍 穴位定位</strong></p>
            <p style="margin-bottom: 15px;">足三里位于小腿外侧，犊鼻穴下 3 寸。</p>
            <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
            <p style="margin-bottom: 15px;">用拇指按压 3-5 分钟</p>
        </section>
    </section>"""

def get_taichong_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 18px; color: #2c5530;">太冲穴</strong></section>
        <section style="margin-bottom: 20px; line-height: 1.8;">
            <p style="margin-bottom: 15px;"><strong>📍 穴位定位</strong></p>
            <p style="margin-bottom: 15px;">太冲穴位于足背侧，第 1、2 跖骨结合部之前。</p>
            <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
            <p style="margin-bottom: 15px;">用拇指按压 3-5 分钟</p>
        </section>
    </section>"""

def create_doctor_section(doctor_img_url, qr_img_url):
    return f"""
    <section style="margin-top: 40px; padding: 20px; background-color: #f5f5f5; border-radius: 10px;">
        <section style="text-align: center; margin-bottom: 20px;"><strong style="font-size: 16px; color: #2c5530;">👨‍⚕️ 医生介绍</strong></section>
        <section style="display: flex; justify-content: center; align-items: flex-start; margin-bottom: 20px;">
            <section style="flex: 0 0 150px; margin-right: 20px;"><img src="{doctor_img_url}" style="width: 150px; height: 200px; object-fit: cover; border-radius: 10px;"/></section>
            <section style="flex: 1; text-align: left; line-height: 1.8;">
                <p style="margin-bottom: 10px;"><strong>娄伯恩</strong> 主治医师</p>
                <p style="margin-bottom: 8px; font-size: 14px;">宋氏中医传承人 | 娄氏风湿病传承人</p>
                <p style="margin-bottom: 10px; font-size: 13px; color: #555;">出身于中医世家，毕业于河南中医学院中医骨伤系，曾在北京积水潭医院中医正骨科进修学习。临床中以虚、邪、瘀治痹理论为基础，中西医结合，辨证论治，在疼痛、骨伤、风湿病的诊治过程中积累丰富经验。</p>
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

def create_draft(access_token, title, content, doctor_img_url, qr_img_url):
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
            "thumb_media_id": COVER_MEDIA_ID,  # 统一使用医生照片作为封面
            "show_cover_pic": 1
        }]
    }
    params = {'access_token': access_token}
    response = requests.post(url, params=params, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'})
    return response.json()

def main():
    print("=" * 60)
    print("🚀 健康科普文章发布（简化版 - 统一封面）")
    print("=" * 60)
    print("\n📌 策略：使用医生照片作为统一封面")
    print("   避免封面与文章标题不匹配的问题\n")
    
    # 1. 随机选择主题
    topic_type = random.choice(list(TOPIC_LIBRARY.keys()))
    topic_info = random.choice(TOPIC_LIBRARY[topic_type])
    
    print(f"📝 主题类型：{topic_type}")
    print(f"📰 文章标题：{topic_info['title']}")
    
    # 2. 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 3. 获取图片 URL
    print("\n🖼️  获取图片 URL...")
    img_urls = get_image_urls(access_token)
    doctor_img_url = img_urls.get('doctor', '')
    qr_img_url = img_urls.get('qr', '')
    print(f"医生照片：{'✅' if doctor_img_url else '❌'}")
    print(f"二维码：{'✅' if qr_img_url else '❌'}")
    
    # 4. 生成文章内容
    print("\n✍️  生成文章内容...")
    content_func = globals()[topic_info['content_func']]
    content = content_func()
    print(f"✅ 内容已生成")
    
    # 5. 创建草稿
    print("\n📤 发布到微信公众号草稿箱...")
    print(f"   使用封面：医生照片（统一封面）")
    result = create_draft(access_token, topic_info['title'], content, doctor_img_url, qr_img_url)
    
    # 6. 处理结果
    if 'media_id' in result:
        print("\n" + "=" * 60)
        print("✅ 发布成功！")
        print("=" * 60)
        print(f"📰 文章标题：{topic_info['title']}")
        print(f"🆔 草稿 ID: {result['media_id']}")
        print(f"🖼️  封面：医生照片（统一）")
        print(f"⏰ 发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📱 请登录微信公众平台预览：")
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
