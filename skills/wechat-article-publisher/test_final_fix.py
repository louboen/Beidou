#!/usr/bin/env python3
"""
测试最终修复
"""

import requests
import json
import os

# 测试 ensure_ascii 参数
test_data = {
    'title': '测试标题',
    'content': '这是一篇测试文章。'
}

print("🔧 测试 ensure_ascii 参数:")
print()

# ensure_ascii=True (默认，有问题)
json_true = json.dumps(test_data, ensure_ascii=True)
print("📊 ensure_ascii=True (默认):")
print(f"  JSON: {json_true}")
print(f"  长度: {len(json_true)} 字符")
contains_unicode = '是' if '\\u' in json_true else '否'
print(f"  包含 \\u: {contains_unicode}")
print(f"  问题: 中文被转换为 Unicode 转义")
print()

# ensure_ascii=False (修复)
json_false = json.dumps(test_data, ensure_ascii=False)
print("📊 ensure_ascii=False (修复):")
print(f"  JSON: {json_false}")
print(f"  长度: {len(json_false)} 字符")
contains_unicode = '是' if '\\u' in json_false else '否'
print(f"  包含 \\u: {contains_unicode}")
print(f"  优点: 中文保持原样")
print()

print("💡 关键发现:")
print("  requests.post(json=data) 默认使用 ensure_ascii=True")
print("  这会导致中文被转换为 Unicode 转义字符")
print("  微信 API 存储这些转义字符")
print("  微信前端显示乱码")
print()
print("🔧 解决方案:")
print("  使用 json.dumps(data, ensure_ascii=False)")
print("  然后手动编码: data.encode('utf-8')")
print("  设置正确的 Content-Type 头")
print()

# 测试实际发送
print("🎯 测试实际发送...")
url = "https://httpbin.org/post"  # 测试用的公共 API

# 错误的方式
print("\n❌ 错误的方式 (ensure_ascii=True):")
try:
    response = requests.post(url, json=test_data, timeout=5)
    print(f"  状态码: {response.status_code}")
    print(f"  发送的数据: {response.json()['json']}")
except Exception as e:
    print(f"  错误: {e}")

# 正确的方式
print("\n✅ 正确的方式 (ensure_ascii=False):")
try:
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    json_data = json.dumps(test_data, ensure_ascii=False)
    response = requests.post(url, data=json_data.encode('utf-8'), headers=headers, timeout=5)
    print(f"  状态码: {response.status_code}")
    print(f"  发送的数据: {response.json()['data']}")
except Exception as e:
    print(f"  错误: {e}")

print()
print("🎉 测试完成!")
print("💡 请使用 ensure_ascii=False 修复微信乱码问题")