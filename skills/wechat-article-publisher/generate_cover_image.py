#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据文章内容生成封面图片（900x500 像素）
使用 PIL 绘制中医食疗主题封面
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配置
WIDTH = 900
HEIGHT = 500
OUTPUT_PATH = "/home/admin/.openclaw/workspace/skills/wechat-article-publisher/assets/cover_shanwei.jpg"

# 文章信息
ARTICLE_TITLE = "脾胃虚弱？喝这碗粥调理"
ARTICLE_SUBTITLE = "中医食疗养生方"

def create_cover():
    """创建封面图片"""
    print("🎨 正在生成封面图片...")
    
    # 创建背景（中医绿色渐变）
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变背景
    for y in range(HEIGHT):
        r = int(44 + (y / HEIGHT) * 20)
        g = int(85 + (y / HEIGHT) * 30)
        b = int(48 + (y / HEIGHT) * 20)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    # 绘制装饰圆形
    draw.ellipse([100, 100, 250, 250], fill=(60, 120, 80, 180))
    draw.ellipse([700, 300, 850, 450], fill=(60, 120, 80, 150))
    
    # 绘制药草装饰图案（简化版）
    for i in range(5):
        x = 150 + i * 120
        draw.ellipse([x, 350, x+40, 390], fill=(100, 160, 120))
    
    # 添加标题文字（使用系统字体）
    try:
        # 尝试使用常见中文字体
        font_paths = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font_title = ImageFont.truetype(font_path, 48)
                    font_subtitle = ImageFont.truetype(font_path, 32)
                    font = True
                    break
                except:
                    continue
        
        if not font:
            # 使用默认字体
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            print("⚠️  未找到中文字体，使用默认字体")
        
        # 绘制标题
        title_text = ARTICLE_TITLE
        draw.text((WIDTH/2, 180), title_text, fill=(255, 255, 255), 
                  font=font_title, anchor="mm", align="center")
        
        # 绘制副标题
        subtitle_text = ARTICLE_SUBTITLE
        draw.text((WIDTH/2, 280), subtitle_text, fill=(200, 255, 220), 
                  font=font_subtitle, anchor="mm", align="center")
        
    except Exception as e:
        print(f"⚠️  文字绘制失败：{e}")
        # 绘制简单文字
        draw.text((350, 230), "脾胃虚弱？", fill=(255, 255, 255))
        draw.text((350, 280), "喝这碗粥调理", fill=(200, 255, 220))
    
    # 保存
    img.save(OUTPUT_PATH, 'JPEG', quality=90)
    print(f"✅ 封面图片已生成：{OUTPUT_PATH}")
    print(f"   尺寸：{WIDTH}x{HEIGHT}")
    print(f"   格式：JPEG")
    
    return OUTPUT_PATH

if __name__ == "__main__":
    create_cover()
