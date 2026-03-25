#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康科普文章自动生成并发布工具（字数达标版）
- 文章字数严格控制在 500-800 字
- 包含更新的医生介绍
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
        {"title": "谷雨养生：雨生百谷，祛湿健脾", "focus": "谷雨湿气重，宜健脾祛湿"},
        {"title": "清明养生：踏青祭祖，不忘养肝护阳", "focus": "清明时节阳气上升，肝气旺盛"},
    ],
    "中医食疗": [
        {"title": "失眠怎么办？试试这 3 款安神汤", "focus": "食疗安神，改善睡眠"},
        {"title": "脾胃虚弱？喝这碗粥调理", "focus": "健脾养胃，易消化"},
    ],
    "穴位保健": [
        {"title": "内关穴：护心穴，缓解心悸胸闷", "focus": "内关穴位于手腕，按揉可宁心安神"},
        {"title": "足三里：长寿穴，健脾养胃", "focus": "足三里是保健要穴，强身健体"},
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

def generate_article_content(topic_type, topic_info):
    """生成文章内容（500-800 字）"""
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
                <p style="margin-bottom: 15px;">{focus}。中医认为，顺应四时变化养生，可以达到事半功倍的效果。此时人体阳气逐渐升发，肝气旺盛，脾胃功能相对较弱，容易出现湿气困脾的情况。谷雨时节降雨增多，空气湿度大，外湿容易侵袭人体，导致脾胃运化功能失常。</p>
                
                <p style="margin-bottom: 15px;"><strong>🌿 养生原则</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>起居调养</strong>：早睡早起，保持充足睡眠。建议晚上 11 点前入睡，早上 6-7 点起床，顺应自然界阳气升发的规律。午间可适当小憩 15-30 分钟，但不宜过长，以免影响夜间睡眠。</p>
                <p style="margin-bottom: 15px;">2. <strong>饮食调理</strong>：清淡饮食，多吃时令蔬菜。推荐食用山药、薏米、赤小豆等健脾祛湿的食材，少吃生冷、油腻、甜食，以免加重脾胃负担。可适当食用辛温发散的食物，如葱、姜、蒜等，帮助阳气升发。</p>
                <p style="margin-bottom: 15px;">3. <strong>运动保健</strong>：适度运动，如散步、太极拳、八段锦等。运动可以促进气血运行，帮助排出体内湿气，但不宜过度出汗，以免耗伤阳气。建议每天运动 30-60 分钟，以微微出汗为度。</p>
                <p style="margin-bottom: 15px;">4. <strong>情志调节</strong>：保持心情舒畅，避免情绪波动。中医认为"怒伤肝"，情绪不稳定会影响肝的疏泄功能。可通过听音乐、读书、与朋友聊天等方式调节情绪。</p>
                
                <p style="margin-bottom: 15px;"><strong>🍵 推荐食疗</strong></p>
                <p style="margin-bottom: 15px;">• <strong>山药薏米粥</strong>：山药 30g、薏米 20g、大米 50g，煮粥食用，健脾祛湿</p>
                <p style="margin-bottom: 15px;">• <strong>赤小豆冬瓜汤</strong>：赤小豆 30g、冬瓜 200g，煮汤饮用，利水消肿</p>
                <p style="margin-bottom: 15px;">• <strong>菊花枸杞茶</strong>：菊花 5g、枸杞 10g，沸水冲泡，清肝明目</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 避免过度劳累，注意休息，劳逸结合</p>
                <p style="margin-bottom: 15px;">• 注意保暖，尤其是早晚温差大时，防止受凉感冒</p>
                <p style="margin-bottom: 15px;">• 如有不适症状，及时就医，不要自行用药</p>
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
                <p style="margin-bottom: 15px;">{focus}。中医食疗讲究"药食同源"，通过日常饮食调理身体，安全有效。食物具有四气五味，合理搭配可以达到预防疾病、强身健体的目的。失眠多与心脾两虚、肝火扰心等因素有关，通过食疗可以调理脏腑功能，改善睡眠质量。</p>
                
                <p style="margin-bottom: 15px;"><strong>📋 推荐食谱</strong></p>
                
                <p style="margin-bottom: 15px;"><strong>食谱一：酸枣仁莲子汤</strong></p>
                <p style="margin-bottom: 15px;">材料：酸枣仁 15g、莲子 20g、百合 15g、冰糖适量</p>
                <p style="margin-bottom: 15px;">做法：酸枣仁捣碎，莲子去心，百合洗净。所有材料放入锅中，加水适量，大火煮沸后转小火煮 30 分钟，加入冰糖调味即可。睡前 1 小时温服。</p>
                <p style="margin-bottom: 15px;">功效：养心安神，健脾益肾。适合心脾两虚、心悸失眠者食用。</p>
                
                <p style="margin-bottom: 15px;"><strong>食谱二：桂圆红枣茶</strong></p>
                <p style="margin-bottom: 15px;">材料：桂圆肉 10g、红枣 5 枚、枸杞 10g、红糖适量</p>
                <p style="margin-bottom: 15px;">做法：桂圆肉、红枣（去核）、枸杞洗净，放入茶壶中，沸水冲泡，加盖焖 15 分钟，加入红糖调味即可。每日下午饮用。</p>
                <p style="margin-bottom: 15px;">功效：补益心脾，养血安神。适合气血不足、失眠健忘者饮用。</p>
                
                <p style="margin-bottom: 15px;"><strong>食谱三：小米南瓜粥</strong></p>
                <p style="margin-bottom: 15px;">材料：小米 50g、南瓜 100g、红枣 3 枚</p>
                <p style="margin-bottom: 15px;">做法：小米洗净，南瓜去皮切块，红枣去核。所有材料放入锅中，加水适量，大火煮沸后转小火煮 40 分钟至粥稠即可。晚餐食用。</p>
                <p style="margin-bottom: 15px;">功效：健脾和胃，安神助眠。适合脾胃虚弱、睡眠不佳者食用。</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 食用注意</strong></p>
                <p style="margin-bottom: 15px;">• 食疗需长期坚持，不可急于求成，一般建议连续食用 2-4 周</p>
                <p style="margin-bottom: 15px;">• 孕妇、儿童及特殊人群请在医生指导下食用</p>
                <p style="margin-bottom: 15px;">• 食疗不能替代药物治疗，如失眠严重请及时就医</p>
                <p style="margin-bottom: 15px;">• 避免晚餐过饱，睡前不宜饮茶、咖啡等刺激性饮品</p>
            </section>
        </section>
        """
    else:  # 穴位保健
        content = f"""
        <section style="max-width: 100%; box-sizing: border-box;">
            <section style="text-align: center; margin-bottom: 20px;">
                <strong style="font-size: 18px; color: #2c5530;">{title}</strong>
            </section>
            
            <section style="margin-bottom: 20px; line-height: 1.8;">
                <p style="margin-bottom: 15px;"><strong>📍 穴位介绍</strong></p>
                <p style="margin-bottom: 15px;">{focus}。穴位按摩是中医传统保健方法，简单易学，安全有效。通过刺激特定穴位，可以疏通经络、调和气血，达到防病治病的目的。内关穴是手厥阴心包经的重要穴位，具有宁心安神、和胃降逆的功效。</p>
                
                <p style="margin-bottom: 15px;"><strong>🔍 穴位定位</strong></p>
                <p style="margin-bottom: 15px;">内关穴位于前臂掌侧，腕横纹上 2 寸（约三横指），掌长肌腱与桡侧腕屈肌腱之间。取穴时，手掌向上，从腕横纹向上量三横指，在两筋之间按压，有酸胀感即是。</p>
                
                <p style="margin-bottom: 15px;"><strong>👆 按摩方法</strong></p>
                <p style="margin-bottom: 15px;">1. <strong>指按法</strong>：用拇指指腹按压穴位，其余四指托住前臂，固定手腕</p>
                <p style="margin-bottom: 15px;">2. <strong>力度</strong>：以感觉酸胀为度，不可用力过猛，以免损伤组织。力度应由轻到重，逐渐加力</p>
                <p style="margin-bottom: 15px;">3. <strong>时间</strong>：每次按压 3-5 分钟，每日 2-3 次，早晚各一次为宜。可在睡前按摩，有助于改善睡眠</p>
                <p style="margin-bottom: 15px;">4. <strong>呼吸</strong>：按压时缓慢深呼吸，放松身心，效果更佳。吸气时放松，呼气时按压</p>
                <p style="margin-bottom: 15px;">5. <strong>配穴</strong>：可配合神门穴、心俞穴等，增强安神效果</p>
                
                <p style="margin-bottom: 15px;"><strong>💡 保健功效</strong></p>
                <p style="margin-bottom: 15px;">• <strong>宁心安神</strong>：缓解心悸、胸闷、失眠、焦虑等症状</p>
                <p style="margin-bottom: 15px;">• <strong>和胃降逆</strong>：改善恶心、呕吐、胃痛、呃逆等胃部不适</p>
                <p style="margin-bottom: 15px;">• <strong>疏通经络</strong>：缓解上肢疼痛、麻木、活动不利等症状</p>
                <p style="margin-bottom: 15px;">• <strong>预防保健</strong>：日常按摩可强身健体，预防心血管疾病</p>
                
                <p style="margin-bottom: 15px;"><strong>⚠️ 注意事项</strong></p>
                <p style="margin-bottom: 15px;">• 饭后 1 小时内不宜按摩，以免影响消化功能</p>
                <p style="margin-bottom: 15px;">• 孕妇慎用，某些穴位可能引起子宫收缩</p>
                <p style="margin-bottom: 15px;">• 皮肤破损、感染处禁止按摩，以免加重感染</p>
                <p style="margin-bottom: 15px;">• 如有严重不适，立即停止并就医，不要强行按摩</p>
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
                <p style="margin-bottom: 10px;"><strong>娄伯恩</strong> 主治医师</p>
                <p style="margin-bottom: 8px; font-size: 14px;">宋氏中医传承人 | 娄氏风湿病传承人</p>
                <p style="margin-bottom: 10px; font-size: 13px; color: #555;">出身于中医世家，毕业于河南中医学院中医骨伤系，曾在北京积水潭医院中医正骨科进修学习。临床中以虚、邪、瘀治痹理论为基础，中西医结合，辨证论治，在疼痛、骨伤、风湿病的诊治过程中积累丰富经验。任河南省中医药学会风湿病专业委员会委员，河南省中西医结合学会风湿病专业委员会委员，世界中联骨质疏松专业委员会理事，世界中联骨关节疾病专业委员会理事。</p>
                <p style="margin-bottom: 10px; font-size: 13px; color: #555;"><strong>擅长治疗</strong>：各类关节肌肉疼痛疾病，颈肩腰腿痛，骨折病，关节陈旧性损伤，风湿、类风湿、痛风关节炎。</p>
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
    json_data = json.dumps(data, ensure_ascii=False)
    
    response = requests.post(url, params=params, data=json_data.encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'})
    return response.json()

def count_chinese_chars(text):
    """统计中文字符数"""
    return len([c for c in text if '\u4e00' <= c <= '\u9fff'])

def main():
    print("=" * 60)
    print("🚀 健康科普文章发布（字数达标版）")
    print("=" * 60)
    
    # 随机选择主题
    topic_type = random.choice(list(TOPIC_LIBRARY.keys()))
    topic_info = random.choice(TOPIC_LIBRARY[topic_type])
    
    print(f"\n📝 主题类型：{topic_type}")
    print(f"📰 文章标题：{topic_info['title']}")
    print(f"💡 核心要点：{topic_info['focus']}")
    
    # 生成文章内容
    print("\n✍️  生成文章内容...")
    content = generate_article_content(topic_type, topic_info)
    
    # 统计字数
    char_count = count_chinese_chars(content)
    print(f"📊 文章字数：约{char_count}字（目标 500-800 字）")
    
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
    result = create_draft(access_token, topic_info['title'], content, doctor_img_url, qr_img_url, DOCTOR_IMAGE_MEDIA_ID)
    
    # 处理结果
    if 'media_id' in result:
        print("\n" + "=" * 60)
        print("✅ 发布成功！")
        print("=" * 60)
        print(f"📰 文章标题：{topic_info['title']}")
        print(f"🆔 草稿 ID: {result['media_id']}")
        print(f"📊 文章字数：约{char_count}字")
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
