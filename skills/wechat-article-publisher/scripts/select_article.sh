#!/bin/bash
# 文章选择与发布菜单

cd /home/admin/.openclaw/workspace/skills/wechat-article-publisher

echo "=========================================="
echo "  微信公众号文章选择与发布系统"
echo "=========================================="
echo ""

# 获取今日日期
TODAY=$(date +%Y-%m-%d)
TOMORROW=$(date -d "tomorrow" +%Y-%m-%d)

echo "📅 选择日期:"
echo "  1. 今日 (${TODAY})"
echo "  2. 明日 (${TOMORROW})"
echo "  3. 自定义日期"
echo ""
read -p "请选择 [1-3]: " date_choice

case $date_choice in
  1) SELECTED_DATE=$TODAY ;;
  2) SELECTED_DATE=$TOMORROW ;;
  3) read -p "请输入日期 (YYYY-MM-DD): " SELECTED_DATE ;;
  *) echo "无效选择"; exit 1 ;;
esac

echo ""
echo "=========================================="
echo "  ${SELECTED_DATE} 的文章列表"
echo "=========================================="

# 读取文章记录
RECORD_FILE="每日文章记录/${SELECTED_DATE}.json"

if [ ! -f "$RECORD_FILE" ]; then
  echo "❌ 未找到 ${SELECTED_DATE} 的文章记录"
  echo "是否生成新文章？(y/n)"
  read -p "> " generate
  if [ "$generate" = "y" ]; then
    python3 scripts/daily_articles.py --date $SELECTED_DATE
  else
    exit 0
  fi
fi

# 显示文章列表
echo ""
python3 -c "
import json
with open('$RECORD_FILE', 'r', encoding='utf-8') as f:
    data = json.load(f)
    articles = data.get('articles', [])
    for i, article in enumerate(articles, 1):
        status = article.get('status', 'draft')
        status_icon = '✅' if status == 'published' else '⏳'
        print(f'{status_icon} {i}. [{article[\"type\"]}] {article[\"title\"]}')
        print(f'   文件：{article[\"filename\"]}')
        print()
"

echo "=========================================="
echo "  操作选项"
echo "=========================================="
echo "  1. 预览文章 (在微信后台)"
echo "  2. 发布文章"
echo "  3. 生成封面图片"
echo "  4. 重新生成文章"
echo "  5. 退出"
echo ""
read -p "请选择操作 [1-5]: " action

case $action in
  1)
    echo ""
    echo "✅ 请前往微信公众平台草稿箱查看"
    echo "   https://mp.weixin.qq.com"
    ;;
  2)
    read -p "请选择要发布的文章编号 [1-3]: " article_num
    FILENAME=$(python3 -c "
import json
with open('$RECORD_FILE', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data['articles'][$(($article_num - 1))]['filename'])
")
    echo "发布文章：$FILENAME"
    read -p "输入封面图片 URL (或按回车使用默认): " cover_url
    cover_url=${cover_url:-"https://picsum.photos/900/500"}
    
    echo ""
    echo "🚀 开始发布..."
    python3 scripts/publish_official.py \
      --html "articles/$FILENAME" \
      --author "娄医生" \
      --cover "$cover_url"
    ;;
  3)
    read -p "请选择文章编号 [1-3]: " article_num
    ARTICLE_TYPE=$(python3 -c "
import json
with open('$RECORD_FILE', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data['articles'][$(($article_num - 1))]['type'])
")
    TITLE=$(python3 -c "
import json
with open('$RECORD_FILE', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data['articles'][$(($article_num - 1))]['title'])
")
    
    echo "生成封面提示词..."
    python3 scripts/generate_cover.py \
      --type "$ARTICLE_TYPE" \
      --title "$TITLE" \
      --save-prompt
    ;;
  4)
    echo "重新生成文章..."
    python3 scripts/daily_articles.py --date $SELECTED_DATE
    ;;
  5)
    echo "退出"
    exit 0
    ;;
  *)
    echo "无效选择"
    ;;
esac

echo ""
echo "=========================================="
echo "  操作完成"
echo "=========================================="
