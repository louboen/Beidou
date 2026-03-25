# 微信公众号发布技能

## 概述

这是一个用于自动发布文章到微信公众号草稿箱的 OpenClaw 技能。通过微信公众号 API，你可以将 Markdown 或 HTML 格式的文章快速发布到微信公众号草稿箱，然后在微信公众平台预览并发布。

## 安装状态

✅ 技能已成功安装并配置到 OpenClaw 工作空间。

## 文件结构

```
~/.openclaw/workspace/skills/wechat-article-publisher/
├── SKILL.md                    # 技能详细文档
├── README.md                   # 本使用指南
├── .env.example                # 环境变量模板
├── test-article.md             # 测试文章
└── scripts/
    ├── wechat_api.py           # 微信公众号 API 客户端
    └── parse_markdown.py       # Markdown 解析器（可选）
```

## 快速开始

### 1. 获取 API 密钥

1. 访问 https://wx.limyai.com
2. 注册并登录账号
3. 授权你的微信公众号
4. 获取 `WECHAT_API_KEY`

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
nano .env
```

`.env` 文件内容：
```bash
WECHAT_API_KEY=你的_api_密钥_这里
```

### 3. 列出已授权的公众号

```bash
cd ~/.openclaw/workspace/skills/wechat-article-publisher
python3 scripts/wechat_api.py list-accounts
```

### 4. 发布测试文章

```bash
# 使用测试文章
python3 scripts/wechat_api.py publish \
  --appid 你的微信公众号AppID \
  --markdown test-article.md
```

## 详细使用指南

### 发布 Markdown 文章

```bash
python3 scripts/wechat_api.py publish \
  --appid wx1234567890 \
  --markdown /path/to/your/article.md \
  --title "自定义标题" \
  --author "作者名"
```

### 发布 HTML 文章

```bash
python3 scripts/wechat_api.py publish \
  --appid wx1234567890 \
  --html /path/to/your/article.html \
  --type news
```

### 发布为小绿书格式

```bash
python3 scripts/wechat_api.py publish \
  --appid wx1234567890 \
  --markdown /path/to/your/article.md \
  --type newspic
```

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--appid` | 微信公众号 AppID | 是 |
| `--markdown` | Markdown 文件路径 | 与 `--html` 二选一 |
| `--html` | HTML 文件路径 | 与 `--markdown` 二选一 |
| `--title` | 文章标题（默认使用文件中的 H1） | 否 |
| `--author` | 作者名称 | 否 |
| `--type` | 文章类型：`news`（普通文章）或 `newspic`（小绿书） | 否 |

## 在 OpenClaw 中使用

### 通过 OpenClaw 命令发布

```bash
# 在 OpenClaw 工作空间中使用
cd ~/.openclaw/workspace

# 发布文章到微信公众号
python3 skills/wechat-article-publisher/scripts/wechat_api.py publish \
  --appid 你的AppID \
  --markdown articles/my-article.md
```

### 创建自动化脚本

创建 `publish-wechat.sh` 脚本：

```bash
#!/bin/bash
# 微信公众号发布脚本

API_KEY="你的_api_密钥"
APPID="你的微信公众号AppID"
ARTICLE_PATH="$1"

cd ~/.openclaw/workspace/skills/wechat-article-publisher

# 设置环境变量
export WECHAT_API_KEY="$API_KEY"

# 发布文章
python3 scripts/wechat_api.py publish \
  --appid "$APPID" \
  --markdown "$ARTICLE_PATH"

echo "文章已发布到微信公众号草稿箱"
```

## 常见问题

### Q: 如何获取微信公众号 AppID？
A: 在微信公众平台 → 设置 → 公众号设置 → 基本配置中查看 AppID。

### Q: API 密钥无效怎么办？
A: 确保在 wx.limyai.com 上正确授权了你的微信公众号。

### Q: 文章发布后在哪里查看？
A: 文章会保存到微信公众号的草稿箱，需要登录微信公众平台进行预览和发布。

### Q: 支持哪些图片格式？
A: 支持 JPG、PNG、GIF 格式，图片需要可公开访问的 URL。

### Q: 文章长度有限制吗？
A: 微信公众号有字数限制，建议文章不超过 2000 字。

## 安全注意事项

1. **保护 API 密钥** - 不要将 `.env` 文件提交到版本控制系统
2. **使用环境变量** - 在生产环境中使用环境变量而非硬编码
3. **定期更新密钥** - 定期更换 API 密钥以提高安全性
4. **权限最小化** - 仅授予必要的 API 权限

## 故障排除

### 错误: "API_KEY_MISSING"
```bash
export WECHAT_API_KEY="你的_api_密钥"
```

### 错误: "ACCOUNT_NOT_FOUND"
- 确认微信公众号已正确授权
- 检查 AppID 是否正确

### 错误: "Python 版本不兼容"
- 确保使用 Python 3.6+
- 已修复 Python 3.6 的兼容性问题

## 扩展功能

### 批量发布
可以编写脚本批量发布多篇文章：

```bash
#!/bin/bash
for article in articles/*.md; do
  echo "发布: $article"
  python3 scripts/wechat_api.py publish \
    --appid "$APPID" \
    --markdown "$article"
  sleep 5  # 避免 API 限制
done
```

### 定时发布
结合 Cron 实现定时发布：

```bash
# 每天上午10点发布
0 10 * * * /path/to/publish-wechat.sh /path/to/daily-article.md
```

## 技术支持

- 技能作者: iamzifei
- 技能主页: https://skills.sh/iamzifei/wechat-article-publisher-skill
- API 文档: https://wx.limyai.com/api/docs

---

**安装时间**: 2026-03-18 13:30  
**安装者**: 司南 (OpenClaw AI 助手)  
**状态**: ✅ 就绪