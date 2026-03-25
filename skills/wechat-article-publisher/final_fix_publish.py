#!/usr/bin/env python3
"""
最终修复方案：解决编码问题和 media_id 问题
"""

import requests
import json
import os
import re
import time
from pathlib import Path

class WeChatPublisher:
    """微信公众号发布器（最终修复版）"""
    
    def __init__(self):
        self.config = self.load_config()
        self.appid = self.config.get('WECHAT_APPID')
        self.appsecret = self.config.get('WECHAT_APPSECRET')
        self.access_token = None
        self.token_expire_time = 0
        
        if not self.appid or not self.appsecret:
            raise ValueError("微信配置不完整")
    
    def load_config(self):
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
    
    def get_access_token(self):
        """获取 access_token"""
        current_time = time.time()
        
        if self.access_token and current_time < self.token_expire_time:
            return self.access_token
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': self.appid,
            'secret': self.appsecret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if 'access_token' in result:
                self.access_token = result['access_token']
                self.token_expire_time = current_time + result.get('expires_in', 7200) - 300
                return self.access_token
            else:
                print(f"❌ 获取 access_token 失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 获取 access_token 异常: {e}")
            return None
    
    def upload_permanent_image(self, image_path):
        """上传图片为永久素材"""
        if not os.path.exists(image_path):
            print(f"❌ 图片文件不存在: {image_path}")
            return None
        
        access_token = self.get_access_token()
        if not access_token:
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
    
    def read_and_fix_content(self, html_path):
        """读取并修复文章内容"""
        if not os.path.exists(html_path):
            print(f"❌ 文章文件不存在: {html_path}")
            return None
        
        try:
            # 读取文件
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ 读取文章: {os.path.basename(html_path)}")
            print(f"📊 原始长度: {len(content)} 字符")
            
            # 检查并修复 Unicode 转义字符
            unicode_pattern = r'\\u[0-9a-fA-F]{4}'
            matches = re.findall(unicode_pattern, content)
            
            if matches:
                print(f"⚠️  发现 {len(matches)} 个 Unicode 转义字符")
                
                # 显示示例
                print("📋 示例转义字符:")
                for i, match in enumerate(set(matches)[:3]):
                    try:
                        decoded = match.encode('ascii').decode('unicode_escape')
                        print(f"  {match} → {decoded}")
                    except:
                        print(f"  {match} → 解码失败")
                
                # 尝试修复
                print("🔄 尝试修复...")
                
                # 方法1: JSON 解码
                try:
                    fixed_content = json.loads(f'"{content}"')
                    print("✅ 使用 JSON 解码修复成功")
                    return fixed_content
                except json.JSONDecodeError:
                    # 方法2: unicode_escape
                    try:
                        fixed_content = content.encode('utf-8').decode('unicode_escape')
                        print("✅ 使用 unicode_escape 修复成功")
                        return fixed_content
                    except:
                        # 方法3: 手动替换
                        fixed_content = content
                        for match in set(matches):
                            try:
                                decoded = match.encode('ascii').decode('unicode_escape')
                                fixed_content = fixed_content.replace(match, decoded)
                            except:
                                pass
                        print("✅ 使用手动替换修复")
                        return fixed_content
            else:
                print("✅ 未发现 Unicode 转义字符")
                return content
                
        except Exception as e:
            print(f"❌ 读取文章异常: {e}")
            return None
    
    def create_draft(self, title, author, content, thumb_media_id):
        """创建草稿（必须提供有效的 thumb_media_id）"""
        if not thumb_media_id:
            print("❌ 错误: thumb_media_id 不能为空")
            return None
        
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {'access_token': access_token}
        
        # 准备文章数据（严格遵循微信要求）
        article = {
            'title': title[:64],  # 微信限制标题≤64字符
            'author': author[:8],  # 微信限制作者≤8字符
            'digest': f'{title[:50]}...' if len(title) > 50 else title,
            'content': content,
            'content_source_url': '',
            'thumb_media_id': thumb_media_id,  # 必须有效
            'need_open_comment': 0,
            'only_fans_can_comment': 0
        }
        
        # 验证数据
        print(f"\n📤 发送数据验证:")
        print(f"  标题: {article['title']} ({len(article['title'])}字符)")
        print(f"  作者: {article['author']} ({len(article['author'])}字符)")
        print(f"  摘要: {article['digest']}")
        print(f"  media_id: {thumb_media_id[:30]}...")
        print(f"  内容预览: {content[:100]}...")
        
        data = {'articles': [article]}
        
        try:
            # 🔧 关键修复：使用 ensure_ascii=False
            json_data = json.dumps(data, ensure_ascii=False)
            response = requests.post(
                url, 
                params=params, 
                data=json_data.encode('utf-8'),
                headers={'Content-Type': 'application/json; charset=utf-8'},
                timeout=30
            )
            result = response.json()
            
            return result
            
        except Exception as e:
            print(f"❌ 创建草稿异常: {e}")
            return {'errcode': -1, 'errmsg': str(e)}
    
    def publish_article(self, html_path, title=None, author="娄医", cover_image_path=None):
        """发布文章主函数"""
        print("=" * 60)
        print("微信公众号发布（最终修复版）")
        print("=" * 60)
        
        # 1. 读取并修复文章内容
        content = self.read_and_fix_content(html_path)
        if not content:
            return False
        
        # 2. 如果没有提供标题，从 HTML 中提取
        if not title:
            # 从 HTML 中提取标题
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                title = title_match.group(1)
                print(f"📝 从 HTML 提取标题: {title}")
            else:
                title = "未命名文章"
                print("⚠️  无法从 HTML 提取标题，使用默认标题")
        
        # 3. 上传封面图片（必须提供）
        if cover_image_path and os.path.exists(cover_image_path):
            thumb_media_id = self.upload_permanent_image(cover_image_path)
        else:
            # 使用默认图片
            default_images = ['wechat_personal_qr.jpg', 'wechat_qr.jpg', 'cover_default.jpg']
            thumb_media_id = None
            
            for img in default_images:
                if os.path.exists(img):
                    thumb_media_id = self.upload_permanent_image(img)
                    if thumb_media_id:
                        break
            
            if not thumb_media_id:
                print("❌ 无法获取有效的封面图片 media_id")
                return False
        
        # 4. 创建草稿
        print(f"\n🎯 创建草稿...")
        result = self.create_draft(title, author, content, thumb_media_id)
        
        print(f"\n📊 发布结果: {json.dumps(result, ensure_ascii=False)}")
        
        if 'media_id' in result:
            print(f"\n🎉 文章发布成功!")
            print(f"📄 文章: {title}")
            print(f"👤 作者: {author}")
            print(f"🆔 草稿ID: {result['media_id']}")
            return True
        else:
            print(f"\n❌ 文章发布失败")
            
            # 分析错误
            errcode = result.get('errcode')
            errmsg = result.get('errmsg', '')
            
            print(f"🔍 错误分析:")
            print(f"  错误代码: {errcode}")
            print(f"  错误信息: {errmsg}")
            
            if errcode == 40007:
                print("  💡 原因: media_id 无效")
                print("  🔧 解决方案: 确保使用永久素材的 media_id")
            elif errcode == 45003:
                print("  💡 原因: 标题长度超限")
                print("  🔧 解决方案: 缩短标题（≤64字符）")
            elif errcode == 45110:
                print("  💡 原因: 作者名长度超限")
                print("  🔧 解决方案: 缩短作者名（≤8字符）")
            
            return False

def main():
    """主函数"""
    print("🚀 微信公众号最终修复发布")
    print("📅 时间: 2026-03-19")
    print()
    
    # 创建发布器
    try:
        publisher = WeChatPublisher()
    except ValueError as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 测试发布修复后的文章
    test_cases = [
        {
            'name': '修复后文章',
            'html_path': 'articles/fixed_中医食疗_养生食谱.html',
            'title': '中医食疗养生方',
            'author': '娄医',
            'cover': 'wechat_personal_qr.jpg'
        },
        {
            'name': '简单测试文章',
            'html_path': None,  # 使用内置内容
            'title': '中医养生测试',
            'author': '娄医',
            'cover': 'wechat_personal_qr.jpg',
            'content': """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>中医养生测试</title>
</head>
<body>
    <h1>中医养生测试文章</h1>
    <p>这是一篇测试文章，验证中文显示是否正常。</p>
    <p>中医认为：药食同源，养生之道在于平衡。</p>
</body>
</html>"""
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试 {i}: {test_case['name']}")
        
        if test_case['html_path'] and os.path.exists(test_case['html_path']):
            # 使用文件
            success = publisher.publish_article(
                test_case['html_path'],
                test_case['title'],
                test_case['author'],
                test_case['cover']
            )
        elif 'content' in test_case:
            # 使用内置内容
            print("📄 使用内置测试内容")
            
            # 创建临时文件
            temp_file = f"temp_test_{i}.html"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(test_case['content'])
            
            success = publisher.publish_article(
                temp_file,
                test_case['title'],
                test_case['author'],
                test_case['cover']
            )
            
            # 清理临时文件
            if os.path.exists(temp_file):
                os.remove(temp_file)
        else:
            print("❌ 测试用例配置错误")
            continue
        
        if success:
            success_count += 1
        
        # 避免频率限制
        if i < len(test_cases):
            print("\n⏳ 等待3秒避免频率限制...")
            time.sleep(3)
    
    # 总结
    print("\n" + "=" * 60)
    print("发布完成总结")
    print("=" * 60)
    print(f"📊 总测试数: {len(test_cases)}")
    print(f"✅ 成功数: {success_count}")
    print(f"❌ 失败数: {len(test_cases) - success_count}")
    
    if success_count > 0:
        print("\n🎉 修复成功!")
        print("💡 关键修复:")
        print("  1. 修复 Unicode 转义字符编码问题")
        print("  2. 必须使用有效的永久素材 media_id")
        print("  3. 自动验证标题和作者长度")
    else:
        print("\n❌ 修复失败")
        print("🔧 请检查:")
        print("  1. 微信公众号权限设置")
        print("  2. 封面图片是否有效")
        print("  3. API 调用频率限制")

if __name__ == "__main__":
    main()