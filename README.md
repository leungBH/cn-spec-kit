# cn-spec-kit

> 面向中国 ToB 软件产品团队的 **Agent-Ready 产品规格生成工具**：从一句话需求，自动产出可被 AI Coding Agent 直接消费的产品规格文档链。

[English](./README.en.md) · [MIT License](./LICENSE)

---

## 为什么做这个工具

中国 ToB 软件团队在产品规格阶段普遍面临四个痛点：

- **需求零散**：客户一句话、客户访谈纪要、领导口头要求，质量参差不齐
- **产物不齐**：PRD、业务流程、页面原型、权限矩阵、验收标准、研发任务往往缺这缺那
- **AI 难消费**：现有文档没有结构化到字段级，AI Coding Agent 拿到也不知道怎么落地
- **质量难控**：缺少跨产物一致性校验，设计漏洞往往到开发后期才暴露

**cn-spec-kit** 把这件事拆成 11 步标准流程，每一步都有自动化质量门禁，**最后产出的是 AI 友好的结构化文档链，可以直接喂给 AI Coding Agent 干活**。

---

## 核心特性

- **11 步标准化流程**：需求输入 → 发现 → 竞品调研 → 追问 → 模板选择与需求文档 → PRD → 开发范围 → 功能依赖DAG → 业务流程 → 页面原型 → 权限矩阵 → 验收标准 → 研发任务
- **三层自动化质量门禁**：
  1. 步骤完整性门禁（每步 checklist 覆盖率 ≥ 90%）
  2. 跨步骤一致性检查（角色、状态、操作、验收场景在产物间保持一致）
  3. 外部大模型评审（10 年+ ToB 专家视角，主动质疑设计缺陷）
- **人类QA确认门**：Step 4.5（需求文档）和 Step 8（页面原型）必须人类确认才能继续
- **模板覆盖机制**：支持行业级（`presets/`）+ 全局默认（`templates/`）两层覆盖
- **并行 Agent 策略**：竞品调研、HTML 原型生成、研发任务拆解等环节支持多 Agent 并行
- **领域知识沉淀**：内置 3 个行业预设（制造/金融/教育），按行业加载定制模板

---

## 快速开始

> cn-spec-kit 是一份 **Skill 资源包**，而不是独立的 CLI 工具。它面向 AI Agent / AI IDE 使用。

### 在 Trae / Claude Code 等支持 Skills 的 IDE 中使用

1. 将本仓库克隆（或复制）到 IDE 的 skills 目录下：

   ```bash
   # Trae
   .trae/skills/cn-spec-kit/
   # Claude Code
   .claude/skills/cn-spec-kit/
   ```

2. 在对话中用一句话触发，例如：

   ```
   帮我做一份合同管理系统的产品规格：客户希望支持合同起草、审批、归档、台账、到期提醒
   ```

3. AI Agent 会按 11 步流程自动执行，每步产出 Markdown 文档 + 自动跑质量门禁。

### 单独使用某个步骤

如果你已有部分前置产物，可以直接跳到对应步骤：

```
我已经有需求发现文档了，请直接基于它生成 PRD
```

详见 [`SKILL.md`](./SKILL.md) 中的「使用模式」章节。

---

## 产物示例

执行完完整流程后，会在 `specs/<序号-功能名>/` 下生成 15 份结构化文档：

| 产物 | 文件 | 用途 |
|------|------|------|
| 需求简述 | `00-brief.md` | 一句话需求原文 |
| 需求发现 | `01-discovery.md` | 客户背景与业务问题 |
| 竞品调研 | `02-competitive-research.md` | 竞品功能借鉴与差距分析 |
| 需求文档 | `03-requirement.md` | 按所选模板生成的正式需求文档 |
| PRD | `04-prd.md` | 产品需求文档 |
| 开发范围 | `05-scope-selection.md` | 用户选择的优先级范围 |
| 功能依赖 | `06-dependency-dag.md` | 模块间依赖关系图 |
| 业务流程 | `07-business-flow.md` | 状态流 + 审批流 |
| 页面规格 | `08-page-spec.md` | 页面清单 + 每页详细规格 |
| HTML 原型 | `09-html-prototype/` | 低保真原型（浏览器打开查看） |
| 权限矩阵 | `10-permission-matrix.md` | 角色 × 功能权限 |
| 验收标准 | `11-acceptance.md` | 正常 + 异常 + 边界验收 |
| 研发任务 | `12-dev-tasks.md` | 前端 / 后端 / 测试任务拆解 |
| 追踪矩阵 | `13-traceability-matrix.md` | 需求 → 产物全链路追溯 |
| 评审日志 | `14-review-log.md` | 全链路评审记录 |

---

## 目录结构

```
cn-spec-kit/
├── SKILL.md                       # 技能入口文档（AI Agent 阅读）
├── checklists/                    # 步骤质量门禁 checklist
│   ├── acceptance-checklist.md
│   ├── permission-checklist.md
│   ├── prd-checklist.md
│   └── requirement-checklist.md
├── steps/                         # 11 步执行逻辑
│   ├── step1-input.md ~ step11-tasks.md
│   ├── consistency-checks.md      # 跨步骤一致性检查规则
│   └── external-review.md         # 外部大模型评审机制
├── templates/                     # 全局默认模板
│   ├── prd.md / business-flow.md / page-spec.md
│   ├── permission-matrix.md / acceptance-criteria.md
│   ├── dev-tasks.md / traceability-matrix.md
│   ├── requirement-sdd.md         # 需求文档模板（SDD 风格）
│   ├── data-dictionary.md         # 可选补充：数据字典
│   ├── non-functional.md          # 可选补充：非功能需求
│   ├── review-log.md              # 评审日志模板
│   └── index.md                   # 模板清单索引
├── presets/                       # 行业预设
│   ├── manufacturing/             # 制造业
│   ├── fintech/                   # 金融业
│   └── education/                 # 教育业
├── references/                    # 参考资料与工具
│   ├── external-llm-config.md     # 外部大模型配置说明
│   ├── .cn-spec-kit-llm.example.json
│   ├── industry-templates.md
│   ├── permission-patterns.md
│   ├── tob-patterns.md
│   ├── prototype-minimal-template.html
│   └── prototype-validator.py     # HTML 原型 8 项硬性约束自检
├── LICENSE
└── .gitignore
```

---

## 模板覆盖机制

模板读取按优先级顺序查找，高优先级覆盖低优先级：

```
1. 行业预设      → presets/<industry>/<template>.md
2. 全局默认      → templates/<template>.md
```

**使用场景**：
- 你在做特定行业（制造/金融/教育）→ 自动加载行业预设
- 默认模板始终兜底，开箱即用

---

## 外部大模型评审（可选）

cn-spec-kit 支持接入外部 LLM 作为评审员，以 10 年+ ToB 专家视角独立评审设计合理性。

**配置方式**：将外部 LLM 配置写入 `.cn-spec-kit-llm.json`（**已在 .gitignore 中忽略，请勿提交**）。参考 [`references/external-llm-config.md`](./references/external-llm-config.md) 和 [`references/.cn-spec-kit-llm.example.json`](./references/.cn-spec-kit-llm.example.json)。

**评审结果**会记录到 `14-review-log.md`，全程可追溯。

---

## 路线图

- [x] 11 步主流程 + 两层质量门禁
- [x] 外部大模型评审机制
- [x] 模板覆盖机制（行业/全局）
- [x] 行业预设（制造/金融/教育）
- [x] HTML 原型 8 项硬性约束 + 自检脚本
- [ ] 更多行业预设（医疗、零售、政务…）
- [ ] OpenAPI / GraphQL 契约自动生成
- [ ] 与主流 AI Coding Agent（Cursor / Trae / Claude Code）深度集成

---

## 贡献

欢迎以 Issue 或 Pull Request 形式贡献：

- **新行业预设**：在 `presets/` 下新增目录，提供 `prd.md` / `permission-matrix.md` 即可
- **新模板**：在 `templates/` 下提供完整模板，并在 `templates/index.md` 索引
- **Bug 反馈**：描述复现步骤、输入、期望产物与实际产物
- **最佳实践**：把你的行业经验沉淀为 checklist / patterns

提交前请确保：所有产物文件用中文撰写，目录与文件名用英文 kebab-case。

---

## 协议

[MIT License](./LICENSE) · Copyright (c) 2026 Jeremy
