#!/bin/bash
# 微信公众号每日自动化发布脚本

cd /home/admin/.openclaw/workspace/skills/wechat-article-publisher

echo "=========================================="
echo "  微信公众号每日自动化发布"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# 1. 检查必要文件
echo "🔍 检查系统状态..."
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 配置文件不存在"
    exit 1
fi

if [ ! -f "auto_publish_final.py" ]; then
    echo "❌ 错误: auto_publish_final.py 不存在"
    exit 1
fi

echo "✅ 系统检查通过"

# 2. 检查今日文章
TODAY=$(date '+%Y-%m-%d')
echo ""
echo "📅 检查今日文章: $TODAY"

if [ -f "每日文章记录/$TODAY.json" ]; then
    echo "✅ 找到今日文章记录"
    
    # 解析文章信息
    echo "📋 今日文章列表:"
    python3 -c "
import json
import os

record_file = '每日文章记录/$TODAY.json'
if os.path.exists(record_file):
    with open(record_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f'日期: {data[\"date\"]}')
    print(f'文章数量: {len(data[\"articles\"])}')
    
    for i, article in enumerate(data['articles'], 1):
        print(f'{i}. [{article[\"type\"]}] {article[\"title\"]}')
        print(f'   文件: {article[\"filename\"]}')
        
        # 检查文件是否存在
        if os.path.exists(f'articles/{article[\"filename\"]}'):
            print('   ✅ 文件存在')
        else:
            print('   ❌ 文件不存在')
        print()
else:
    print('❌ 文章记录文件不存在')
" 2>&1
    
else
    echo "⚠️  未找到今日文章记录，使用默认文章"
fi

# 3. 运行自动化发布
echo ""
echo "🚀 开始自动化发布..."
echo ""

python3 auto_publish_final.py

# 4. 记录发布结果
echo ""
echo "📝 记录发布日志..."
LOG_FILE="publish_logs/$(date '+%Y-%m-%d').log"
mkdir -p publish_logs

{
    echo "=========================================="
    echo "发布时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "发布脚本: auto_publish_final.py"
    echo "发布结果: $?"
    echo "=========================================="
} >> "$LOG_FILE"

echo "✅ 发布日志已保存: $LOG_FILE"

# 5. 发送通知（可选）
echo ""
echo "📨 发布完成通知"
echo "✅ 微信公众号自动化发布已完成"
echo "📅 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📊 详情请查看日志文件: $LOG_FILE"

echo ""
echo "=========================================="
echo "  发布完成"
echo "=========================================="