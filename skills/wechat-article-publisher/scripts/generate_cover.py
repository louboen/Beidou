#!/usr/bin/env python3
"""
中医养生文章封面图片生成工具
使用 AI 绘画生成与文章标题相关的封面图片
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# 配置
OUTPUT_DIR = Path(__file__).parent.parent / "素材库" / "01_封面图库"

# 文章类型与提示词模板
PROMPT_TEMPLATES = {
    "节气养生": {
        "base": "{season} wellness theme, traditional Chinese medicine elements, {element}, soft natural lighting, minimalist style",
        "elements": {
            "春": "fresh green sprouts and flowers, balance yin yang",
            "夏": "lotus flower, sunshine, vibrant red",
            "秋": "golden leaves, harvest, chrysanthemum",
            "冬": "plum blossom, snow, peaceful blue"
        }
    },
    "中医食疗": {
        "base": "Chinese {food_type}, {ingredients}, white porcelain container, wooden table, natural sunlight, food photography, warm tone",
        "foods": {
            "养生茶": "herbal tea, goji berry and chrysanthemum flowers",
            "药膳汤": "medicinal soup, chinese herbs and meat",
            "养生粥": "healthy porridge, grains and vegetables",
            "药酒": "herbal wine, traditional chinese medicine bottle"
        }
    },
    "穴位保健": {
        "base": "acupuncture point diagram, {body_part}, {acupoint_name} highlighted, medical illustration, clean background, educational",
        "parts": {
            "足部": "human foot, Taichong point",
            "手部": "human hand, Hegu point",
            "腿部": "human leg, Zusanli point",
            "背部": "human back, Shenshu point"
        }
    },
    "健康新闻": {
        "base": "medical news theme, {theme_element}, professional, modern hospital background, soft lighting",
        "themes": {
            "医学突破": "laboratory, microscope, research",
            "健康政策": "hospital building, healthcare insurance symbol",
            "疾病防控": "vaccine, protection, medical mask",
            "养生热点": "fitness, healthy food, wellness"
        }
    }
}

def generate_prompt(article_type, sub_type, title_keywords):
    """生成 AI 绘画提示词"""
    template = PROMPT_TEMPLATES.get(article_type, {})
    base = template.get("base", "")
    
    if article_type == "节气养生":
        season = "spring" if "春" in title_keywords else "summer" if "夏" in title_keywords else "autumn" if "秋" in title_keywords else "winter"
        element = template.get("elements", {}).get(season[0].upper(), "herbs")
        return base.format(season=season, element=element)
    
    elif article_type == "中医食疗":
        food = template.get("foods", {}).get(sub_type, "herbal tea")
        return base.format(food_type=sub_type, ingredients=food)
    
    elif article_type == "穴位保健":
        body_part = template.get("parts", {}).get(sub_type, "human foot")
        return base.format(body_part=body_part, acupoint_name=sub_type)
    
    elif article_type == "健康新闻":
        theme = template.get("themes", {}).get(sub_type, "wellness")
        return base.format(theme_element=theme)
    
    return base

def save_prompt_to_file(filename, prompt):
    """保存提示词到文件"""
    prompt_file = OUTPUT_DIR.parent / "AI 绘画提示词" / f"{filename}.txt"
    prompt_file.parent.mkdir(exist_ok=True)
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"✅ 提示词已保存：{prompt_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="中医养生文章封面生成工具")
    parser.add_argument("--type", type=str, required=True, 
                       choices=["节气养生", "中医食疗", "穴位保健", "健康新闻"],
                       help="文章类型")
    parser.add_argument("--subtype", type=str, default="", help="子分类")
    parser.add_argument("--title", type=str, required=True, help="文章标题")
    parser.add_argument("--output", type=str, default="", help="输出文件名")
    parser.add_argument("--save-prompt", action="store_true", help="保存提示词到文件")
    
    args = parser.parse_args()
    
    # 生成提示词
    prompt = generate_prompt(args.type, args.subtype, args.title)
    
    print(f"📝 文章标题：{args.title}")
    print(f"🎨 文章类型：{args.type}")
    print(f"💡 AI 绘画提示词:\n{prompt}\n")
    
    # 保存提示词
    if args.save_prompt:
        if not args.output:
            args.output = f"cover_{args.type}_{datetime.now().strftime('%Y%m%d')}"
        save_prompt_to_file(args.output, prompt)
    
    # 输出使用说明
    print("=" * 60)
    print("📋 使用方法:")
    print("=" * 60)
    print("\n1. Midjourney:")
    print(f"   /imagine prompt: {prompt} --ar 9:5 --v 5.2\n")
    print("\n2. Stable Diffusion:")
    print(f"   Prompt: {prompt}")
    print("   Negative prompt: low quality, blurry, text, watermark")
    print("   Size: 900x500\n")
    print("\n3. DALL-E 3:")
    print(f"   {prompt}\n")
    print("=" * 60)
    print("\n✅ 生成后保存到：素材库/01_封面图库/{分类}/")

if __name__ == "__main__":
    main()
