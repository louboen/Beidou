#!/usr/bin/env python3
"""
微信公众号官方 API 客户端
使用 AppID 和 AppSecret 获取 access_token，然后调用微信公众号 API
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, Any

# 微信公众号 API 配置
WECHAT_API_BASE = "https://api.weixin.qq.com"
APPID = "wx1a0fadc458656bef"
APPSECRET = "8640812d15d97219575da73caef1e80e"

class WeChatOfficialAPI:
    """微信公众号官方 API 客户端"""
    
    def __init__(self, appid: str = None, appsecret: str = None):
        self.appid = appid or APPID
        self.appsecret = appsecret or APPSECRET
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self) -> str:
        """获取 access_token"""
        url = f"{WECHAT_API_BASE}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "access_token" in data:
                self.access_token = data["access_token"]
                # 默认有效期为 7200 秒，提前 300 秒刷新
                self.token_expires_at = time.time() + data.get("expires_in", 7200) - 300
                return self.access_token
            else:
                print(f"获取 access_token 失败: {data}")
                return None
                
        except Exception as e:
            print(f"获取 access_token 时出错: {e}")
            return None
    
    def ensure_token(self) -> bool:
        """确保有有效的 access_token"""
        import time
        if not self.access_token or time.time() >= self.token_expires_at:
            return self.get_access_token() is not None
        return True
    
    def upload_media(self, media_type: str, media_path: str) -> Optional[Dict]:
        """上传临时素材"""
        if not self.ensure_token():
            return None
            
        url = f"{WECHAT_API_BASE}/cgi-bin/media/upload"
        params = {
            "access_token": self.access_token,
            "type": media_type  # image, voice, video, thumb
        }
        
        try:
            with open(media_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, params=params, files=files, timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"上传素材失败: {e}")
            return None
    
    def upload_permanent_media(self, media_type: str, media_path: str) -> Optional[Dict]:
        """上传永久素材"""
        if not self.ensure_token():
            return None
            
        url = f"{WECHAT_API_BASE}/cgi-bin/material/add_material"
        params = {
            "access_token": self.access_token,
            "type": media_type
        }
        
        try:
            with open(media_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, params=params, files=files, timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"上传永久素材失败: {e}")
            return None
    
    def create_draft(self, articles: list) -> Optional[Dict]:
        """
        创建草稿
        articles: 文章列表，每个文章包含:
            - title: 标题
            - author: 作者
            - digest: 摘要
            - content: 内容 (HTML)
            - content_source_url: 原文链接
            - thumb_media_id: 封面图片 media_id
            - need_open_comment: 是否打开评论
            - only_fans_can_comment: 是否粉丝才可评论
        """
        if not self.ensure_token():
            return None
            
        url = f"{WECHAT_API_BASE}/cgi-bin/draft/add"
        params = {
            "access_token": self.access_token
        }
        
        data = {
            "articles": articles
        }
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"创建草稿失败: {e}")
            return None
    
    def publish_draft(self, media_id: str) -> Optional[Dict]:
        """发布草稿"""
        if not self.ensure_token():
            return None
            
        url = f"{WECHAT_API_BASE}/cgi-bin/freepublish/submit"
        params = {
            "access_token": self.access_token
        }
        
        data = {
            "media_id": media_id
        }
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"发布草稿失败: {e}")
            return None
    
    def get_draft_list(self, offset: int = 0, count: int = 20, no_content: bool = True) -> Optional[Dict]:
        """获取草稿列表"""
        if not self.ensure_token():
            return None
            
        url = f"{WECHAT_API_BASE}/cgi-bin/draft/batchget"
        params = {
            "access_token": self.access_token
        }
        
        data = {
            "offset": offset,
            "count": count,
            "no_content": no_content
        }
        
        try:
            response = requests.post(url, params=params, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取草稿列表失败: {e}")
            return None
    
    def get_account_info(self) -> Optional[Dict]:
        """获取公众号信息"""
        if not self.ensure_token():
            return None
            
        url = f"{WECHAT_API_BASE}/cgi-bin/account/getaccountinfo"
        params = {
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取公众号信息失败: {e}")
            return None

def test_api():
    """测试 API 连接"""
    print("测试微信公众号官方 API 连接...")
    
    api = WeChatOfficialAPI()
    
    # 测试获取 access_token
    print("1. 获取 access_token...")
    token = api.get_access_token()
    if token:
        print(f"✅ access_token 获取成功: {token[:20]}...")
    else:
        print("❌ access_token 获取失败")
        return False
    
    # 测试获取公众号信息
    print("2. 获取公众号信息...")
    account_info = api.get_account_info()
    if account_info and "errcode" in account_info and account_info["errcode"] == 0:
        print(f"✅ 公众号信息获取成功:")
        print(f"   公众号名称: {account_info.get('nickname', '未知')}")
        print(f"   公众号类型: {account_info.get('service_type_info', {}).get('id', '未知')}")
        print(f"   认证状态: {account_info.get('verify_type_info', {}).get('id', '未知')}")
        return True
    else:
        print(f"❌ 公众号信息获取失败: {account_info}")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号官方 API 客户端")
    parser.add_argument("--test", action="store_true", help="测试 API 连接")
    parser.add_argument("--info", action="store_true", help="获取公众号信息")
    parser.add_argument("--list-drafts", action="store_true", help="获取草稿列表")
    parser.add_argument("--count", type=int, default=10, help="草稿数量")
    
    args = parser.parse_args()
    
    if args.test:
        if test_api():
            print("\n✅ API 测试通过")
            sys.exit(0)
        else:
            print("\n❌ API 测试失败")
            sys.exit(1)
    
    elif args.info:
        api = WeChatOfficialAPI()
        info = api.get_account_info()
        if info:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print("获取公众号信息失败")
            sys.exit(1)
    
    elif args.list_drafts:
        api = WeChatOfficialAPI()
        drafts = api.get_draft_list(count=args.count)
        if drafts:
            print(json.dumps(drafts, indent=2, ensure_ascii=False))
        else:
            print("获取草稿列表失败")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    import time
    main()