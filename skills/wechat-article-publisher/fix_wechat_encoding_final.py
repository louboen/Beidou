#!/usr/bin/env python3
"""
最终解决微信编码问题
问题：微信 API 存储内容为 Unicode 转义，但前端显示乱码
解决方案：确保发送到 API 的内容是纯 UTF-8 编码，不是 Unicode 转义
"""

import requests
import json
import os
import re
import time
from pathlib import Path

class WeChatEncoder:
    """微信编码处理器"""
    
    @staticmethod
    def ensure_utf8_not_unicode_escape(text):
        """
        确保文本是 UTF-8 编码，不是 Unicode 转义
        将 Unicode 转义字符转换为实际 UTF-8 字符
        """
        if not text:
            return text
        
        # 检查是否包含 Unicode 转义
        unicode_pattern = r'\\u[0-9a-fA-F]{4}'
        matches = re.findall(unicode_pattern, text)
        
        if not matches:
            # 没有 Unicode 转义，直接返回
            return text
        
        print(f"🔧 发现 {len(matches)} 个 Unicode 转义字符，转换为 UTF-8...")
        
        # 方法1: 使用 unicode_escape 解码
        try:
            # 确保文本是字符串，然后编码为 latin-1 再解码
            decoded = text.encode('latin-1').decode('unicode_escape')
            print("✅ 使用 unicode_escape 解码成功")
            return decoded
        except Exception as e:
            print(f"❌ unicode_escape 解码失败: {e}")
        
        # 方法2: 使用 JSON 解码
        try:
            # 包装在 JSON 字符串中
            decoded = json.loads(f'"{text}"')
            print("✅ 使用 JSON 解码成功")
            return decoded
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解码失败: {e}")
        
        # 方法3: 手动替换
        print("🔄 尝试手动替换...")
        decoded_text = text
        replaced_count = 0
        
        for match in set(matches):  # 去重
            try:
                # 解码单个 Unicode 转义字符
                char = match.encode('latin-1').decode('unicode_escape')
                decoded_text = decoded_text.replace(match, char)
                replaced_count += 1
            except:
                pass
        
        print(f"✅ 手动替换 {replaced_count} 个字符")
        return decoded_text
    
    @staticmethod
    def read_and_convert_file(file_path):
        """读取文件并确保 UTF-8 编码"""
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ 读取文件: {os.path.basename(file_path)}")
            print(f"📊 原始长度: {len(content)} 字符")
            
            # 转换 Unicode 转义
            converted = WeChatEncoder.ensure_utf8_not_unicode_escape(content)
            
            if converted != content:
                print(f"📈 转换后长度: {len(converted)} 字符")
                print("📋 转换示例:")
                
                # 显示转换前后的对比
                sample_original = content[:100]
                sample_converted = converted[:100]
                
                if sample_original != sample_converted:
                    print(f"  原始: {repr(sample_original)}")
                    print(f"  转换: {repr(sample_converted)}")
            
            return converted
            
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return None

class WeChatPublisherFinal:
    """微信公众号发布器（最终版）"""
    
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
    
    def create_draft_final(self, title, author, content, thumb_media_id):
        """创建草稿（最终版，确保 UTF-8 编码）"""
        if not thumb_media_id:
            print("❌ 错误: thumb_media_id 不能为空")
            return None
        
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {'access_token': access_token}
        
        # 确保所有文本都是 UTF-8，不是 Unicode 转义
        title_utf8 = WeChatEncoder.ensure_utf8_not_unicode_escape(title)
        author_utf8 = WeChatEncoder.ensure_utf8_not_unicode_escape(author)
        content_utf8 = WeChatEncoder.ensure_utf8_not_unicode_escape(content)
        
        # 准备文章数据
        article = {
            'title': title_utf8[:64],
            'author': author_utf8[:8],
            'digest': f'{title_utf8[:50]}...' if len(title_utf8) > 50 else title_utf8,
            'content': content_utf8,
            'content_source_url': '',
            'thumb_media_id': thumb_media_id,
            'need_open_comment': 0,
            'only_fans_can_comment': 0
        }
        
        # 验证编码
        print(f"\n📤 发送数据验证（确保 UTF-8）:")
        print(f"  标题: {repr(article['title'])}")
        print(f"  作者: {repr(article['author'])}")
        print(f"  摘要: {repr(article['digest'])}")
        print(f"  内容前100字符: {repr(content_utf8[:100])}")
        contains_unicode = '是' if '\\u' in content_utf8[:100] else '否'
        print(f"  内容是否包含 \\u: {contains_unicode}")
        
        data = {'articles': [article]}
        
        try:
            # 发送请求
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            response = requests.post(
                url, 
                params=params, 
                json=data, 
                headers=headers,
                timeout=30
            )
            
            result = response.json()
            return result
            
        except Exception as e:
            print(f"❌ 创建草稿异常: {e}")
            return {'errcode': -1, 'errmsg': str(e)}
    
    def publish_article_final(self, html_path, title=None, author="娄医", cover_image_path=None):
        """发布文章（最终版）"""
        print("=" * 60)
        print("微信公众号发布（最终编码修复版）")
        print("=" * 60)
        
        # 1. 读取并转换文件
        content = WeChatEncoder.read_and_convert_file(html_path)
        if not content:
            return False
        
        # 2. 提取标题
        if not title:
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                title = title_match.group(1)
                print(f"📝 从 HTML 提取标题: {title}")
            else:
                title = "未命名文章"
        
        # 3. 上传封面
        if cover_image_path and os.path.exists(cover_image_path):
            thumb_media_id = self.upload_permanent_image(cover_image_path)
        else:
            # 使用默认图片
            default_images = ['wechat_personal_qr.jpg', 'wechat_qr.jpg']
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
        print(f"\n🎯 创建草稿（确保 UTF-8 编码）...")
        result = self.create_draft_final(title, author, content, thumb_media_id)
        
        print(f"\n📊 发布结果: {json.dumps(result, ensure_ascii=False)}")
        
        if 'media_id' in result:
            print(f"\n🎉 文章发布成功!")
            print(f"📄 文章: {title}")
            print(f"👤 作者: {author}")
            print(f"🆔 草稿ID: {result['media_id']}")
            
            # 立即检查草稿内容
            self.check_draft_encoding(result['media_id'])
            
            return True
        else:
            print(f"\n❌ 文章发布失败")
            self.analyze_error(result)
            return False
    
    def check_draft_encoding(self, draft_media_id):
        """检查草稿编码"""
        print(f"\n🔍 检查草稿编码: {draft_media_id[:30]}...")
        
        access_token = self.get_access_token()
        if not access_token:
            return
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/get"
        params = {'access_token': access_token}
        get_data = {'media_id': draft_media_id}
        
        try:
            # 🔧 修复：使用 data= 参数
            json_get_data = json.dumps(get_data, ensure_ascii=False)
            response = requests.post(
                url, 
                params=params, 
                data=json_get_data.encode('utf-8'),
                headers={'Content-Type': 'application/json; charset=utf-8'},
                timeout=30
            )
            result = response.json()
            
            if 'news_item' in result:
                article = result['news_item'][0]
                
                print(f"📋 微信返回的内容:")
                print(f"  标题: {repr(article.get('title', ''))}")
                print(f"  作者: {repr(article.get('author', ''))}")
                
                content = article.get('content', '')
                print(f"  内容前100字符: {repr(content[:100])}")
                
                # 检查是否包含 Unicode 转义
                unicode_count = len(re.findall(r'\\u[0-9a-fA-F]{4}', content[:200]))
                print(f"  前200字符中 Unicode 转义数量: {unicode_count}")
                
                if unicode_count > 0:
                    print("⚠️  警告: 微信 API 返回了 Unicode 转义字符")
                    print("💡 这可能意味着微信内部存储就是这种格式")
                else:
                    print("✅ 微信返回了纯 UTF-8 编码")
                    
            else:
                print(f"❌ 无法获取草稿内容: {result}")
                
        except Exception as e:
            print(f"❌ 检查草稿失败: {e}")
    
    def analyze_error(self, result):
        """分析错误"""
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

def create_test_article():
    """创建测试文章"""
    return """<!DOCTYPE html>
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

def main():
    """主函数"""
    print("🚀 微信公众号最终编码修复发布")
    print("📅 时间: 2026-03-19")
    print()
    
    # 创建发布器
    try:
        publisher = WeChatPublisherFinal()
    except ValueError as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 测试 1: 使用修复后的文章
    print("\n📋 测试 1: 修复后的文章")
    
    test_file = 'articles/fixed_中医食疗_养生食谱.html'
    if os.path.exists(test_file):
        success = publisher.publish_article_final(
            test_file,
            title='中医食疗养生方（最终测试）',
            author='娄医',
            cover_image_path='wechat_personal_qr.jpg'
        )
    else:
        print(f"❌ 测试文件不存在: {test_file}")
        
        # 创建临时测试文件
        temp_file = 'temp_test_article.html'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(create_test_article())
        
        success = publisher.publish_article_final(
            temp_file,
            title='编码测试文章',
            author='测试',
            cover_image_path='wechat_personal_qr.jpg'
        )
        
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # 测试 2: 纯中文测试
    print("\n📋 测试 2: 纯中文测试")
    
    pure_chinese = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>纯中文测试</title>
</head>
<body>
    <h1>纯中文测试文章</h1>
    <p>这是一篇纯中文测试文章，没有任何Unicode转义字符。</p>
    <p>中医养生，药食同源。</p>
</body>
</html>"""
    
    temp_file2 = 'temp_pure_chinese.html'
    with open(temp_file2, 'w', encoding='utf-8') as f:
        f.write(pure_chinese)
    
    success2 = publisher.publish_article_final(
        temp_file2,
        title='纯中文测试',
        author='测试',
        cover_image_path='wechat_personal_qr.jpg'
    )
    
    # 清理临时文件
    if os.path.exists(temp_file2):
        os.remove(temp_file2)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    print("\n💡 关键修复:")
