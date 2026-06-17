#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cn-spec-kit Step 8 页面原型 验证脚本

用途：LLM 生成 HTML 页面后，调用此脚本做 8 项硬性约束自检。
调用方式：python prototype-validator.py <page.html> [page2.html ...]
        python prototype-validator.py --dir <prototypes-dir>

退出码：
  0 = 全部通过
  1 = 有失败项（输出失败详情）
  2 = 参数错误

设计原则：
- 单文件、无第三方依赖、开箱即用
- 中文路径友好（Windows + Linux 都跑）
- 输出清晰可读，方便 LLM 根据结果自动修复
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Windows PowerShell 默认 GBK 编码会导致中文/Emoji 报错，强制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ============== 8 项硬性约束检查 ==============

CHECKS = [
    {
        "id": "C1",
        "name": "引用 common.css",
        "severity": "block",
        "pattern": r'<link\s+rel=["\']stylesheet["\']\s+href=["\']common\.css["\']',
        "fix": "在 <head> 中添加 <link rel=\"stylesheet\" href=\"common.css\">",
    },
    {
        "id": "C2",
        "name": "引用 common.js（紧跟 common.css 之后）",
        "severity": "block",
        "pattern": r'<link\s+rel=["\']stylesheet["\']\s+href=["\']common\.css["\']\s*>\s*<script\s+src=["\']common\.js["\']',
        "fix": "在 common.css <link> 之后立即添加 <script src=\"common.js\"></script>，缺它则 tab 切换、protocol、drawer、sortable 全部失灵",
    },
    {
        "id": "C3",
        "name": "侧边栏菜单项 ≤ 25",
        "severity": "block",
        "check_type": "menu_count",
        "max": 25,
        "fix": "菜单分组 ≤ 6、菜单项 ≤ 25；多余入口用首页/面包屑访问",
    },
    {
        "id": "C4",
        "name": "侧边栏无 Emoji 图标",
        "severity": "block",
        # 只匹配真正 Emoji 范围（U+1F000 起），不包含 U+2600-U+27FF（里面有 ☰ ⚙ ⌂ 等允许的方块字符）
        # 用 .menu-item 上下文搜索，避免误伤 .user-area 里的功能铃铛 🔔
        "check_type": "emoji_in_menu",
        "pattern": r'[\U0001F000-\U0001FFFF\U0001F300-\U0001FAFF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF]',
        "fix": "把侧边栏图标统一改为方块字符：▦▣▤▥▧▨▩▪▫◌◍◎●☰⚙⌂",
    },
    {
        "id": "C5",
        "name": "业务组件用标准类名（无自创前缀）",
        "severity": "block",
        # 禁自创 my-/custom-/local-；允许 page-（page-head、page-title、page-sub、page-actions）
        "pattern_neg": r'class=["\'][^"\']*\b(my-|custom-|local-)\w+',
        "fix": "复用 common.css 标准类名：.diag .lib-cell .topo .perm .phone .protocol .grid-2/3/4 .chart-card .period-tabs 等",
    },
    {
        "id": "C6",
        "name": "表格页有 .filter 筛选条",
        "severity": "warn",
        "check_type": "table_has_filter",
        "fix": "表格页必须含 <div class=\"filter\">，5 列 .field + 末列 .filter-actions",
    },
    {
        "id": "C7",
        "name": "复杂页（≥3 子视图）有 .tabs",
        "severity": "warn",
        "check_type": "complex_has_tabs",
        "fix": "≥ 3 个子视图必须 .tabs 拆分；不足 3 个无需 tabs",
    },
    {
        "id": "C8",
        "name": "未引入外部 UI 框架 CDN",
        "severity": "block",
        "pattern_neg": r'(tailwindcss|element-plus|element-ui|antd|ant-design|bootstrap\.min)',
        "fix": "删除所有外部 UI 框架 CDN 引用；保持原生 CSS + common.css 体系",
    },
    {
        "id": "C9",
        "name": "含标准侧边栏 <nav class=\"menu\">",
        "severity": "block",
        "pattern": r'<nav\s+class=["\']menu["\']',
        "fix": "必须含 <aside class=\"sidebar\"><nav class=\"menu\"> 结构；菜单分组用 <div class=\"menu-group-title\">，菜单项用 <div class=\"menu-item\"><span class=\"icon\">○</span>名称</div>",
    },
    {
        "id": "C10",
        "name": "含顶部 <header class=\"header\">",
        "severity": "block",
        "pattern": r'<header\s+class=["\']header["\']',
        "fix": "必须含 <header class=\"header\">，内含 <div class=\"crumbs\">面包屑</div> + <div class=\"user-area\">用户名/头像</div>",
    },
    {
        "id": "C11",
        "name": "含 page-head（page-title + page-sub + page-actions）",
        "severity": "block",
        "pattern": r'class=["\'][^"\']*\bpage-head\b',
        "fix": "页面内容容器必须以 <div class=\"page-head\"> 开头，含 <div class=\"page-title\">主标题</div> + <div class=\"page-sub\">副标题</div> + <div class=\"page-actions\">操作按钮</div>",
    },
    {
        "id": "C12",
        "name": "侧边栏菜单项含 <span class=\"icon\">",
        "severity": "block",
        "pattern": r'class=["\'][^"\']*\bmenu-item\b[^>]*>[\s\S]*?<span\s+class=["\']icon["\']',
        "fix": "每个 .menu-item 必须内含 <span class=\"icon\">○</span> 字符图标，统一用方块字符：▦▣▤▥▧▨▩▪▫◌◍◎●☰⚙⌂",
    },
    {
        "id": "C13",
        "name": "含 <div class=\"user-area\">",
        "severity": "block",
        "pattern": r'class=["\'][^"\']*\buser-area\b',
        "fix": "顶部 header 内必须含 <div class=\"user-area\">，含通知/头像/用户名",
    },
]


def check_file(path: Path) -> dict:
    """对单个 HTML 文件执行 8 项检查。"""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"path": str(path), "error": f"读取失败: {e}", "results": []}

    results = []
    has_table = bool(re.search(r'<table[\s>]', content))
    tab_count = len(re.findall(r'class=["\'][^"\']*\btab\b(?!-)', content))
    menu_count = len(re.findall(r'class=["\'][^"\']*\bmenu-item\b', content))

    for c in CHECKS:
        r = {"id": c["id"], "name": c["name"], "severity": c["severity"], "pass": True, "detail": ""}

        if c.get("check_type") == "menu_count":
            if menu_count > c["max"]:
                r["pass"] = False
                r["detail"] = f"菜单项 {menu_count} > {c['max']}"
            else:
                r["detail"] = f"菜单项 {menu_count}（≤ {c['max']}）"

        elif c.get("check_type") == "table_has_filter":
            # 启发式：含 <table> 且页面结构（≥ 1 section 或 ≥ 1 h2）像表格页时，需 .filter
            # 业务组件白名单：含 .perm/.diag/.topo/.phone/.chart-card/.lib-cell 的页面，其内 <table> 是组件一部分，不视为数据表
            business_components = re.findall(r'class=["\'][^"\']*\b(perm|diag|topo|phone|chart-card|lib-cell|protocol|chart-grid)\b', content)
            section_count = len(re.findall(r'<section[\s>]', content))
            h2_count = len(re.findall(r'<h2[\s>]', content))
            is_business_page = len(business_components) >= 1
            if has_table and not is_business_page and (section_count >= 1 or h2_count >= 1) and "filter" not in content:
                r["pass"] = False
                r["detail"] = f"页面含 <table> + {section_count} <section>/{h2_count} <h2>，且非业务组件页，但无 .filter"
            elif is_business_page:
                r["detail"] = f"含业务组件（{', '.join(set(business_components))}），跳过"
            elif not has_table:
                r["detail"] = "无表格，跳过"
            else:
                r["detail"] = "含 .filter"

        elif c.get("check_type") == "complex_has_tabs":
            # 启发式：≥ 3 个 <section> 或 ≥ 3 个 <h2> 视为复杂页
            section_count = len(re.findall(r'<section[\s>]', content))
            h2_count = len(re.findall(r'<h2[\s>]', content))
            if (section_count >= 3 or h2_count >= 3) and tab_count < 3:
                r["pass"] = False
                r["detail"] = f"检测到 {section_count} 个 <section> / {h2_count} 个 <h2>，但 tab 数量仅 {tab_count} < 3"
            else:
                r["detail"] = f"tab 数量 {tab_count}（或页面不复杂）"

        elif c.get("check_type") == "emoji_in_menu":
            # 只检查 .menu-item 块内是否含 Emoji；.user-area 里的功能铃铛 🔔 视为允许
            # 截取 .menu 容器内全部文本（在 </nav> 之前）
            menu_match = re.search(r'<nav class=["\']menu["\']>(.*?)</nav>', content, re.DOTALL)
            menu_text = menu_match.group(1) if menu_match else ""
            m = re.search(c["pattern"], menu_text)
            if m:
                r["pass"] = False
                r["detail"] = f"侧边栏菜单内匹配到 Emoji：{m.group(0)!r}"
            else:
                r["detail"] = "侧边栏菜单内无 Emoji"

        elif "pattern" in c:
            m = re.search(c["pattern"], content, re.IGNORECASE)
            if not m:
                r["pass"] = False
                r["detail"] = "未匹配到模式"

        elif "pattern_neg" in c:
            m = re.search(c["pattern_neg"], content)
            if m:
                r["pass"] = False
                r["detail"] = f"匹配到禁用字符：{m.group(0)!r}"

        r["fix"] = c.get("fix", "")
        results.append(r)

    return {"path": str(path), "error": None, "results": results}


def print_result(r: dict, verbose: bool = True) -> bool:
    """打印单文件检查结果，返回是否全部通过。"""
    path = r["path"]
    name = Path(path).name
    if r.get("error"):
        print(f"❌ {name}: {r['error']}")
        return False

    block_fail = [x for x in r["results"] if not x["pass"] and x["severity"] == "block"]
    warn_fail = [x for x in r["results"] if not x["pass"] and x["severity"] == "warn"]
    passed = [x for x in r["results"] if x["pass"]]

    if not block_fail and not warn_fail:
        print(f"✅ {name}: {len(r['results'])}/{len(r['results'])} 通过")
        return True

    status = "❌" if block_fail else "⚠️ "
    print(f"{status} {name}: {len(passed)}/{len(r['results'])} 通过，"
          f"{len(block_fail)} 阻塞，{len(warn_fail)} 警告")

    if not verbose:
        return not block_fail

    for x in r["results"]:
        if x["pass"]:
            print(f"  ✅ {x['id']} {x['name']} — {x['detail']}")
        else:
            icon = "🔴" if x["severity"] == "block" else "🟡"
            print(f"  {icon} {x['id']} {x['name']} — {x['detail']}")
            print(f"     修复：{x['fix']}")

    return not block_fail


def main():
    parser = argparse.ArgumentParser(
        description="cn-spec-kit Step 8 页面原型 8 项硬性约束验证器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python prototype-validator.py prototypes/index.html
  python prototype-validator.py prototypes/*.html
  python prototype-validator.py --dir prototypes/
  python prototype-validator.py --dir prototypes/ --quiet
        """,
    )
    parser.add_argument("files", nargs="*", help="要验证的 HTML 文件")
    parser.add_argument("--dir", help="验证指定目录下所有 .html 文件（排除 index.html/login.html）")
    parser.add_argument("--quiet", "-q", action="store_true", help="只输出失败项")
    args = parser.parse_args()

    targets = []
    if args.dir:
        d = Path(args.dir)
        if not d.is_dir():
            print(f"❌ 目录不存在: {d}", file=sys.stderr)
            sys.exit(2)
        for p in sorted(d.glob("*.html")):
            if p.name in ("index.html", "login.html"):
                continue
            targets.append(p)
    else:
        targets = [Path(f) for f in args.files]

    if not targets:
        print("❌ 未提供待验证文件", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(2)

    print(f"🔍 cn-spec-kit Step 8 验证器  |  共 {len(targets)} 个文件\n")
    all_pass = True
    for t in targets:
        if not t.exists():
            print(f"❌ 文件不存在: {t}")
            all_pass = False
            continue
        r = check_file(t)
        if not print_result(r, verbose=not args.quiet):
            all_pass = False
        print()

    total = len(targets)
    passed = sum(1 for t in targets
                 if (r := check_file(t)) and not r.get("error")
                 and all(x["pass"] for x in r["results"]))
    print(f"📊 总结：通过 {passed}/{total}（{passed*100//total if total else 0}%）")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
