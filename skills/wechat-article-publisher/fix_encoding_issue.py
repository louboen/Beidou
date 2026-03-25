#!/usr/bin/env python3
"""
修复微信文章编码问题
问题：发布的文章显示为 Unicode 转义字符（如 \u4e2d\u533b）
原因：微信 API 对 HTML 内容编码处理问题
"""

import json
import re
import os
from pathlib import Path

def decode_unicode_escape(text):
    """解码 Unicode 转义字符"""
    try:
        # 方法1: 使用 json.loads 解码
        decoded = json.loads(f'"{text}"')
        return decoded
    except:
        # 方法2: 使用 unicode_escape 解码
        try:
            return text.encode('utf-8').decode('unicode_escape')
        except:
            # 方法3: 手动替换常见 Unicode 转义
            return text

def fix_html_encoding(html_content):
    """修复 HTML 内容的编码问题"""
    if not html_content:
        return html_content
    
    # 检查是否包含 Unicode 转义字符
    unicode_pattern = r'\\u[0-9a-fA-F]{4}'
    matches = re.findall(unicode_pattern, html_content)
    
    if matches:
        print(f"⚠️  发现 {len(matches)} 个 Unicode 转义字符")
        
        # 尝试解码整个内容
        try:
            # 将内容包装在 JSON 字符串中解码
            fixed_content = json.loads(f'"{html_content}"')
            print("✅ 使用 JSON 解码成功")
            return fixed_content
        except:
            print("❌ JSON 解码失败，尝试其他方法")
    
    # 如果没有 Unicode 转义，直接返回
    return html_content

def test_wechat_api_encoding():
    """测试微信 API 编码处理"""
    print("🔍 测试微信 API 编码处理...")
    
    # 测试字符串
    test_strings = [
        "中医食疗养生方",
        "作者: 娄医生",
        "药食同源，中医食疗养生方助您健康生活。",
        "一、食疗原则",
        "中医认为\"药食同源\"，食物不仅可以充饥，还能调理身体。"
    ]
    
    for i, text in enumerate(test_strings, 1):
        print(f"\n测试 {i}: {text}")
        
        # 检查原始编码
        print(f"  原始: {repr(text)}")
        print(f"  UTF-8: {text.encode('utf-8')}")
        
        # 模拟可能的编码问题
        unicode_escaped = text.encode('unicode_escape').decode('ascii')
        print(f"  Unicode 转义: {unicode_escaped}")
        
        # 尝试解码
        try:
            decoded = unicode_escaped.encode('ascii').decode('unicode_escape')
            print(f"  解码后: {decoded}")
            print(f"  ✅ 解码成功")
        except Exception as e:
            print(f"  ❌ 解码失败: {e}")

def check_article_files():
    """检查文章文件的编码"""
    print("\n📄 检查文章文件编码...")
    
    article_files = [
        'articles/auto_中医食疗_养生食谱.html',
        'articles/auto_中医养生_春季养生.html',
        'articles/auto_穴位保健_常用穴位.html'
    ]
    
    for file_path in article_files:
        if os.path.exists(file_path):
            print(f"\n检查文件: {file_path}")
            
            try:
                # 尝试不同编码读取
                encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
                
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read(500)  # 只读取前500字符
                        
                        # 检查是否包含 Unicode 转义
                        unicode_count = len(re.findall(r'\\u[0-9a-fA-F]{4}', content))
                        
                        if unicode_count > 0:
                            print(f"  ⚠️  {encoding}: 发现 {unicode_count} 个 Unicode 转义字符")
                        else:
                            print(f"  ✅ {encoding}: 编码正常")
                            
                        # 显示前100字符
                        preview = content[:100].replace('\n', ' ')
                        print(f"    预览: {preview}...")
                        
                    except UnicodeDecodeError:
                        print(f"  ❌ {encoding}: 解码失败")
                        
            except Exception as e:
                print(f"  ❌ 检查失败: {e}")
        else:
            print(f"\n❌ 文件不存在: {file_path}")

def create_fixed_article():
    """创建修复后的文章"""
    print("\n🔧 创建修复后的文章...")
    
    source_file = 'articles/auto_中医食疗_养生食谱.html'
    target_file = 'articles/fixed_中医食疗_养生食谱.html'
    
    if not os.path.exists(source_file):
        print(f"❌ 源文件不存在: {source_file}")
        return None
    
    try:
        # 读取原始内容
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ 读取原始文章: {len(content)} 字符")
        
        # 检查编码问题
        unicode_pattern = r'\\u[0-9a-fA-F]{4}'
        matches = re.findall(unicode_pattern, content)
        
        if matches:
            print(f"⚠️  发现 {len(matches)} 个 Unicode 转义字符")
            
            # 尝试修复
            try:
                # 方法1: 使用 JSON 解码
                fixed_content = json.loads(f'"{content}"')
                print("✅ 使用 JSON 解码修复")
            except:
                # 方法2: 使用 unicode_escape 解码
                try:
                    fixed_content = content.encode('utf-8').decode('unicode_escape')
                    print("✅ 使用 unicode_escape 解码修复")
                except Exception as e:
                    print(f"❌ 解码失败: {e}")
                    # 方法3: 手动替换
                    fixed_content = content
                    for match in set(matches):  # 去重
                        try:
                            decoded = match.encode('ascii').decode('unicode_escape')
                            fixed_content = fixed_content.replace(match, decoded)
                        except:
                            pass
                    print("✅ 使用手动替换修复")
        else:
            print("✅ 未发现 Unicode 转义字符")
            fixed_content = content
        
        # 保存修复后的文件
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ 保存修复后的文章: {target_file}")
        print(f"📊 文件大小: {len(fixed_content)} 字符")
        
        return target_file
        
    except Exception as e:
        print(f"❌ 创建修复文章失败: {e}")
        return None

def update_publish_script():
    """更新发布脚本，修复编码问题"""
    print("\n📝 更新发布脚本...")
    
    script_file = 'auto_publish_final.py'
    
    if not os.path.exists(script_file):
        print(f"❌ 脚本文件不存在: {script_file}")
        return False
    
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找 read_article_content 方法
        method_start = content.find('def read_article_content')
        if method_start == -1:
            print("❌ 找不到 read_article_content 方法")
            return False
        
        # 查找方法结束
        method_end = content.find('\n    def ', method_start + 1)
        if method_end == -1:
            method_end = len(content)
        
        method_content = content[method_start:method_end]
        
        print("📋 当前 read_article_content 方法:")
        print("-" * 40)
        print(method_content)
        print("-" * 40)
        
        # 创建修复版本
        fixed_method = '''    def read_article_content(self, html_path):
        """读取文章内容，修复编码问题"""
        if not os.path.exists(html_path):
            print(f"❌ 文章文件不存在: {html_path}")
            return None
        
        try:
            # 读取文件内容
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ 文章读取成功: {os.path.basename(html_path)}")
            print(f"📊 内容长度: {len(content)} 字符")
            
            # 检查并修复 Unicode 转义字符
            import re
            import json
            
            unicode_pattern = r'\\\\u[0-9a-fA-F]{4}'
            matches = re.findall(unicode_pattern, content)
            
            if matches:
                print(f"⚠️  发现 {len(matches)} 个 Unicode 转义字符，尝试修复...")
                
                try:
                    # 尝试使用 JSON 解码修复
                    fixed_content = json.loads(f'"{content}"')
                    print("✅ Unicode 转义字符修复成功")
                    return fixed_content
                except:
                    print("⚠️  JSON 解码失败，返回原始内容")
                    return content
            else:
                print("✅ 未发现 Unicode 转义字符")
                return content
                
        except Exception as e:
            print(f"❌ 读取文章异常: {e}")
            return None'''
        
        # 替换方法
        fixed_content = content[:method_start] + fixed_method + content[method_end:]
        
        # 保存更新后的脚本
        backup_file = f"{script_file}.backup"
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ 发布脚本已更新")
        print(f"📁 原始脚本备份: {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新脚本失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("微信文章编码问题修复工具")
    print("=" * 60)
    
    # 1. 测试编码处理
    test_wechat_api_encoding()
    
    # 2. 检查文章文件
    check_article_files()
    
    # 3. 创建修复后的文章
    fixed_file = create_fixed_article()
    
    # 4. 更新发布脚本
    if update_publish_script():
        print("\n🎉 修复完成!")
        print("\n📋 下一步:")
        print("1. 使用修复后的文章测试发布:")
        print(f"   python3 auto_publish_final.py")
        print("2. 或者使用修复后的文章:")
        print(f"   {fixed_file}")
        print("3. 检查微信平台是否正常显示")
    else:
        print("\n❌ 修复失败，请手动检查")

if __name__ == "__main__":
    main()