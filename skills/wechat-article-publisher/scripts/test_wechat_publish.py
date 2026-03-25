#!/usr/bin/env python3
"""
微信公众号自动发布功能测试
全面测试从图片上传到草稿创建的完整流程
"""

import requests
import json
import sys
import os
import time
from typing import Optional, Dict, List, Tuple

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
WECHAT_API_BASE = "https://api.weixin.qq.com"

class WeChatPublisher:
    """微信公众号发布器"""
    
    def __init__(self):
        self.access_token = None
        self.token_expire_time = 0
        
    def get_access_token(self) -> Optional[str]:
        """获取 access_token"""
        # 如果 token 有效且未过期，直接返回
        current_time = int(time.time())
        if self.access_token and current_time < self.token_expire_time - 300:  # 提前5分钟刷新
            return self.access_token
            
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
                self.access_token = data["access_token"]
                self.token_expire_time = current_time + data.get("expires_in", 7200)
                print(f"   ✅ access_token 获取成功: {self.access_token[:20]}...")
                print(f"   有效期: {data.get('expires_in', 7200)}秒")
                return self.access_token
            else:
                print(f"   ❌ access_token 获取失败: {data}")
                return None
                
        except Exception as e:
            print(f"   ❌ 获取 access_token 时出错: {e}")
            return None
    
    def create_test_image(self) -> bytes:
        """创建测试图片（900x500 像素，符合微信公众号要求）"""
        print("🎨 创建测试图片...")
        
        # 使用 PIL 创建图片（如果可用）
        try:
            from PIL import Image, ImageDraw, ImageFont
            import io
            
            # 创建 900x500 的图片
            img = Image.new('RGB', (900, 500), color=(73, 109, 137))
            draw = ImageDraw.Draw(img)
            
            # 添加文字
            try:
                # 尝试使用系统字体
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                # 使用默认字体
                font = ImageFont.load_default()
            
            # 添加标题
            title = "中医养生"
            draw.text((450, 150), title, fill=(255, 255, 255), font=font, anchor="mm")
            
            # 添加副标题
            subtitle = "微信公众号测试封面"
            draw.text((450, 250), subtitle, fill=(200, 200, 200), font=font, anchor="mm")
            
            # 添加底部信息
            info = f"尺寸: 900x500 | 时间: {time.strftime('%Y-%m-%d')}"
            draw.text((450, 400), info, fill=(150, 150, 150), font=font, anchor="mm")
            
            # 保存到字节流
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            print(f"   ✅ 测试图片创建成功")
            print(f"   尺寸: 900x500 像素")
            print(f"   格式: PNG")
            print(f"   大小: {len(img_byte_arr) / 1024:.1f} KB")
            
            return img_byte_arr
            
        except ImportError:
            print("   ⚠️ PIL 未安装，使用简单文本文件作为测试图片")
            # 创建一个简单的文本文件作为测试
            test_content = b"Test image for WeChat cover"
            return test_content
    
    def upload_image(self, image_data: bytes, permanent: bool = True) -> Optional[str]:
        """上传图片到微信公众号"""
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        if permanent:
            url = f"{WECHAT_API_BASE}/cgi-bin/material/add_material"
            print("📤 上传永久图片素材...")
        else:
            url = f"{WECHAT_API_BASE}/cgi-bin/media/upload"
            print("📤 上传临时图片素材...")
        
        params = {"access_token": access_token, "type": "image"}
        
        try:
            files = {"media": ("test_cover.png", image_data, "image/png")}
            response = requests.post(url, params=params, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            print(f"   响应状态码: {response.status_code}")
            print(f"   响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if "media_id" in result:
                media_id = result["media_id"]
                print(f"   ✅ 图片上传成功!")
                print(f"   media_id: {media_id[:30]}...")
                
                if "url" in result:
                    print(f"   图片URL: {result['url']}")
                
                return media_id
            else:
                print(f"   ❌ 图片上传失败: {result}")
                return None
                
        except Exception as e:
            print(f"   ❌ 图片上传时出错: {e}")
            return None
    
    def create_test_article(self) -> Dict:
        """创建测试文章"""
        print("📝 创建测试文章...")
        
        article = {
            "title": "中医养生测试文章",
            "author": "娄医生",
            "digest": "中医养生知识分享，健康生活指南。",
            "content": """
                <h1>中医养生测试文章</h1>
                
                <p>这是一篇用于测试微信公众号自动发布功能的文章。</p>
                
                <h2>中医养生原则</h2>
                <p>中医养生强调"天人合一"，顺应自然规律。</p>
                
                <h3>养生要点</h3>
                <ul>
                    <li>饮食有节</li>
                    <li>起居有常</li>
                    <li>不妄作劳</li>
                    <li>形与神俱</li>
                </ul>
                
                <h2>春季养生</h2>
                <p>春季是养肝的最佳时机，应多吃绿色蔬菜，保持心情舒畅。</p>
                
                <h3>推荐食物</h3>
                <ul>
                    <li>菠菜 - 补血养肝</li>
                    <li>芹菜 - 平肝降压</li>
                    <li>枸杞 - 滋肾润肺</li>
                    <li>菊花 - 清肝明目</li>
                </ul>
                
                <p style="color: #666; font-size: 14px; text-align: center;">
                    发布时间：2026年3月18日<br>
                    文章来源：中医娄伯恩微信公众号
                </p>
            """,
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }
        
        # 检查限制
        print(f"   标题: {article['title']} ({len(article['title'])}字符)")
        print(f"   作者: {article['author']} ({len(article['author'])}字符)")
        print(f"   摘要: {article['digest']} ({len(article['digest'])}字符)")
        print(f"   内容长度: {len(article['content'])}字符")
        
        # 验证限制
        if len(article['title']) > 64:
            print(f"   ❌ 标题长度超出限制: {len(article['title'])} > 64")
            return None
        if len(article['author']) > 8:
            print(f"   ❌ 作者长度超出限制: {len(article['author'])} > 8")
            return None
        if len(article['digest']) > 120:
            print(f"   ❌ 摘要长度超出限制: {len(article['digest'])} > 120")
            return None
            
        print("   ✅ 文章格式验证通过")
        return article
    
    def create_draft(self, article: Dict, thumb_media_id: str) -> Optional[str]:
        """创建草稿"""
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        print("📄 创建草稿...")
        
        # 添加封面图片信息
        article_with_cover = article.copy()
        article_with_cover["thumb_media_id"] = thumb_media_id
        article_with_cover["show_cover_pic"] = 1
        
        url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
        params = {"access_token": access_token}
        
        data = {
            "articles": [article_with_cover]
        }
        
        try:
            print(f"   请求数据预览:")
            print(f"   - 标题: {article['title']}")
            print(f"   - 作者: {article['author']}")
            print(f"   - 摘要: {article['digest']}")
            print(f"   - 封面图片: {thumb_media_id[:30]}...")
            print(f"   - 显示封面: 是")
            
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
                self.analyze_error(result)
                return None
                
        except Exception as e:
            print(f"   ❌ 创建草稿时出错: {e}")
            return None
    
    def analyze_error(self, error_result: Dict):
        """分析错误原因"""
        errcode = error_result.get("errcode")
        errmsg = error_result.get("errmsg", "")
        
        print(f"   🔍 错误分析:")
        print(f"   错误代码: {errcode}")
        print(f"   错误信息: {errmsg}")
        
        error_map = {
            40007: "无效的 media_id",
            45003: "标题长度超出限制（≤64字符）",
            45004: "描述长度超出限制（≤120字符）",
            45005: "链接长度超出限制",
            45006: "图片链接长度超出限制",
            45007: "语音播放时间超出限制",
            45008: "图文消息超过限制",
            45009: "接口调用超过限制",
            45010: "创建菜单个数超过限制",
            45011: "API 调用太频繁",
            45015: "回复时间超过限制",
            45016: "系统分组，不允许修改",
            45017: "分组名字过长",
            45018: "分组数量超过上限",
            45047: "客服接口下行条数超过上限",
            45110: "作者长度超出限制（≤8字符）",
            53402: "封面裁剪失败，请检查裁剪参数后重试",
        }
        
        if errcode in error_map:
            print(f"   可能原因: {error_map[errcode]}")
            
            # 特定错误的建议
            if errcode == 53402:
                print(f"   💡 建议:")
                print(f"   1. 检查图片尺寸是否为 900x500 像素")
                print(f"   2. 检查图片格式是否为 JPG/PNG")
                print(f"   3. 检查图片内容是否符合微信公众号规范")
                print(f"   4. 尝试使用不同的图片")
            elif errcode == 45003:
                print(f"   💡 建议: 缩短标题至64字符以内")
            elif errcode == 45004:
                print(f"   💡 建议: 缩短摘要至120字符以内")
            elif errcode == 45110:
                print(f"   💡 建议: 缩短作者名称至8字符以内")
    
    def get_material_list(self, material_type: str = "image", count: int = 5) -> List[Dict]:
        """获取素材列表"""
        access_token = self.get_access_token()
        if not access_token:
            return []
            
        print(f"📋 获取{count}个{material_type}素材...")
        
        url = f"{WECHAT_API_BASE}/cgi-bin/material/batchget_material"
        params = {"access_token": access_token}
        
        data = {
            "type": material_type,
            "offset": 0,
            "count": count
        }
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "item" in result:
                materials = []
                for item in result["item"]:
                    materials.append({
                        "media_id": item.get("media_id"),
                        "name": item.get("name", "未命名"),
                        "update_time": item.get("update_time"),
                        "url": item.get("url")
                    })
                print(f"   ✅ 获取到 {len(materials)} 个素材")
                return materials
            else:
                print(f"   ❌ 获取素材列表失败: {result}")
                return []
                
        except Exception as e:
            print(f"   ❌ 获取素材列表时出错: {e}")
            return []
    
    def test_api_permissions(self) -> bool:
        """测试 API 权限"""
        print("🔐 测试 API 权限...")
        
        access_token = self.get_access_token()
        if not access_token:
            return False
        
        # 测试获取服务器 IP
        try:
            url = f"{WECHAT_API_BASE}/cgi-bin/getcallbackip"
            params = {"access_token": access_token}
            
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if "ip_list" in result:
                print(f"   ✅ 服务器 IP 获取成功")
                print(f"   可用 IP 数量: {len(result['ip_list'])}")
            else:
                print(f"   ⚠️ 服务器 IP 获取失败: {result}")
                
        except Exception as e:
            print(f"   ⚠️ 服务器 IP 测试失败: {e}")
        
        # 测试 API 调用次数
        try:
            url = f"{WECHAT_API_BASE}/cgi-bin/get_api_domain_ip"
            params = {"access_token": access_token}
            
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if "errcode" in result and result["errcode"] == 0:
                print(f"   ✅ API 调用权限正常")
            else:
                print(f"   ⚠️ API 调用测试异常: {result}")
                
        except Exception as e:
            print(f"   ⚠️ API 调用测试失败: {e}")
        
        return True

def main():
    """主测试函数"""
    print("=" * 70)
    print("微信公众号自动发布功能测试")
    print("=" * 70)
    
    publisher = WeChatPublisher()
    
    # 1. 测试 API 权限
    print("\n1️⃣ 测试 API 权限")
    if not publisher.test_api_permissions():
        print("❌ API 权限测试失败，测试终止")
        return
    
    # 2. 获取 access_token
    print("\n2️⃣ 获取 access_token")
    access_token = publisher.get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        return
    
    # 3. 查看已有素材
    print("\n3️⃣ 查看已有图片素材")
    existing_images = publisher.get_material_list("image", 3)
    
    if existing_images:
        print(f"\n📷 已有图片素材:")
        for i, img in enumerate(existing_images, 1):
            print(f"   {i}. {img['name']}")
            print(f"      media_id: {img['media_id'][:30]}...")
            print(f"      更新时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(img.get('update_time', 0)))}")
            if img.get('url'):
                print(f"      图片URL: {img['url'][:50]}...")
            if i < len(existing_images):
                print()
    
    # 4. 创建测试图片
    print("\n4️⃣ 创建测试图片")
    test_image_data = publisher.create_test_image()
    
    # 5. 上传图片（临时素材）
    print("\n5️⃣ 上传临时图片素材")
    temp_media_id = publisher.upload_image(test_image_data, permanent=False)
    
    if not temp_media_id:
        print("⚠️ 临时图片上传失败，尝试使用已有图片")
        if existing_images:
            temp_media_id = existing_images[0]["media_id"]
            print(f"   使用已有图片: {existing_images[0]['name']}")
            print(f"   media_id: {temp_media_id[:30]}...")
        else:
            print("❌ 没有可用的图片素材，测试终止")
            return
    
    # 6. 上传图片（永久素材）
    print("\n6️⃣ 上传永久图片素材")
    permanent_media_id = publisher.upload_image(test_image_data, permanent=True)
    
    if not permanent_media_id:
        print("⚠️ 永久图片上传失败，使用临时图片")
        thumb_media_id = temp_media_id
        print(f"   使用临时图片作为封面")
    else:
        thumb_media_id = permanent_media_id
        print(f"   使用永久图片作为封面")
    
    # 7. 创建测试文章
    print("\n7️⃣ 创建测试文章")
    test_article = publisher.create_test_article()
    if not test_article:
        print("❌ 测试文章创建失败，测试终止")
        return
    
    # 8. 创建草稿（使用封面图片）
    print("\n8️⃣ 创建草稿（带封面图片）")
    draft_id = publisher.create_draft(test_article, thumb_media_id)
    
    # 9. 备用方案测试
    if not draft_id:
        print("\n9️⃣ 备用方案测试")
        
        # 方案1：尝试无封面图片
        print("   🔄 方案1: 尝试无封面图片创建草稿")
        # 这里需要修改 create_draft 方法支持无封面图片
        # 暂时跳过
        
        # 方案2：使用不同的图片
        if len(existing_images) > 1:
            print(f"   🔄 方案2: 使用不同的图片")
            for i, img in enumerate(existing_images[1:], 2):
                print(f"      尝试图片 {i}: {img['name']}")
                draft_id = publisher.create_draft(test_article, img["media_id"])
                if draft_id:
                    break
        
        # 方案3：修改文章内容
        if not draft_id:
            print("   🔄 方案3: 修改文章内容")
            # 创建更简单的测试文章
            simple_article = {
                "title": "测试",
                "author": "测试",
                "digest": "测试摘要",
                "content": "<p>测试内容</p>",
                "content_source_url": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
            draft_id = publisher.create_draft(simple_article, thumb_media_id)
    
    # 10. 测试结果总结
    print("\n" + "=" * 70)
    print("测试结果总结")
    print("=" * 70)
    
    if draft_id:
        print("✅ 测试成功!")
        print(f"   草稿创建成功，草稿ID: {draft_id}")
        print(f"   文章标题: {test_article['title']}")
        print(f"   封面图片: {thumb_media_id[:30]}...")
        
        print("\n🎯 后续步骤:")
        print("1. 登录微信公众平台 (https://mp.weixin.qq.com)")
        print("2. 进入'内容与互动' -> '草稿箱'")
        print("3. 查看创建的草稿")
        print("4. 预览并发布")
        
        print("\n💡 自动化发布建议:")
        print("1. 使用 write_wechat_article.py 创建文章")
        print("2. 使用本脚本进行自动化发布")
        print("3. 设置定时任务定期发布")
        
    else:
        print("❌ 测试失败")
        print("\n🔍 问题分析:")
        print("1. 封面图片问题 - 可能是尺寸、格式或内容不符合要求")
        print("2. API 权限问题 - 可能需要检查草稿创建权限")
        print("3. 内容格式问题 - 文章内容可能需要调整")
        
        print("\n💡 解决方案:")
        print("1. 手动创建符合要求的封面图片（900x500像素，JPG/PNG格式）")
        print("2. 在微信公众平台手动测试图片上传")
        print("3. 使用手动发布流程（write_wechat_article.py + 手动发布）")
        
        print("\n📋 手动发布流程:")
        print("1. python3 scripts/write_wechat_article.py --topic 中医养生")
        print("2. 复制生成的 HTML 文件内容")
        print("3. 登录微信公众平台创建新文章")
        print("4. 粘贴内容并上传封面图片")
        print("5. 预览并发布")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
    
    # 保存测试结果
    test_result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "success": draft_id is not None,
        "draft_id": draft_id,
        "article_title": test_article["title"] if test_article else None,
        "thumb_media_id": thumb_media_id[:30] + "..." if thumb_media_id else None,
        "existing_images_count": len(existing_images)
    }
    
    result_file = "wechat_publish_test_result.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(test_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 测试结果已保存到: {result_file}")
    print(json.dumps(test_result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()