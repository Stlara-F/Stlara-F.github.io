"""验证博客多语言产物的行为。

注意：产物是 `--minify` 过的，HTML 属性不带引号（`lang=zh-CN`），
所以下面的正则都要容忍引号可缺省。
"""
import re
import sys
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "public"

# 加语言之前的中文 URL（基线，来自多语言改造前的构建产物）
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


print("=== 1. 中文 URL 与基线一致 ===")
now = {str(p.relative_to(P)).replace("\\", "/")
       for p in P.rglob("index.html")
       if not str(p.relative_to(P)).startswith(("en/", "zh-cn/"))}
missing = BASELINE - now
check("中文 URL 一条不少", not missing, f"丢了 {sorted(missing)}")

print("\n=== 2. 英文 URL 在 /en/ 下 ===")
for rel in ["en/index.html", "en/about/index.html", "en/posts/index.html",
            "en/posts/hello-world/index.html", "en/posts/markdown-cheatsheet/index.html",
            "en/tags/index.html"]:
    check(rel, (P / rel).exists())

print("\n=== 3. hreflang 双向 ===")
zh = hreflangs("posts/hello-world/index.html")
en = hreflangs("en/posts/hello-world/index.html")
check("中文页有 zh-CN 与 en", set(zh) >= {"zh-CN", "en"}, f"{sorted(zh)}")
check("英文页有 zh-CN 与 en", set(en) >= {"zh-CN", "en"}, f"{sorted(en)}")
check("两边指向同一对地址", zh == en, f"{zh} vs {en}")
check("zh-CN 指向根路径", zh.get("zh-CN", "").endswith("/posts/hello-world/"),
      zh.get("zh-CN", ""))
check("en 指向 /en/ 路径", zh.get("en", "").endswith("/en/posts/hello-world/"),
      zh.get("en", ""))

print("\n=== 4. <html lang> ===")
for rel, want in [("index.html", "zh-CN"), ("en/index.html", "en"),
                  ("posts/hello-world/index.html", "zh-CN"),
                  ("en/posts/hello-world/index.html", "en")]:
    got = html_lang(rel)
    check(f"{rel} -> {want}", got == want, f"实际 {got}")

print("\n=== 5. 界面文案跟随语言 ===")
check("中文页有「预计阅读」", "预计阅读" in text("posts/hello-world/index.html"))
check("英文页有 Reading time", "Reading time" in text("en/posts/hello-world/index.html"))
check("英文页没有中文界面词", "预计阅读" not in text("en/posts/hello-world/index.html"))

print("\n=== 6. 菜单跟随语言 ===")
zh_labels = {l for l, _ in menu_links("index.html")}
en_labels = {l for l, _ in menu_links("en/index.html")}
check("中文菜单有 文章/标签/关于", {"文章", "标签", "关于"} <= zh_labels, f"{sorted(zh_labels)}")
check("英文菜单有 Posts/Tags/About", {"Posts", "Tags", "About"} <= en_labels,
      f"{sorted(en_labels)}")
check("英文菜单没有中文残留", not ({"文章", "标签", "关于"} & en_labels),
      f"{sorted(en_labels)}")

print("\n=== 7. 语言切换入口 ===")
zh_all = text("index.html")
check("中文页有语言切换组件", "translation nested-menu" in zh_all)
check("切换项显示 displayName", "简体中文" in zh_all and "English" in zh_all)
en_all = text("en/index.html")
check("英文页也有切换组件", "translation nested-menu" in en_all)

print("\n=== 8. 菜单链接都有落点 ===")
for rel in ["index.html", "en/index.html", "posts/hello-world/index.html",
            "en/posts/hello-world/index.html"]:
    bad = []
    for label, href in menu_links(rel):
        target = href.strip("/")
        cand = P / target / "index.html" if target else P / "index.html"
        if not cand.exists():
            bad.append(f"{label}->{href}")
    check(f"{rel} 菜单无悬空链接", not bad, f"悬空 {bad}")

print(f"\n=== 汇总：{ok} 通过 / {fail} 失败 ===")
sys.exit(1 if fail else 0)
