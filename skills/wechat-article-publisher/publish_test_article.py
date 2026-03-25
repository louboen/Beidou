#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布测试文章 - 验证编码修复
"""

import json
import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 微信配置
APPID = os.getenv('WECHAT_APPID')
APPSECRET = os.getenv('WECHAT_APPSECRET')

def get_access_token():
    """获取访问令牌"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': APPID,
        'secret': APPSECRET
    }
    response = requests.get(url, params=params)
    result = response.json()
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception(f"获取 access_token 失败：{result}")

def upload_permanent_image(image_path, access_token):
    """上传永久素材图片"""
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    # 如果没有图片，使用默认二维码
    if not os.path.exists(image_path):
        image_path = 'wechat_personal_qr.jpg'
    
    if not os.path.exists(image_path):
        print(f"⚠️ 警告：图片文件不存在：{image_path}")
        return None
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, params=params, files=files)
    
    result = response.json()
    if 'media_id' in result:
        print(f"✅ 永久素材上传成功：{result['media_id']}")
        return result['media_id']
    else:
        print(f"❌ 上传失败：{result}")
        return None

def publish_article(html_path, title, author, access_token):
    """发布文章到草稿箱"""
    print(f"\n📖 读取文章：{html_path}")
    
    # 读取文章内容
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📊 文章长度：{len(content)} 字符")
    
    # 检查编码
    has_unicode_escape = '\\u' in content
    if has_unicode_escape:
        print("⚠️ 警告：文章包含 Unicode 转义字符")
    else:
        print("✅ 文章是纯 UTF-8 编码")
    
    # 上传封面（使用默认图片）
    cover_path = 'wechat_personal_qr.jpg'
    thumb_media_id = upload_permanent_image(cover_path, access_token)
    
    if not thumb_media_id:
        print("⚠️ 使用空封面（可能失败）")
        thumb_media_id = ""
    
    # 准备草稿数据
    draft_data = {
        "articles": [
            {
                "title": title[:64],  # 截断为 64 字符
                "author": author[:8],  # 截断为 8 字符
                "digest": title[:120],
                "content": content,
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": 1 if thumb_media_id else 0
            }
        ]
    }
    
    # 关键修复：使用 ensure_ascii=False
    json_data = json.dumps(draft_data, ensure_ascii=False)
    
    print(f"\n📤 发送数据（使用 ensure_ascii=False）:")
    print(f"  标题：'{title}'")
    print(f"  作者：'{author}'")
    print(f"  内容前 100 字符：{content[:100]}")
    
    # 检查 JSON 是否包含 Unicode 转义
    has_unicode_in_json = '\\u' in json_data
    print(f"🔤 JSON 是否包含 \\u: {'是' if has_unicode_in_json else '否'}")
    
    # 发送到微信 API
    url = "https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {'access_token': access_token}
    
    response = requests.post(
        url,
        params=params,
        data=json_data.encode('utf-8'),  # 关键：手动编码为 UTF-8
        headers={'Content-Type': 'application/json; charset=utf-8'}
    )
    
    result = response.json()
    
    print(f"\n📊 发布结果：{result}")
    
    if 'errcode' in result and result['errcode'] == 0:
        draft_id = result.get('media_id', '未知')
        print(f"\n🎉 文章发布成功!")
        print(f"🆔 草稿 ID: {draft_id}")
        return draft_id
    else:
        print(f"\n❌ 发布失败：{result}")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号文章发布测试")
    print("=" * 60)
    
    try:
        # 获取 access_token
        print("\n🔑 获取 access_token...")
        access_token = get_access_token()
        print("✅ access_token 获取成功")
        
        # 发布测试文章
        html_path = 'test_20260319_final.html'
        title = '春季中医养生指南 - 最终编码测试'
        author = '娄医'
        
        print(f"\n📝 准备发布：{title}")
        draft_id = publish_article(html_path, title, author, access_token)
        
        if draft_id:
            print("\n" + "=" * 60)
            print("✅ 测试完成！")
            print("=" * 60)
            print(f"\n请前往微信公众平台检查：")
            print(f"https://mp.weixin.qq.com")
            print(f"进入「草稿箱」查看文章显示效果")
            print(f"\n草稿 ID: {draft_id}")
        else:
            print("\n❌ 测试失败，请检查错误信息")
            
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
