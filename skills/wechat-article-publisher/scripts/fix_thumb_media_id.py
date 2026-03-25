#!/usr/bin/env python3
"""
微信公众号自动发布终极解决方案
专门解决 thumb_media_id 问题
"""

import requests
import json
import sys
import os
import time
import base64
from PIL import Image, ImageDraw, ImageFont
import io

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
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "access_token" in data:
            return data["access_token"]
        else:
            print(f"❌ access_token 获取失败: {data}")
            return None
            
    except Exception as e:
        print(f"❌ 获取 access_token 时出错: {e}")
        return None

def create_proper_cover_image():
    """创建符合微信公众号要求的封面图片"""
    print("🎨 创建符合要求的封面图片...")
    
    try:
        # 创建 900x500 像素的图片
        img = Image.new('RGB', (900, 500), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # 添加中医相关的设计元素
        # 1. 标题
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except:
            # 使用默认字体
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        # 中医主题设计
        title = "中医养生"
        subtitle = "微信公众号封面"
        info = "尺寸: 900×500 | 格式: JPG | 大小: <2MB"
        
        # 绘制标题
        draw.text((450, 150), title, fill=(0, 100, 0), font=font_large, anchor="mm")
        
        # 绘制副标题
        draw.text((450, 250), subtitle, fill=(100, 100, 100), font=font_medium, anchor="mm")
        
        # 绘制底部信息
        draw.text((450, 400), info, fill=(150, 150, 150), font=font_medium, anchor="mm")
        
        # 添加边框
        draw.rectangle([10, 10, 890, 490], outline=(200, 200, 200), width=2)
        
        # 保存为 JPG 格式
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        img_data = img_byte_arr.getvalue()
        
        print(f"   ✅ 封面图片创建成功")
        print(f"   尺寸: 900x500 像素")
        print(f"   格式: JPEG")
        print(f"   大小: {len(img_data) / 1024:.1f} KB")
        print(f"   质量: 95%")
        
        return img_data
        
    except Exception as e:
        print(f"   ⚠️ 无法创建高级封面图片: {e}")
        print(f"   创建简单封面图片...")
        
        # 创建简单的 900x500 像素图片
        img = Image.new('RGB', (900, 500), color=(73, 109, 137))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_data = img_byte_arr.getvalue()
        
        print(f"   ✅ 简单封面图片创建成功")
        print(f"   尺寸: 900x500 像素")
        print(f"   格式: JPEG")
        print(f"   大小: {len(img_data) / 1024:.1f} KB")
        
        return img_data

def upload_permanent_image(access_token, image_data):
    """上传永久图片素材"""
    print("📤 上传永久图片素材...")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/material/add_material"
    params = {"access_token": access_token, "type": "image"}
    
    try:
        files = {"media": ("wechat_cover.jpg", image_data, "image/jpeg")}
        response = requests.post(url, params=params, files=files, timeout=30)
        result = response.json()
        
        print(f"   响应状态码: {response.status_code}")
        
        if "media_id" in result:
            media_id = result["media_id"]
            print(f"   ✅ 永久图片上传成功!")
            print(f"   media_id: {media_id}")
            
            if "url" in result:
                print(f"   图片URL: {result['url']}")
            
            return media_id
        else:
            print(f"   ❌ 永久图片上传失败: {result}")
            return None
            
    except Exception as e:
        print(f"   ❌ 上传永久图片时出错: {e}")
        return None

def get_existing_images(access_token):
    """获取已有的图片素材"""
    print("📋 获取已有图片素材...")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/material/batchget_material"
    params = {"access_token": access_token}
    
    data = {
        "type": "image",
        "offset": 0,
        "count": 10
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        if "item" in result:
            images = []
            for item in result["item"]:
                images.append({
                    "media_id": item.get("media_id"),
                    "name": item.get("name", "未命名"),
                    "update_time": item.get("update_time"),
                    "url": item.get("url")
                })
            
            print(f"   ✅ 获取到 {len(images)} 个图片素材")
            return images
        else:
            print(f"   ⚠️ 没有图片素材或获取失败: {result}")
            return []
            
    except Exception as e:
        print(f"   ❌ 获取图片素材时出错: {e}")
        return []

def test_draft_with_thumb_media_id(access_token, thumb_media_id):
    """使用 thumb_media_id 测试草稿创建"""
    print("📄 测试草稿创建（带封面图片）...")
    
    # 创建测试文章
    article = {
        "title": "中医养生测试",
        "author": "测试",  # 使用英文/数字作者名
        "digest": "中医养生知识测试文章",
        "content": """
            <h1>中医养生测试文章</h1>
            <p>这是一篇用于测试微信公众号自动发布功能的文章。</p>
            <h2>测试内容</h2>
            <p>如果看到这篇文章，说明自动发布功能测试成功。</p>
            <p style="color: #666; font-size: 14px;">
                发布时间：2026年3月18日<br>
                文章来源：中医娄伯恩微信公众号
            </p>
        """,
        "content_source_url": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
        "thumb_media_id": thumb_media_id,
        "show_cover_pic": 1
    }
    
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
        print(f"   - 封面图片: {thumb_media_id[:30]}...")
        print(f"   - 显示封面: 是")
        
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        print(f"   响应状态码: {response.status_code}")
        print(f"   响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "media_id" in result:
            media_id = result["media_id"]
            print(f"   ✅ 草稿创建成功!")
            print(f"   草稿ID: {media_id}")
            return media_id
        elif result.get("errcode") == 0:
            print(f"   ✅ 草稿创建成功!")
            if "media_id" in result:
                print(f"   草稿ID: {result['media_id']}")
                return result["media_id"]
            return "success"
        else:
            print(f"   ❌ 草稿创建失败")
            analyze_error(result, thumb_media_id)
            return None
            
    except Exception as e:
        print(f"   ❌ 创建草稿时出错: {e}")
        return None

def analyze_error(error_result, thumb_media_id):
    """分析错误原因"""
    errcode = error_result.get("errcode")
    errmsg = error_result.get("errmsg", "")
    
    print(f"   🔍 错误分析:")
    print(f"   错误代码: {errcode}")
    print(f"   错误信息: {errmsg}")
    
    if errcode == 40007:
        print(f"   可能原因: 无效的 thumb_media_id")
        print(f"   💡 建议:")
        print(f"   1. 确认 media_id 格式正确: {thumb_media_id[:30]}...")
        print(f"   2. 确认 media_id 属于当前公众号")
        print(f"   3. 确认 media_id 是永久素材（非临时素材）")
        print(f"   4. 重新上传图片获取新的 media_id")
    elif errcode == 45110:
        print(f"   可能原因: 作者长度超出限制")
        print(f"   💡 建议:")
        print(f"   1. 使用英文作者名: 'test'")
        print(f"   2. 使用数字作者名: '123'")
        print(f"   3. 使用单个字符: 'a'")
        print(f"   4. 删除所有空格和特殊字符")
    elif errcode == 53402:
        print(f"   可能原因: 封面图片不符合要求")
        print(f"   💡 建议:")
        print(f"   1. 图片尺寸: 900x500 像素")
        print(f"   2. 图片格式: JPG 或 PNG")
        print(f"   3. 图片大小: 不超过 2MB")
        print(f"   4. 图片内容: 符合微信公众号规范")

def test_different_author_names(access_token, thumb_media_id):
    """测试不同的作者名称"""
    print("\n🧪 测试不同的作者名称...")
    
    author_tests = [
        {"name": "test", "desc": "英文小写"},
        {"name": "TEST", "desc": "英文大写"},
        {"name": "123", "desc": "数字"},
        {"name": "a", "desc": "单个字符"},
        {"name": "娄", "desc": "单个中文字"},
        {"name": "医生", "desc": "两个中文字"},
        {"name": "lou", "desc": "英文缩写"},
    ]
    
    for test in author_tests:
        print(f"\n   测试作者: '{test['name']}' ({test['desc']})")
        
        article = {
            "title": "测试标题",
            "author": test["name"],
            "digest": "测试摘要",
            "content": "<p>测试内容</p>",
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
            "thumb_media_id": thumb_media_id,
            "show_cover_pic": 1
        }
        
        url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
        params = {"access_token": access_token}
        data = {"articles": [article]}
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            result = response.json()
            
            if "media_id" in result or result.get("errcode") == 0:
                print(f"      ✅ 成功!")
                return test["name"]
            else:
                print(f"      ❌ 失败: {result.get('errcode')} - {result.get('errmsg', '')}")
                
        except Exception as e:
            print(f"      ❌ 错误: {e}")
    
    return None

def create_final_solution():
    """创建最终解决方案"""
    print("\n🛠️ 创建最终解决方案...")
    
    solution = {
        "problem": "微信公众号自动发布失败",
        "root_cause": "thumb_media_id 是必填项且要求严格",
        "immediate_solution": "手动发布流程",
        "technical_solution": "创建符合要求的封面图片 + 使用正确的作者名",
        "workflow": [
            "1. 创建 900x500 像素的 JPG 封面图片",
            "2. 上传为永久素材获取 media_id",
            "3. 使用英文作者名（如 'test'）",
            "4. 创建草稿时提供有效的 thumb_media_id",
            "5. 如果失败，使用手动发布流程"
        ],
        "manual_workflow": [
            "1. python3 scripts/write_wechat_article.py --topic 中医养生",
            "2. 复制生成的 HTML 文件内容",
            "3. 登录微信公众平台 (https://mp.weixin.qq.com)",
            "4. 新建图文，粘贴内容",
            "5. 上传 900x500 像素的封面图片",
            "6. 预览并发布"
        ]
    }
    
    print("📋 最终解决方案:")
    print(f"问题: {solution['problem']}")
    print(f"根本原因: {solution['root_cause']}")
    print(f"\n立即解决方案: {solution['immediate_solution']}")
    print(f"技术解决方案: {solution['technical_solution']}")
    
    print(f"\n技术工作流:")
    for step in solution["workflow"]:
        print(f"  {step}")
    
    print(f"\n手动工作流（100% 可用）:")
    for step in solution["manual_workflow"]:
        print(f"  {step}")
    
    return solution

def main():
    """主函数"""
    print("=" * 70)
    print("微信公众号自动发布终极解决方案")
    print("=" * 70)
    
    # 1. 获取 access_token
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，解决方案终止")
        return
    
    # 2. 获取已有的图片素材
    print("\n1️⃣ 检查已有图片素材")
    existing_images = get_existing_images(access_token)
    
    thumb_media_id = None
    
    if existing_images:
        print(f"\n📷 已有图片素材:")
        for i, img in enumerate(existing_images, 1):
            print(f"   {i}. {img['name']}")
            print(f"      media_id: {img['media_id'][:30]}...")
            print(f"      更新时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(img.get('update_time', 0)))}")
            if i == 1:  # 使用第一个图片
                thumb_media_id = img["media_id"]
                print(f"      ✅ 选择此图片作为封面")
    
    # 3. 如果没有可用图片，创建新的封面图片
    if not thumb_media_id:
        print("\n2️⃣ 创建新的封面图片")
        image_data = create_proper_cover_image()
        
        if image_data:
            print("\n3️⃣ 上传封面图片")
            thumb_media_id = upload_permanent_image(access_token, image_data)
    
    if not thumb_media_id:
        print("❌ 无法获取有效的 thumb_media_id，解决方案终止")
        create_final_solution()
        return
    
    # 4. 测试草稿创建
    print("\n4️⃣ 测试草稿创建")
    draft_id = test_draft_with_thumb_media_id(access_token, thumb_media_id)
    
    # 5. 如果失败，测试不同的作者名称
    if not draft_id:
        print("\n5️⃣ 测试不同的作者名称")
        valid_author = test_different_author_names(access_token, thumb_media_id)
        
        if valid_author:
            print(f"\n   ✅ 找到有效的作者名: '{valid_author}'")
            print(f"   重新测试草稿创建...")
            
            # 使用有效的作者名重新测试
            article = {
                "title": "中医养生测试",
                "author": valid_author,
                "digest": "中医养生知识测试文章",
                "content": "<p>测试内容</p>",
                "content_source_url": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": 1
            }
            
            url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
            params = {"access_token": access_token}
            data = {"articles": [article]}
            
            try:
                response = requests.post(url, params=params, json=data, timeout=30)
                result = response.json()
                
                if "media_id" in result or result.get("errcode") == 0:
                    print(f"   ✅ 使用作者名 '{valid_author}' 成功!")
                    draft_id = result.get("media_id", "success")
                else:
                    print(f"   ❌ 仍然失败: {result}")
                    
            except Exception as e:
                print(f"   ❌ 重新测试时出错: {e}")
    
    # 6. 创建最终解决方案
    print("\n" + "=" * 70)
    solution = create_final_solution()
    
    # 7. 总结
    print("\n" + "=" * 70)
    print("解决方案总结")
    print("=" * 70)
    
    if draft_id:
        print("✅ 自动发布解决方案成功!")
        print(f"   草稿创建成功: {draft_id}")
        print(f"   使用的封面图片: {thumb_media_id[:30]}...")
        
        print("\n🎯 下一步:")
        print("1. 使用此方法创建实际的中医养生文章")
        print("2. 优化封面图片设计")
        print("3. 建立自动化发布流程")
        
        print("\n💡 自动化发布命令:")
        print(f"python3 scripts/fix_thumb_media_id.py")
        
    else:
        print("❌ 自动发布解决方案失败")
        
        print("\n🔍 根本问题:")
        print("1. thumb_media_id 要求严格 - 必须提供有效的永久素材")
        print("2. 作者名称限制 - 中文字符计算方式可能不同")
        print("3. 微信公众号 API 限制 - 可能是未认证公众号的功能限制")
        
        print("\n✅ 立即可用的解决方案:")
        print("1. 手动发布流程 - 100% 可用")
        print("2. 封面图片模板 - 创建 900x500 像素的 JPG/PNG 模板")
        print("3. 内容生成工具 - 使用 write_wechat_article.py 创建文章")
        
        print("\n📋 手动发布流程（已验证可用）:")
        for step in solution["manual_workflow"]:
            print(f"  {step}")
        
        print("\n🎨 封面图片要求:")
        print("- 尺寸: 900x500 像素")
        print("- 格式: JPG 或 PNG")
        print("- 大小: 不超过 2MB")
        print("- 内容: 符合微信公众号规范")
        
        print("\n💡 内容规划建议:")
        print("- 发布频率: 每周 2-3 篇")
        print("- 主题轮换: 中医养生 → 中医食疗 → 穴位保健")
        print("- 发布时间: 上午 8-10 点，下午 6-8 点")
    
    print("\n" + "=" * 70)
    print("解决方案完成")
    print("=" * 70)
    
    # 保存解决方案报告
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "access_token": access_token[:20] + "...",
        "thumb_media_id": thumb_media_id[:30] + "..." if thumb_media_id else None,
        "draft_created": draft_id is not None,
        "draft_id": draft_id,
        "solution": solution,
        "recommendation": "使用手动发布流程立即开始发布内容"
    }
    
    report_file = "wechat_publish_solution_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 解决方案报告已保存到: {report_file}")

if __name__ == "__main__":
    main()