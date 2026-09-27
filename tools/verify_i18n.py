"""验证博客多语言产物的行为。

语言集合从 hugo.toml 的 [languages] 读取，期望 URL 从内容文件的语言
后缀推导 —— 加一种语言不需要改这个脚本：它会对每个配置的语言自动
核对「有翻译的内容都生成了页面」。

注意：产物是 `--minify` 过的，HTML 属性不带引号（`lang=zh-CN`），
所以下面的正则都要容忍引号可缺省。

用法：先 `hugo --gc --minify` 构建出 public/，再 `python tools/verify_i18n.py`。
"""
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "public"

# 多语言改造前的中文 URL（基线，来自多语言改造前的构建产物）。
# 这是默认语言的回归契约：基线里的一条都不能少。
BASELINE = {
    "about/index.html", "categories/index.html", "categories/建站笔记/index.html",
    "categories/建站笔记/page/1/index.html", "index.html", "page/1/index.html",
    "posts/hello-world/index.html", "posts/index.html",
    "posts/markdown-cheatsheet/index.html", "posts/page/1/index.html",
    "series/index.html", "tags/github-pages/index.html",
    "tags/github-pages/page/1/index.html", "tags/hugo/index.html",
    "tags/hugo/page/1/index.html", "tags/index.html", "tags/markdown/index.html",
    "tags/markdown/page/1/index.html", "tags/写作/index.html",
    "tags/写作/page/1/index.html",
}

cfg = tomllib.loads((ROOT / "hugo.toml").read_text(encoding="utf-8"))
DEFAULT = cfg.get("defaultContentLanguage", "")
LANGS: list[dict] = []          # [{key, locale, name}]，默认语言排最前
for key, block in (cfg.get("languages") or {}).items():
    params = block.get("params") or {}
    LANGS.append({"key": key, "locale": block.get("locale") or key,
                  "name": params.get("displayName") or key})
LANGS.sort(key=lambda l: l["key"] != DEFAULT)
OTHERS = [l for l in LANGS if l["key"] != DEFAULT]

ok = fail = 0


def check(name, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"  [PASS] {name}")
    else:
        fail += 1
        print(f"  [FAIL] {name}  {detail}")


def text(rel):
    f = P / rel
    return f.read_text(encoding="utf-8") if f.exists() else ""


def hreflangs(rel):
    """{语言代码: href}"""
    return dict(re.findall(
        r'<link rel=alternate hreflang="?([^"\s>]+)"? href="?([^"\s>]+)"?', text(rel)))


def html_lang(rel):
    m = re.findall(r'<html\s+lang="?([^"\s>]+)"?', text(rel))
    return m[0] if m else None


def menu_links(rel):
    """页头菜单里的 (文字, href) 对。"""
    seg = re.search(r"<header.*?</header>", text(rel), re.S)
    if not seg:
        return []
    out = []
    for href, inner in re.findall(r'<a\b[^>]*?href="?(/[^"\s>]*)"?[^>]*>(.*?)</a>',
                                  seg.group(0), re.S):
        label = re.sub(r"<[^>]+>", "", inner).strip()
        out.append((label, href))
    return out


def content_url(rel_md: str) -> str:
    """content/ 下的 .md 相对路径 → 期望的产物 URL（相对语言根）。"""
    rel = re.sub(r"\.[A-Za-z]{2}(?:-[A-Za-z]{2,4})?\.md$", ".md", rel_md)
    base = rel[:-3]                                    # 去掉 .md
    if base == "_index" or base.endswith("/_index"):
        url = base[: -len("_index")]                   # 首页/栏目页 → 目录本身
    elif base == "index" or base.endswith("/index"):   # bundle 正文
        url = base[: -len("index")]
    else:
        url = base + "/"
    return url + "index.html"


def lang_urls(key: str) -> set[str]:
    """该语言有翻译的内容 → 期望的产物 URL（相对 public/<key>/）。"""
    out = set()
    for f in (ROOT / "content").rglob("*.md"):
        if f.name.endswith(f".{key}.md"):
            out.add(content_url(f.relative_to(ROOT / "content").as_posix()))
    return out


def lang_product(key: str) -> set[str]:
    """该语言前缀下实际生成的产物 URL。"""
    root = P / key
    if not root.is_dir():
        return set()
    return {str(p.relative_to(root)).replace("\\", "/")
            for p in root.rglob("index.html")}


def default_urls() -> set[str]:
    """默认语言的产物 URL（排除其余语言前缀与默认语言自己的重定向目录）。"""
    prefixes = tuple(f"{l['key']}/" for l in OTHERS) + (f"{DEFAULT}/",)
    return {str(p.relative_to(P)).replace("\\", "/")
            for p in P.rglob("index.html")
            if not str(p.relative_to(P)).replace("\\", "/").startswith(prefixes)}


def fully_translated() -> list[str]:
    """在所有语言里都有翻译的页面（默认语言 URL 视角），按 URL 排序。"""
    sets = [lang_urls(l["key"]) for l in OTHERS]
    if not sets:
        return []
    pages = set.intersection(*sets)
    return sorted(pages & default_urls())


print("=== 1. 默认语言 URL 与基线一致 ===")
missing = BASELINE - default_urls()
check("中文 URL 一条不少", not missing, f"丢了 {sorted(missing)}")

print("\n=== 2. 其余语言：有翻译的内容都生成了页面 ===")
for lang in OTHERS:
    key = lang["key"]
    expected = lang_urls(key)
    missing = {f"{key}/{u}" for u in expected} - {f"{key}/{u}" for u in lang_product(key)}
    check(f"{key}：{len(expected)} 个翻译页面全部生成", not missing,
          f"缺 {sorted(missing)[:5]}")

print("\n=== 3. hreflang：翻译页双向对照 ===")
pages_all = fully_translated()
check("存在全语言都翻译的页面", bool(pages_all), "没有任何内容覆盖全部语言")
sample = "index.html" if "index.html" in pages_all else (pages_all[0] if pages_all else "")
if sample:
    d = hreflangs(sample)
    want = {l["locale"] for l in LANGS}
    check(f"{sample} 的 hreflang 覆盖全部语言", set(d) >= want, f"{sorted(d)}")
    for lang in OTHERS:
        v = hreflangs(f"{lang['key']}/{sample}")
        check(f"{lang['key']} 版与默认语言指向同一组地址", v == d, f"{v} vs {d}")
        # 自己语言的 alternate 必须落在自己的子树里（首页即 /<key>/ 本身）。
        # href 是绝对地址，先剥掉协议和主机再比路径。
        own = re.sub(r"^https?://[^/]+", "", v.get(lang["locale"], ""))
        check(f"{lang['key']} 版自身 href 在 /{lang['key']} 下",
              own == f"/{lang['key']}" or own.startswith(f"/{lang['key']}/"), own)

print("\n=== 4. <html lang> 跟随语言 ===")
for lang in LANGS:
    rel = "index.html" if lang["key"] == DEFAULT else f"{lang['key']}/index.html"
    check(f"{rel} -> {lang['locale']}", html_lang(rel) == lang["locale"],
          f"实际 {html_lang(rel)}")

print("\n=== 5. 界面文案无串语言 ===")
if sample:
    check("默认语言页有「预计阅读」", "预计阅读" in text(sample))
    for lang in OTHERS:
        v = text(f"{lang['key']}/{sample}")
        check(f"{lang['key']} 版没有中文界面词", "预计阅读" not in v)

print("\n=== 6. 菜单跟随语言且无悬空 ===")
default_labels = {l for l, _ in menu_links("index.html")}
self_names = {l["name"] for l in LANGS}     # 切换器里的语言自称，出现是合法的
for lang in LANGS:
    rel = "index.html" if lang["key"] == DEFAULT else f"{lang['key']}/index.html"
    links = menu_links(rel)
    bad = []
    for label, href in links:
        target = href.strip("/")
        cand = P / target / "index.html" if target else P / "index.html"
        if not cand.exists():
            bad.append(f"{label}->{href}")
    check(f"{rel} 菜单无悬空链接", not bad, f"悬空 {bad}")
    if lang["key"] != DEFAULT:
        residue = (default_labels & {l for l, _ in links}) - self_names
        check(f"{lang['key']} 菜单没有默认语言残留", not residue, f"{sorted(residue)}")

print("\n=== 7. 语言切换入口 ===")
for lang in LANGS:
    rel = "index.html" if lang["key"] == DEFAULT else f"{lang['key']}/index.html"
    check(f"{rel} 有语言切换组件", "translation nested-menu" in text(rel))
check("切换项显示全部 displayName",
      all(l["name"] and l["name"] in text("index.html") for l in LANGS),
      str([l["name"] for l in LANGS]))

print(f"\n=== 汇总：{ok} 通过 / {fail} 失败 ===")
sys.exit(1 if fail else 0)
