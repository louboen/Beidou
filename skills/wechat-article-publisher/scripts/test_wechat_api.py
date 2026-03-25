#!/usr/bin/env python3
"""
测试微信公众号 API 权限和功能
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
            print(f"✅ access_token 获取成功: {data['access_token'][:20]}...")
            print(f"   有效期: {data.get('expires_in', '未知')} 秒")
            return data["access_token"]
        else:
            print(f"❌ access_token 获取失败: {data}")
            return None
            
    except Exception as e:
        print(f"❌ 获取 access_token 时出错: {e}")
        return None

def test_api_permissions(access_token):
    """测试 API 权限"""
    print("\n测试 API 权限:")
    
    # 测试 1: 获取服务器 IP
    print("1. 获取微信服务器 IP 地址...")
    url = f"{WECHAT_API_BASE}/cgi-bin/getcallbackip"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if "ip_list" in data:
            print(f"   ✅ 成功获取 {len(data['ip_list'])} 个服务器 IP")
            print(f"   示例 IP: {data['ip_list'][:3] if len(data['ip_list']) > 3 else data['ip_list']}")
        else:
            print(f"   ❌ 失败: {data}")
    except Exception as e:
        print(f"   ❌ 出错: {e}")
    
    # 测试 2: 获取 API 调用次数
    print("\n2. 获取 API 调用次数...")
    url = f"{WECHAT_API_BASE}/cgi-bin/openapi/quota/get"
    params = {"access_token": access_token}
    
    try:
        response = requests.post(url, params=params, json={"cgi_path": "/cgi-bin/token"}, timeout=10)
        data = response.json()
        if "quota" in data:
            print(f"   ✅ 成功获取调用次数信息")
            quota = data["quota"]
            print(f"   每日限额: {quota.get('daily_limit', '未知')}")
            print(f"   已使用: {quota.get('used', '未知')}")
            print(f"   剩余: {quota.get('remain', '未知')}")
        else:
            print(f"   ❌ 失败: {data}")
    except Exception as e:
        print(f"   ❌ 出错: {e}")
    
    # 测试 3: 获取素材总数
    print("\n3. 获取素材总数...")
    url = f"{WECHAT_API_BASE}/cgi-bin/material/get_materialcount"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if "voice_count" in data:
            print(f"   ✅ 成功获取素材统计")
            print(f"   图片数量: {data.get('image_count', 0)}")
            print(f"   语音数量: {data.get('voice_count', 0)}")
            print(f"   视频数量: {data.get('video_count', 0)}")
            print(f"   图文数量: {data.get('news_count', 0)}")
        else:
            print(f"   ❌ 失败: {data}")
    except Exception as e:
        print(f"   ❌ 出错: {e}")
    
    # 测试 4: 获取草稿箱数量
    print("\n4. 获取草稿箱统计...")
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/count"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if "total_count" in data:
            print(f"   ✅ 成功获取草稿统计")
            print(f"   草稿总数: {data.get('total_count', 0)}")
        else:
            print(f"   ❌ 失败: {data}")
    except Exception as e:
        print(f"   ❌ 出错: {e}")

def check_menu_permission(access_token):
    """检查菜单权限"""
    print("\n检查菜单权限:")
    
    # 获取当前菜单
    url = f"{WECHAT_API_BASE}/cgi-bin/get_current_selfmenu_info"
    params = {"access_token": access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if "is_menu_open" in data:
            print(f"   ✅ 菜单状态: {'开启' if data['is_menu_open'] == 1 else '关闭'}")
            if data.get('selfmenu_info'):
                print(f"   菜单按钮数量: {len(data['selfmenu_info'].get('button', []))}")
        else:
            print(f"   ❌ 获取菜单失败: {data}")
    except Exception as e:
        print(f"   ❌ 出错: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号 API 权限测试")
    print(f"AppID: {APPID[:10]}...")
    print("=" * 60)
    
    # 获取 access_token
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        sys.exit(1)
    
    # 测试 API 权限
    test_api_permissions(access_token)
    
    # 检查菜单权限
    check_menu_permission(access_token)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    # 总结
    print("\n📋 权限总结:")
    print("✅ 基础 API 权限: 已获得 access_token")
    print("⚠️  需要进一步测试草稿创建功能")
    print("💡 建议: 尝试创建测试草稿验证发布权限")

if __name__ == "__main__":
    main()