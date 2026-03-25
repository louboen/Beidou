#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布已确认封面的文章
"""

import os
import sys
import json
import requests
from datetime import datetime

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

def upload_cover(access_token, cover_path):
    """上传封面到素材库"""
    print("📤 上传封面到素材库...")
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    with open(cover_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, params=params, files=files)
    
    data = response.json()
    if 'media_id' in data:
        print("✅ 封面上传成功！")
        print("   MediaID: %s" % data['media_id'])
        return data['media_id']
    else:
        print("❌ 封面上传失败：%s" % data)
        return None

def get_qingming_content():
    return """<section style="max-width: 100%; box-sizing: border-box;">
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
    </section>"""

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
    full_content = content + create_doctor_section(doctor_img_url, qr_img_url) + create_hospital_section()
    
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

def main():
    print("=" * 60)
    print("🚀 发布清明养生文章")
    print("=" * 60)
    
    # 1. 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 2. 获取图片 URL
    print("\n🖼️  获取图片 URL...")
    img_urls = get_image_urls(access_token)
    doctor_img_url = img_urls.get('doctor', '')
    qr_img_url = img_urls.get('qr', '')
    print("医生照片：%s" % ('✅' if doctor_img_url else '❌'))
    print("二维码：%s" % ('✅' if qr_img_url else '❌'))
    
    # 3. 上传封面
    cover_path = "/home/admin/.openclaw/media/browser/b69db9c7-a75d-45b5-b2c5-d4db7fced74c.png"
    cover_media_id = upload_cover(access_token, cover_path)
    
    if not cover_media_id:
        print("❌ 封面上传失败，使用医生照片")
        cover_media_id = DOCTOR_IMAGE_MEDIA_ID
    
    # 4. 生成文章内容
    print("\n✍️  生成文章内容...")
    content = get_qingming_content()
    print("✅ 内容已生成")
    
    # 5. 创建草稿
    print("\n📤 发布到微信公众号草稿箱...")
    result = create_draft(access_token, "清明养生", content, doctor_img_url, qr_img_url, cover_media_id)
    
    # 6. 处理结果
    if 'media_id' in result:
        print("\n" + "=" * 60)
        print("✅ 发布成功！")
        print("=" * 60)
        print("📰 文章标题：清明养生")
        print("🆔 草稿 ID: %s" % result['media_id'])
        print("🖼️  封面 MediaID: %s" % cover_media_id)
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
