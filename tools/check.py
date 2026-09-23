#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客规范检查器 —— 只检查，不改任何文件。

用法：python tools/check.py   （有问题时退出码 1）

只依赖 Python 标准库（需要 3.11+ 的 tomllib），CI 里不用装任何东西。
front matter 的语法错误由 `hugo` 构建去抓，这里只查语义
（该有的字段有没有、类型对不对），不做完整 YAML 解析。
"""

import re
import subprocess
import sys
import tomllib
from pathlib import Path

# ---------------------------------------------------------------- 基础工具

ERRORS: list[str] = []
WARNINGS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def find_repo_root() -> Path:
    """从脚本所在位置往上找，直到发现 hugo.toml。"""
    for base in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
        if (base / "hugo.toml").is_file():
            return base
    return Path(__file__).resolve().parent.parent


def git(*args: str) -> str | None:
    """跑 git 命令。不在 git 仓库里就返回 None，不算失败。"""
    try:
        out = subprocess.run(
            ["git", *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        return out.stdout if out.returncode == 0 else None
    except FileNotFoundError:
        return None


def tracked_files(root: Path) -> list[str] | None:
    out = git("-C", str(root), "ls-files")
    return out.splitlines() if out is not None else None


# ---------------------------------------------------------------- 配置检查

def check_config(root: Path) -> dict | None:
    """hugo.toml 必须能解析，且关键项都在。"""
    cfg_path = root / "hugo.toml"
    if not cfg_path.is_file():
        err("找不到 hugo.toml —— 脚本要在博客仓库里跑")
        return None

    text = cfg_path.read_text(encoding="utf-8")
    try:
        cfg = tomllib.loads(text)
    except tomllib.TOMLDecodeError as e:
        err(f"hugo.toml 不是合法的 TOML（Hugo 会直接构建失败）：{e}")
        # 同一个键写两遍是最常见的一种：tomllib 报 "Cannot overwrite a value"，
        # Hugo 报 "key ... is already defined"。典型成因是注释里留着示例，
        # 下面又有一行同名生效值。
        low = str(e).lower()
        if "already defined" in low or "duplicate" in low or "overwrite" in low:
            err("  ↑ 多半是同一个键写了两遍。"
                "\n    取消注释示例时，记得把那行同名默认值一起删掉。")
        return None

    # baseURL：CI 会覆盖，但本地构建出来的 canonical / RSS 靠它
    base = cfg.get("baseURL", "")
    if not base:
        err("hugo.toml 缺少 baseURL")
    else:
        if "example.com" in base:
            err(f"baseURL 还是占位的 example.com：{base}")
        if not base.endswith("/"):
            err(f"baseURL 结尾必须带斜杠，现在是：{base}")

    # 时区：没有它，只写日期的文章会被当成 UTC 零点，当天发布会被判为「未来」
    if "timeZone" not in cfg:
        err("hugo.toml 缺少 timeZone —— 删掉会导致当天发布的文章不显示")

    # languageCode 在 Hugo 0.158+ 已弃用
    if "languageCode" in cfg:
        warn("hugo.toml 还在用已弃用的 languageCode，改用 locale")
    if "locale" not in cfg:
        warn("hugo.toml 没有 locale，日期等本地化会退回英文")

    # 主题目录必须真的存在
    theme = cfg.get("theme")
    if not theme:
        err("hugo.toml 缺少 theme")
    elif not (root / "themes" / theme).is_dir():
        err(f"hugo.toml 写的主题是 {theme}，但 themes/{theme}/ 不存在")
    elif not (root / "themes" / theme / "theme.toml").is_file():
        err(f"themes/{theme}/ 里没有 theme.toml，主题没装完整")

    return cfg


def check_author_links(root: Path, cfg: dict) -> None:
    """社交链接：图标名要有对应 svg，email 不能带 mailto: 前缀。"""
    links = cfg.get("params", {}).get("author", {}).get("links")
    if links is None:
        return
    if not isinstance(links, list):
        err("[params.author].links 应该是一个数组，现在是别的东西")
        return

    theme = cfg.get("theme", "blowfish")
    icon_dir = root / "themes" / theme / "assets" / "icons"
    have_icons = {p.stem for p in icon_dir.glob("*.svg")} if icon_dir.is_dir() else set()

    for i, item in enumerate(links, 1):
        if not isinstance(item, dict):
            err(f"[params.author].links 第 {i} 项不是一个表，写法应为 {{ 名字 = \"地址\" }}")
            continue
        for name, url in item.items():
            # 图标名对应不上 svg 时，主题不报错，只是那个图标不显示
            if have_icons and name not in have_icons:
                err(f"社交链接第 {i} 项的图标名 '{name}' 在 themes/{theme}/assets/icons/ "
                    f"里没有对应文件，图标会不显示")
            if not isinstance(url, str) or not url.strip():
                err(f"社交链接第 {i} 项（{name}）的地址是空的")
                continue
            if name == "email":
                # 主题模板做 base64 编码，前端 JS 再自己补 mailto:
                if url.lower().startswith("mailto:"):
                    err(f"社交链接的 email 不要写 mailto: 前缀（主题会自动加），"
                        f"现在是：{url}")
                elif "@" not in url:
                    err(f"社交链接的 email 看着不像邮箱地址：{url}")
                elif re.fullmatch(r"[A-Za-z0-9+/=]{16,}", url):
                    err(f"社交链接的 email 填的是 base64 串 —— 主题会再编一次，"
                        f"直接填邮箱明文即可：{url}")


def check_menu(cfg: dict) -> None:
    """导航菜单每一项都要有名字和地址。"""
    menu = cfg.get("menu", {})
    if not isinstance(menu, dict):
        err("[[menu.*]] 配置格式不对")
        return
    for section, items in menu.items():
        if not isinstance(items, list):
            err(f"[[menu.{section}]] 应该是一组表，现在是别的东西")
            continue
        for i, item in enumerate(items, 1):
            if not isinstance(item, dict):
                continue
            if not item.get("name"):
                err(f"[[menu.{section}]] 第 {i} 项缺少 name（菜单上会显示成空白）")
            if not item.get("url") and not item.get("pageRef"):
                err(f"[[menu.{section}]] 第 {i} 项（{item.get('name', '?')}）"
                    f"既没有 url 也没有 pageRef，点了没反应")


# ---------------------------------------------------------------- 内容检查

def split_front_matter(path: Path) -> tuple[list[str] | None, str]:
    """取出 front matter 的行。没有就返回 (None, 全文)。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() not in ("---", "+++"):
        return None, "\n".join(lines)
    fence = lines[0].strip()
    for i in range(1, len(lines)):
        if lines[i].strip() == fence:
            return lines[1:i], "\n".join(lines[i + 1:])
    return None, "\n".join(lines)


def simple_value(raw: str):
    """把 front matter 里的标量值粗略还原成 Python 值。

    只处理这个博客用到的写法：字符串、true/false、行内数组 ["a", "b"]。
    语法正确性交给 hugo 构建去抓。
    """
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [x.strip().strip("\"'") for x in inner.split(",") if x.strip()] if inner else []
    low = raw.lower()
    if low in ("true", "false"):
        return low == "true"
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    return raw


def parse_fields(fm_lines: list[str]) -> dict:
    """解析顶层 `key: value`。缩进的行（多行数组）跳过。"""
    fields: dict = {}
    for line in fm_lines:
        if not line.strip() or line[0] in " \t":
            continue
        m = re.match(r"^([A-Za-z_][\w.-]*)\s*:\s*(.*)$", line)
        if m:
            fields[m.group(1)] = simple_value(m.group(2))
    return fields


def check_content(root: Path) -> None:
    """每篇内容的 front matter 该有的字段要有、类型要对。"""
    content_dir = root / "content"
    if not content_dir.is_dir():
        err("找不到 content/ 目录")
        return

    for md in sorted(content_dir.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        fm, body = split_front_matter(md)
        if fm is None:
            err(f"{rel}：开头没有 front matter（要用 --- 包起来）")
            continue

        fields = parse_fields(fm)
        is_home = rel == "content/_index.md"
        is_branch = md.name == "_index.md"

        # 首页刻意不写 title，否则正文上方会多出一个「首页」大标题
        if not fields.get("title") and not is_home:
            err(f"{rel}：front matter 缺少 title")
        if is_home and fields.get("title"):
            warn(f"{rel}：首页写了 title，页面正文上方会多出一个大标题")

        # 栏目页（_index.md）是结构文件，不参与文章排序和草稿逻辑
        if not is_branch:
            if "date" not in fields:
                err(f"{rel}：front matter 缺少 date（没有日期的文章排序会乱）")
            if "draft" in fields and not isinstance(fields["draft"], bool):
                err(f"{rel}：draft 必须是 true 或 false，现在是 {fields['draft']!r}")
        elif "draft" in fields:
            warn(f"{rel}：栏目页写 draft 没有意义（它不参与草稿逻辑）")

        if not body.strip() and not is_branch:
            warn(f"{rel}：正文是空的")


# ---------------------------------------------------------------- 卫生检查

# 构建产物提交进仓库会让 diff 变噪音，还容易和别人冲突
BUILD_DIRS = ("public/", "resources/_gen/")


def check_tracked_artifacts(root: Path) -> None:
    """构建产物不该被 git 跟踪。"""
    files = tracked_files(root)
    if files is None:
        warn("不在 git 仓库里（或没装 git），跳过「构建产物是否被跟踪」检查")
        return

    bad = [f for f in files if any(f.startswith(d) for d in BUILD_DIRS)]
    if bad:
        tops = " ".join(sorted({b.split("/")[0] for b in bad}))
        err(f"有构建产物被 git 跟踪了（{len(bad)} 个，例如 {bad[0]}）。"
            f"执行：git rm -r --cached {tops}")
    if ".hugo_build.lock" in files:
        err(".hugo_build.lock 被 git 跟踪了，执行：git rm --cached .hugo_build.lock")


def check_icons(root: Path) -> None:
    """站点图标和 webmanifest 里引用的文件要真的存在。"""
    static = root / "static"
    if not static.is_dir():
        return

    for name in ("favicon.ico", "favicon-16x16.png", "favicon-32x32.png",
                 "apple-touch-icon.png"):
        if not (static / name).is_file():
            warn(f"static/ 下缺少 {name} —— 浏览器会用主题自带的默认图标，"
                 f"看不出是你的站点")

    mw = static / "site.webmanifest"
    if not mw.is_file():
        return
    try:
        import json
        data = json.loads(mw.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"site.webmanifest 不是合法的 JSON：{e}")
        return
    for icon in data.get("icons", []):
        src = icon.get("src", "").lstrip("/")
        if src and not (static / src).is_file():
            err(f"site.webmanifest 引用了 static/{src}，但文件不存在")


# ---------------------------------------------------------------- 入口

def main() -> int:
    root = find_repo_root()
    print(f"检查目录：{root}")

    cfg = check_config(root)
    if cfg:
        check_author_links(root, cfg)
        check_menu(cfg)
    check_content(root)
    check_icons(root)
    check_tracked_artifacts(root)

    for m in ERRORS:
        print(f"  [错误] {m}")
    for m in WARNINGS:
        print(f"  [警告] {m}")

    if ERRORS:
        print(f"\n检查未通过：{len(ERRORS)} 个错误、{len(WARNINGS)} 个警告")
        return 1
    if WARNINGS:
        print(f"\n检查通过（有 {len(WARNINGS)} 个警告）")
        return 0
    print("检查通过，没发现问题")
    return 0


if __name__ == "__main__":
    sys.exit(main())
