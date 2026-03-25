#!/usr/bin/env python3
"""
创建短标题的微信公众号草稿
微信公众号标题限制：64字符以内
"""

import requests
import json
import sys

# 配置
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"
WECHAT_API_BASE = "https://api.weixin.qq.com"

# 永久图片 media_id（从之前测试获取）
PERMANENT_IMAGE_MEDIA_ID = "K03y2eZTmx34znaim3BBR05xm8XZ3Lek78z_tzFm6n_AK8a61hRKxD1DC3V62CRH"

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

def create_short_title_draft(access_token, thumb_media_id):
    """创建短标题的草稿（标题在64字符以内）"""
    print("创建短标题草稿...")
    
    # 短标题：春季养肝养生指南 (10个字符)
    short_title = "春季养肝养生指南"
    print(f"标题长度: {len(short_title)} 字符 (限制: 64字符)")
    
    # 中医养生文章内容（简化版）
    article = {
        "title": short_title,
        "author": "中医娄伯恩",
        "digest": "春季是养肝的最佳时机，中医养生指南助您健康度过春天。",
        "content": """
            <h1>春季养肝养生指南</h1>
            
            <h2>春季养生要点</h2>
            <p>春季是万物复苏的季节，也是养肝护肝的最佳时机。中医认为，春季对应肝脏，肝主疏泄，喜条达而恶抑郁。</p>
            
            <h3>饮食调养</h3>
            <ul>
                <li>多吃绿色蔬菜：菠菜、芹菜、西兰花</li>
                <li>适量食用酸味食物：柠檬、山楂、醋</li>
                <li>避免油腻、辛辣食物</li>
            </ul>
            
            <h3>起居有常</h3>
            <ul>
                <li>早睡早起，顺应自然</li>
                <li>适当运动，如散步、太极拳</li>
                <li>保持心情舒畅，避免生气</li>
            </ul>
            
            <h3>穴位保健</h3>
            <ul>
                <li><strong>太冲穴</strong>：足背第一、二跖骨结合部前方凹陷处</li>
                <li><strong>肝俞穴</strong>：背部第九胸椎棘突下旁开1.5寸</li>
                <li>每日按摩5-10分钟，有助疏肝理气</li>
            </ul>
            
            <h2>春季养生食谱</h2>
            <h3>枸杞菊花茶</h3>
            <p><strong>材料</strong>：枸杞10克，菊花5克</p>
            <p><strong>做法</strong>：沸水冲泡，代茶饮</p>
            <p><strong>功效</strong>：清肝明目，缓解眼疲劳</p>
            
            <h3>菠菜猪肝汤</h3>
            <p><strong>材料</strong>：菠菜200克，猪肝100克</p>
            <p><strong>做法</strong>：猪肝切片焯水，与菠菜同煮</p>
            <p><strong>功效</strong>：补血养肝，改善视力</p>
            
            <hr>
            
            <p style="color: #666; font-size: 14px;">
                <strong>发布时间</strong>：2026年3月18日<br>
                <strong>发布工具</strong>：OpenClaw AI助手<br>
                <strong>文章类型</strong>：中医养生科普
            </p>
            
            <p style="color: #999; font-size: 12px; margin-top: 20px;">
                注意：本文仅供参考，如有不适请及时就医。
            </p>
        """,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
        "show_cover_pic": 1  # 显示封面图片
    }
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
    params = {"access_token": access_token}
    
    data = {
        "articles": [article]
    }
    
    try:
        print("发送创建草稿请求...")
        response = requests.post(url, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "media_id" in result:
            print(f"\n✅ 草稿创建成功!")
            print(f"   媒体 ID: {result['media_id']}")
            return result["media_id"]
        elif "errcode" in result and result["errcode"] == 0:
            print(f"\n✅ 草稿创建成功!")
            if "media_id" in result:
                print(f"   媒体 ID: {result['media_id']}")
            return True
        else:
            print(f"\n❌ 草稿创建失败: {result}")
            print(f"   错误代码: {result.get('errcode', '未知')}")
            print(f"   错误信息: {result.get('errmsg', '未知')}")
            return False
            
    except Exception as e:
        print(f"❌ 创建草稿时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_draft_list(access_token):
    """获取草稿列表"""
    print("\n获取草稿列表...")
    
    url = f"{WECHAT_API_BASE}/cgi-bin/draft/batchget"
    params = {"access_token": access_token}
    
    data = {
        "offset": 0,
        "count": 10,
        "no_content": 1  # 不返回内容，只返回基本信息
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "item" in result:
            print(f"✅ 获取到 {len(result['item'])} 篇草稿:")
            for i, item in enumerate(result["item"], 1):
                print(f"  {i}. {item.get('title', '无标题')}")
                print(f"     媒体 ID: {item.get('media_id', '未知')}")
                print(f"     更新时间: {item.get('update_time', '未知')}")
                if i < len(result["item"]):
                    print()
            return result["item"]
        else:
            print(f"❌ 获取草稿列表失败: {result}")
            return []
            
    except Exception as e:
        print(f"❌ 获取草稿列表时出错: {e}")
        return []

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号短标题草稿创建测试")
    print(f"封面图片 media_id: {PERMANENT_IMAGE_MEDIA_ID[:30]}...")
    print("=" * 60)
    
    # 获取 access_token
    print("1. 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 access_token，测试终止")
        sys.exit(1)
    
    print(f"   ✅ access_token 获取成功: {access_token[:20]}...")
    
    # 先查看现有草稿
    print("\n2. 查看现有草稿...")
    existing_drafts = get_draft_list(access_token)
    
    # 创建短标题草稿
    print("\n3. 创建短标题草稿...")
    media_id = create_short_title_draft(access_token, PERMANENT_IMAGE_MEDIA_ID)
    
    if media_id:
        # 等待一下让服务器处理
        import time
        print("\n等待3秒让服务器处理...")
        time.sleep(3)
        
        # 再次查看草稿列表确认
        print("\n4. 验证草稿创建...")
        new_drafts = get_draft_list(access_token)
        
        if new_drafts:
            new_count = len(new_drafts) - len(existing_drafts) if existing_drafts else len(new_drafts)
            if new_count > 0:
                print(f"\n✅ 测试完成! 成功创建 {new_count} 篇草稿。")
                print(f"   请登录微信公众平台查看草稿箱。")
                print(f"\n📋 创建的文章:")
                for draft in new_drafts[:new_count]:
                    print(f"   - {draft.get('title', '无标题')}")
            else:
                print(f"\n⚠️  草稿可能创建成功，但未在列表中显示。")
                print(f"   请登录微信公众平台查看草稿箱确认。")
        else:
            print(f"\n⚠️  无法获取草稿列表，但创建请求可能已成功。")
            print(f"   请登录微信公众平台查看草稿箱确认。")
    else:
        print(f"\n❌ 草稿创建失败。")
        print(f"   可能原因:")
        print(f"   1. media_id 无效或已过期")
        print(f"   2. 内容格式不符合微信公众号要求")
        print(f"   3. API 权限限制")
        print(f"   4. 网络或服务器问题")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    
    # 提供后续步骤
    print("\n🎯 后续步骤:")
    print("1. 登录微信公众平台 (https://mp.weixin.qq.com)")
    print("2. 进入'内容与互动' -> '草稿箱'")
    print("3. 查看刚刚创建的测试文章")
    print("4. 预览并发布（如果需要）")
    print("5. 删除测试文章（如果需要）")

if __name__ == "__main__":
    main()