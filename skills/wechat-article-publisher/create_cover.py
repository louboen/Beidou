#!/usr/bin/env python3
"""
创建简单的封面图片
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_cover_image():
    """创建封面图片"""
    
    # 创建新图片
    width, height = 900, 500
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 添加背景色块
    draw.rectangle([0, 0, width, 150], fill=(76, 175, 80))  # 绿色标题栏
    
    # 添加标题
    try:
        # 尝试使用系统字体
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        # 使用默认字体
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # 绘制标题
    title = "失眠怎么办？"
    subtitle = "试试这 3 款安神汤"
    author = "中医娄伯恩"
    
    draw.text((width//2, 75), title, fill=(255, 255, 255), font=font_large, anchor="mm")
    draw.text((width//2, 140), subtitle, fill=(255, 255, 255), font=font_medium, anchor="mm")
    
    # 添加中医元素装饰
    draw.ellipse([100, 200, 300, 400], outline=(76, 175, 80), width=3)
    draw.ellipse([600, 200, 800, 400], outline=(76, 175, 80), width=3)
    
    # 添加作者信息
    draw.text((width//2, height-50), author, fill=(100, 100, 100), font=font_medium, anchor="mm")
    
    # 保存图片
    output_path = "cover_insomnia.jpg"
    image.save(output_path, "JPEG", quality=95)
    
    print(f"✅ 封面图片已创建: {output_path}")
    print(f"📏 尺寸: {width}x{height} 像素")
    
    # 显示文件信息
    file_size = os.path.getsize(output_path)
    print(f"📊 文件大小: {file_size} 字节 ({file_size/1024:.1f} KB)")
    
    return output_path

if __name__ == "__main__":
    create_cover_image()