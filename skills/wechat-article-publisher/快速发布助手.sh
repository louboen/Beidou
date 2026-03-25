#!/bin/bash
# 微信公众号快速发布助手

cd /home/admin/.openclaw/workspace/skills/wechat-article-publisher

echo "=========================================="
echo "  微信公众号快速发布助手"
echo "=========================================="
echo ""

echo "📋 可用文章列表:"
echo ""

# 显示文章列表
i=1
for file in articles/auto_*.html articles/2026-03-19_*_已填充.html; do
    if [ -f "$file" ]; then
        title=$(grep -o "<title>.*</title>" "$file" | sed 's/<title>//;s/<\/title>//')
        size=$(wc -c < "$file")
        echo "  $i. $(basename "$file")"
        echo "     标题: $title"
        echo "     大小: $size 字符"
        echo ""
        i=$((i+1))
    fi
done

echo "=========================================="
echo "  操作选项"
echo "=========================================="
echo "  1. 查看文章内容"
echo "  2. 复制文章到剪贴板"
echo "  3. 检查文章完整性"
echo "  4. 测试微信 API"
echo "  5. 退出"
echo ""

read -p "请选择操作 [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "📄 选择要查看的文章:"
        files=($(ls articles/auto_*.html articles/2026-03-19_*_已填充.html 2>/dev/null))
        for idx in "${!files[@]}"; do
            echo "  $((idx+1)). $(basename "${files[$idx]}")"
        done
        
        read -p "请输入文章编号: " article_num
        if [ -n "$article_num" ] && [ "$article_num" -ge 1 ] && [ "$article_num" -le "${#files[@]}" ]; then
            selected_file="${files[$((article_num-1))]}"
            echo ""
            echo "🔍 查看文章: $(basename "$selected_file")"
            echo "=========================================="
            # 显示前100行内容
            head -100 "$selected_file"
            echo "=========================================="
            echo "📊 完整文件: $selected_file"
            echo "📏 大小: $(wc -c < "$selected_file") 字符"
        else
            echo "❌ 无效的选择"
        fi
        ;;
        
    2)
        echo ""
        echo "📋 选择要复制的文章:"
        files=($(ls articles/auto_*.html articles/2026-03-19_*_已填充.html 2>/dev/null))
        for idx in "${!files[@]}"; do
            echo "  $((idx+1)). $(basename "${files[$idx]}")"
        done
        
        read -p "请输入文章编号: " article_num
        if [ -n "$article_num" ] && [ "$article_num" -ge 1 ] && [ "$article_num" -le "${#files[@]}" ]; then
            selected_file="${files[$((article_num-1))]}"
            
            # 检查是否支持 xclip
            if command -v xclip >/dev/null 2>&1; then
                cat "$selected_file" | xclip -selection clipboard
                echo "✅ 文章内容已复制到剪贴板 (使用 xclip)"
            elif command -v pbcopy >/dev/null 2>&1; then
                cat "$selected_file" | pbcopy
                echo "✅ 文章内容已复制到剪贴板 (使用 pbcopy)"
            else
                echo "⚠️  未找到剪贴板工具，显示前500字符:"
                echo ""
                head -c 500 "$selected_file"
                echo "..."
                echo ""
                echo "📋 请手动复制以上内容"
            fi
        else
            echo "❌ 无效的选择"
        fi
        ;;
        
    3)
        echo ""
        echo "🔍 检查文章完整性:"
        echo ""
        
        for file in articles/auto_*.html articles/2026-03-19_*_已填充.html; do
            if [ -f "$file" ]; then
                echo "📄 $(basename "$file"):"
                
                # 检查模板标记
                if grep -q "\[.*\]" "$file"; then
                    echo "  ⚠️  包含模板标记"
                    grep "\[.*\]" "$file" | head -3 | sed 's/^/    /'
                else
                    echo "  ✅ 无模板标记"
                fi
                
                # 检查基本结构
                if grep -q "<title>" "$file" && grep -q "<h1>" "$file"; then
                    echo "  ✅ 结构完整"
                else
                    echo "  ⚠️  结构不完整"
                fi
                
                # 显示大小
                size=$(wc -c < "$file")
                echo "  📏 大小: $size 字符"
                echo ""
            fi
        done
        ;;
        
    4)
        echo ""
        echo "🔧 测试微信 API:"
        echo ""
        
        # 检查 .env 文件
        if [ -f ".env" ]; then
            echo "✅ .env 文件存在"
            appid=$(grep "WECHAT_APPID" .env | cut -d= -f2)
            if [ -n "$appid" ]; then
                echo "✅ AppID: $appid"
            else
                echo "❌ 未找到 AppID"
            fi
        else
            echo "❌ .env 文件不存在"
        fi
        
        echo ""
        echo "🔄 测试 access_token 获取..."
        python3 -c "
import requests
from pathlib import Path

env_path = Path('.env')
config = {}
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip().strip('\"').strip(\"'\")

appid = config.get('WECHAT_APPID')
appsecret = config.get('WECHAT_APPSECRET')

if appid and appsecret:
    print('🔑 使用配置:')
    print(f'   AppID: {appid}')
    print(f'   AppSecret: {appsecret[:10]}...')
    
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': appid,
        'secret': appsecret
    }
    
    try:
        response = requests.get(token_url, params=params, timeout=10)
        result = response.json()
        
        if 'access_token' in result:
            print(f'✅ access_token 获取成功: {result[\"access_token\"][:20]}...')
            print(f'📊 有效期: {result[\"expires_in\"]} 秒')
        else:
            print(f'❌ 获取失败: {result}')
            
    except Exception as e:
        print(f'❌ 请求异常: {e}')
        
else:
    print('❌ 配置不完整')
" 2>&1
        ;;
        
    5)
        echo "退出"
        ;;
        
    *)
        echo "❌ 无效的选择"
        ;;
esac

echo ""
echo "=========================================="
echo "  操作完成"
echo "=========================================="