---
name: cn-spec-kit
description: 面向中国 ToB 软件产品团队的 Agent-Ready 产品规格生成工具。从一句话需求到完整需求文档、PRD、业务流程、页面原型、权限矩阵、验收标准、研发任务。当用户提到 PRD、产品需求文档、ToB需求、业务流程设计、页面规格、权限矩阵、字段字典、验收标准、研发任务拆解、需求规格、客户需求、功能设计、产品规格、合同管理、客户管理、采购管理、库存管理、审批流程、报表需求、AI SDD、售前需求文档时触发此技能。也适用于用户给出一句话需求、客户访谈纪要、简单业务描述，希望生成完整产品规格文档链的场景。
---

# cn-spec-kit：中国 ToB 软件产品规格生成工具

将一句话需求、客户访谈纪要或简单业务描述，转化为完整的 Agent-Ready 产品规格文档链。

---

## 核心流程

```
需求输入 → 发现 → 竞品调研 → 追问 → 模板选择与需求文档 → PRD → 开发范围选择 → 功能依赖DAG → 业务流程 → 页面原型 → 权限矩阵 → 验收标准 → 研发任务
```

每个步骤产出一份 Markdown 文档，**每步都有质量检查**：

1. **步骤完整性门禁**：内部 checklist 覆盖率检查
2. **跨步骤一致性检查**：跨产物一致性校验
3. **外部大模型评审**：调用外部 LLM 以**产品设计合理性**视角独立评审，主动发现问题、质疑设计缺陷、驱动迭代，而非仅做完整性打分
4. **人类QA确认门**（仅 Step 5 和 Step 9）：三层自动化检查通过后，暂停等待人类确认产物质量后才进入下一步

门禁通过后才进入下一步，未通过则回到本步修补。

---

## 质量门禁机制（三层自动化检查 + 人类QA确认门）

### 第一层：步骤完整性门禁

1. **文件存在性检查**：确认产物文件已成功写入磁盘
2. **完整性检查**：读取对应 checklist，逐条检查产物是否覆盖
3. **评分**：按 checklist 计算覆盖率得分（覆盖项数/总项数）
4. **判定**：
   - 得分 ≥ 90%：✅ 通过，进入第二层
   - 得分 70%-89%：⚠️ 基本通过，列出缺失项供用户确认是否需要补充
   - 得分 < 70%：❌ 不通过，回到本步修补缺失内容，重新生成后再检查
5. **输出**：每次门禁检查结果用 `log()` 输出，让用户看到检查过程

各步骤对应的 checklist：

| Step | 产物 | Checklist |
|------|------|-----------|
| Step 1 | 00-brief.md | 内联检查（输入质量判断） |
| Step 2 | 01-discovery.md | 内联检查（7维度覆盖） |
| Step 3 | 02-competitive-research.md | 内联检查（3竞品+5功能点） |
| Step 4 | 01-discovery.md 追问补充 | 阻塞性维度必须明确（审批流+权限层级） |
| Step 5 | 03-requirement.md | checklists/requirement-checklist.md |
| Step 6 | 04-prd.md | checklists/prd-checklist.md |
| Step 7 | 05-scope-selection.md | 用户确认即通过 |
| Step 8 | 06-dependency-dag.md + 07-business-flow.md | 内联检查（DAG覆盖选定模块+每模块4要素） |
| Step 9 | 08-page-spec.md + HTML | 内联检查（12规格要素） |
| Step 10 | 10-permission-matrix.md | checklists/permission-checklist.md |
| Step 11 | 11-acceptance.md | checklists/acceptance-checklist.md |
| Step 12 | 12-dev-tasks.md + 13-traceability | 内联检查（4类任务完整+追踪全覆盖） |

### 第二层：跨步骤一致性检查

在关键步骤完成后，自动执行跨产物一致性校验（详细规则见 `steps/consistency-checks.md`）：

| 检查时机 | 检查内容 | 严重程度 |
|----------|----------|----------|
| Step 5 后 | 需求文档中的角色列表 ↔ discovery 中的干系人 | 🟡 警告 |
| Step 5 后 | 需求文档中的验收指标 ↔ discovery 中的成功指标 | 🔴 阻塞 |
| Step 9 后 | 页面规格中的状态名 ↔ 业务流程中的状态定义 | 🔴 阻塞 |
| Step 9 后 | DAG 依赖关系 ↔ 页面跳转关系 | 🟡 警告 |
| Step 10 后 | 权限矩阵中的操作 ↔ 页面规格中的按钮操作 | 🔴 阻塞 |
| Step 10 后 | 权限矩阵中的角色 ↔ PRD 角色定义 | 🟡 警告 |
| Step 11 后 | 验收标准中的场景 ↔ PRD 业务场景 | 🔴 阻塞 |
| Step 12 后 | 研发任务中的 API ↔ 页面规格中的字段和操作 | 🟡 警告 |
| Step 12 后 | 研发任务构建顺序 ↔ DAG 构建顺序建议 | 🟡 警告 |

🔴 阻塞级不一致必须修复后才能继续；🟡 警告级列出差异供用户确认。

### 第三层：外部大模型评审

第一层和第二层都通过后，自动触发外部大模型评审（详细机制见 `steps/external-review.md`）。

**评审定位**：评审员以**10年+ToB产品专家视角**评审设计合理性，主动发现问题、提出质疑、驱动迭代优化，而非仅做完整性检查（完整性由第一层内部门禁负责）。

**评审流程**：
```
内部门禁通过 → 一致性检查通过 → 外部大模型评审 → 通过/不通过/⚠️通过但需关注
                                                ↓ 不通过或⚠️需关注
                                            根据评审意见优化 → 重新内部门禁 → 重新外部评审
                                                ↓ 通过（最多重试3轮）
                                            记录评审结果 → 进入下一步（或触发人类QA确认门）
```

**评审触发时机**：

| Step | 产物 | 重点评审维度 |
|------|------|-------------|
| Step 2 | 01-discovery.md | 角色识别遗漏？场景覆盖偏窄？成功指标可量化？ |
| Step 3 | 02-competitive-research.md | 借鉴功能与客户场景匹配？差距分析过于乐观？ |
| Step 4 | 01-discovery.md 追问补充 | 审批/权限答案真正解决问题？默认假设有二义性？ |
| Step 5 | 03-requirement.md | 需求描述具体到字段级？验收指标可测试？裁剪遗漏关键需求？ |
| Step 6 | 04-prd.md | 功能优先级合理？P0构成最小闭环？模块边界清晰？ |
| Step 7 | 05-scope-selection.md | **无需外部评审**（用户手动确认） |
| Step 8 | 06+07 | DAG遗漏冗余？审批流死锁？状态定义歧义？ |
| Step 9 | 08-page-spec.md | 布局符合操作习惯？筛选覆盖实际查询？角色视图遗漏差异？ |
| Step 10 | 10-permission-matrix.md | 权限死角？数据隔离漏洞？审批权限覆盖所有层级？ |
| Step 11 | 11-acceptance.md | 验收覆盖真实业务分支？边界条件遗漏？权限验收真验证了隔离？ |
| Step 12 | 12+13 | 任务粒度适中？依赖反映技术依赖？追踪矩阵无断链？ |

**通过标准**：✅总分 ≥ 75 且无🔴严重问题；⚠️总分 ≥ 75 但有≤1个🔴严重问题可快速修复；❌总分 < 75 或🔴严重问题 ≥ 2个
**不通过**：根据评审意见优化产物，最多重试 3 轮
**评审结果记录到 `14-review-log.md`**

**外部大模型注册**：通过 OpenAI Chat Completions 格式，用户提供 URL、Key、Model（详见 `references/external-llm-config.md`）。配置文件 `.cn-spec-kit-llm.json` 存储在项目根目录。

**多评审员策略**：
- 1 个评审员：该评审员结果决定是否通过
- 2+ 个评审员：严格多数通过（>50%通过才视为通过），且任一评审员发现🔴严重问题时必须人类确认

### 第四层：人类QA确认门（仅 Step 5 和 Step 9）

**Step 5（需求文档）和 Step 9（页面原型）** 在三层自动化检查全部通过后，必须暂停等待人类确认，不能自动进入下一步。这两个步骤的产物直接影响后续所有设计决策，需要人类从业务真实性和交互体验角度做最终把关。

**确认流程**：

```
三层自动化检查通过 → 结构化提问展示产物摘要+评审问题 → 用户确认
                                                                    ↓ ✅确认通过
                                                                记录确认 → 进入下一步
                                                                    ↓ 🔧需要修改
                                                                根据反馈修改 → 重新三层检查 → 重新人类确认
```

**确认内容**：向用户展示（1）三层检查结果概要（2）产物关键摘要3-5条（3）外部评审发现的🔴🟡💡问题（4）特别提醒（Step 8提醒用户实际体验HTML原型）

**用户未回应时不自动进入下一步**。人类确认不计入外部评审的3轮重试限制。

---

## 🚨 Step 9（页面原型）硬性约束速查（一行不能漏）

> **本章节是整个 skill 中最高频踩坑的章节，单独提炼到这里便于 LLM 在生成 HTML 时快速对照。**
> 详细规则见 `steps/step9-prototype.md`；本章节是「最少必要规则」。

### 8 个不可违反的硬性约束

| # | 约束 | 漏掉的代价 | 速查 |
|---|------|-----------|------|
| 1 | **必须同时引用 `common.css` + `common.js`** | tab 切换、protocol 标签、drawer、sortable 全部失灵 | `<link rel="stylesheet" href="common.css">` 紧跟 `<script src="common.js"></script>` |
| 2 | **菜单项 ≤ 25、分组 ≤ 6、图标用方块字符** | 侧边栏滚动可见、跨设备 Emoji 渲染不一致 | 图标用 `▦▣▤▥▧▨▩▪▫◌◍◎●☰⚙⌂` |
| 3 | **业务组件用标准类名，不许自创** | 跨页面风格漂移 | 复用 `.diag .lib-cell .topo .perm .phone .protocol .grid-2/3/4 .chart-card .period-tabs` |
| 4 | **表格页必须有 `.filter` 筛选条** | 用户无法按条件查询 | 5 列 `.field` + 末列 `.filter-actions` |
| 5 | **复杂页（≥ 3 子视图）必须有 `.tabs`** | 一屏堆叠、页面超长 | 至少 3 个 `.tab` 配对应 `.tab-pane` |
| 6 | **不引入外部框架** | 引入即破坏样式一致性 | 禁止 Tailwind / Element Plus / Element UI / Ant Design CDN |
| 7 | **核心页独立 HTML，不堆 panel** | 单文件 5000+ 行、维护地狱 | 1 个 P0/P1 页 = 1 个 `xxx.html`，详情用 `.drawer` |
| 8 | **`<style>` 内有 `:root` CSS 变量** | 主题色/字号无法统一 | 必须在 style 开头定义 `--primary` 等变量 |

### 标准模板与参考

- **最小标准模板**（生成新页面时直接模仿它）：`references/prototype-minimal-template.html`
- **标准 CSS 变量与组件类名**：见 `steps/step9-prototype.md` 的「视觉规范」章节（唯一权威来源）
- **通用交互脚本**（tab 切换 / 协议标签 / 抽屉 / 排序 / Toast）：部署到 `prototypes/common.js`，所有原型页必须引用

### LLM 生成 HTML 后的 8 项自检（每次输出前必过）

```
□ 1. 引用了 common.css
□ 2. 引用了 common.js（紧跟 common.css 之后）
□ 3. 侧边栏菜单 ≤ 25、无 Emoji 图标
□ 4. 业务组件用标准类名（无 .my- .custom- .local- 前缀）
□ 5. 表格页有 .filter
□ 6. 复杂页（≥3 子视图）有 .tabs
□ 7. 无 Tailwind / Element Plus / Element UI / Ant Design CDN
□ 8. <style> 内有 :root CSS 变量定义
```

**自检未通过必须当场修复**，不允许写"已知问题、后续优化"。

### 常见反模式（真实踩过的坑）

| 反模式 | 症状 | 解法 |
|--------|------|------|
| 50 panel 塞 1 HTML | 单文件 5000+ 行、找不到菜单 | 核心页独立 HTML + 抽屉 |
| 每个页面内联 tab 切换 JS | 50 份相同 JS 散落各处 | 统一走 common.js |
| 漏掉 common.js | tab 点击没反应 | 强制引用 common.js |
| 自创类名 `.face-grid` `.my-diag` | 跨页面漂移 | 100% 复用 common.css 标准类名 |

---

## 模板覆盖机制

模板读取按优先级顺序查找，高优先级覆盖低优先级。**技能根目录**根据运行环境自动检测：Trae 环境为 `.trae/skills/cn-spec-kit/`，Claude Code 环境为 `.claude/skills/cn-spec-kit/`。

```
1. 行业预设      → <技能根>/presets/<industry>/<template>.md
2. 全局默认      → <技能根>/templates/<template>.md
```

**使用方式**：
- 用户选择行业预设时（Step 2 中识别行业），自动从 `presets/<industry>/` 读取行业定制模板
- 默认模板始终兜底，无需任何配置即可使用

**预设行业**：manufacturing（制造业）、fintech（金融业）、education（教育业）。可在 `presets/` 下新增目录扩展。

**可用需求文档模板**（详见 `templates/index.md`）：

| 模板ID | 名称 | 适用场景 |
|--------|------|----------|
| `requirement-sdd` | AI SDD 标准化需求文档 | 面向 AI 辅助开发环境，按数据/流程/功能开发分类，字段级可追溯 |

Step 5 会自动从 `templates/index.md` 加载模板清单，让用户选择。

---

## 并行 Agent 策略

以下步骤适合并行执行，提升效率：

| Step | 并行点 | 说明 |
|------|--------|------|
| Step 3 竞品调研 | 多角度搜索 | 5+不同关键词同时搜索，每个搜索一个 Agent |
| Step 3 竞品调研 | 深度分析 | 对多个竞品同时 WebFetch 抓取分析 |
| Step 9 页面原型 | HTML生成 | 多个角色视图入口同时生成（CSS 变量体系，每个角色一个 Agent） |
| Step 12 研发任务 | FE/BE/TEST | 前端、后端、测试三类任务同时拆解 |
| 外部评审 | 多评审员 | 多个外部评审员同时调用评审（如注册了 2+ 个评审员） |

使用并行工具调用或多个 Agent 同时执行。其余步骤顺序执行。

---

## 各步骤概述

详细执行逻辑在 `steps/` 目录的对应文件中。每个步骤文件包含：读取什么、生成什么、质量门禁标准、外部评审维度。

| Step | 步骤文件 | 产物 | 说明 |
|------|----------|------|------|
| 1 需求输入 | steps/step1-input.md | 判断输入质量 + **初始化外部评审员** | 不足则追问；检查/创建 `.cn-spec-kit-llm.json` |
| 2 需求发现 | steps/step2-discover.md | 00-brief.md + 01-discovery.md | 7维度覆盖 + 外部评审 |
| 3 竞品调研 | steps/step3-research.md | 02-competitive-research.md | **并行搜索+深度分析** + 外部评审 |
| 4 需求追问 | steps/step4-clarify.md | discovery追问补充 | **阻塞性澄清门** + 外部评审 |
| 5 模板选择与需求文档 | steps/step5-requirement.md | 03-requirement.md | **用户选模板，生成需求文档** + 外部评审 |
| 6 PRD | steps/step6-prd.md | 04-prd.md | 模板覆盖生效 + 外部评审 |
| 7 开发范围 | steps/step7-scope.md | 05-scope-selection.md | 用户选择P0/P0+P1/全量（**无外部评审**） |
| 8 依赖DAG+流程 | steps/step8-flow.md | 06-dependency-dag.md + 07-business-flow.md | **功能依赖DAG** + 外部评审 |
| 9 页面原型 | steps/step9-prototype.md | 08-page-spec.md + 09-html-prototype/ | **并行生成HTML** + 外部评审 |
| 10 权限矩阵 | steps/step10-permission.md | 10-permission-matrix.md | 模板覆盖生效 + 外部评审 |
| 11 验收标准 | steps/step11-acceptance.md | 11-acceptance.md | 覆盖选定优先级 + 外部评审 |
| 12 研发任务 | steps/step12-tasks.md | 12-dev-tasks.md + 13-traceability-matrix.md | **并行拆解FE/BE/TEST** + 外部评审 |

**新增机制文件**：

| 文件 | 说明 |
|------|------|
| steps/external-review.md | 外部大模型评审机制定义（调用方式、评审流程、结果处理） |
| references/external-llm-config.md | 外部大模型配置参考（常见模型配置示例） |
| templates/review-log.md | 评审记录日志模板 |

**序号规则**：查找 `specs/` 目录下已有子目录的最大序号，+1。如果 `specs/` 不存在则从 `001` 开始。功能名取英文 kebab-case。

**产物目录结构**：
```
specs/<序号-功能名>/
├── 00-brief.md
├── 01-discovery.md
├── 02-competitive-research.md
├── 03-requirement.md           ← 需求文档（按所选模板生成）
├── 04-prd.md
├── 05-scope-selection.md
├── 06-dependency-dag.md
├── 07-business-flow.md
├── 08-page-spec.md
├── 09-html-prototype/
├── 10-permission-matrix.md
├── 11-acceptance.md
├── 12-dev-tasks.md
├── 13-traceability-matrix.md
└── 14-review-log.md            ← 【新增】外部评审记录日志
```

**项目根目录新增文件**：
```
.cn-spec-kit-llm.json           ← 【新增】外部大模型评审员配置（URL/Key/Model）
```

---

## 使用模式

1. **完整流程**：输入一句话需求，自动走完 12 个步骤（推荐）
2. **单步执行**：用户只想要某个产物（如"只做PRD""只做需求文档""只做权限矩阵"），读取已有前置文档，跳到对应步骤执行
3. **增量补充**：已有部分文档，只需补充后续产物

单步执行时，跳过前置步骤，直接读取已有文档作为输入。但**仍需执行三层质量检查**。

如果前置产物不存在（如没有 PRD 就要做权限矩阵），提示用户先生成前置产物。

---

## 完成后输出

所有步骤完成后，显示总结：

```
## cn-spec-kit 生成完成

**功能模块**: <功能名>
**开发范围**: <用户选择的范围，如 P0+P1>
**需求文档模板**: <Step 5 选择的模板ID>
**产物目录**: specs/<序号-功能名>/
**外部评审**: <已注册评审员数量>位评审员，<通过/跳过>

| 产物 | 文件 | 说明 |
|------|------|------|
| 需求简述 | 00-brief.md | 一句话需求原文 |
| 需求发现 | 01-discovery.md | 客户背景与业务问题 |
| 竞品调研 | 02-competitive-research.md | 竞品功能借鉴与差距分析 |
| 需求文档 | 03-requirement.md | 按所选模板生成的正式需求文档 |
| PRD | 04-prd.md | 产品需求文档 |
| 开发范围 | 05-scope-selection.md | 用户选择的优先级范围 |
| 功能依赖 | 06-dependency-dag.md | 模块间依赖关系图 |
| 业务流程 | 07-business-flow.md | 状态流 + 审批流 |
| 页面规格 | 08-page-spec.md | 页面清单 + 每页详细规格 |
| HTML原型 | 09-html-prototype/ | 低保真原型（浏览器打开查看） |
| 权限矩阵 | 10-permission-matrix.md | 角色×功能权限 |
| 验收标准 | 11-acceptance.md | 正常+异常+边界验收 |
| 研发任务 | 12-dev-tasks.md | 前端/后端/测试任务拆解 |
| 追踪矩阵 | 13-traceability-matrix.md | 需求→产物全链路追溯 |
| 评审日志 | 14-review-log.md | 全链路评审记录（每个Step四层检查结果、问题编号追踪、修改内容、人类QA确认、统计汇总） |

下一步：
- 用浏览器打开 09-html-prototype/ 中的 HTML 文件查看原型
- 将 12-dev-tasks.md 交给研发团队或 AI coding agent
- 对照 11-acceptance.md 制定测试计划
- 未选定的 P2 功能可在二期启动时重新运行本 skill 补充
- 如果走 AI SDD 流程，可直接将 03-requirement.md 喂给 SDD 环境
- 查看 14-review-log.md 了解外部评审过程和优化记录
```

---

## Guardrails

- 每个步骤生成产物后，必须执行质量检查（内部门禁+一致性检查+外部评审），未通过不能进入下一步
- **Step 5（需求文档）和 Step 9（页面原型）在三层自动化检查通过后，必须暂停等待人类QA确认才能进入下一步**，不能自动跳过
- 外部评审以产品设计合理性为核心，评审员必须主动发现问题、质疑设计缺陷、驱动迭代，不能只做完整性打分
- 阻塞性维度（审批流程、权限层级）必须明确回答，不能跳过或假设
- 追问非阻塞性维度不要超过 3 轮，宁可做合理假设也不要无限追问
- 竞品调研至少搜索 5 个不同关键词，至少覆盖 3 个竞品
- 模板选择（Step 5）必须由用户确认，不能自动决定
- 开发范围选择必须由用户确认，不能自动决定
- 选定范围后的所有产物只覆盖选定优先级，未选定的简要标注"二期"
- HTML 原型为所有选定优先级的页面生成，不做部分跳过
- 研发任务粒度适中：前端每个页面一个任务，后端每个模块一个任务，测试每个验收标准一组
- 所有文档使用中文撰写，技术术语可以中英混用
- 产物文件名和目录名使用英文 kebab-case，文档内容使用中文
- 竞品调研报告单独存为 02-competitive-research.md，不合并到 discovery
- 需求文档模板的"填写要求"段落必须保留在产物中（这是文档的填写规范说明）
- 需求文档模板的"示例"段落必须替换为本次实际内容，不允许直接复制示例
- 需求文档中所有 `{{占位符}}` 必须显式替换或标注"待补充"
- **外部评审最多重试 3 轮**，超过 3 轮必须让用户介入决定
- **外部评审调用失败时不阻塞流程**：跳过外部评审，仅依赖内部门禁继续，但需在 review-log 中记录失败原因
- **`.cn-spec-kit-llm.json` 不应提交到版本控制**（建议加入 .gitignore）
- **评审员配置信息（尤其是 API Key）不写入任何产物文档**

---

## 可选补充产物

以下产物不在主流程中自动生成，但用户可按需单独请求。注意：编号 14 已用于评审日志（`14-review-log.md`），因此补充产物从 15 开始编号。

| 编号 | 产物 | 模板 | 适用场景 |
|------|------|------|----------|
| 15 | 15-data-dictionary.md | templates/data-dictionary.md | 数据模型复杂、需要独立字段字典文档时（字段定义已在 08-page-spec.md 和 PRD Section 6 中覆盖） |
| 16 | 16-non-functional.md | templates/non-functional.md | 需要独立非功能需求规格书时（内容已在 PRD Section 5 和 11-acceptance.md 中覆盖） |

使用方式：用户提出"生成数据字典"或"生成非功能需求规格书"时，读取已有 PRD 和页面规格作为输入，按对应模板生成。