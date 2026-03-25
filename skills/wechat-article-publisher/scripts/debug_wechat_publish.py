#!/usr/bin/env python3
"""
微信公众号自动发布问题深度诊断
查找根本原因并提供解决方案
"""

import requests
import json
import sys
import os
import time
import re

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

def analyze_error_patterns():
    """分析错误模式"""
    print("🔍 分析错误模式...")
    
    # 收集到的错误信息
    errors = [
        {
            "code": 40007,
            "message": "invalid media_id",
            "context": "即使不使用封面图片也出现",
            "tests": ["官方示例", "最简化数据", "无封面测试"]
        },
        {
            "code": 45110,
            "message": "author size out of limit",
            "context": "作者'娄医生'只有3个字符",
            "tests": ["使用永久素材", "带封面图片"]
        },
        {
            "code": 53402,
            "message": "封面裁剪失败",
            "context": "封面图片不符合要求",
            "tests": ["使用临时素材", "使用永久素材"]
        }
    ]
    
    print("📋 错误模式总结:")
    for error in errors:
        print(f"  • 错误 {error['code']}: {error['message']}")
        print(f"    上下文: {error['context']}")
        print(f"    出现场景: {', '.join(error['tests'])}")
        print()

def check_wechat_account_type(access_token):
    """检查微信公众号类型"""
    print("📱 检查微信公众号类型...")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/account/getaccount"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "errcode" in result:
            print(f"   ⚠️ 无法获取账户信息: {result.get('errmsg')}")
            return None
        else:
            print(f"   ✅ 账户信息获取成功")
            return result
            
    except Exception as e:
        print(f"   ❌ 检查账户类型时出错: {e}")
        return None

def test_draft_api_directly(access_token):
    """直接测试草稿 API"""
    print("🧪 直接测试草稿 API...")
    
    # 测试 1: 使用最简单的 JSON
    print("1. 测试最简单的 JSON 结构...")
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    # 最简单的可能结构
    simple_data = {
        "articles": [
            {
                "title": "T",
                "author": "A",
                "digest": "D",
                "content": "C"
            }
        ]
    }
    
    try:
        response = requests.post(url, params=params, json=simple_data, timeout=30)
        result = response.json()
        
        print(f"   请求数据: {json.dumps(simple_data, indent=2, ensure_ascii=False)}")
        print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "media_id" in result:
            print(f"   ✅ 成功! 草稿ID: {result['media_id']}")
            return True
        else:
            print(f"   ❌ 失败")
            
    except Exception as e:
        print(f"   ❌ 测试出错: {e}")
    
    # 测试 2: 使用 curl 命令格式（排除 Python 库问题）
    print("\n2. 生成 curl 命令测试...")
    
    curl_command = f"""curl -X POST \\
  "https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}" \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(simple_data, ensure_ascii=False)}'"""
    
    print(f"   curl 命令:\n{curl_command}")
    
    # 测试 3: 检查 API 文档要求
    print("\n3. 检查 API 文档要求...")
    print("   根据微信公众号官方文档:")
    print("   - 标题(title): 必填，不超过64字符")
    print("   - 作者(author): 必填，不超过8字符")
    print("   - 摘要(digest): 必填，不超过120字符")
    print("   - 内容(content): 必填，支持HTML")
    print("   - 封面图片(thumb_media_id): 必填")
    print("   - 显示封面(show_cover_pic): 选填，0或1")
    
    return False

def check_api_permissions_detail(access_token):
    """详细检查 API 权限"""
    print("🔐 详细检查 API 权限...")
    
    # 检查接口调用次数
    print("1. 检查接口调用次数...")
    url = f"{WECHAT_API_BASE}/cgi-bin/get_api_domain_ip"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if "errcode" in result and result["errcode"] == 0:
            print(f"   ✅ API 调用权限正常")
        else:
            print(f"   ⚠️ API 调用权限异常: {result}")
            
    except Exception as e:
        print(f"   ❌ 检查 API 调用权限时出错: {e}")
    
    # 检查草稿箱详细权限
    print("\n2. 检查草稿箱详细权限...")
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/count"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "total_count" in result:
            print(f"   ✅ 草稿箱读取权限正常")
            print(f"   草稿总数: {result['total_count']}")
        elif result.get("errcode") == 48001:
            print(f"   ❌ API 功能未授权")
            print(f"   可能原因: 公众号未认证或功能未开通")
        else:
            print(f"   ⚠️ 未知响应")
            
    except Exception as e:
        print(f"   ❌ 检查草稿箱权限时出错: {e}")

def test_with_different_content_formats(access_token):
    """测试不同的内容格式"""
    print("📝 测试不同的内容格式...")
    
    test_cases = [
        {
            "name": "纯文本内容",
            "content": "测试内容",
            "expectation": "可能失败，需要HTML"
        },
        {
            "name": "简单HTML",
            "content": "<p>测试内容</p>",
            "expectation": "应该成功"
        },
        {
            "name": "复杂HTML",
            "content": "<h1>标题</h1><p>段落</p><ul><li>列表1</li><li>列表2</li></ul>",
            "expectation": "应该成功"
        },
        {
            "name": "带特殊字符",
            "content": "<p>测试&nbsp;内容</p>",
            "expectation": "可能有问题"
        },
        {
            "name": "空内容",
            "content": "",
            "expectation": "应该失败"
        }
    ]
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    for test in test_cases:
        print(f"\n测试: {test['name']}")
        print(f"预期: {test['expectation']}")
        
        data = {
            "articles": [{
                "title": "测试标题",
                "author": "测试作者",
                "digest": "测试摘要",
                "content": test["content"],
                "content_source_url": "",
                "thumb_media_id": "",
                "show_cover_pic": 0,
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }]
        }
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            result = response.json()
            
            print(f"   响应代码: {result.get('errcode', '未知')}")
            print(f"   响应消息: {result.get('errmsg', '未知')}")
            
            if "media_id" in result:
                print(f"   ✅ 成功!")
            else:
                print(f"   ❌ 失败")
                
        except Exception as e:
            print(f"   ❌ 测试出错: {e}")

def analyze_common_solutions():
    """分析常见解决方案"""
    print("\n💡 分析常见解决方案...")
    
    solutions = [
        {
            "problem": "错误 40007: invalid media_id",
            "possible_causes": [
                "封面图片 thumb_media_id 是必填项",
                "提供的 media_id 格式不正确",
                "media_id 已过期（临时素材3天）",
                "media_id 不属于当前公众号"
            ],
            "solutions": [
                "确保提供有效的 thumb_media_id",
                "使用永久素材的 media_id",
                "重新上传图片获取新的 media_id",
                "检查 media_id 是否属于当前公众号"
            ]
        },
        {
            "problem": "错误 45110: author size out of limit",
            "possible_causes": [
                "中文字符计算方式不同（UTF-8 vs GBK）",
                "包含不可见字符或空格",
                "微信公众号API的bug",
                "作者名称包含特殊字符"
            ],
            "solutions": [
                "使用英文或数字作者名测试",
                "删除所有空格和特殊字符",
                "使用更短的作者名（1-2字符）",
                "联系微信客服确认限制"
            ]
        },
        {
            "problem": "错误 53402: 封面裁剪失败",
            "possible_causes": [
                "图片尺寸不符合要求（需要900x500）",
                "图片格式不支持（需要JPG/PNG）",
                "图片内容不符合规范（如二维码、广告）",
                "图片大小超过限制（2MB）"
            ],
            "solutions": [
                "创建900x500像素的图片",
                "使用JPG或PNG格式",
                "确保图片内容符合微信公众号规范",
                "压缩图片大小到2MB以下"
            ]
        }
    ]
    
    for solution in solutions:
        print(f"\n🔧 问题: {solution['problem']}")
        print(f"   可能原因:")
        for cause in solution["possible_causes"]:
            print(f"     • {cause}")
        print(f"   解决方案:")
        for sol in solution["solutions"]:
            print(f"     • {sol}")

def create_workaround_plan():
    """创建绕过方案"""
    print("\n🛠️ 创建绕过方案...")
    
    plan = {
        "immediate": [
            "使用手动发布流程（100%可用）",
            "创建符合要求的封面图片模板",
            "测试不同的作者名称格式"
        ],
        "short_term": [
            "申请微信公众号认证",
            "联系微信客服确认API限制",
            "创建测试用例验证各种边界条件"
        ],
        "long_term": [
            "开发浏览器自动化发布方案",
            "使用第三方发布平台API",
            "等待微信公众号API修复或更新"
        ]
    }
    
    print("📋 绕过方案计划:")
    print("\n立即行动:")
    for action in plan["immediate"]:
        print(f"  • {action}")
    
    print("\n短期方案（1-2周）:")
    for action in plan["short_term"]:
        print(f"  • {action}")
    
    print("\n长期方案（1个月以上）:")
    for action in plan["long_term"]:
        print(f"  • {action}")

def main():
    """主函数"""
    print("=" * 70)
    print("微信公众号自动发布问题深度诊断")
    print("=" * 70)
    
    # 1. 获取 access_token
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，诊断终止")
        return
    
    # 2. 分析错误模式
    analyze_error_patterns()
    
    # 3. 检查微信公众号类型
    print("\n" + "=" * 70)
    account_info = check_wechat_account_type(access_token)
    
    # 4. 直接测试草稿 API
    print("\n" + "=" * 70)
    test_draft_api_directly(access_token)
    
    # 5. 详细检查 API 权限
    print("\n" + "=" * 70)
    check_api_permissions_detail(access_token)
    
    # 6. 测试不同的内容格式
    print("\n" + "=" * 70)
    test_with_different_content_formats(access_token)
    
    # 7. 分析常见解决方案
    print("\n" + "=" * 70)
    analyze_common_solutions()
    
    # 8. 创建绕过方案
    print("\n" + "=" * 70)
    create_workaround_plan()
    
    # 9. 总结
    print("\n" + "=" * 70)
    print("诊断总结")
    print("=" * 70)
    
    print("🔍 根本问题分析:")
    print("1. 微信公众号 API 限制 - 可能是未认证公众号的功能限制")
    print("2. 封面图片要求严格 - 必须提供有效的 thumb_media_id")
    print("3. 字符计算方式问题 - 中文字符长度计算可能不同")
    print("4. API 文档不一致 - 实际要求可能与文档不符")
    
    print("\n✅ 立即可用的解决方案:")
    print("1. 手动发布流程 - 使用 write_wechat_article.py + 微信公众平台")
    print("2. 封面图片模板 - 创建 900x500 像素的 JPG/PNG 模板")
    print("3. 内容格式验证 - 确保 HTML 格式正确")
    
    print("\n🔧 技术解决方案:")
    print("1. 申请微信公众号认证 - 解锁更多 API 功能")
    print("2. 联系微信客服 - 确认 API 限制和错误原因")
    print("3. 开发替代方案 - 浏览器自动化或第三方平台")
    
    print("\n📋 下一步行动:")
    print("1. 立即: 使用手动流程发布测试文章")
    print("2. 短期: 申请公众号认证，创建封面模板")
    print("3. 长期: 监控 API 更新，开发自动化方案")
    
    print("\n💡 关键建议:")
    print("• 不要等待自动发布功能修复 - 手动流程完全可用")
    print("• 建立内容发布节奏 - 每周2-3篇，固定时间")
    print("• 积累内容库 - 使用写作工具创建多篇文章备用")
    print("• 关注微信公众号更新 - API 可能会修复或改进")
    
    print("\n" + "=" * 70)
    print("诊断完成")
    print("=" * 70)
    
    # 创建诊断报告
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "access_token": access_token[:20] + "...",
        "problems_identified": [
            "错误 40007: invalid media_id",
            "错误 45110: author size out of limit", 
            "错误 53402: 封面裁剪失败"
        ],
        "root_causes": [
            "微信公众号类型/认证限制",
            "封面图片要求严格",
            "字符计算方式问题"
        ],
        "immediate_solutions": [
            "手动发布流程",
            "封面图片模板",
            "内容格式验证"
        ],
        "recommended_actions": [
            "使用手动流程立即开始发布",
            "申请微信公众号认证",
            "创建内容发布计划"
        ]
    }
    
    report_file = "wechat_publish_diagnosis_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 诊断报告已保存到: {report_file}")

if __name__ == "__main__":
    main()