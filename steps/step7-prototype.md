# Step 7: 页面原型 (prototype)

读取页面规格模板（按行业/全局两级覆盖查找）：
- 命中行业时 `presets/<industry>/page-spec.md`
- 否则 `templates/page-spec.md`

读取 `04-prd.md` 和 `05-flow.md` 获取功能、流程和依赖信息。

只对选定优先级的功能生成详细页面规格和 HTML 原型。

生成 `06-prototype.md`（页面规格文档）。

---

## 🚨 设计硬性约束（违反必须重做，不允许"先这样"）

> **本章节是 Step 9 最高优先级规则**，任何"内部门禁通过 + 外部评审通过 + 人类确认"的组合都不能豁免本章约束。
> 内部门禁 checklist 必须逐条核验本章所有条款。

### 1. 公共框架强制约束（每个原型页必须有）

> **这是最常被忽略的"风格统一"问题**。所有原型页**必须**使用统一的公共框架，否则会出现"有的页面有侧边栏、有的没有"等视觉割裂。

**强制结构**（body 内必须包含）：
```html
<body>
  <div class="layout">
    <aside class="sidebar">                ← 必须
      <div class="sidebar-logo">...</div>
      <nav class="menu">                   ← 必须
        <div class="menu-group-title">工作台</div>
        <div class="menu-item"><span class="icon">▦</span>概览</div>
        <div class="menu-item active"><span class="icon">▣</span>设备接入</div>  ← 当前页 active
        ...
      </nav>
    </aside>
    <div class="main">
      <header class="header">              ← 必须
        <div class="crumbs">系统管理<span class="sep">/</span>角色管理</div>
        <div class="user-area">            ← 必须
          <span>🔔 3</span>
          <div class="avatar">A</div>
          <span>admin</span>
        </div>
      </header>
      <main class="content">
        <div class="page-head">            ← 必须
          <div>
            <div class="page-title">主标题</div>
            <div class="page-sub">副标题</div>
          </div>
          <div class="page-actions">       ← 至少 1 个 .btn-primary
            <button class="btn">次要操作</button>
            <button class="btn btn-primary">主要操作</button>
          </div>
        </div>
        <!-- 原内容 -->
      </main>
    </div>
  </div>
</body>
```

**绝对禁止**：
- ❌ 没有 `<aside class="sidebar">` 整个侧边栏
- ❌ 用 `<h2>` 代替 `<div class="page-title">`
- ❌ 没有 `<header class="header">` 顶部栏
- ❌ 没有 `<div class="user-area">` 用户区
- ❌ 没有 `<div class="page-actions">` 操作按钮

**反例**（典型"风格不统一"页面）：
```html
❌ <body>
   <h2>👥 角色管理</h2>
   <div class="card">...</div>            ← 没有 sidebar / header / page-head
   </body>
```

### 2. 侧边栏信息架构约束（最常被违反）

- **菜单分组 ≤ 6 个**
- **菜单项 ≤ 25 个**（包括"概览""API 文档"等所有项）
- **未列入侧边栏的页面**：通过顶部面包屑、表格行按钮、首页入口等二级入口访问
- **图标风格统一**：一律使用方块字符（▦▣▤▥▧▨▩▪▫◌◍◎●☰⚙⌂），**禁用 Emoji**（🛸🚶📱📷🛡 等）
- **菜单文字**：2-4 个中文字，不超过 6 个字（如"策略列表""用户组织"）

**反例**（必须避免）：
```
❌ 10 个分组 + 50 个菜单项（视频管理 8 项 + AI 智能 6 项 + 高可用 4 项 + 配置管理 6 项 + 协议扩展 4 项 + 视频增强 4 项 + 智能回放 4 项 + 安全管理 6 项 + 移动应用 4 项 + 系统设置 4 项）
❌ 侧边栏使用 🛸🚶📱📷🛡📈🖥🔐🏢📨🌐 等 Emoji
```

**正例**（标准侧边栏 ≤ 25 项）：
```
✅ 6~8 个分组 + 23 个菜单项
✅ 图标统一 ▦▣▤▥▧▨▩▪▫◌◍◎●☰⚙⌂
```

### 3. 页面结构标准模板（每个核心页必须包含）

```
[ 顶部 Header：面包屑 + 用户区 ]
[ page-head：标题 + 副标题 + 右侧操作区 ]
[ 4 个统计卡 .stats（每个带 .stat-icon）]                ← 表格页必须有
[ 筛选条 .filter（5 列 .field + filter-actions）]        ← 表格页必须有
  或
[ Tabs .tabs（≥ 3 个子视图）]                            ← 复杂页必须有
[ 主内容：.card → .table-wrap → .pager ]                ← 表格页三段式
[ 末尾：业务特殊组件（.diag / .topo / .perm / .phone）]   ← 按页面性质选
```

**硬性规则**：
- 每个 `.stat` **必须**有 `.stat-icon`（绝对定位右上角，36×36 圆角 8px）
- 表格页**必须**有 `.filter` 筛选条（即使查询字段少也要占位 5 列）
- 复杂页（≥ 3 个子视图）**必须**用 `.tabs` 拆分（不允许一屏堆叠）
- 表格列数 ≥ 5 **必须**给关键列加 `.sortable` + `.arrow`（ID / 时间 / 数值 / 状态）

### 4. 三大组件强制使用规则

| 组件 | 适用页面 | 强制要求 |
|------|----------|----------|
| **`.filter` 筛选条** | 所有表格页 | 5 列 `.field` + 末列 `.filter-actions`（查询/重置按钮），即使数据少也要占位 |
| **`.tabs` 标签页** | 含 ≥ 3 个子视图的复杂页 | 必须 ≥ 3 个 tab（否则视为简单页，禁用 tabs 强行拆分） |
| **`.sortable` 排序** | 列数 ≥ 5 的表格 | 关键列（ID/时间/数值/状态）必须加 `class="sortable"` + `<span class="arrow">↓</span>` |

### 5. 脚本引用约束（最常被遗漏，导致 tab 切换失灵）

- **所有原型页必须在 `<head>` 引用 `common.js`**，紧跟 `common.css` 之后：
  ```html
  <link rel="stylesheet" href="common.css">
  <script src="common.js"></script>
  ```
- `common.js` 已统一实现：tab 切换 / 协议标签单选 / 抽屉开关 / 表格排序箭头 / Toast 提示
- **禁止**每个页面内联重复的 tab 切换脚本（会造成 50 份相同 JS 散落各处）
- **禁止**漏掉 `common.js` 引用（漏掉后 tab 点击无反应、protocol 标签不能切换、drawer 打不开）
- 唯一例外：`index.html` / `login.html` / 自包含的 demo 页面可以不引用

**正例**（强制使用 filter）：
```html
<div class="card">
  <div class="card-body">
    <div class="filter">
      <div class="field"><label>报告 ID</label><input placeholder="QD-001"></div>
      <div class="field"><label>设备</label><input placeholder="搜索设备名称"></div>
      <div class="field"><label>异常类型</label><select>...</select></div>
      <div class="field"><label>严重程度</label><select>...</select></div>
      <div class="filter-actions">
        <button class="btn btn-primary">查询</button>
        <button class="btn">重置</button>
      </div>
    </div>
  </div>
</div>
```

**正例**（强制使用 tabs）：
```html
<div class="tabs">
  <div class="tab active" data-tab="items">检测项</div>
  <div class="tab" data-tab="report">诊断报告</div>
  <div class="tab" data-tab="stats">诊断统计</div>
  <div class="tab" data-tab="config">诊断策略</div>
</div>
<section class="tab-pane active" data-pane="items">...</section>
<section class="tab-pane" data-pane="report">...</section>
<section class="tab-pane" data-pane="stats">...</section>
<section class="tab-pane" data-pane="config">...</section>
```

**正例**（强制使用 sortable）：
```html
<thead>
  <tr>
    <th>报告 ID</th>
    <th>设备</th>
    <th>异常类型</th>
    <th class="sortable sorted">评分 <span class="arrow">↓</span></th>  ← 强制
    <th>快照</th>
    <th>发生时间</th>
    <th>状态</th>
    <th>操作</th>
  </tr>
</thead>
```

### 6. 业务组件标准库（必须复用，不允许自由发挥）

> 所有业务特殊组件**必须**使用以下标准类名（CSS 变量见下方 `:root`）。
> **禁止**自创类名（如 `.my-diag`、`.face-grid`、`.custom-topo` 等），避免风格漂移。

| 业务场景 | 强制类名 | 用途与结构 |
|----------|----------|-----------|
| 视频质量诊断 6 类检测项 | `.diag` | 6 网格图标+名称+准确率+本月次数 |
| 容灾备份拓扑 | `.topo` | 双中心+主备节点关系图（含连线动画） |
| RBAC 权限矩阵 | `.perm` | 角色 × 模块 × 操作 三维网格（行=角色，列=模块） |
| 手机 H5 预览 | `.phone` | iPhone 14 Pro 框架 393×852，居中显示 |
| 人脸库/车辆库 | `.lib` | 缩略图网格+名称+数量统计 |
| 视频窗口 | `.grid-2 / .grid-3 / .grid-4` | 2×2 / 3×3 / 4×4 视频窗口 |
| 鹰眼/缩略图 | `.mini-map` | 右下角小地图（300×200） |
| 时序数据/统计图 | `.chart-card` + `.chart-grid` | 1×1 / 1×2 图表卡片 |
| 协议选择 | `.protocol` | 6+ 协议标签 + 说明 |
| 时间段选择 | `.period-tabs` | 7 天 / 30 天 / 90 天切换 |
| 描述网格（详情用） | `.desc-grid` | 2 列 key-value 描述 |

**正例**（标准 .diag 写法）：
```html
<div class="diag">
  <div>
    <div class="diag-icon">❄</div>
    <strong>雪花</strong>
    <div class="text-sub text-sm" style="margin-top:6px">准确率 <span style="color:var(--success)">92%</span></div>
    <div class="text-mute text-sm" style="margin-top:2px">本月 1,256 次</div>
  </div>
  <!-- 重复 6 次 -->
</div>
```

### 7. 图标风格统一规范

| 类别 | 字符集 | 用途示例 |
|------|--------|----------|
| 业务图标 | ▦▣▤▥▧▨▩▪▫◌◍◎● | 数据/列表/资源/网格 |
| 状态图标 | ⌂▦▧▨▩ | 工作台/统计/模块 |
| 操作图标 | ▶▸▹▷▫ | 详情/编辑/播放 |
| 通用图标 | ⚙ ⌂ ➡ | 设置/工作台/转发 |
| **禁用** | 🛸🚶📱📷🛡📈🖥🔐🏢📨🌐 | Emoji 全部禁用 |

**业务内允许少量功能性 Emoji**（仅限以下场景）：
- 铃铛 🔔：在 `.user-area` 显示通知数
- 雪人 ❄ / 太阳 ☀：在 `.diag` 6 类检测项中表达具体含义

### 8. 页面顶部右侧操作区规范

| 内容类型 | 强制类名 | 示例 |
|----------|----------|------|
| 单按钮 | 直接 `<button>`，不包 div | `<button class="btn btn-primary">+ 新建策略</button>` |
| 多按钮 | `<div class="page-actions">` 包裹 | `<div class="page-actions"><button>...</button><button>...</button></div>` |
| 描述性信息 | `<div class="next-reset">` 或 `<div class="page-actions text-sub">` | `<div class="next-reset">下次重置：<b>2026-06-22</b></div>` |

**反例**（禁止）：
```html
❌ <div class="flex gap-8">
     <button class="btn btn-primary">+ 新建</button>
     <button class="btn">📊 统计</button>
     <button class="btn">📈 监控</button>
   </div>
```

**正例**（规范）：
```html
✅ <div class="page-actions">
     <button class="btn btn-primary">+ 新建</button>
     <button class="btn">📊 统计</button>
     <button class="btn">📈 监控</button>
   </div>
```

---

## 🚨 反模式清单（出现必须重做）

| # | 反模式 | 严重度 |
|---|--------|--------|
| 1 | 侧边栏菜单项超过 25 个 | 🔴 阻塞 |
| 2 | 侧边栏使用 Emoji 图标（🛸🚶📱📷🛡 等） | 🔴 阻塞 |
| 3 | 表格页缺少 `.filter` 筛选条 | 🔴 阻塞 |
| 4 | 复杂页（≥ 3 子视图）没有 `.tabs` 拆分 | 🔴 阻塞 |
| 5 | 表格列 ≥ 5 但无 `.sortable` 排序 | 🔴 阻塞 |
| 6 | 统计卡 `.stat` 缺少 `.stat-icon` | 🟡 警告 |
| 7 | 页面顶部右侧用 `<div class="flex gap-8">` 自创容器 | 🟡 警告 |
| 8 | 业务组件自创类名（如 `.my-diag`、`.face-grid`、`.custom-topo`） | 🔴 阻塞 |
| 9 | 50 个 panel 挤一个 HTML 入口文件（除外部入口外） | 🔴 阻塞 |
| 10 | 使用 Tailwind CDN / Element Plus / Element UI 等外部框架 | 🔴 阻塞 |
| 11 | 内联 `<style>` 缺失 `:root` CSS 变量体系 | 🔴 阻塞 |
| 12 | 表格 `<th>` 缺少 `position:sticky` 视觉（应在 common.css 强制） | 🟡 警告 |
| 13 | **页面未引用 `common.js`**（tab 切换、protocol 标签、drawer、sortable 全部失灵） | 🔴 阻塞 |
| 14 | **按钮点击无反应**（`<button>` 无 `onclick` 且无 `type=submit`，点击不触发任何 JS/跳转/Toast） | 🔴 阻塞 |
| 15 | **链接无 href**（菜单项、面包屑、表格行链接用 `<div>`/`<span>` 模拟，或 `<a>` 缺 `href`） | 🔴 阻塞 |
| 16 | **菜单点击不跳转**（侧边栏菜单项点击不切换页面/不激活当前项） | 🔴 阻塞 |
| 17 | **tab/抽屉/弹窗/筛选/排序 5 种核心交互未全部实现** | 🔴 阻塞 |
| 18 | **页面缺少真实导航入口**（当前页面无法从首页/侧边栏/其他页面跳入） | 🔴 阻塞 |

---

## 原型组织方式：核心页独立 HTML + 详情用抽屉

**🚨 升级说明**：原"50 panel 挤一个 HTML"是反模式，已废弃。

**新规则**：
- **核心页面独立 HTML**：每个 P0/P1 页面单独一个 HTML 文件（`xxx.html`）
- **详情/编辑/创建用抽屉**：通过 `.drawer` 右侧滑入（720px 宽），不切换页面
- **不生成 50 panel 的"超级 HTML"**：维护成本高、加载慢、调试困难
- **同主题页面可聚合**：如"策略中心"可拆为 `policy-record.html` / `policy-storage.html` / `policy-ptz.html` 等子页，菜单只放"策略列表"作为聚合入口

**外部入口文件**（如客户门户、代理商门户）：仍然按角色合并为单文件（`index-客户.html`），但其内部子页面通过抽屉或弹层切换，不堆 panel。

**内部管理后台的侧边栏标准结构**（23 项模板，可按需调整）：

```
工作台（2）
  概览 / 电子地图
视频接入（3）
  设备接入 / 资源目录 / 视频播放
视频处理（3）
  录像文件 / 流转发 / 级联管理
策略中心（2）
  策略列表 / 审批中心
AI 与高可用（5）
  视频质量诊断 / 人脸识别 / 车辆识别 / 行为分析 / 容灾备份
系统管理（8）
  租户管理 / 角色管理 / 用户组织 / 系统配置 / 安全管理 / API 文档
  （根据实际模块增减，限 ≤ 8 项）
```

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

   创建 `specs/<序号-功能名>/06-html-prototype/` 目录。

   **🟢 页面文件命名**：

   - **核心页面**：`xxx.html`（如 `device-access.html`、`forward.html`、`ai-quality.html`）
   - **聚合入口**：`index-角色.html`（仅外部角色门户需要；内部管理后台无需聚合）
   - **子页面 / 详情 / 编辑**：通过 `.drawer` 抽屉实现，不单独生成 HTML

---

## 视觉规范（必须严格遵守）

> 以下 CSS 变量和组件类名是硬性标准，不允许自由发挥替代。下方 `:root` 块是唯一权威来源，所有原型必须内联此段；如需扩展组件，请在本节追加。

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
- **强制约束**：菜单项 ≤ 25，分组 ≤ 6，图标用方块字符（参见"设计硬性约束 1"）

### 顶部 Header（管理后台）

- 白色顶栏：`.header` `height:var(--header-h);background:#fff;border-bottom:1px solid var(--border);position:sticky;top:0`
- 面包屑：`.crumbs` `color:var(--text-sub);font-size:13px`，`.sep` 分隔符，`.current` 当前页名加粗
- 用户区：`.user-area` 右侧显示当前角色 + `.avatar` 圆形头像（`background:var(--primary-light);color:var(--primary)`）

### 页面标题区

- `.page-head` `display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:14px`
- `.page-title` `font-size:20px;font-weight:600`
- `.page-sub` `color:var(--text-sub);font-size:13px;margin-top:4px`
- 右侧操作区：单按钮直接 `<button>`；多按钮用 `<div class="page-actions">`；描述性信息用 `<div class="next-reset">`

### 统计卡片

- 容器网格：`.stats` `display:grid;grid-template-columns:repeat(4,1fr);gap:14px`
- 单卡片：`.stat` 白色圆角边框卡片，`padding:18px 20px`，`position:relative`
- 标签：`.stat .label` `color:var(--text-sub);font-size:13px`
- 数值：`.stat .value` `font-size:24px;font-weight:600;color:var(--text)`，`.unit` 单位小号灰色
- 趋势文字：`.stat .extra` `font-size:12px`，`.up` 绿色 `var(--success)`，`.down` 红色 `var(--danger)`
- **图标徽章**（强制）：`.stat-icon` 绝对定位右上角，`width:36px;height:36px;border-radius:8px;background:var(--primary-light);color:var(--primary)`，18px 方块字符图标

### 内容区块 / 卡片

- 区块容器：`.card` `background:var(--bg-card);border:1px solid var(--border);border-radius:8px;margin-bottom:14px`
- 区块内容：`.card-body` `padding:16px 20px`
- 区块头部：`.card-head` `padding:14px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between`
- 区块标题：`.card-head h3` `font-size:15px;font-weight:600`

### 筛选栏（表格页强制）

- 容器：`.filter` `display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px 16px`
- 字段：`.field label` 12px 灰色标签 + `input/select` 34px 高度、6px 圆角、`border:1px solid var(--border)`
- 操作区：`.filter-actions` 放在网格最后一列，`display:flex;gap:8px;align-items:flex-end`

### Tab 切换（复杂页强制）

- 容器：`.tabs` `display:flex;gap:4px;background:#fff;border:1px solid var(--border);border-radius:8px;padding:4px;width:fit-content`
- Tab 按钮：`.tab` `padding:7px 18px;border-radius:6px;color:var(--text-sub)`
- Tab 选中：`.tab.active` `background:var(--primary);color:#fff`
- Tab 内容区：`.tab-pane` 默认 `display:none`，选中 `.tab-pane.active` `display:block`

**不再使用下划线式 Tab（`border-b-2`），一律使用圆角胶囊 Tab。**

### 表格

- 表头行：`thead th` `background:#f9fafb;color:var(--text-sub);font-weight:500;padding:12px 14px;border-bottom:1px solid var(--border);position:sticky;top:0`
- 数据行：`tbody td` `padding:12px 14px;border-bottom:1px solid var(--border-light)`
- 行悬停：`tbody tr:hover{background:#fafbfc}`
- **可排序**（强制）：`<th class="sortable">列名 <span class="arrow">↓</span></th>`，点击后 `<th class="sortable sorted">`

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

---

## 🚨 LLM 生成 HTML 时强制自检 8 项（每次输出前必过）

> **本章节是「主动防御」机制**。即使设计了硬性约束和检查清单，LLM 仍可能在长输出中遗漏关键元素。
> 因此：**每生成一个 HTML 文件后、输出"完成"前，必须按以下 8 项对照一次**，未通过必须当场修复，不要交付"先这样"的版本。

| # | 自检项 | 通过标志 | 不通过的修复 |
|---|--------|----------|--------------|
| 1 | **`common.css` 已引用** | `<link rel="stylesheet" href="common.css">` 在 `<head>` 中 | 立即补上 |
| 2 | **`common.js` 已引用** | `<script src="common.js"></script>` 紧跟 common.css 之后 | 立即补上（缺它则 tab 切换、protocol 标签、drawer、sortable 全部失灵） |
| 3 | **侧边栏菜单项 ≤ 25、图标无 Emoji** | `grep -c "menu-item" < 26` 且没有 🛸🚶📱📷🛡 等字符 | 删减菜单 / 改用方块字符（▦▣▤▥▧▨▩▪▫◌◍◎●☰⚙⌂） |
| 4 | **业务组件用标准类名** | 没有 `.my-diag` `.face-grid` `.custom-topo` 等自创类名 | 改用标准库类名（`.diag` `.lib-cell` `.topo` `.perm` `.protocol` 等） |
| 5 | **表格页有 `.filter` 筛选条** | 含 `<div class="filter">` 且有 5 列 `.field` + `.filter-actions` | 补筛选条 |
| 6 | **复杂页有 `.tabs` ≥ 3 个** | 至少 3 个 `.tab` 配对应数量的 `.tab-pane` | 加 tab，或确认页面不复杂可不用 |
| 7 | **未引入外部框架** | 没有 Tailwind / Element Plus / Element UI / Ant Design CDN | 删除所有 CDN 引用 |
| 8 | **`<style>` 内有 `:root` CSS 变量** | 内联 style 块中包含 `--primary: #1e6fff;` 等变量定义 | 在 style 开头补上 |

**自检失败处理**：
- 自检未通过 → **必须当场修复并重新输出**，不允许写"已知问题，后续优化"等推诿
- 修复后再自检 → 8 项全过 → 才能输出"✅ 页面 X 已生成"

**自检方法（可调用工具验证）**：
```bash
# 1. 验证 common.css / common.js 引用
grep -E "common\.(css|js)" <file>.html

# 2. 验证菜单项数量
grep -c "menu-item" <file>.html  # 应 ≤ 26（25 菜单 + 1 logo）

# 3. 验证没有 Emoji
grep -E "🛸|🚶|📱|📷|🛡|📈|🖥|🔐|🏢|📨|🌐" <file>.html  # 应无输出

# 4. 验证业务组件没有自创类名
grep -E "class=\"(my-|custom-|local-)" <file>.html  # 应无输出

# 5. 验证没有外部框架
grep -E "tailwindcss|element-plus|antd|element-ui" <file>.html  # 应无输出
```

---

## 已知反模式速查（AI 写原型时常犯的错）

> 这一节是「前车之鉴」。每条都来自实际生成中真实出现的 bug。

### 反模式 1：50 个 panel 塞进 1 个 HTML
**症状**：1 个文件 5000+ 行，侧边栏滚动半天找不到菜单
**正解**：每个 P0/P1 页面独立 HTML 文件（`xxx.html`），详情用 `.drawer` 抽屉

### 反模式 2：每个页面都内联一份 tab 切换 JS
**症状**：50 个文件里 50 份相同的 `querySelectorAll('.tab').forEach(...)`
**正解**：所有交互统一在 `common.js`，每个 HTML 只引用一行 `<script src="common.js"></script>`

### 反模式 3：漏掉 common.js 导致 tab 切换失灵
**症状**：页面渲染正常，但点击 tab 没有任何反应
**正解**：必须引用 common.js；自检时 grep `common.js` 验证

### 反模式 4：自创业务组件类名（`.face-grid` `.my-diag`）
**症状**：单个页面看着对，但跨页面风格漂移
**正解**：100% 复用 `common.css` 标准类名（`.diag` `.lib-cell` `.topo` `.perm` `.phone` `.protocol` `.grid-2/3/4` `.chart-card` `.period-tabs` 等）

### 反模式 5：菜单项超过 25 个
**症状**：侧边栏滚动条可见，菜单找起来累
**正解**：菜单 ≤ 25、分组 ≤ 6；其他页面用面包屑、表格按钮、首页入口访问

### 反模式 6：侧边栏用 Emoji 图标
**症状**：跨设备/浏览器显示不一致，部分 Emoji 渲染成方块
**正解**：用方块字符 `▦▣▤▥▧▨▩▪▫◌◍◎●☰⚙⌂` 替代

### 反模式 7：表格页没有筛选条
**症状**：用户想查特定数据但只能翻页
**正解**：表格页必须有 `.filter`（5 列 `.field` + 末列 `.filter-actions`）

### 反模式 8：复杂页不拆 tab 一屏堆叠
**症状**：3+ 个子视图挤一起，页面超长，找不到内容
**正解**：≥ 3 子视图必须 `.tabs` 拆分

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

### 分页器

- 容器：`.pager` `display:flex;align-items:center;justify-content:space-between;padding:12px 4px 4px`
- 信息：`.pager .info` `color:var(--text-sub);font-size:13px`
- 页码按钮：`.pg` 30px 高、6px 圆角、1px 边框
- 选中页码：`.pg.active` `background:var(--primary);border-color:var(--primary);color:#fff`

### 业务特殊组件（必须复用，不允许自由发挥）

| 组件 | 类名 | 用途 |
|------|------|------|
| 视频质量诊断 6 类检测项 | `.diag` | 6 网格图标+名称+准确率+本月次数 |
| 容灾备份拓扑 | `.topo` | 双中心+主备节点关系图 |
| RBAC 权限矩阵 | `.perm` | 角色 × 模块 × 操作 三维网格 |
| 手机 H5 预览 | `.phone` | iPhone 14 Pro 框架 393×852 |
| 人脸库/车辆库 | `.lib` | 缩略图网格+名称+数量 |
| 视频窗口 | `.grid-2/.grid-3/.grid-4` | 2×2 / 3×3 / 4×4 视频窗口 |
| 鹰眼/缩略图 | `.mini-map` | 右下角小地图（300×200） |
| 时序/统计图 | `.chart-card` + `.chart-grid` | 1×1 / 1×2 图表卡片 |
| 协议选择 | `.protocol` | 6+ 协议标签 + 说明 |
| 时间段选择 | `.period-tabs` | 7 天 / 30 天 / 90 天切换 |

### 说明提示

- 管理后台：`<div class="mt-6" style="background:var(--primary-light);border:1px solid var(--border);border-radius:8px;padding:16px 20px;font-size:14px;color:var(--primary)"><strong>说明：</strong>...</div>`
- 代理商门户：`<div class="mt-6" style="background:#fff4e0;border:1px solid #f5d28e;border-radius:8px;padding:16px 20px;font-size:14px;color:#d97706">...</div>`
- 客户门户：同管理后台蓝色样式

---

## 交互 JavaScript（必须）——所有 HTML 文件必须可交互，不是纯静态页面：

1. **Tab 切换**（核心，复杂页必用）：页面中有多个 Tab 页时，必须实现点击切换——toggle `.active` class on `.tab` 和 `.tab-pane`。

2. **抽屉打开/关闭**：表格行"查看明细"按钮打开右侧抽屉面板，显示行数据详情。toggle `.open` class on `.drawer` 和 `.drawer-mask`，CSS transition 驱动滑入动画。点击遮罩层或关闭按钮关闭抽屉。

3. **弹窗打开/关闭**（简单确认操作）：toggle `display:flex / display:none` on 弹窗遮罩，点击遮罩层关闭。

4. **表单提交反馈**：点击"提交"按钮后显示 Toast 提示（`<div class="toast">提交成功</div>`，3秒后自动消失），不需要真实后端逻辑。

5. **下拉联动**（如果规格中有联动逻辑）：选择套餐后自动计算金额/折扣价/佣金，用 JS 函数模拟。

6. **筛选条交互**：点击"查询"按钮后 `console.log` 筛选条件 + 弹出 Toast 提示"已查询 X 条数据"。

7. **表格排序交互**：点击 `th.sortable` 切换 `.sorted` class，箭头方向 ↑/↓ 切换。

**交互实现方式**：
- **必须引用 `common.js`**（与 `common.css` 并列），所有 tab/protocol/drawer/sortable 逻辑都在 common.js 统一实现
- 禁止每个页面内联相同的 tab 切换脚本（参考硬性约束 4）
- 页面专属交互（页面级业务逻辑）才在 `<body>` 末尾加 `<script>` 块
- 使用原生 JavaScript（不引入额外框架）
- 所有切换通过 CSS class toggle（`.active` / `.open`）驱动，不通过 `style.display` 直接控制（抽屉除外）

**Tab 切换标准实现**：
```js
document.querySelectorAll('.tab').forEach(t => {
  t.addEventListener('click', () => {
    const key = t.dataset.tab;
    document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(x => x.classList.remove('active'));
    t.classList.add('active');
    document.querySelector(`[data-pane="${key}"]`).classList.add('active');
  });
});
```

**抽屉标准实现**：
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
document.getElementById('drawerMask').addEventListener('click', closeDrawer);
```

**Toast 标准实现**：
```js
function showToast(msg) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  t.style.display = 'block';
  setTimeout(() => t.remove(), 3000);
}
```

**排序交互标准实现**：
```js
document.querySelectorAll('th.sortable').forEach(th => {
  th.addEventListener('click', () => {
    document.querySelectorAll('th.sortable').forEach(x => x.classList.remove('sorted'));
    th.classList.add('sorted');
  });
});
```

---

## Step 9 内部门禁 Checklist（升级版）

完成 HTML 原型后，**必须**逐条核验：

| 类别 | 检查项 | 阻塞/警告 |
|------|--------|-----------|
| **信息架构** | 侧边栏菜单项 ≤ 25 | 🔴 |
| **信息架构** | 侧边栏分组 ≤ 6 | 🔴 |
| **信息架构** | 侧边栏无 Emoji 图标 | 🔴 |
| **公共框架** | **含标准侧边栏 `<aside class="sidebar">` + `<nav class="menu">`** | 🔴 |
| **公共框架** | **含顶部 `<header class="header">`（含 `.crumbs` + `.user-area`）** | 🔴 |
| **公共框架** | **含 `<div class="page-head">`（含 `.page-title` + `.page-sub` + `.page-actions`）** | 🔴 |
| **公共框架** | **菜单项含 `<span class="icon">` 图标** | 🔴 |
| **公共框架** | **含 `<div class="user-area">` 用户区** | 🔴 |
| **页面结构** | 表格页有 `.filter` 筛选条（5 列） | 🔴 |
| **页面结构** | 复杂页有 `.tabs`（≥ 3 个） | 🔴 |
| **页面结构** | 每个 `.stat` 有 `.stat-icon` | 🟡 |
| **页面结构** | 表格列 ≥ 5 有关键列 `.sortable` | 🔴 |
| **页面结构** | 页面顶部右侧用 `.page-actions` / `.next-reset` / 单按钮 | 🟡 |
| **业务组件** | 业务特殊组件用标准类名（`.diag`/`.topo`/`.perm`/`.phone`/`.lib`） | 🔴 |
| **业务组件** | 无自创业务类名（`.my-diag`、`.face-grid` 等） | 🔴 |
| **组织方式** | 核心页独立 HTML（不挤 50 panel） | 🔴 |
| **技术约束** | 单文件、内联 CSS+JS、不依赖 Tailwind/Element Plus | 🔴 |
| **技术约束** | 含 `:root` CSS 变量体系 | 🔴 |
| **技术约束** | 含交互 JS（tabs/drawer/toast/sortable） | 🔴 |
| **技术约束** | 所有 `<button>` 必须有 `onclick` 或 `type=submit`（点击触发 JS/Toast/跳转） | 🔴 |
| **技术约束** | 所有菜单项用 `<a href="...">` 实现，点击真实跳转 | 🔴 |
| **技术约束** | 所有面包屑/操作链接 `<a>` 必须有 `href` | 🔴 |
| **技术约束** | 表格行"详情/编辑/删除"按钮必须能打开抽屉或跳详情页 | 🔴 |
| **技术约束** | 至少 1 个 tab 切换 + 1 个 drawer 打开 + 1 个 toast 反馈可演示 | 🔴 |
| **设计规范** | 无反模式（参见"反模式清单"） | 🔴 |

**得分规则**：
- 19 条 🔴 全部通过 = 内部门禁通过
- 任一 🔴 不通过 = 必须重做，停止后续评审

**自动化验证（推荐）**：
- 直接调用 `references/prototype-validator.py` 跑 **13 项硬性约束**自检（C1–C13）：
  ```bash
  python references/prototype-validator.py --dir 06-html-prototype/
  ```
- 13 项检查覆盖：① common.css 引用 ② common.js 引用 ③ 菜单项 ≤ 25 ④ 侧边栏无 Emoji ⑤ 业务组件类名 ⑥ .filter 筛选条 ⑦ .tabs 复杂页 ⑧ 无外部 CDN ⑨ 标准侧边栏结构 ⑩ 顶部 header 结构 ⑪ page-head 标题区 ⑫ 菜单项 icon ⑬ user-area 用户区
- 脚本会逐文件输出 13 项 ✅/❌ 状态 + 修复建议，**通过 = 内部门禁本节视为通过**
- 单文件验证：`python references/prototype-validator.py 06-html-prototype/keyframe.html`
- 脚本退出码 0=通过，1=失败（适合 CI 集成）

---

## 人类QA确认（Step 7 必走门）

**完成内部门禁 + 外部评审后，必须暂停等待人类确认。**

**确认流程**：
- 展示产物摘要：核心页面数、HTML 文件清单、侧边栏菜单数（必须 ≤ 25）
- 展示检查结果：内部门禁 / 外部评审 / 反模式清单逐条状态
- 展示 1-2 个**最佳实践页面截图**（推荐用 Chrome DevTools MCP 截图）
- 特别提醒：用户必须**实际打开 HTML 在浏览器中查看效果**，不能只看代码

**用户选择**：
- 用户选择"确认通过" → 记录确认结果到 `10-review-log.md`，进入 Step 8
- 用户选择"需要修改" → 根据用户反馈修改 `06-prototype.md` 和对应 HTML 原型，重新执行内部门禁+外部评审+人类确认（不重算重试轮次，人类确认不算在3轮重试内）
- 用户未回应时 → **不能自动进入下一步**，必须等待

外部评审通过后，才能触发人类QA确认。
