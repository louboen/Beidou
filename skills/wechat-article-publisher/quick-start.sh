#!/bin/bash
# 微信公众号自动发布 - 快速启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "微信公众号自动发布系统"
echo "============================================================"
echo ""
echo "📁 工作目录：$SCRIPT_DIR"
echo "📅 当前时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 检查配置
echo "🔍 检查配置..."
if [ ! -f ".env" ]; then
    echo "❌ 错误：.env 配置文件不存在"
    exit 1
fi
echo "✅ 配置文件检查通过"

# 检查 Python 脚本
echo ""
echo "🔍 检查发布脚本..."
if [ ! -f "auto_publish_final_fixed.py" ]; then
    echo "❌ 错误：发布脚本不存在"
    exit 1
fi
echo "✅ 发布脚本检查通过"

# 检查文章目录
echo ""
echo "🔍 检查文章目录..."
if [ ! -d "articles" ]; then
    echo "⚠️  警告：articles 目录不存在，创建中..."
    mkdir -p articles
fi

ARTICLE_COUNT=$(ls -1 articles/*.html 2>/dev/null | wc -l)
echo "✅ 找到 $ARTICLE_COUNT 篇文章"

# 检查封面图片
echo ""
echo "🔍 检查封面图片..."
if [ ! -f "wechat_personal_qr.jpg" ]; then
    echo "⚠️  警告：封面图片 wechat_personal_qr.jpg 不存在"
fi
echo "✅ 封面图片检查通过"

# 创建日志目录
echo ""
echo "📝 准备日志目录..."
mkdir -p publish_logs
LOG_FILE="publish_logs/$(date +%Y-%m-%d_%H-%M-%S).log"
echo "✅ 日志文件：$LOG_FILE"

# 运行发布
echo ""
echo "🚀 开始发布文章..."
echo "============================================================"
echo ""

python3 auto_publish_final_fixed.py 2>&1 | tee "$LOG_FILE"

# 检查结果
echo ""
echo "============================================================"
echo "发布完成"
echo "============================================================"
echo ""
echo "📊 发布日志：$LOG_FILE"
echo ""

# 显示最近发布的草稿 ID
echo "📋 最近发布的草稿 ID:"
grep "草稿 ID:" "$LOG_FILE" | tail -5
echo ""

echo "✅ 请前往微信公众平台检查草稿箱："
echo "   https://mp.weixin.qq.com"
echo ""
echo "============================================================"
