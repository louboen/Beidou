#!/usr/bin/env python3
"""
完整测试微信 API，找出自动化发布失败的根本原因
"""

import requests
import json
import os
import sys
from pathlib import Path
import time

def load_config():
    """加载配置"""
    env_path = Path('.env')
    config = {}
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"').strip("'")
    return config

def get_access_token(appid, appsecret):
    """获取 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': appid,
        'secret': appsecret
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        return result
    except Exception as e:
        return {'error': str(e)}

def test_image_upload(access_token, image_path):
    """测试图片上传"""
    if not os.path.exists(image_path):
        return {'errcode': -1, 'errmsg': f'文件不存在: {image_path}'}
    
    url = f"https://api.weixin.qq.com/cgi-bin/media/upload"
    params = {'access_token': access_token, 'type': 'image'}
    
    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
        return response.json()
    except Exception as e:
        return {'errcode': -2, 'errmsg': str(e)}

def test_draft_creation(access_token, media_id, title, author, content):
    """测试草稿创建"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {'access_token': access_token}
    
    # 准备文章数据
    article = {
        'title': title,
        'author': author,
        'digest': f'{title} - 来自中医娄伯恩',
        'content': content,
        'content_source_url': '',
        'thumb_media_id': media_id,
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }
    
    data = {
        'articles': [article]
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        return response.json()
    except Exception as e:
        return {'errcode': -3, 'errmsg': str(e)}

def create_test_content():
    """创建测试内容"""
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>测试文章</title>
</head>
<body>
    <h1>测试文章标题</h1>
    <p>这是一篇测试文章，用于验证微信API功能。</p>
    <p>如果这个文章能够成功发布，说明API配置正确。</p>
</body>
</html>"""

def create_minimal_image():
    """创建最小的测试图片"""
    # 创建一个 1x1 像素的 PNG 图片
    png_data = (
        b'\x89PNG\r\n\x1a\n' +  # PNG 签名
        b'\x00\x00\x00\x0d' +    # IHDR 长度
        b'IHDR' +                # IHDR 类型
        b'\x00\x00\x00\x01' +    # 宽度: 1
        b'\x00\x00\x00\x01' +    # 高度: 1
        b'\x08\x02\x00\x00\x00' + # 位深、颜色类型等
        b'\x00\x00\x00\x00' +    # CRC (简化)
        b'\x00\x00\x00\x00' +    # IDAT 长度
        b'IDAT' +                # IDAT 类型
        b'\x00' +                # 图像数据
        b'\x00\x00\x00\x00' +    # CRC (简化)
        b'\x00\x00\x00\x00' +    # IEND 长度
        b'IEND' +                # IEND 类型
        b'\xae\x42\x60\x82'      # IEND CRC
    )
    
    return png_data

def main():
    """主测试函数"""
    print("=" * 60)
    print("微信 API 完整测试")
    print("=" * 60)
    
    # 1. 加载配置
    config = load_config()
    appid = config.get('WECHAT_APPID')
    appsecret = config.get('WECHAT_APPSECRET')
    
    if not appid or not appsecret:
        print("❌ 配置不完整")
        return
    
    print(f"🔑 AppID: {appid}")
    print(f"🔐 AppSecret: {appsecret[:10]}...")
    
    # 2. 获取 access_token
    print("\n1️⃣ 获取 access_token...")
    token_result = get_access_token(appid, appsecret)
    
    if 'access_token' in token_result:
        access_token = token_result['access_token']
        print(f"✅ access_token 获取成功: {access_token[:20]}...")
        print(f"📊 有效期: {token_result.get('expires_in', 'N/A')} 秒")
    else:
        print(f"❌ 获取失败: {token_result}")
        return
    
    # 3. 创建测试图片
    print("\n2️⃣ 创建测试图片...")
    test_image_data = create_minimal_image()
    test_image_path = "test_minimal_image.png"
    
    with open(test_image_path, 'wb') as f:
        f.write(test_image_data)
    
    print(f"✅ 测试图片已创建: {test_image_path}")
    print(f"📊 图片大小: {len(test_image_data)} 字节")
    
    # 4. 测试图片上传
    print("\n3️⃣ 测试图片上传...")
    upload_result = test_image_upload(access_token, test_image_path)
    
    if 'media_id' in upload_result:
        media_id = upload_result['media_id']
        print(f"✅ 图片上传成功!")
        print(f"📊 media_id: {media_id[:30]}...")
        print(f"📊 类型: {upload_result.get('type', 'N/A')}")
        print(f"📊 创建时间: {upload_result.get('created_at', 'N/A')}")
    else:
        print(f"❌ 图片上传失败: {upload_result}")
        # 清理测试文件
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        return
    
    # 5. 测试草稿创建
    print("\n4️⃣ 测试草稿创建...")
    test_content = create_test_content()
    test_title = "API测试文章"
    test_author = "娄医"  # 使用短作者名
    
    draft_result = test_draft_creation(
        access_token, 
        media_id, 
        test_title, 
        test_author, 
        test_content
    )
    
    print(f"📊 草稿创建响应: {json.dumps(draft_result, ensure_ascii=False)}")
    
    if 'media_id' in draft_result:
        draft_media_id = draft_result['media_id']
        print(f"✅ 草稿创建成功!")
        print(f"📊 草稿 media_id: {draft_media_id}")
    else:
        print(f"❌ 草稿创建失败")
        
        # 分析错误原因
        errcode = draft_result.get('errcode')
        errmsg = draft_result.get('errmsg', '')
        
        print(f"\n🔍 错误分析:")
        print(f"  错误代码: {errcode}")
        print(f"  错误信息: {errmsg}")
        
        if errcode == 40007:
            print("  💡 可能原因: media_id 无效或已过期")
            print("  🔧 解决方案: 重新上传图片，使用永久素材")
        elif errcode == 45110:
            print("  💡 可能原因: 作者名长度超限")
            print("  🔧 解决方案: 作者名不超过8个字符")
        elif errcode == 53402:
            print("  💡 可能原因: 封面图片裁剪失败")
            print("  🔧 解决方案: 使用标准900×500像素图片")
        elif errcode == 45009:
            print("  💡 可能原因: API 调用频率限制")
            print("  🔧 解决方案: 等待一段时间后重试")
        else:
            print("  💡 可能原因: 其他API限制或配置问题")
            print("  🔧 解决方案: 检查微信公众号权限设置")
    
    # 6. 清理测试文件
    print("\n5️⃣ 清理测试文件...")
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
        print(f"✅ 已删除测试图片: {test_image_path}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()