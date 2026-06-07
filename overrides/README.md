# 项目级模板覆盖目录

此目录用于存放项目定制模板，覆盖全局默认模板。

## 使用方式

将你定制的模板文件放入此目录，文件名必须与默认模板文件名一致：

| 文件名 | 覆盖的默认模板 | 对应步骤 |
|--------|---------------|----------|
| prd.md | templates/prd.md | Step 5 |
| business-flow.md | templates/business-flow.md | Step 7 |
| page-spec.md | templates/page-spec.md | Step 8 |
| permission-matrix.md | templates/permission-matrix.md | Step 9 |
| acceptance-criteria.md | templates/acceptance-criteria.md | Step 10 |
| dev-tasks.md | templates/dev-tasks.md | Step 11 |
| traceability-matrix.md | templates/traceability-matrix.md | Step 11 |

以下模板不在主流程中自动生成，但可按需覆盖：

| 文件名 | 覆盖的默认模板 | 适用场景 |
|--------|---------------|----------|
| data-dictionary.md | templates/data-dictionary.md | 数据模型复杂时按需生成 |
| non-functional.md | templates/non-functional.md | 需独立非功能规格书时按需生成 |

## 覆盖优先级

```
overrides/（项目级） > presets/<industry>/（行业预设） > templates/（全局默认）
```

项目级覆盖优先级最高，适合有特殊定制需求的团队使用。

## 示例

如果你的团队需要 PRD 中包含"安全评估"章节，而默认模板没有，你可以：
1. 复制 `templates/prd.md` 到 `overrides/prd.md`
2. 在 overrides 版本中增加"安全评估"章节
3. 生成 PRD 时将自动使用 overrides 版本

## HTML 原型定制

如果需要定制 HTML 原型的视觉风格（如品牌色、侧栏宽度、字体），可以：

1. 修改 `references/prototype-style-reference.html` 中的 CSS 变量：
   - `--sidebar-bg`：侧栏背景色（默认 `#001a3a`）
   - `--sidebar-width`：侧栏宽度（默认 `220px`）
   - `--primary-color`：主色（默认 `#2563eb`）
   - `--header-height`：顶栏高度（默认 `56px`）
2. 或者在 `overrides/` 中创建 `prototype-style.html`，Step 8 会优先读取此文件作为原型样式参考
3. 原型的内容结构（菜单项、表格列、筛选条件等）来自 `08-page-spec.md`，不在 style reference 中定义