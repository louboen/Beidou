#!/usr/bin/env python3
"""
检查微信公众号草稿功能权限
"""

import requests
import json
import sys

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

def check_api_permissions(access_token):
    """检查 API 权限"""
    print("\n🔐 检查 API 权限...")
    
    # 1. 检查草稿箱统计（如果有权限，应该能获取）
    print("1. 检查草稿箱权限...")
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/count"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "total_count" in result:
            print(f"   ✅ 草稿箱权限正常")
            print(f"   草稿总数: {result['total_count']}")
            return True
        elif result.get("errcode") == 48001:
            print(f"   ❌ 草稿功能未授权")
            return False
        else:
            print(f"   ⚠️ 未知响应")
            return False
            
    except Exception as e:
        print(f"   ❌ 检查草稿箱权限时出错: {e}")
        return False

def test_draft_creation(access_token):
    """测试草稿创建（最简单的方式）"""
    print("\n📝 测试草稿创建...")
    
    # 最简单的文章数据
    article = {
        "title": "权限测试",
        "author": "测试",
        "digest": "权限测试",
        "content": "<p>权限测试</p>",
        "content_source_url": "",
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    # 尝试不提供封面图片
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [article]
    }
    
    try:
        print(f"   请求数据:")
        print(f"   - 标题: {article['title']}")
        print(f"   - 作者: {article['author']}")
        print(f"   - 摘要: {article['digest']}")
        print(f"   - 内容: {article['content']}")
        print(f"   - 封面图片: 无")
        
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        print(f"   响应状态码: {response.status_code}")
        print(f"   响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "media_id" in result:
            print(f"   ✅ 草稿创建成功!")
            print(f"   草稿ID: {result['media_id']}")
            return True
        elif result.get("errcode") == 48001:
            print(f"   ❌ API 功能未授权")
            return False
        else:
            print(f"   ❌ 草稿创建失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试草稿创建时出错: {e}")
        return False

def check_wechat_configuration():
    """检查微信公众号配置"""
    print("\n⚙️ 检查微信公众号配置...")
    
    print("1. 公众号类型检查:")
    print("   - 订阅号: 支持草稿功能")
    print("   - 服务号: 支持草稿功能")
    print("   - 企业号: 可能不支持或需要特殊配置")
    
    print("\n2. 权限配置检查:")
    print("   - 需要开启'草稿箱'功能")
    print("   - 需要 API 调用权限")
    print("   - 可能需要微信认证")
    
    print("\n3. 常见问题:")
    print("   - 未认证的订阅号可能功能受限")
    print("   - 新注册的公众号可能有功能限制")
    print("   - 需要开启'开发者模式'")

def main():
    """主函数"""
    print("=" * 70)
    print("微信公众号草稿功能权限检查")
    print("=" * 70)
    
    # 1. 获取 access_token
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，检查终止")
        return
    
    # 2. 检查 API 权限
    has_draft_permission = check_api_permissions(access_token)
    
    # 3. 测试草稿创建
    if has_draft_permission:
        can_create_draft = test_draft_creation(access_token)
    else:
        can_create_draft = False
    
    # 4. 检查配置
    check_wechat_configuration()
    
    # 5. 总结
    print("\n" + "=" * 70)
    print("权限检查总结")
    print("=" * 70)
    
    if has_draft_permission and can_create_draft:
        print("✅ 权限检查通过!")
        print("   草稿功能完全可用")
        
        print("\n🎯 下一步:")
        print("1. 修复图片上传问题")
        print("2. 完善文章内容")
        print("3. 实现自动化发布")
        
    elif has_draft_permission and not can_create_draft:
        print("⚠️ 权限部分可用")
        print("   可以查看草稿箱，但不能创建草稿")
        
        print("\n🔍 可能原因:")
        print("1. 文章格式问题")
        print("2. 缺少必要字段")
        print("3. API 调用方式错误")
        
    elif not has_draft_permission:
        print("❌ 权限检查失败")
        print("   草稿功能未授权")
        
        print("\n💡 解决方案:")
        print("1. 检查微信公众号类型")
        print("2. 确认是否已认证")
        print("3. 开启开发者模式")
        print("4. 申请相关权限")
        
        print("\n📋 替代方案:")
        print("1. 使用手动发布流程")
        print("2. 使用第三方平台（如 wx.limyai.com）")
        print("3. 申请微信公众号认证")
    
    print("\n" + "=" * 70)
    print("检查完成")
    print("=" * 70)

if __name__ == "__main__":
    main()