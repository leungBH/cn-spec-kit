# Step 8: 页面原型 (prototype)

读取页面规格模板（按覆盖优先级查找）：
- 先查 `overrides/page-spec.md`
- 再查 `presets/<industry>/page-spec.md`
- 最后 `templates/page-spec.md`

读取 `04-prd.md`、`07-business-flow.md`、`06-dependency-dag.md` 和 `05-scope-selection.md` 获取功能、流程和依赖信息。

只对选定优先级的功能生成详细页面规格和 HTML 原型。

生成 `08-page-spec.md`（页面规格文档）。

---

## 页面规格文档必须包含

1. **页面清单总览表**（表格：页面名称 | 入口 | 目标 | 关联功能 | 优先级）
   - 选定优先级的页面：详细规格 + HTML 原型
   - 未选定优先级的页面：只在总览表中列出，标注"二期"

2. **角色视图分区表**——按角色分组列出各自可见的菜单和页面：

   ToB 产品通常有多种角色，不同角色看到不同的菜单和界面。必须在页面规格中明确区分：

   **内部角色**（公司员工）：同一个管理后台，侧栏菜单根据角色权限动态显示/隐藏
   **外部角色**（客户、代理商等）：独立的门户界面，布局和导航完全不同

   在页面规格中增加一张**角色视图分区表**：

   | 角色 | 界面类型 | 可见菜单/页面 | 界面特征 |
   |------|----------|---------------|----------|
   | 集团管理员 | 管理后台(全菜单) | 全部模块 | 侧栏全菜单，数据全公司 |
   | 分公司管理员 | 管理后台(部分菜单) | 本分公司数据范围 | 侧栏隐藏系统配置 |
   | 运营人员 | 管理后台(业务菜单) | 套餐/充值/余额/Key/渠道 | 侧栏隐藏报表/配置 |
   | 财务人员 | 管理后台(财务菜单) | 充值(财务确认)/退款/报表 | 侧栏仅财务相关模块 |
   | 客户(外部) | **客户门户** | 我的余额/我的Key/我的用量/充值记录 | 简洁导航，仅本人数据 |
   | 代理商 | **代理商门户** | 分销充值/下级客户/佣金 | 折扣价显示，佣金统计 |
   | 系统管理员 | 管理后台(配置菜单) | 系统配置+全局查看 | 侧栏突出配置模块 |

3. **选定页面的详细规格**，12 个规格要素：
   - 页面名称和入口路径
   - 页面目标（用户在这个页面做什么）
   - 适用角色
   - 布局描述（头部、侧栏、主区域，用 ASCII 方框图）——**必须标注该页面属于哪个角色视图**
   - 字段列表（字段名 | 类型 | 必填 | 校验规则 | 默认值 | 说明）
   - 按钮操作（按钮名 | 触发动作 | 权限要求）
   - 筛选条件（筛选字段 | 类型 | 默认值 | 说明）
   - 表格列（列名 | 数据字段 | 排序 | 固定列 | 说明）
   - 弹窗说明（弹窗名称 | 触发条件 | 内容 | 操作）
   - 状态显示（空数据、加载中、网络异常、权限不足）
   - 权限控制（哪些角色可见/可操作）
   - 页面跳转关系（Mermaid flowchart + 跳转表格）

4. **HTML 低保真原型**：按角色视图生成入口文件

   创建 `specs/<序号-功能名>/09-html-prototype/` 目录。

   **🟢 原型组织方式：按角色视图合并为入口文件**

   不再为每个页面单独生成 HTML。而是按角色视图合并——一个入口文件包含该角色可见的所有页面，通过侧栏菜单或顶部导航在文件内部跳转。

   **合并规则**：
   - **内部角色**（公司员工）：共用管理后台布局（顶部导航 + 侧栏 + 主区域），侧栏菜单项对应不同页面。如果多个内部角色的菜单差异只在"隐藏某些菜单项"（如运营隐藏报表/配置），则合并为同一个入口文件，侧栏菜单标注角色可见性。如果角色视角差异显著（如运营审批 vs 财务确认的操作按钮完全不同），则为差异角色单独生成入口文件。
   - **外部角色**（客户、代理商等）：每个外部角色一个独立入口文件，布局和导航与管理后台完全不同。

   **文件命名**：`index-<角色名>.html`
   - 示例：`index-管理员.html`、`index-运营人员.html`、`index-财务人员.html`、`index-客户.html`、`index-代理商.html`
   - 如果多个内部角色可以合并（菜单只是增减），取覆盖范围最广的角色命名（如 `index-管理员.html` 包含全菜单，其他角色看到的只是部分菜单）

   **入口文件结构**：
   ```
   index-管理员.html 结构示意（深色侧栏 + 白色顶栏布局）：
   ┌─ 深色侧栏(#001a3a) ──┐  ┌─ 白色顶栏(header) ────────────────────────────────┐
   │  · Logo + 平台名    │  │  面包屑: 统计与日志 / 用量统计   用户区: 角色+头像  │
   │  ── 工作台 ──       │  ├─ 主区域(.content) ───────────────────────────────────┤
   │    · 概览           │  │  ┌─ page-panel:套餐列表 ───────────────────────────┐ │
   │  ── 资源管理 ──     │  │  │  页面标题 + 页面说明                             │ │
   │    · 套餐管理 [运营] │  │  │  筛选栏 → 表格 → 分页                           │ │
   │    · 充值管理 [运营] │  │  │  统计卡片 → 内容区 → 抽屉详情                   │ │
   │    · Key管理  [运营] │  │  ├─ page-panel:充值列表 ──────────────────────────┤ │
   │  ── 订单与计费 ──   │  │  ├─ page-panel:Key管理 ───────────────────────────┤ │
   │    · 订单管理 [财务] │  │  ├─ page-panel:余额总览 ──────────────────────────┤ │
   │  ── 统计与日志 ──   │  │  └─ (所有页面都在这里，点击侧栏菜单切换显示)       │ │
   │    · 用量统计       │  │                                                    │ │
   │  ── 系统 ──         │  └────────────────────────────────────────────────────┘ │
   │    · 系统配置 [管理] │  └────────────────────────────────────────────────────┘ │
   └──────────────────────┘                                                        │
   ```

   - 每个 `<div id="panel-xxx" class="page-panel">` 包含一个完整页面的内容
   - 默认只显示第一个 panel，其余 `display:none`
   - 点击侧栏菜单项 → `showPanel('xxx')` → 隐藏所有 panel，显示目标 panel，高亮菜单项

   **角色视图差异实现**：
   - 侧栏菜单项旁标注角色可见性（如 `[运营+]` `[财务+]` `[管理+]` `[系统+]`）
   - 如果差异仅在菜单项增减：在入口文件中用 `<span class="role-tag">` 标注即可，所有 panel 都包含
   - 如果差异在页面内容（按钮、字段不同）：为差异角色单独生成入口文件（如 `index-财务人员.html` 仅有财务确认视角的充值审批、退款审批）

   **原型要求**：
   - 单文件，内联 CSS + 内联 JavaScript，**不依赖 Tailwind CDN 或任何外部样式框架**
   - CSS 变量体系 + 内联 `<style>` 定义所有组件样式（参考 `references/prototype-style-reference.html`）
   - `<style>` 块中设置 `body{font-family:-apple-system,"PingFang SC","Microsoft YaHei","Segoe UI",Arial,sans-serif}`
   - 管理后台入口：深色侧栏 + 白色顶部 header + 面包屑导航 + 主区域内容
   - 外部门户入口：顶部导航栏（非侧栏），突出角色身份和关键操作

   **🟢 视觉规范（必须严格遵守）**——以下 CSS 变量和组件类名是硬性标准，不允许自由发挥替代。完整 CSS 定义见 `references/prototype-style-reference.html`（约920行，含完整组件样式+交互JS+示例数据绑定），生成时必须从该文件复制 `:root` 变量和所有组件 CSS 规则。下文列出的是关键摘要，供执行参考；如 reference 文件有更新，以 reference 为准。

   ### CSS 变量体系（`:root` 必须定义）

   ```css
   :root{
     --primary:#1e6fff;
     --primary-hover:#4080ff;
     --primary-light:#e8f1ff;
     --success:#16a34a;
     --warning:#f59e0b;
     --danger:#ef4444;
     --text:#1f2937;
     --text-sub:#6b7280;
     --text-mute:#9ca3af;
     --border:#e5e7eb;
     --border-light:#f3f4f6;
     --bg:#f5f7fa;
     --bg-card:#ffffff;
     --header-h:56px;
     --side-w:220px;
   }
   ```

   所有颜色、间距、尺寸必须使用变量引用，不得硬编码数值。

   ### 整体布局

   **管理后台**：`.layout` flex 容器 → `.sidebar`（固定定位，深色海军蓝 `#001a3a`）+ `.main`（`flex:1; margin-left:var(--side-w)`）→ `.header`（sticky 白色顶栏）+ `.content`（`padding:16px 24px 32px`）

   ```html
   <div class="layout">
     <aside class="sidebar">...</aside>
     <div class="main">
       <header class="header">面包屑 + 用户区</header>
       <main class="content">页面内容</main>
     </div>
   </div>
   ```

   **外部门户**：无侧栏，顶部导航栏 + 居中主区域

   - 客户门户顶部：`<nav style="background:#1e6fff;color:#fff;padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,0.1)">`，主区域 `<main style="max-width:720px;margin:0 auto;padding:24px">`
   - 代理商门户顶部：`<nav style="background:#f97316;color:#fff;padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,0.1)">`，主区域 `<main style="max-width:720px;margin:0 auto;padding:24px">`

   ### 侧栏（管理后台）

   - 侧栏容器：深色背景 `#001a3a`，固定定位 `position:fixed;top:0;left:0;bottom:0;width:var(--side-w)`
   - Logo 区：`.sidebar-logo` 高度 `var(--header-h)`，白色文字，含 `.dot` 图标方块（`background:var(--primary);border-radius:6px`）
   - 菜单分组：`.menu-group-title` 小号灰色标题（`font-size:12px;color:#64748b`），分隔不同功能区域
   - 菜单项默认：`.menu-item` `padding:10px 20px;color:#cbd5e1;border-left:3px solid transparent`，含 `.icon` 18px 图标
   - 菜单项选中：`.menu-item.active` `background:rgba(30,111,255,0.15);color:#fff;border-left-color:var(--primary)`
   - 角色可见性标注：菜单名后 `<span class="role-tag">[运营]</span>`（`font-size:11px;color:#64748b;margin-left:auto`）

   ### 顶部 Header（管理后台）

   - 白色顶栏：`.header` `height:var(--header-h);background:#fff;border-bottom:1px solid var(--border);position:sticky;top:0`
   - 面包屑：`.crumbs` `color:var(--text-sub);font-size:13px`，`.sep` 分隔符，`.current` 当前页名加粗
   - 用户区：`.user-area` 右侧显示当前角色 + `.avatar` 圆形头像（`background:var(--primary-light);color:var(--primary)`）

   ### 统计卡片

   - 容器网格：`.stats` `display:grid;grid-template-columns:repeat(4,1fr);gap:14px`
   - 单卡片：`.stat` 白色圆角边框卡片，`padding:18px 20px`，`position:relative`
   - 标签：`.stat .label` `color:var(--text-sub);font-size:13px`
   - 数值：`.stat .value` `font-size:24px;font-weight:600;color:var(--text)`，`.unit` 单位小号灰色
   - 趋势文字：`.stat .extra` `font-size:12px`，`.up` 绿色 `var(--success)`，`.down` 红色 `var(--danger)`
   - 图标徽章：`.stat-icon` 绝对定位右上角，`width:36px;height:36px;border-radius:8px;background:var(--primary-light);color:var(--primary)`，18px emoji/字符图标

   ### 内容区块 / 卡片

   - 区块容器：`.card` `background:var(--bg-card);border:1px solid var(--border);border-radius:8px;margin-bottom:14px`
   - 区块内容：`.card-body` `padding:16px 20px`

   ### 筛选栏

   - 容器：`.filter` `display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px 16px`
   - 字段：`.field label` 12px 灰色标签 + `input/select` 34px 高度、6px 圆角、`border:1px solid var(--border)`
   - 操作区：`.filter-actions` 放在网格最后一列，`display:flex;gap:8px;align-items:flex-end`

   ### 表格

   - 表头行：`thead th` `background:#f9fafb;color:var(--text-sub);font-weight:500;padding:12px 14px;border-bottom:1px solid var(--border);position:sticky;top:0`
   - 数据行：`tbody td` `padding:12px 14px;border-bottom:1px solid var(--border-light)`
   - 行悬停：`tbody tr:hover{background:#fafbfc}`

   ### 状态标签（Tag）

   6 种颜色变体，圆角 4px，12px 字号：

   | 类名 | 背景色 | 文字色 | 适用状态 |
   |------|--------|--------|----------|
   | `.tag-green` | `#e8f7ee` | `#16a34a` | 生效中/活跃/正常/已通过 |
   | `.tag-orange` | `#fff4e0` | `#d97706` | 预警/待审批/付费/部分完成 |
   | `.tag-red` | `#fde8e8` | `#ef4444` | 已耗尽/已拒绝/异常/一级预警 |
   | `.tag-blue` | `#e8f1ff` | `#1e6fff` | 信息/套餐/文本类型 |
   | `.tag-gray` | `#f1f3f5` | `#6b7280` | 已过期/已取消/未激活 |
   | `.tag-purple` | `#f1e8ff` | `#7a3edb` | 特殊标注/内部标识 |

   使用方式：`<span class="tag tag-green">生效中</span>`

   ### 进度条

   - 容器：`.progress` `width:100px;height:6px;background:#eef2f7;border-radius:3px`
   - 填充：`<i style="width:67.9%"></i>` `height:100%;background:var(--primary)`
   - 警告态：`.progress.warn` 填充色 `var(--warning)`
   - 危险态：`.progress.danger` 填充色 `var(--danger)`
   - 配合文字：`.progress-text` `color:var(--text-sub);font-size:12px`

   使用方式：`<div class="progress warn"><i style="width:67.9%"></i></div><span class="progress-text">67.9%</span>`

   ### 按钮

   | 类名 | 样式 | 适用场景 |
   |------|------|----------|
   | `.btn` | 白底边框 34px 高 6px 圆角 | 默认/次操作 |
   | `.btn-primary` | `var(--primary)` 蓝底白字 | 主操作（管理后台） |
   | `.btn-primary.btn-orange` | 需额外定义 `background:#f97316` | 主操作（代理商门户） |
   | `.btn-link` | 透明背景 `var(--primary)` 蓝字 | 表格内操作/文字链接 |

   按钮放内容区块右上方：与标题同一行 `.page-head` 用 `display:flex;align-items:flex-end;justify-content:space-between` 排列

   ### 抽屉（Drawer，替代弹窗/模态框）

   **数据详情页必须使用抽屉而非居中弹窗**——右侧 720px 滑入面板，更适合展示列表行的详细数据。

   - 遮罩：`.drawer-mask` `position:fixed;inset:0;background:rgba(15,23,42,0.45);opacity:0;pointer-events:none;transition:opacity .2s;z-index:99`
   - 遮罩打开：`.drawer-mask.open` `opacity:1;pointer-events:auto`
   - 抽屉体：`.drawer` `position:fixed;top:0;right:0;bottom:0;width:720px;max-width:90vw;background:#fff;transform:translateX(100%);transition:transform .25s;z-index:100;display:flex;flex-direction:column`
   - 抽屉打开：`.drawer.open` `transform:translateX(0)`
   - 抽屉头：`.drawer-head` `padding:16px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between`
   - 抽屉标题：`.drawer-title` `font-size:16px;font-weight:600`
   - 抽屉关闭按钮：`.drawer-close` 28px 圆角方块，hover 时红色
   - 抽屉内容：`.drawer-body` `padding:16px 20px;overflow:auto;flex:1`
   - 抽屉分区：`.drawer-section` `margin-bottom:18px`，内含 `.drawer-section h4` 分区标题
   - 描述网格：`.desc-grid` `display:grid;grid-template-columns:repeat(2,1fr);gap:10px 24px`
   - 描述行：`.desc-grid .row .k`（key，88px 固定宽度，`var(--text-sub)`）+ `.desc-grid .row .v`（value，`var(--text)`）

   **简单确认操作**（如"是否确认删除"）仍可使用居中弹窗，但数据详情一律使用抽屉。

   ### Tab 切换

   - 容器：`.tabs` `display:flex;gap:4px;background:#fff;border:1px solid var(--border);border-radius:8px;padding:4px;width:fit-content`
   - Tab 按钮：`.tab` `padding:7px 18px;border-radius:6px;color:var(--text-sub)`
   - Tab 选中：`.tab.active` `background:var(--primary);color:#fff`
   - Tab 内容区：`.tab-pane` 默认 `display:none`，选中 `.tab-pane.active` `display:block`

   **不再使用下划线式 Tab（`border-b-2`），一律使用圆角胶囊 Tab。**

   ### 分页器

   - 容器：`.pager` `display:flex;align-items:center;justify-content:space-between;padding:12px 4px 4px`
   - 信息：`.pager .info` `color:var(--text-sub);font-size:13px`
   - 页码按钮：`.pg` 30px 高、6px 圆角、1px 边框
   - 选中页码：`.pg.active` `background:var(--primary);border-color:var(--primary);color:#fff`

   ### 页面标题区

   - `.page-head` `display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:14px`
   - `.page-title` `font-size:20px;font-weight:600`
   - `.page-sub` `color:var(--text-sub);font-size:13px;margin-top:4px`

   ### 说明提示

   - 管理后台：`<div class="mt-6" style="background:var(--primary-light);border:1px solid var(--border);border-radius:8px;padding:16px 20px;font-size:14px;color:var(--primary)"><strong>说明：</strong>...</div>`
   - 代理商门户：`<div class="mt-6" style="background:#fff4e0;border:1px solid #f5d28e;border-radius:8px;padding:16px 20px;font-size:14px;color:#d97706">...</div>`
   - 客户门户：同管理后台蓝色样式

   **🟢 交互 JavaScript（必须）**——所有入口文件必须可交互，不是纯静态页面：

   1. **页面切换（核心）**：侧栏菜单 / 顶部导航点击时，切换主区域内容。管理后台用 `showPanel(id)` 函数隐藏所有 `.page-panel`，显示目标 panel，toggle `.active` class 高亮菜单项。外部门户用同样的逻辑切换内容区。

   2. **Tab 切换**：页面中有多个 Tab 页时，必须实现点击切换——toggle `.active` class on `.tab` 和 `.tab-pane`。

   3. **抽屉打开/关闭**：表格行"查看明细"按钮打开右侧抽屉面板，显示行数据详情。toggle `.open` class on `.drawer` 和 `.drawer-mask`，CSS transition 驱动滑入动画。点击遮罩层或关闭按钮关闭抽屉。

   4. **弹窗打开/关闭**（简单确认操作）：toggle `display:flex / display:none` on 弹窗遮罩，点击遮罩层关闭。

   5. **表单提交反馈**：点击"提交"按钮后显示 Toast 提示（`<div class="toast">提交成功</div>`，3秒后自动消失），不需要真实后端逻辑。

   6. **下拉联动**（如果规格中有联动逻辑）：选择套餐后自动计算金额/折扣价/佣金，用 JS 函数模拟。

   **交互实现方式**：
   - 在 `<body>` 末尾加 `<script>` 块，内联所有交互逻辑
   - 使用原生 JavaScript（不引入额外框架）
   - 所有切换通过 CSS class toggle（`.active` / `.open`）驱动，不通过 `style.display` 直接控制（抽屉除外）
   - 页面切换核心函数示例：
     ```js
     function showPanel(panelId) {
       document.querySelectorAll('.page-panel').forEach(p => p.style.display = 'none');
       document.getElementById(panelId).style.display = 'block';
       document.querySelectorAll('.menu-item').forEach(n => n.classList.remove('active'));
       document.querySelector(`[data-panel="${panelId}"]`).classList.add('active');
     }
     ```
   - Tab 切换：
     ```js
     document.querySelectorAll('.tab').forEach(t => {
       t.addEventListener('click', () => {
         document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
         document.querySelectorAll('.tab-pane').forEach(x => x.classList.remove('active'));
         t.classList.add('active');
         document.querySelector(`.tab-pane[data-pane="${t.dataset.tab}"]`).classList.add('active');
       });
     });
     ```
   - 抽屉：
     ```js
     function openDrawer(dataKey) {
       // 填充抽屉内容...
       document.getElementById('drawer').classList.add('open');
       document.getElementById('drawerMask').classList.add('open');
     }
     function closeDrawer() {
       document.getElementById('drawer').classList.remove('open');
       document.getElementById('drawerMask').classList.remove('open');
     }
     ```
   - Toast：
     ```js
     function showToast(msg) {
       const t = document.getElementById('toast');
       t.textContent = msg;
       t.style.display = 'block';
       setTimeout(() => t.style.display = 'none', 3000);
     }
     ```
   - 不需要真实数据交互，只需要 UI 层面的可点击、可切换体验

   **入口文件数量 = 角色视图数（合并后）**
   - 通常 2~5 个入口文件（管理后台合并 1~3 个 + 外部门户各 1 个）
   - 具体数量取决于角色间差异程度

---

## 并行生成 HTML 原型

使用 **parallel Agent** 为每个角色视图入口同时生成 HTML 原型：
- 每个角色视图入口一个 Agent（如 `index-管理员.html`、`index-客户.html`）
- 每个 Agent 接收该角色可见的所有页面规格 + 角色视图信息 + CSS 变量视觉规范 + 交互要求作为输入
- Agent 必须先读取 `references/prototype-style-reference.html`，从该文件复制 `:root` CSS 变量定义和所有组件 CSS 规则到入口文件的 `<style>` 块中，在此基础上扩展该角色的页面内容
- Agent 将该角色的所有页面合并到一个入口文件中，实现页面切换和交互
- 所有 HTML 文件写入 `09-html-prototype/` 目录

---

## 贪量门禁

### 第一层：步骤完整性门禁

检查：

- 每个选定页面是否覆盖 12 个规格要素
- 角色视图分区表是否覆盖所有 PRD 角色
- 入口文件数量是否覆盖所有角色视图（内部角色合并后 + 外部门户各一个）
- 每个入口文件是否包含该角色可见的所有页面内容（`page-panel` 切换机制）
- 外部角色（如有）是否有独立的门户入口文件
- 每个入口文件是否使用 CSS 变量体系（`:root` 定义 + 组件类名），而非 Tailwind CDN
- 每个管理后台入口是否使用深色侧栏布局（`#001a3a` 背景 + 分组菜单 + 面包屑顶栏）
- 每个入口文件是否包含交互 JavaScript（页面切换、Tab切换、抽屉/弹窗、按钮响应）
- 在浏览器中打开任意入口文件，验证：侧栏/导航切换页面、Tab 可切换、抽屉可打开/关闭、按钮有响应
- 缺失 ≥ 3 个要素回到本步补充

### 第二层：外部大模型评审

内部门禁通过后，触发外部大模型评审（详见 `steps/external-review.md`）：

- 评审维度：页面规格要素完整性、角色视图覆盖度、布局描述可理解性、字段和按钮定义准确性
- 通过标准：总分 ≥ 75 且无严重问题
- 不通过：根据评审意见补充页面规格，最多重试 3 轮
- 评审结果记录到 `14-review-log.md`

### 第三层：人类QA确认门

外部评审通过后（或⚠️通过但需关注），**必须暂停等待人类确认**才能进入 Step 9。

使用 `AskUserQuestion` 向用户展示本步骤产物摘要和评审发现的问题：

```json
{
  "questions": [
    {
      "header": "QA确认",
      "question": "Step 8 页面原型已完成，三层质量检查结果如下：\n\n**内部门禁**: ✅通过 / ⚠️基本通过（缺失X项）\n**一致性检查**: ✅通过 / 🔴阻塞级不一致 / 🟡有差异需关注\n**外部评审**: ✅通过 / ⚠️通过但需关注 / ❌不通过\n\n**产物关键摘要**:\n- <3-5条：页面总数、角色视图分区概要、核心页面功能概要>\n\n**外部评审发现的问题**:\n- 🔴 <严重问题：如操作流程不合理、字段遗漏关键校验>\n- 🟡 <需关注问题：如筛选条件不够实用、布局认知负担重>\n- 💡 <优化建议>\n\n**特别提醒**：请在浏览器中打开 09-html-prototype/ 中的 HTML 文件，实际体验原型交互后再做判断。\n\n请确认是否可以进入下一步？",
      "multiSelect": false,
      "options": [
        {
          "label": "✅ 确认通过，进入 Step 9",
          "description": "产物质量可接受，原型交互体验符合预期"
        },
        {
          "label": "🔧 需要修改，指出调整内容",
          "description": "原型交互或页面规格存在问题，请在'Other'中说明需要调整什么"
        }
      ]
    }
  ]
}
```

- 用户选择"确认通过" → 记录确认结果到 `14-review-log.md`，进入 Step 9
- 用户选择"需要修改" → 根据用户反馈修改 `08-page-spec.md` 和对应 HTML 原型，重新执行内部门禁+外部评审+人类确认（不重算重试轮次，人类确认不算在3轮重试内）
- 用户未回应时 → **不能自动进入下一步**，必须等待

外部评审通过后，才能触发人类QA确认。
