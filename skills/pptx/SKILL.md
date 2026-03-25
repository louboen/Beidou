---
name: pptx
description: Create, edit, and analyze PowerPoint presentations (.pptx files). Supports reading content, creating from scratch, editing templates, and applying professional design principles.
---

# PPTX Skill - PowerPoint 演示文稿制作

本技能提供 PowerPoint 演示文稿的完整制作能力，包括：
- 读取和分析 PPTX 文件内容
- 从模板创建或编辑现有演示文稿
- 从零开始创建新演示文稿
- 应用专业设计原则

## 快速参考

| 任务 | 方法 |
|------|------|
| 读取/分析内容 | `python -m markitdown presentation.pptx` |
| 编辑或从模板创建 | 读取 editing.md |
| 从零开始创建 | 读取 pptxgenjs.md |

## 读取内容

### 文本提取
```bash
python -m markitdown presentation.pptx
```

### 可视化概览
```bash
python scripts/thumbnail.py presentation.pptx
```

### 原始 XML
```bash
python scripts/office/unpack.py presentation.pptx unpacked/
```

## 编辑工作流程

1. 使用 thumbnail.py 分析模板
2. 解压缩 → 操作幻灯片 → 编辑内容 → 清理 → 打包

## 从零开始创建

当没有模板或参考演示文稿时使用。

## 设计原则

### 开始之前

1. **选择大胆的颜色方案**：配色应该为这个主题量身定制
2. **主导色优先**：一种颜色占主导（60-70% 视觉权重），1-2 种辅助色，1 种强调色
3. **明暗对比**：标题和结尾幻灯片使用深色背景，内容幻灯片使用浅色
4. **视觉主题**：选择一个独特的元素并在所有幻灯片中重复使用

### 推荐配色方案

| 主题 | 主色 | 辅助色 | 强调色 |
|------|------|--------|--------|
| 午夜行政 | #1E2761 (海军蓝) | #CADCFC (冰蓝) | #FFFFFF (白) |
| 森林苔藓 | #2C5F2D (森林绿) | #97BC62 (苔藓绿) | #F5F5F5 (奶油) |
| 珊瑚能量 | #F96167 (珊瑚) | #F9E795 (金) | #2F3C7E (海军蓝) |
| 温暖陶土 | #B85042 (陶土) | #E7E8D1 (沙) | #A7BEAE (鼠尾草) |
| 海洋渐变 | #065A82 (深蓝) | #1C7293 (青) | #21295C (午夜) |
| 木炭极简 | #36454F (木炭) | #F2F2F2 (灰白) | #212121 (黑) |

### 每页幻灯片设计

**布局选项**：
- 两列布局（左侧文本，右侧插图）
- 图标 + 文本行（彩色圆圈中的图标，粗体标题，下方描述）
- 2x2 或 2x3 网格（一侧图像，另一侧内容块网格）
- 半出血图像（左侧或右侧全幅）与内容叠加

**数据显示**：
- 大数字标注（60-72pt 大数字，下方小标签）
- 对比列（前后对比、优缺点、并排选项）
- 时间线或流程图（编号步骤、箭头）

**视觉润色**：
- 章节标题旁的彩色圆圈图标
- 关键数据或标语的斜体强调文本

### 字体建议

| 标题字体 | 正文字体 |
|----------|----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Trebuchet MS | Calibri |

| 元素 | 大小 |
|------|------|
| 幻灯片标题 | 36-44pt 粗体 |
| 章节标题 | 20-24pt 粗体 |
| 正文文本 | 14-16pt |
| 说明文字 | 10-12pt 浅色 |

### 间距规范

- 最小边距：0.5 英寸
- 内容块间距：0.3-0.5 英寸
- 留白：不要填满每个角落

### 避免常见错误

- ❌ 不要重复相同的布局
- ❌ 不要居中对齐正文文本（标题除外）
- ❌ 不要忽略大小对比（标题需要 36pt+）
- ❌ 不要使用纯白色背景上的纯黑色文本

## 使用方法

当用户需要制作 PPT 时：

1. **确定内容**：从用户获取主题、大纲、关键信息
2. **选择方法**：
   - 有模板 → 编辑工作流程
   - 无模板 → 从零开始创建
3. **应用设计原则**：选择合适的配色、字体、布局
4. **生成文件**：创建 .pptx 文件
5. **提供下载**：告知用户文件位置

## 工具依赖

- `python-pptx`：Python PPTX 库
- `markitdown`：文档内容提取
- `pptxgenjs`：JavaScript PPTX 生成（可选）

## 示例命令

```bash
# 安装依赖
pip install python-pptx markitdown

# 提取内容
python -m markitdown presentation.pptx

# 创建新演示文稿
python scripts/create_pptx.py --output new_presentation.pptx
```
