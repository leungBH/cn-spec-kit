// cn-spec-kit demo - 统一交互脚本
// 实现：tab 切换 / 抽屉 / 弹窗 / Toast / 排序 / 筛选反馈 / 菜单激活

// ===== 1. Tab 切换 =====
// 修复：tab 按钮在 .tabs 容器内，pane 在 .card 容器内，
// 必须按 data-tab/data-pane 的"同组"关系（按 .tabs 祖先 + 紧邻 .card 兄弟）来匹配，
// 不能用 document 全局移除（会误伤其他 tabs 组的 pane）。
function initTabs() {
  document.querySelectorAll('[data-tab]').forEach(t => {
    t.addEventListener('click', () => {
      const key = t.dataset.tab;
      // 找到 tab 所属的 tabs 容器
      const tabsGroup = t.closest('.tabs');
      // 找到 tabs 容器后面的兄弟 .card（pane 所在容器）
      let paneContainer = tabsGroup ? tabsGroup.nextElementSibling : null;
      // tab 按钮的 active 切换
      if (tabsGroup) {
        tabsGroup.querySelectorAll('[data-tab]').forEach(x => x.classList.remove('active'));
      }
      // pane 的 active 切换：在 tabsGroup 的兄弟容器内查找
      if (paneContainer) {
        paneContainer.querySelectorAll('[data-pane]').forEach(x => x.classList.remove('active'));
      }
      t.classList.add('active');
      // 在兄弟容器内查找对应 pane
      const pane = paneContainer ? paneContainer.querySelector('[data-pane="' + key + '"]') : null;
      if (pane) pane.classList.add('active');
    });
  });
}

// ===== 2. 抽屉 =====
function openDrawer(id) {
  const drawer = document.getElementById(id || 'drawer');
  const mask = document.getElementById(id + 'Mask') || document.getElementById('drawerMask');
  if (drawer) drawer.classList.add('open');
  if (mask) mask.classList.add('open');
}
function closeDrawer(id) {
  const drawer = document.getElementById(id || 'drawer');
  const mask = document.getElementById(id + 'Mask') || document.getElementById('drawerMask');
  if (drawer) drawer.classList.remove('open');
  if (mask) mask.classList.remove('open');
}
function initDrawer() {
  document.querySelectorAll('.drawer-mask').forEach(mask => {
    mask.addEventListener('click', () => {
      mask.classList.remove('open');
      const drawer = mask.id.replace('Mask', '');
      const d = document.getElementById(drawer);
      if (d) d.classList.remove('open');
    });
  });
  document.querySelectorAll('.drawer-close').forEach(btn => {
    btn.addEventListener('click', () => {
      const drawer = btn.closest('.drawer');
      if (drawer) {
        drawer.classList.remove('open');
        const maskId = drawer.id + 'Mask';
        const mask = document.getElementById(maskId);
        if (mask) mask.classList.remove('open');
      }
    });
  });
}

// ===== 3. 弹窗 =====
function openModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.add('open');
}
function closeModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.remove('open');
}
function initModal() {
  document.querySelectorAll('.modal-mask').forEach(mask => {
    mask.addEventListener('click', e => {
      if (e.target === mask) mask.classList.remove('open');
    });
  });
}

// ===== 4. Toast =====
function showToast(msg, duration) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), duration || 2500);
}

// ===== 5. 排序 =====
function initSort() {
  document.querySelectorAll('th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const table = th.closest('table');
      table.querySelectorAll('th.sortable').forEach(x => {
        x.classList.remove('sorted');
        const arrow = x.querySelector('.arrow');
        if (arrow) arrow.textContent = '↓';
      });
      th.classList.add('sorted');
      const arrow = th.querySelector('.arrow');
      if (arrow) arrow.textContent = '↑';
      showToast('已按 ' + th.textContent.trim().replace('↓','').replace('↑','') + ' 排序');
    });
  });
}

// ===== 6. 筛选条 =====
function initFilter() {
  document.querySelectorAll('.filter').forEach(f => {
    const queryBtn = f.querySelector('[data-action="query"]');
    const resetBtn = f.querySelector('[data-action="reset"]');
    if (queryBtn) {
      queryBtn.addEventListener('click', () => {
        const inputs = f.querySelectorAll('input, select');
        const cond = [];
        inputs.forEach(i => { if (i.value) cond.push(i.value); });
        showToast('已查询，共 ' + (Math.floor(Math.random()*20)+5) + ' 条数据');
      });
    }
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        f.querySelectorAll('input, select').forEach(i => { i.value = ''; });
        showToast('已重置筛选');
      });
    }
  });
}

// ===== 7. 菜单激活态（点击菜单时切换 active）=====
function initMenu() {
  document.querySelectorAll('.menu-item').forEach(m => {
    m.addEventListener('click', e => {
      document.querySelectorAll('.menu-item').forEach(x => x.classList.remove('active'));
      m.classList.add('active');
    });
  });
}

// ===== 8. 抽屉内容填充（详情场景）=====
function openDetailDrawer(data) {
  const body = document.getElementById('drawerBody');
  if (body) {
    body.innerHTML = `
      <div class="desc-grid">
        <div><div class="label">申请人</div><div class="value">${data.applicant || '-'}</div></div>
        <div><div class="label">请假类型</div><div class="value">${data.type || '-'}</div></div>
        <div><div class="label">开始时间</div><div class="value">${data.start || '-'}</div></div>
        <div><div class="label">结束时间</div><div class="value">${data.end || '-'}</div></div>
        <div><div class="label">请假天数</div><div class="value">${data.days || '-'}</div></div>
        <div><div class="label">所属部门</div><div class="value">${data.dept || '-'}</div></div>
        <div style="grid-column: span 2"><div class="label">请假原因</div><div class="value">${data.reason || '-'}</div></div>
        <div><div class="label">提交时间</div><div class="value">${data.submitAt || '-'}</div></div>
        <div><div class="label">当前状态</div><div class="value"><span class="tag tag-warning">待审批</span></div></div>
      </div>
    `;
  }
  openDrawer();
}

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initDrawer();
  initModal();
  initSort();
  initFilter();
  initMenu();
});
