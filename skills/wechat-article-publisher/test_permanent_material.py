#!/usr/bin/env python3
"""
测试微信永久素材接口
"""

import requests
import json
import os
from pathlib import Path

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
    
    response = requests.get(url, params=params, timeout=10)
    return response.json()

def add_permanent_material(access_token, image_path):
    """添加永久素材"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
        return response.json()
    except Exception as e:
        return {'errcode': -1, 'errmsg': str(e)}

def test_with_permanent_material():
    """使用永久素材测试"""
    print("=" * 60)
    print("永久素材测试")
    print("=" * 60)
    
    # 1. 加载配置
    config = load_config()
    appid = config.get('WECHAT_APPID')
    appsecret = config.get('WECHAT_APPSECRET')
    
    if not appid or not appsecret:
        print("❌ 配置不完整")
        return
    
    print(f"🔑 AppID: {appid}")
    
    # 2. 获取 access_token
    print("\n1️⃣ 获取 access_token...")
    token_result = get_access_token(appid, appsecret)
    
    if 'access_token' in token_result:
        access_token = token_result['access_token']
        print(f"✅ access_token 获取成功: {access_token[:20]}...")
    else:
        print(f"❌ 获取失败: {token_result}")
        return
    
    # 3. 使用现有图片作为测试
    test_images = ['cover_default.jpg', 'wechat_personal_qr.jpg']
    
    for image_file in test_images:
        if os.path.exists(image_file):
            print(f"\n📄 测试图片: {image_file}")
            file_size = os.path.getsize(image_file)
            print(f"📊 文件大小: {file_size} 字节")
            
            if file_size > 2 * 1024 * 1024:
                print("⚠️  文件太大 (>2MB)，跳过")
                continue
            
            # 4. 上传为永久素材
            print("🔄 上传为永久素材...")
            result = add_permanent_material(access_token, image_file)
            
            print(f"📊 响应: {json.dumps(result, ensure_ascii=False)}")
            
            if 'media_id' in result:
                media_id = result['media_id']
                print(f"✅ 永久素材上传成功!")
                print(f"📊 media_id: {media_id}")
                print(f"📊 url: {result.get('url', 'N/A')}")
                
                # 测试使用这个 media_id 创建草稿
                return test_draft_with_material(access_token, media_id, image_file)
            else:
                print(f"❌ 上传失败: {result}")
    
    print("\n❌ 所有图片测试失败")
    return None

def test_draft_with_material(access_token, media_id, image_name):
    """使用永久素材创建草稿"""
    print(f"\n🎯 使用永久素材创建草稿: {image_name}")
    
    # 准备测试内容
    test_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>永久素材测试</title>
</head>
<body>
    <h1>永久素材测试文章</h1>
    <p>使用永久素材 media_id 测试草稿创建。</p>
    <p>图片: {image_name}</p>
</body>
</html>""".format(image_name=image_name)
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {'access_token': access_token}
    
    article = {
        'title': '永久素材测试',
        'author': '娄医',
        'digest': '测试永久素材 media_id 的使用',
        'content': test_content,
        'content_source_url': '',
        'thumb_media_id': media_id,
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }
    
    data = {'articles': [article]}
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        print(f"📊 草稿创建响应: {json.dumps(result, ensure_ascii=False)}")
        
        if 'media_id' in result:
            print(f"✅ 草稿创建成功!")
            print(f"📊 草稿 media_id: {result['media_id']}")
            return True
        else:
            print(f"❌ 草稿创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def check_account_type(access_token):
    """检查公众号类型"""
    url = f"https://api.weixin.qq.com/cgi-bin/account/getaccount"
    params = {'access_token': access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        print(f"\n📊 账号信息: {json.dumps(result, ensure_ascii=False)}")
        return result
    except Exception as e:
        print(f"❌ 获取账号信息失败: {e}")
        return None

def main():
    """主函数"""
    print("开始永久素材测试...")
    
    # 1. 加载配置
    config = load_config()
    appid = config.get('WECHAT_APPID')
    appsecret = config.get('WECHAT_APPSECRET')
    
    if not appid or not appsecret:
        print("❌ 配置不完整")
        return
    
    # 2. 获取 access_token
    token_result = get_access_token(appid, appsecret)
    
    if 'access_token' not in token_result:
        print(f"❌ 获取 access_token 失败: {token_result}")
        return
    
    access_token = token_result['access_token']
    
    # 3. 检查账号类型
    print("\n🔍 检查公众号类型和权限...")
    account_info = check_account_type(access_token)
    
    if account_info:
        print("📋 账号信息已获取")
    
    # 4. 测试永久素材
    print("\n🚀 开始永久素材测试...")
    success = test_with_permanent_material()
    
    if success:
        print("\n🎉 测试成功! 永久素材可以用于草稿创建。")
        print("💡 解决方案: 使用永久素材接口上传封面图片")
    else:
        print("\n❌ 测试失败")
        print("💡 可能原因:")
        print("  1. 公众号类型不支持草稿功能")
        print("  2. API 权限限制")
        print("  3. 需要微信认证")
        print("🔧 建议:")
        print("  1. 检查微信公众号认证状态")
        print("  2. 确认有草稿箱管理权限")
        print("  3. 联系微信客服确认API权限")

if __name__ == "__main__":
    main()