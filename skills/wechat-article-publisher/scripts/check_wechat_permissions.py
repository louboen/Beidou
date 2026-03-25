#!/usr/bin/env python3
"""
检查微信公众号接口权限
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
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "access_token" in data:
            return data["access_token"]
        else:
            print(f"❌ access_token 获取失败: {data}")
            return None
            
    except Exception as e:
        print(f"❌ 获取 access_token 时出错: {e}")
        return None

def check_interface_permissions(access_token):
    """检查接口权限"""
    print("\n检查微信公众号接口权限:")
    
    interfaces = [
        ("获取服务器IP", "/cgi-bin/getcallbackip", "GET"),
        ("获取API调用次数", "/cgi-bin/openapi/quota/get", "POST"),
        ("获取素材总数", "/cgi-bin/material/get_materialcount", "GET"),
        ("获取草稿箱数量", "/cgi-bin/draft/count", "GET"),
        ("获取菜单信息", "/cgi-bin/get_current_selfmenu_info", "GET"),
        ("获取账号信息", "/cgi-bin/account/getaccountinfo", "GET"),
    ]
    
    results = []
    
    for name, endpoint, method in interfaces:
        url = f"{WECHAT_API_BASE}{endpoint}"
        params = {"access_token": access_token}
        
        try:
            if method == "GET":
                response = requests.get(url, params=params, timeout=10)
            else:  # POST
                response = requests.post(url, params=params, json={}, timeout=10)
            
            data = response.json()
            
            if "errcode" in data:
                if data["errcode"] == 0:
                    results.append((name, "✅ 有权限", ""))
                elif data["errcode"] == 48001:
                    results.append((name, "❌ 无权限", "API功能未授权"))
                elif data["errcode"] == 48004:
                    results.append((name, "❌ 无权限", "API接口被封禁"))
                else:
                    results.append((name, "⚠️  错误", f"错误码: {data['errcode']}"))
            else:
                results.append((name, "✅ 有权限", ""))
                
        except Exception as e:
            results.append((name, "❌ 异常", str(e)))
    
    # 打印结果
    print("\n接口权限检查结果:")
    print("-" * 60)
    for name, status, detail in results:
        print(f"{name:20} {status:10} {detail}")
    print("-" * 60)
    
    return results

def check_draft_permission(access_token):
    """检查草稿权限"""
    print("\n检查草稿功能权限:")
    
    # 尝试获取草稿列表
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/batchget"
    params = {"access_token": access_token}
    
    data = {
        "offset": 0,
        "count": 1,
        "no_content": 1
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        data = response.json()
        
        if "item" in data:
            print("✅ 草稿列表读取权限: 有")
            print(f"   现有草稿数量: {len(data['item'])}")
            return True
        elif "errcode" in data:
            if data["errcode"] == 48001:
                print("❌ 草稿列表读取权限: 无 (API功能未授权)")
                return False
            else:
                print(f"⚠️  草稿列表读取权限: 错误 (错误码: {data['errcode']})")
                return False
        else:
            print("✅ 草稿列表读取权限: 有")
            return True
            
    except Exception as e:
        print(f"❌ 检查草稿权限时出错: {e}")
        return False

def check_material_permission(access_token):
    """检查素材权限"""
    print("\n检查素材功能权限:")
    
    # 尝试获取素材统计
    url = f"{WECHAT_API_BASE}/cgi-bin/material/get_materialcount"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "image_count" in data:
            print("✅ 素材管理权限: 有")
            print(f"   图片数量: {data.get('image_count', 0)}")
            print(f"   图文数量: {data.get('news_count', 0)}")
            print(f"   视频数量: {data.get('video_count', 0)}")
            return True
        elif "errcode" in data:
            if data["errcode"] == 48001:
                print("❌ 素材管理权限: 无 (API功能未授权)")
                return False
            else:
                print(f"⚠️  素材管理权限: 错误 (错误码: {data['errcode']})")
                return False
        else:
            print("✅ 素材管理权限: 有")
            return True
            
    except Exception as e:
        print(f"❌ 检查素材权限时出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号接口权限检查")
    print(f"AppID: {APPID}")
    print("=" * 60)
    
    # 获取 access_token
    print("1. 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，检查终止")
        sys.exit(1)
    
    print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
    
    # 检查接口权限
    results = check_interface_permissions(access_token)
    
    # 检查草稿权限
    has_draft_permission = check_draft_permission(access_token)
    
    # 检查素材权限
    has_material_permission = check_material_permission(access_token)
    
    # 总结
    print("\n" + "=" * 60)
    print("权限检查总结")
    print("=" * 60)
    
    # 统计结果
    total = len(results)
    success = sum(1 for _, status, _ in results if "✅" in status)
    warning = sum(1 for _, status, _ in results if "⚠️" in status)
    error = sum(1 for _, status, _ in results if "❌" in status)
    
    print(f"接口检查总数: {total}")
    print(f"有权限接口: {success}")
    print(f"警告接口: {warning}")
    print(f"无权限接口: {error}")
    
    print(f"\n草稿功能权限: {'✅ 有' if has_draft_permission else '❌ 无'}")
    print(f"素材功能权限: {'✅ 有' if has_material_permission else '❌ 无'}")
    
    # 建议
    print("\n💡 建议:")
    
    if not has_draft_permission:
        print("1. 草稿功能可能未授权，需要在微信公众平台开启相应权限")
        print("2. 登录微信公众平台 -> 设置 -> 安全中心 -> 风险操作提醒")
        print("3. 确保已开启'素材管理'和'草稿箱'相关权限")
    
    if not has_material_permission:
        print("1. 素材管理功能可能未授权")
        print("2. 需要检查微信公众号类型（订阅号/服务号）")
        print("3. 服务号有更多API权限")
    
    if error > 0:
        print("1. 部分接口无权限，可能影响功能使用")
        print("2. 建议检查微信公众号类型和权限设置")
    
    print("\n🔗 相关链接:")
    print("1. 微信公众平台: https://mp.weixin.qq.com")
    print("2. 接口权限说明: https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Explanation_of_interface_privileges.html")
    print("3. 草稿箱API文档: https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html")
    
    print("\n" + "=" * 60)
    print("检查完成")
    print("=" * 60)

if __name__ == "__main__":
    main()