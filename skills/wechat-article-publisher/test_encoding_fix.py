#!/usr/bin/env python3
"""
测试编码修复后的文章发布
"""

import requests
import json
import os
import re
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

def read_and_fix_content(html_path):
    """读取并修复文章内容"""
    if not os.path.exists(html_path):
        return None
    
    try:
        # 读取文件
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ 读取文章: {os.path.basename(html_path)}")
        print(f"📊 原始长度: {len(content)} 字符")
        
        # 检查是否包含 Unicode 转义
        unicode_pattern = r'\\u[0-9a-fA-F]{4}'
        matches = re.findall(unicode_pattern, content)
        
        if matches:
            print(f"⚠️  发现 {len(matches)} 个 Unicode 转义字符")
            
            # 显示前几个示例
            print("📋 示例转义字符:")
            for i, match in enumerate(matches[:5]):
                try:
                    decoded = match.encode('ascii').decode('unicode_escape')
                    print(f"  {match} → {decoded}")
                except:
                    print(f"  {match} → 解码失败")
            
            # 尝试修复
            print("🔄 尝试修复...")
            
            # 方法1: 使用 JSON 解码
            try:
                # 需要正确处理转义字符
                fixed_content = json.loads(f'"{content}"')
                print("✅ 使用 JSON 解码修复成功")
                return fixed_content
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解码失败: {e}")
            
            # 方法2: 使用 unicode_escape
            try:
                fixed_content = content.encode('utf-8').decode('unicode_escape')
                print("✅ 使用 unicode_escape 修复成功")
                return fixed_content
            except Exception as e:
                print(f"❌ unicode_escape 解码失败: {e}")
            
            # 方法3: 手动替换
            print("🔄 尝试手动替换...")
            fixed_content = content
            replaced_count = 0
            
            for match in set(matches):  # 去重
                try:
                    decoded = match.encode('ascii').decode('unicode_escape')
                    fixed_content = fixed_content.replace(match, decoded)
                    replaced_count += 1
                except:
                    pass
            
            print(f"✅ 手动替换 {replaced_count} 个字符")
            return fixed_content
            
        else:
            print("✅ 未发现 Unicode 转义字符")
            return content
            
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None

def test_draft_creation(access_token, title, author, content, thumb_media_id):
    """测试草稿创建"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {'access_token': access_token}
    
    # 准备文章数据
    article = {
        'title': title[:64],
        'author': author[:8],
        'digest': f'{title[:50]}...' if len(title) > 50 else title,
        'content': content,
        'content_source_url': '',
        'thumb_media_id': thumb_media_id,
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }
    
    data = {'articles': [article]}
    
    try:
        print(f"\n📤 发送数据预览:")
        print(f"  标题: {article['title']}")
        print(f"  作者: {article['author']}")
        print(f"  摘要: {article['digest']}")
        print(f"  内容前100字符: {content[:100]}...")
        
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        return result
        
    except Exception as e:
        return {'errcode': -1, 'errmsg': str(e)}

def upload_image(access_token, image_path):
    """上传图片"""
    if not os.path.exists(image_path):
        return None
    
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
        
        result = response.json()
        
        if 'media_id' in result:
            return result['media_id']
        else:
            print(f"❌ 图片上传失败: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 上传图片异常: {e}")
        return None

def main():
    """主测试函数"""
    print("=" * 60)
    print("编码修复测试")
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
    
    # 3. 上传封面图片
    print("\n2️⃣ 上传封面图片...")
    cover_image = "wechat_personal_qr.jpg"
    
    if os.path.exists(cover_image):
        thumb_media_id = upload_image(access_token, cover_image)
        if thumb_media_id:
            print(f"✅ 封面图片上传成功")
            print(f"📊 media_id: {thumb_media_id[:30]}...")
        else:
            print("❌ 封面图片上传失败，使用空值")
            thumb_media_id = ""
    else:
        print("⚠️  封面图片不存在，使用空值")
        thumb_media_id = ""
    
    # 4. 测试不同版本的文章
    test_articles = [
        {
            'name': '原始文章',
            'path': 'articles/auto_中医食疗_养生食谱.html',
            'title': '中医食疗养生方（原始）',
            'author': '娄医'
        },
        {
            'name': '修复后文章',
            'path': 'articles/fixed_中医食疗_养生食谱.html',
            'title': '中医食疗养生方（修复后）',
            'author': '娄医'
        },
        {
            'name': '简单测试',
            'path': None,
            'title': '编码测试文章',
            'author': '测试',
            'content': '这是一篇测试文章，检查中文显示是否正常。中医食疗养生方。'
        }
    ]
    
    print("\n3️⃣ 测试文章发布...")
    
    for article in test_articles:
        print(f"\n📋 测试: {article['name']}")
        print(f"📄 标题: {article['title']}")
        
        if article['path'] and os.path.exists(article['path']):
            # 读取并修复内容
            content = read_and_fix_content(article['path'])
        elif 'content' in article:
            # 使用预设内容
            content = article['content']
            print(f"📊 使用预设内容: {len(content)} 字符")
        else:
            print("❌ 文章文件不存在")
            continue
        
        if not content:
            print("❌ 无法获取文章内容")
            continue
        
        # 测试发布
        result = test_draft_creation(
            access_token,
            article['title'],
            article['author'],
            content,
            thumb_media_id
        )
        
        print(f"📊 发布结果: {json.dumps(result, ensure_ascii=False)}")
        
        if 'media_id' in result:
            print(f"✅ 发布成功!")
            print(f"🆔 草稿ID: {result['media_id']}")
            
            # 检查返回的内容
            if 'item' in result and result['item']:
                print(f"📋 返回项目: {len(result['item'])} 个")
        else:
            print(f"❌ 发布失败")
            
            # 分析错误
            errcode = result.get('errcode')
            errmsg = result.get('errmsg', '')
            
            print(f"🔍 错误分析:")
            print(f"  错误代码: {errcode}")
            print(f"  错误信息: {errmsg}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()