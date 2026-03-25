#!/usr/bin/env python3
"""
修复微信公众号草稿创建问题
错误代码 45004: description size out of limit
"""

import requests
import json
import os
import time

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
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if "access_token" in data:
        return data["access_token"]
    else:
        print(f"❌ access_token 获取失败: {data}")
        return None

def analyze_error_45004():
    """分析错误 45004"""
    print("🔍 分析错误 45004: description size out of limit")
    print()
    
    # 官方文档信息
    print("📖 微信公众号官方文档要求:")
    print("   摘要 (digest): 总长度不超过128个字")
    print("   注意: '字' 可能指中文字符，不是字节")
    print()
    
    # 当前摘要
    current_digest = "春季养生正当时，中医教你如何顺应时节调养身体。"
    print(f"📝 当前摘要: '{current_digest}'")
    print(f"   字符数: {len(current_digest)}")
    print(f"   字节数 (UTF-8): {len(current_digest.encode('utf-8'))}")
    print()
    
    # 可能的问题
    print("🔍 可能的问题:")
    print("   1. 中文字符计算方式不同")
    print("   2. 标点符号可能被特殊计算")
    print("   3. 微信公众号API可能有内部限制")
    print("   4. 摘要可能包含不可见字符")
    print()
    
    return current_digest

def create_test_drafts(access_token, thumb_media_id):
    """创建多个测试草稿，使用不同的摘要"""
    print("🧪 创建测试草稿...")
    
    # 读取文章内容
    html_file = "wechat_article_春季中医养生指南_20260318_173832.html"
    
    if not os.path.exists(html_file):
        print(f"❌ HTML 文件不存在: {html_file}")
        return None
    
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"✅ 读取文章内容: {len(content)} 字符")
    except Exception as e:
        print(f"❌ 读取文章内容失败: {e}")
        return None
    
    # 测试不同的摘要
    test_digests = [
        {
            "title": "春季中医养生指南",
            "digest": "春季养生指南",
            "description": "最短摘要 (5字)"
        },
        {
            "title": "春季养生",
            "digest": "中医春季养生方法",
            "description": "简短摘要 (6字)"
        },
        {
            "title": "养生指南",
            "digest": "中医教你春季养生",
            "description": "中等摘要 (7字)"
        },
        {
            "title": "中医养生",
            "digest": "顺应时节调养身体",
            "description": "无标点摘要 (8字)"
        },
        {
            "title": "测试文章",
            "digest": "test",
            "description": "英文摘要 (4字符)"
        }
    ]
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    results = []
    
    for i, test in enumerate(test_digests, 1):
        print(f"\n🧪 测试 {i}: {test['description']}")
        print(f"   标题: {test['title']} ({len(test['title'])}字)")
        print(f"   摘要: '{test['digest']}' ({len(test['digest'])}字)")
        
        draft_data = {
            "articles": [{
                "title": test["title"],
                "author": "测试",
                "digest": test["digest"],
                "content": content,
                "thumb_media_id": thumb_media_id,
                "content_source_url": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }]
        }
        
        try:
            response = requests.post(url, params=params, json=draft_data, timeout=30)
            result = response.json()
            
            if "media_id" in result:
                print(f"   ✅ 成功! media_id: {result['media_id'][:20]}...")
                results.append({
                    "test": test,
                    "success": True,
                    "media_id": result["media_id"]
                })
            else:
                print(f"   ❌ 失败: {result.get('errcode', '未知')} - {result.get('errmsg', '未知')}")
                results.append({
                    "test": test,
                    "success": False,
                    "error": result
                })
        except Exception as e:
            print(f"   ❌ 请求失败: {e}")
            results.append({
                "test": test,
                "success": False,
                "error": str(e)
            })
    
    return results

def create_minimal_draft(access_token, thumb_media_id):
    """创建最小化的测试草稿"""
    print("\n🎯 创建最小化测试草稿...")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    # 最小化的内容
    minimal_content = "<p>测试内容</p>"
    
    draft_data = {
        "articles": [{
            "title": "测试",
            "author": "测",
            "digest": "测试",
            "content": minimal_content,
            "thumb_media_id": thumb_media_id,
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }]
    }
    
    print(f"📋 最小化草稿数据:")
    print(f"   标题: {draft_data['articles'][0]['title']} ({len(draft_data['articles'][0]['title'])}字)")
    print(f"   作者: {draft_data['articles'][0]['author']} ({len(draft_data['articles'][0]['author'])}字)")
    print(f"   摘要: '{draft_data['articles'][0]['digest']}' ({len(draft_data['articles'][0]['digest'])}字)")
    print(f"   内容: {len(draft_data['articles'][0]['content'])} 字符")
    print(f"   封面: {thumb_media_id[:20]}...")
    
    try:
        response = requests.post(url, params=params, json=draft_data, timeout=30)
        result = response.json()
        
        if "media_id" in result:
            print(f"✅ 最小化草稿创建成功!")
            print(f"   media_id: {result['media_id']}")
            return result["media_id"]
        else:
            print(f"❌ 最小化草稿创建失败: {result}")
            print(f"   错误代码: {result.get('errcode', '未知')}")
            print(f"   错误信息: {result.get('errmsg', '未知')}")
            return None
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        return None

def check_draft_permissions(access_token):
    """检查草稿相关权限"""
    print("\n🔍 检查草稿相关权限...")
    
    # 1. 检查草稿箱
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/count"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if "total_count" in result:
            print(f"✅ 草稿箱权限正常")
            print(f"   草稿总数: {result['total_count']}")
        else:
            print(f"❌ 草稿箱权限检查失败: {result}")
    except Exception as e:
        print(f"❌ 检查草稿箱时出错: {e}")
    
    # 2. 检查素材权限
    url = f"{WECHAT_API_BASE}/cgi-bin/material/get_materialcount"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if "image_count" in result:
            print(f"✅ 素材权限正常")
            print(f"   图片素材数: {result['image_count']}")
            print(f"   图文素材数: {result['news_count']}")
            print(f"   视频素材数: {result['video_count']}")
        else:
            print(f"❌ 素材权限检查失败: {result}")
    except Exception as e:
        print(f"❌ 检查素材权限时出错: {e}")

def main():
    """主函数"""
    print("=" * 70)
    print("微信公众号草稿问题修复")
    print("=" * 70)
    print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"公众号: 中医娄伯恩")
    print()
    
    # 1. 获取 access_token
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法继续，access_token 获取失败")
        return
    
    # 2. 分析错误
    current_digest = analyze_error_45004()
    
    # 3. 获取已有的素材
    print("📋 获取已有素材...")
    url = f"{WECHAT_API_BASE}/cgi-bin/material/batchget_material"
    params = {"access_token": access_token}
    
    data = {
        "type": "image",
        "offset": 0,
        "count": 1
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=10)
        result = response.json()
        
        if "item" in result and len(result["item"]) > 0:
            thumb_media_id = result["item"][0].get("media_id")
            print(f"✅ 使用素材: {thumb_media_id[:30]}...")
        else:
            print("❌ 没有可用的素材")
            return
    except Exception as e:
        print(f"❌ 获取素材时出错: {e}")
        return
    
    # 4. 检查权限
    check_draft_permissions(access_token)
    
    # 5. 创建最小化测试草稿
    draft_media_id = create_minimal_draft(access_token, thumb_media_id)
    
    if draft_media_id:
        print("\n🎉 最小化测试成功!")
        print(f"✅ 草稿创建成功: {draft_media_id}")
        print(f"📋 可以在微信公众平台草稿箱查看")
        
        # 6. 尝试创建完整草稿
        print("\n🔧 现在尝试创建完整草稿...")
        
        # 创建更短的摘要
        short_digest = "春季养生指南"
        print(f"📝 使用短摘要: '{short_digest}' ({len(short_digest)}字)")
        
        # 读取文章内容
        html_file = "wechat_article_春季中医养生指南_20260318_173832.html"
        
        if os.path.exists(html_file):
            try:
                with open(html_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
                params = {"access_token": access_token}
                
                draft_data = {
                    "articles": [{
                        "title": "春季中医养生指南",
                        "author": "娄医生",
                        "digest": short_digest,
                        "content": content,
                        "thumb_media_id": thumb_media_id,
                        "content_source_url": "",
                        "need_open_comment": 0,
                        "only_fans_can_comment": 0
                    }]
                }
                
                response = requests.post(url, params=params, json=draft_data, timeout=30)
                result = response.json()
                
                if "media_id" in result:
                    print(f"✅ 完整草稿创建成功!")
                    print(f"   media_id: {result['media_id']}")
                else:
                    print(f"❌ 完整草稿创建失败: {result}")
                    print(f"   错误代码: {result.get('errcode', '未知')}")
                    print(f"   错误信息: {result.get('errmsg', '未知')}")
            except Exception as e:
                print(f"❌ 创建完整草稿时出错: {e}")
    else:
        print("\n⚠️ 最小化测试也失败")
        print("📋 将进行更详细的测试...")
        
        # 7. 进行多个测试
        results = create_test_drafts(access_token, thumb_media_id)
        
        print("\n📊 测试结果总结:")
        for i, result in enumerate(results, 1):
            if result["success"]:
                print(f"   {i}. ✅ {result['test']['description']}: 成功")
            else:
                print(f"   {i}. ❌ {result['test']['description']}: 失败")
        
        # 分析结果
        success_count = sum(1 for r in results if r["success"])
        if success_count > 0:
            print(f"\n✅ {success_count}/{len(results)} 个测试成功")
            print("📋 说明某些摘要格式可以工作")
        else:
            print(f"\n❌ 所有测试都失败")
            print("🔍 可能的问题:")
            print("   1. 微信公众号类型限制（未认证订阅号）")
            print("   2. API 权限问题")
            print("   3. 封面图片不符合要求")
            print("   4. 其他未知限制")

if __name__ == "__main__":
    main()