#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康科普文章自动生成并发布工具（使用自定义封面）
- 使用生成的谷雨养生封面图片
- 包含医生照片、二维码、医院信息
- 自动发布到微信公众号草稿箱
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

# 图片素材 ID（已上传）
DOCTOR_IMAGE_MEDIA_ID = "K03y2eZTmx34znaim3BBRy-hW8MwrIRYoS1C9TYHWzs-KFA98jdCEYv-hPoYqtep"
QR_CODE_MEDIA_ID = "K03y2eZTmx34znaim3BBR8vT0SAOIjvDpXukxrl6NjB0b1C_Z9D_ummnCemdfcSN"
COVER_MEDIA_ID = "K03y2eZTmx34znaim3BBR4kTbKiKLgdUEFmkiKJsiJJWkoqame005uol_LqmVMn_"  # 谷雨养生封面

# 医院信息
HOSPITAL_INFO = {
    "name": "郑州金庚中医康复医院",
    "address": "郑州市中牟县芦医庙大街与象湖南路交叉口",
    "phone": "0371-68216120"
}

# 文章主题库
TOPIC_LIBRARY = {
    "节气养生": [
        {"title": "清明养生：踏青祭祖，不忘养肝护阳", "focus": "清明时节阳气上升，肝气旺盛，宜养肝护阳"},
        {"title": "谷雨养生：雨生百谷，祛湿健脾", "focus": "谷雨湿气重，宜健脾祛湿"},
        {"title": "立夏养生：养心安神，防暑降温", "focus": "立夏心气渐旺，宜养心安神"},
    ],
    "中医食疗": [
        {"title": "春季养肝食谱：3 道家常菜，疏肝理气", "focus": "春季养肝，多吃绿色蔬菜"},
        {"title": "失眠怎么办？试试这 3 款安神汤", "focus": "食疗安神，改善睡眠"},
        {"title": "脾胃虚弱？喝这碗粥调理", "focus": "健脾养胃，易消化"},
    ],
    "穴位保健": [
        {"title": "内关穴：护心穴，缓解心悸胸闷", "focus": "内关穴位于手腕，按揉可宁心安神"},
        {"title": "足三里：长寿穴，健脾养胃", "focus": "足三里是保健要穴，强身健体"},
        {"title": "太冲穴：消气穴，疏肝解郁", "focus": "太冲穴位于足背，按揉可疏肝理气"},
    ]
}

def get_access_token():
    """获取微信公众号 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': APPID,
        'secret': APPSECRET
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        raise Exception(f"获取 access_token 失败：{data}")

def generate_article_content(topic_type, topic_info):
    """生成文章内容"""
    title = topic_info["title"]
    focus = topic_info["focus"]
    
    if topic_type == "节气养生":
        content = f"""
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;">
                <strong style="font-size: 18px; color: #2c5530;">{title}</strong>
            </section>
            
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📅 节气特点</strong></p>
                <p style="margin-bottom: 15px;">{focus}。中医认为，顺应四时变化养生，可以达到事半功倍的效果。</p>
                
                <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，保持充足睡眠</p>
                <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃时令蔬菜</p>
                <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：适度运动，如散步、太极拳</p>
                <p style="margin-bottom: 15px;">4. <strong>情志调节</strong>：保持心情舒畅，避免情绪波动</p>
                
                <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
                <p style="margin-bottom: 15px;">• 菊花枸杞茶：清肝明目</p>
                <p style="margin-bottom: 15px;">• 山药粥：健脾养胃</p>
                <p style="margin-bottom: 15px;">• 菠菜汤：养血润燥</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 避免过度劳累，注意休息</p>
                <p style="margin-bottom: 15px;">• 注意保暖，防止受凉</p>
                <p style="margin-bottom: 15px;">• 如有不适，及时就医</p>
            </section>
        </section>
        """
    elif topic_type == "中医食疗":
        content = f"""
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;">
                <strong style="font-size: 18px; color: #2c5530;">{title}</strong>
            </section>
            
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>🍲 食疗原理</strong></p>
                <p style="margin-bottom: 15px;">{focus}。中医食疗讲究"药食同源"，通过日常饮食调理身体，安全有效。</p>
                
                <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
                <p style="margin-bottom: 15px;"><strong>食谱一：山药莲子粥</strong></p>
                <p style="margin-bottom: 15px;">材料：山药 30g、莲子 15g、小米 50g</p>
                <p style="margin-bottom: 15px;">做法：所有材料洗净，加水煮粥，早晚食用</p>
                <p style="margin-bottom: 15px;">功效：健脾养胃，安神助眠</p>
                
                <p style="margin-bottom: 15px;"><strong>食谱二：菊花枸杞茶</strong></p>
                <p style="margin-bottom: 15px;">材料：菊花 5g、枸杞 10g、红枣 3 枚</p>
                <p style="margin-bottom: 15px;">做法：沸水冲泡，代茶饮用</p>
                <p style="margin-bottom: 15px;">功效：清肝明目，养血安神</p>
                
                <p style="margin-bottom: 15px;"><strong>食谱三：百合银耳汤</strong></p>
                <p style="margin-bottom: 15px;">材料：百合 20g、银耳 10g、冰糖适量</p>
                <p style="margin-bottom: 15px;">做法：所有材料炖煮 1 小时，加冰糖调味</p>
                <p style="margin-bottom: 15px;">功效：滋阴润肺，美容养颜</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 食用注意</strong></p>
                <p style="margin-bottom: 15px;">• 食疗需长期坚持，不可急于求成</p>
                <p style="margin-bottom: 15px;">• 孕妇、儿童及特殊人群请咨询医生</p>
                <p style="margin-bottom: 15px;">• 食疗不能替代药物治疗</p>
            </section>
        </section>
        """
    else:
        content = f"""
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;">
                <strong style="font-size: 18px; color: #2c5530;">{title}</strong>
            </section>
            
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📍 穴位介绍</strong></p>
                <p style="margin-bottom: 15px;">{focus}。穴位按摩是中医传统保健方法，简单易学，安全有效。</p>
                
                <p style="margin-bottom: 15px;"><strong>🔍 穴位定位</strong></p>
                <p style="margin-bottom: 15px;">请参照标准穴位图，准确定位穴位位置。</p>
                
                <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>指按法</strong>：用拇指指腹按压穴位</p>
                <p style="margin-bottom: 15px;">2. <strong>力度</strong>：以感觉酸胀为度，不可用力过猛</p>
                <p style="margin-bottom: 15px;">3. <strong>时间</strong>：每次按压 3-5 分钟，每日 2-3 次</p>
                <p style="margin-bottom: 15px;">4. <strong>呼吸</strong>：按压时缓慢深呼吸，放松身心</p>
                
                <p style="margin-bottom: 15px;"><strong>💡 保健功效</strong></p>
                <p style="margin-bottom: 15px;">• 疏通经络，调和气血</p>
                <p style="margin-bottom: 15px;">• 缓解疲劳，强身健体</p>
                <p style="margin-bottom: 15px;">• 预防疾病，延年益寿</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 饭后 1 小时内不宜按摩</p>
                <p style="margin-bottom: 15px;">• 孕妇慎用某些穴位</p>
                <p style="margin-bottom: 15px;">• 皮肤破损处禁止按摩</p>
                <p style="margin-bottom: 15px;">• 如有不适，立即停止并就医</p>
            </section>
        </section>
        """
    
    return content.strip()

def create_doctor_section(doctor_img_url, qr_img_url):
    """生成医生介绍部分"""
    return f"""
    <section style="margin-top: 40px; padding: 20px; background-color: #f5f5f5; border-radius: 10px;">
        <section style="text-align: center; margin-bottom: 20px;">
            <strong style="font-size: 16px; color: #2c5530;">👨‍️ 医生介绍</strong>
        </section>
        
        <section style="display: flex; justify-content: center; align-items: flex-start; margin-bottom: 20px;">
            <section style="flex: 0 0 150px; margin-right: 20px;">
                <img src="{doctor_img_url}" style="width: 150px; height: 200px; object-fit: cover; border-radius: 10px;" alt="娄伯恩医生"/>
            </section>
            <section style="flex: 1; text-align: left; line-height: 1.8;">
                <p style="margin-bottom: 10px;"><strong>娄伯恩</strong> 中医师</p>
                <p style="margin-bottom: 10px;">• 从事中医临床工作多年</p>
                <p style="margin-bottom: 10px;">• 擅长中医养生保健指导</p>
                <p style="margin-bottom: 10px;">• 精通中医食疗与穴位保健</p>
                <p style="margin-bottom: 10px;">• 致力于推广中医健康理念</p>
            </section>
        </section>
        
        <section style="text-align: center; margin-bottom: 20px;">
            <img src="{qr_img_url}" style="width: 150px; height: 150px;" alt="微信二维码"/>
            <p style="font-size: 14px; color: #666; margin-top: 10px;">扫码添加微信 咨询健康问题</p>
        </section>
    </section>
    """

def create_hospital_section():
    """生成医院信息部分"""
    return f"""
    <section style="margin-top: 30px; padding: 20px; background-color: #e8f4ea; border-radius: 10px;">
        <section style="text-align: center; margin-bottom: 20px;">
            <strong style="font-size: 16px; color: #2c5530;">🏥 就诊信息</strong>
        </section>
        
        <section style="line-height: 2; text-align: center;">
            <p style="margin-bottom: 10px;"><strong>医院名称</strong>：{HOSPITAL_INFO["name"]}</p>
            <p style="margin-bottom: 10px;"><strong>医院地址</strong>：{HOSPITAL_INFO["address"]}</p>
            <p style="margin-bottom: 10px;"><strong>咨询电话</strong>：{HOSPITAL_INFO["phone"]}</p>
        </section>
    </section>
    """

def get_image_urls_from_library(access_token):
    """从素材库获取图片 URL"""
    url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material"
    params = {'access_token': access_token}
    data = {'type': 'image', 'offset': 0, 'count': 20}
    json_data = json.dumps(data, ensure_ascii=False)
    
    response = requests.post(url, params=params, data=json_data.encode('utf-8'))
    result = response.json()
    
    urls = {}
    if 'item' in result:
        for item in result['item']:
            media_id = item.get('media_id', '')
            img_url = item.get('url', '')
            if media_id == DOCTOR_IMAGE_MEDIA_ID:
                urls['doctor'] = img_url
            elif media_id == QR_CODE_MEDIA_ID:
                urls['qr'] = img_url
    
    return urls

def create_draft(access_token, title, content, doctor_img_url, qr_img_url, cover_media_id):
    """创建草稿"""
    url = "https://api.weixin.qq.com/cgi-bin/draft/add"
    
    full_content = f"""
    <section style="max-width: 100%; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif;">
        {content}
        {create_doctor_section(doctor_img_url, qr_img_url)}
        {create_hospital_section()}
    </section>
    """
    
    data = {
        "articles": [
            {
                "title": title[:64],
                "author": "娄医",
                "digest": f"中医健康科普 - {title[:30]}",
                "content": full_content,
                "thumb_media_id": cover_media_id,  # 使用自定义封面
                "show_cover_pic": 1
            }
        ]
    }
    
    params = {'access_token': access_token}
    json_data = json.dumps(data, ensure_ascii=False)
    
    response = requests.post(
        url,
        params=params,
        data=json_data.encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    
    return response.json()

def main():
    print("=" * 60)
    print("🚀 健康科普文章发布（使用自定义封面）")
    print("=" * 60)
    
    # 固定使用谷雨养生主题
    topic_type = "节气养生"
    topic_info = {"title": "谷雨养生：雨生百谷，祛湿健脾", "focus": "谷雨湿气重，宜健脾祛湿"}
    
    print(f"\n📝 主题类型：{topic_type}")
    print(f"📰 文章标题：{topic_info['title']}")
    print(f"💡 核心要点：{topic_info['focus']}")
    print(f"🖼️  封面：自定义谷雨养生封面")
    
    # 生成文章内容
    print("\n✍️  生成文章内容...")
    content = generate_article_content(topic_type, topic_info)
    
    # 获取 access_token
    print("\n🔑 获取访问令牌...")
    access_token = get_access_token()
    print("✅ 令牌获取成功")
    
    # 获取图片 URL
    print("\n🖼️  获取图片 URL...")
    img_urls = get_image_urls_from_library(access_token)
    
    doctor_img_url = img_urls.get('doctor', '')
    qr_img_url = img_urls.get('qr', '')
    
    print(f"医生照片 URL: {doctor_img_url[:60]}...")
    print(f"二维码 URL: {qr_img_url[:60]}...")
    
    # 创建草稿
    print("\n📤 发布到微信公众号草稿箱...")
    result = create_draft(access_token, topic_info['title'], content, doctor_img_url, qr_img_url, COVER_MEDIA_ID)
    
    # 处理结果
    if 'media_id' in result:
        print("\n" + "=" * 60)
        print("✅ 发布成功！")
        print("=" * 60)
        print(f"📰 文章标题：{topic_info['title']}")
        print(f"🆔 草稿 ID: {result['media_id']}")
        print(f"🖼️  封面：自定义谷雨养生封面")
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
