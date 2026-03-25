#!/usr/bin/env python3
"""
最终编码修复测试
使用 ensure_ascii=False 解决微信乱码问题
"""

import requests
import json
import os
import time
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

def upload_permanent_image(access_token, image_path):
    """上传图片为永久素材"""
    if not os.path.exists(image_path):
        print(f"❌ 图片文件不存在: {image_path}")
        return None
    
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {'access_token': access_token, 'type': 'image'}
    
    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
        
        result = response.json()
        
        if 'media_id' in result:
            print(f"✅ 永久素材上传成功")
            print(f"📊 media_id: {result['media_id'][:30]}...")
            return result['media_id']
        else:
            print(f"❌ 永久素材上传失败: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 上传图片异常: {e}")
        return None

def create_draft_with_encoding_fix(access_token, title, author, content, thumb_media_id):
    """创建草稿（使用 ensure_ascii=False 修复编码）"""
    if not thumb_media_id:
        print("❌ 错误: thumb_media_id 不能为空")
        return None
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
    params = {'access_token': access_token}
    
    # 准备文章数据
    article = {
        'title': title[:64],  # 限制长度
        'author': author[:8],  # 限制长度
        'digest': f'{title[:50]}...' if len(title) > 50 else title,
        'content': content,
        'content_source_url': '',
        'thumb_media_id': thumb_media_id,
        'need_open_comment': 0,
        'only_fans_can_comment': 0
    }
    
    data = {'articles': [article]}
    
    print(f"\n📤 发送数据（使用 ensure_ascii=False）:")
    print(f"  标题: {repr(article['title'])}")
    print(f"  作者: {repr(article['author'])}")
    print(f"  摘要: {repr(article['digest'])}")
    print(f"  内容前100字符: {repr(content[:100])}")
    
    # 关键修复：使用 ensure_ascii=False
    json_data = json.dumps(data, ensure_ascii=False)
    print(f"📊 JSON数据（前200字符）: {json_data[:200]}...")
    contains_unicode = '是' if '\\u' in json_data else '否'
    print(f"🔤 JSON是否包含 \\u: {contains_unicode}")
    
    try:
        # 发送请求，使用 ensure_ascii=False
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        response = requests.post(
            url, 
            params=params, 
            data=json_data.encode('utf-8'),  # 手动编码
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        return result
        
    except Exception as e:
        print(f"❌ 创建草稿异常: {e}")
        return {'errcode': -1, 'errmsg': str(e)}

def check_draft_content(access_token, draft_media_id):
    """检查草稿内容"""
    print(f"\n🔍 检查草稿内容: {draft_media_id[:30]}...")
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get"
    params = {'access_token': access_token}
    data = {'media_id': draft_media_id}
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        if 'news_item' in result:
            article = result['news_item'][0]
            
            print(f"📋 微信返回的内容:")
            print(f"  标题: {repr(article.get('title', ''))}")
            print(f"  作者: {repr(article.get('author', ''))}")
            
            content = article.get('content', '')
            print(f"  内容前100字符: {repr(content[:100])}")
            
            # 检查是否包含 Unicode 转义
            import re
            unicode_count = len(re.findall(r'\\u[0-9a-fA-F]{4}', content[:200]))
            print(f"  前200字符中 Unicode 转义数量: {unicode_count}")
            
            if unicode_count > 0:
                print("⚠️  警告: 微信 API 返回了 Unicode 转义字符")
                
                # 尝试解码
                try:
                    decoded_title = article.get('title', '').encode('latin-1').decode('unicode_escape')
                    print(f"  解码标题: {decoded_title}")
                except:
                    print("  无法解码标题")
            else:
                print("✅ 微信返回了纯 UTF-8 编码")
                
        else:
            print(f"❌ 无法获取草稿内容: {result}")
            
    except Exception as e:
        print(f"❌ 检查草稿失败: {e}")

def test_simple_article(access_token, thumb_media_id):
    """测试简单文章"""
    print("\n📋 测试 1: 简单测试文章")
    
    simple_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>编码测试文章</title>
</head>
<body>
    <h1>编码测试文章</h1>
    <p>这是一篇测试文章，验证中文显示是否正常。</p>
    <p>中医养生测试：药食同源，养生之道在于平衡。</p>
    <p>作者：测试医生</p>
</body>
</html>"""
    
    result = create_draft_with_encoding_fix(
        access_token,
        title='编码测试文章',
        author='测试医生',
        content=simple_content,
        thumb_media_id=thumb_media_id
    )
    
    print(f"\n📊 发布结果: {json.dumps(result, ensure_ascii=False)}")
    
    if 'media_id' in result:
        print(f"\n🎉 文章发布成功!")
        print(f"🆔 草稿ID: {result['media_id']}")
        
        # 等待一下，避免频率限制
        time.sleep(2)
        
        # 检查草稿内容
        check_draft_content(access_token, result['media_id'])
        
        return result['media_id']
    else:
        print(f"\n❌ 文章发布失败")
        return None

def test_fixed_article(access_token, thumb_media_id):
    """测试修复后的文章"""
    print("\n📋 测试 2: 修复后的文章")
    
    # 读取修复后的文章
    article_path = 'articles/fixed_中医食疗_养生食谱.html'
    if not os.path.exists(article_path):
        print(f"❌ 文章文件不存在: {article_path}")
        return None
    
    try:
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ 读取文章: {os.path.basename(article_path)}")
        print(f"📊 文章长度: {len(content)} 字符")
        
        # 检查是否包含 Unicode 转义
        import re
        unicode_matches = re.findall(r'\\u[0-9a-fA-F]{4}', content[:500])
        if unicode_matches:
            print(f"⚠️  文章包含 {len(unicode_matches)} 个 Unicode 转义字符")
            print(f"📋 示例: {unicode_matches[:3]}")
        else:
            print("✅ 文章是纯 UTF-8 编码")
        
    except Exception as e:
        print(f"❌ 读取文章失败: {e}")
        return None
    
    result = create_draft_with_encoding_fix(
        access_token,
        title='中医食疗养生方（最终测试）',
        author='娄医',
        content=content,
        thumb_media_id=thumb_media_id
    )
    
    print(f"\n📊 发布结果: {json.dumps(result, ensure_ascii=False)}")
    
    if 'media_id' in result:
        print(f"\n🎉 文章发布成功!")
        print(f"🆔 草稿ID: {result['media_id']}")
        
        # 等待一下，避免频率限制
        time.sleep(2)
        
        # 检查草稿内容
        check_draft_content(access_token, result['media_id'])
        
        return result['media_id']
    else:
        print(f"\n❌ 文章发布失败")
        return None

def test_ensure_ascii_comparison():
    """测试 ensure_ascii 参数对比"""
    print("\n🔧 测试 ensure_ascii 参数对比...")
    
    test_data = {
        'title': '测试标题',
        'content': '这是一篇测试文章。'
    }
    
    # ensure_ascii=True (默认)
    json_true = json.dumps(test_data, ensure_ascii=True)
    print(f"📊 ensure_ascii=True:")
    print(f"  JSON: {json_true}")
    print(f"  长度: {len(json_true)} 字符")
    contains_unicode_true = '是' if '\\u' in json_true else '否'
    print(f"  包含 \\u: {contains_unicode_true}")
    
    # ensure_ascii=False (修复)
    json_false = json.dumps(test_data, ensure_ascii=False)
    print(f"\n📊 ensure_ascii=False:")
    print(f"  JSON: {json_false}")
    print(f"  长度: {len(json_false)} 字符")
    contains_unicode_false = '是' if '\\u' in json_false else '否'
    print(f"  包含 \\u: {contains_unicode_false}")
    
    print(f"\n💡 关键区别:")
    print(f"  ensure_ascii=True: 中文 → Unicode 转义")
    print(f"  ensure_ascii=False: 中文 → 保持原样")

def main():
    """主函数"""
    print("=" * 60)
    print("微信编码最终修复测试")
    print("使用 ensure_ascii=False 解决乱码问题")
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
    cover_image = 'wechat_personal_qr.jpg'
    if not os.path.exists(cover_image):
        cover_image = 'wechat_qr.jpg'
    
    thumb_media_id = upload_permanent_image(access_token, cover_image)
    if not thumb_media_id:
        print("❌ 无法获取有效的封面图片 media_id")
        return
    
    # 4. 测试 ensure_ascii 参数对比
    test_ensure_ascii_comparison()
    
    # 5. 测试简单文章
    draft_id1 = test_simple_article(access_token, thumb_media_id)
    
    # 等待一下，避免频率限制
    time.sleep(3)
    
    # 6. 测试修复后的文章
    draft_id2 = test_fixed_article(access_token, thumb_media_id)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n📊 测试结果总结:")
    print(f"  总测试数: 2")
    print(f"  成功数: {2 if draft_id1 and draft_id2 else 1 if draft_id1 or draft_id2 else 0}")
    print(f"  失败数: {0 if draft_id1 and draft_id2 else 1 if draft_id1 or draft_id2 else 2}")
    
    print("\n💡 关键修复:")
    print("  1. 使用 json.dumps(data, ensure_ascii=False)")
    print("  2. 手动编码为 UTF-8: data.encode('utf-8')")
    print("  3. 设置正确的 Content-Type 头")
    print("  4. 避免 requests 的默认 ensure_ascii=True 行为")
    
    print("\n🔧 技术原理:")
    print("  requests.post(json=data) 默认使用 ensure_ascii=True")
    print("  这会将中文转换为 Unicode 转义字符")
    print("  微信 API 存储这些转义字符")
    print("  微信前端显示乱码")
    print("  解决方案: 使用 ensure_ascii=False 发送纯 UTF-8")
    
    print("\n🎯 下一步:")
    print("  1. 请用户在微信草稿箱检查文章显示")
    print("  2. 如果显示正常，更新所有发布脚本")
    print("  3. 如果仍有问题，进一步调试微信前端")

if __name__ == "__main__":
    main()