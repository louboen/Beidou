#!/usr/bin/env python3
"""
微信公众号发布功能修复方案
解决图片上传和草稿创建问题
"""

import requests
import json
import sys
import os
import time
import base64

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
WECHAT_API_BASE = "https://api.weixin.qq.com"

def get_access_token():
    """获取 access_token"""
    url = f"{WECHAT_API_BASE}/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET
    }
    
    try:
        print("🔑 获取 access_token...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "access_token" in data:
            access_token = data["access_token"]
            print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
            return access_token
        else:
            print(f"   ❌ access_token 获取失败: {data}")
            return None
            
    except Exception as e:
        print(f"   ❌ 获取 access_token 时出错: {e}")
        return None

def create_simple_image():
    """创建简单的测试图片（使用 base64 编码的 1x1 像素 PNG）"""
    print("🎨 创建简单测试图片...")
    
    # 1x1 像素的 PNG 图片（base64 编码）
    # 这是一个最小的有效 PNG 图片
    base64_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    try:
        image_data = base64.b64decode(base64_png)
        print(f"   ✅ 测试图片创建成功")
        print(f"   格式: PNG")
        print(f"   大小: {len(image_data)} 字节")
        return image_data
    except Exception as e:
        print(f"   ❌ 创建测试图片失败: {e}")
        return None

def upload_simple_image(access_token):
    """上传简单图片"""
    print("📤 上传简单图片...")
    
    # 创建图片数据
    image_data = create_simple_image()
    if not image_data:
        return None
    
    # 上传临时素材
    url = f"{WECHAT_API_BASE}/cgi-bin/media/upload"
    params = {"access_token": access_token, "type": "image"}
    
    try:
        files = {"media": ("test.png", image_data, "image/png")}
        response = requests.post(url, params=params, files=files, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print(f"   响应状态码: {response.status_code}")
        print(f"   响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "media_id" in result:
            media_id = result["media_id"]
            print(f"   ✅ 图片上传成功!")
            print(f"   media_id: {media_id}")
            return media_id
        else:
            print(f"   ❌ 图片上传失败: {result}")
            return None
            
    except Exception as e:
        print(f"   ❌ 图片上传时出错: {e}")
        return None

def create_minimal_draft(access_token, thumb_media_id=None):
    """创建最小化的草稿"""
    print("📄 创建最小化草稿...")
    
    # 最小化的文章数据
    article = {
        "title": "测试",  # 2个字符
        "author": "测试",  # 2个字符
        "digest": "测试",  # 2个字符
        "content": "<p>测试</p>",  # 最简单的 HTML
        "content_source_url": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    # 如果有封面图片，添加
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
        article["show_cover_pic"] = 1
        print(f"   使用封面图片: {thumb_media_id[:30]}...")
    else:
        print("   无封面图片")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [article]
    }
    
    try:
        print(f"   请求数据:")
        print(f"   - 标题: {article['title']} ({len(article['title'])}字符)")
        print(f"   - 作者: {article['author']} ({len(article['author'])}字符)")
        print(f"   - 摘要: {article['digest']} ({len(article['digest'])}字符)")
        print(f"   - 内容: {article['content']}")
        
        response = requests.post(url, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print(f"   响应状态码: {response.status_code}")
        print(f"   响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "media_id" in result:
            media_id = result["media_id"]
            print(f"   ✅ 草稿创建成功!")
            print(f"   草稿ID: {media_id}")
            return media_id
        elif "errcode" in result and result["errcode"] == 0:
            print(f"   ✅ 草稿创建成功!")
            if "media_id" in result:
                print(f"   草稿ID: {result['media_id']}")
                return result["media_id"]
            return "success"
        else:
            print(f"   ❌ 草稿创建失败")
            analyze_error(result)
            return None
            
    except Exception as e:
        print(f"   ❌ 创建草稿时出错: {e}")
        return None

def analyze_error(error_result):
    """分析错误原因"""
    errcode = error_result.get("errcode")
    errmsg = error_result.get("errmsg", "")
    
    print(f"   🔍 错误分析:")
    print(f"   错误代码: {errcode}")
    print(f"   错误信息: {errmsg}")
    
    # 常见错误代码
    error_map = {
        40005: "无效的文件类型",
        40007: "无效的 media_id",
        40113: "不支持的文件类型",
        45003: "标题长度超出限制（≤64字符）",
        45004: "描述长度超出限制（≤120字符）",
        45110: "作者长度超出限制（≤8字符）",
        53402: "封面裁剪失败，请检查裁剪参数后重试",
    }
    
    if errcode in error_map:
        print(f"   可能原因: {error_map[errcode]}")
        
        # 特定建议
        if errcode in [40005, 40113]:
            print(f"   💡 建议:")
            print(f"   1. 确保图片格式为 JPG 或 PNG")
            print(f"   2. 检查图片内容是否有效")
            print(f"   3. 尝试使用不同的图片")
        elif errcode == 53402:
            print(f"   💡 建议:")
            print(f"   1. 图片尺寸应为 900x500 像素")
            print(f"   2. 图片格式应为 JPG/PNG")
            print(f"   3. 图片内容应符合微信公众号规范")

def test_different_scenarios(access_token):
    """测试不同的场景"""
    print("\n🔬 测试不同场景...")
    
    scenarios = [
        {
            "name": "场景1: 无封面图片",
            "thumb_media_id": None,
            "article": {
                "title": "测试文章",
                "author": "测试作者",
                "digest": "测试摘要",
                "content": "<p>测试内容</p>",
                "content_source_url": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
        },
        {
            "name": "场景2: 最短内容",
            "thumb_media_id": None,
            "article": {
                "title": "测",
                "author": "测",
                "digest": "测",
                "content": "<p>测</p>",
                "content_source_url": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
        },
        {
            "name": "场景3: 纯文本",
            "thumb_media_id": None,
            "article": {
                "title": "纯文本测试",
                "author": "测试",
                "digest": "纯文本摘要",
                "content": "纯文本内容，没有HTML标签",
                "content_source_url": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 {scenario['name']}")
        
        url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
        params = {"access_token": access_token}
        
        # 准备文章数据
        article = scenario["article"].copy()
        if scenario["thumb_media_id"]:
            article["thumb_media_id"] = scenario["thumb_media_id"]
            article["show_cover_pic"] = 1
        
        data = {
            "articles": [article]
        }
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            result = response.json()
            
            print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if "media_id" in result or (result.get("errcode") == 0):
                print(f"   ✅ 成功!")
                return True
            else:
                print(f"   ❌ 失败")
                
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    
    return False

def main():
    """主函数"""
    print("=" * 70)
    print("微信公众号发布功能修复测试")
    print("=" * 70)
    
    # 1. 获取 access_token
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        return
    
    # 2. 尝试上传简单图片
    print("\n2️⃣ 尝试上传简单图片")
    media_id = upload_simple_image(access_token)
    
    # 3. 创建最小化草稿
    print("\n3️⃣ 创建最小化草稿")
    if media_id:
        # 使用上传的图片
        draft_id = create_minimal_draft(access_token, media_id)
    else:
        # 不使用图片
        draft_id = create_minimal_draft(access_token)
    
    # 4. 测试不同场景
    if not draft_id:
        print("\n4️⃣ 测试不同场景")
        test_different_scenarios(access_token)
    
    # 5. 总结
    print("\n" + "=" * 70)
    print("修复测试总结")
    print("=" * 70)
    
    if draft_id:
        print("✅ 修复成功!")
        print(f"   草稿创建成功: {draft_id}")
        
        print("\n🎯 下一步:")
        print("1. 使用此方法创建实际文章")
        print("2. 优化图片上传功能")
        print("3. 完善文章内容")
    else:
        print("❌ 修复失败")
        
        print("\n🔍 根本问题:")
        print("1. 图片上传失败 - 可能是服务器环境问题")
        print("2. 草稿创建失败 - 可能是权限或格式问题")
        
        print("\n💡 解决方案:")
        print("1. 在微信公众平台手动上传正确的封面图片")
        print("2. 使用手动发布流程")
        print("3. 检查微信公众号 API 权限设置")
        
        print("\n📋 手动发布流程:")
        print("1. 使用 write_wechat_article.py 创建文章")
        print("2. 登录微信公众平台手动发布")
        print("3. 上传正确的封面图片")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

if __name__ == "__main__":
    main()