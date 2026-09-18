#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成博客的站点图标（favicon 全套）。

用 Blowfish 期望的文件名输出到站点 static/ 目录：
    favicon-16x16.png  favicon-32x32.png  apple-touch-icon.png
    android-chrome-192x192.png  android-chrome-512x512.png
    favicon.ico  site.webmanifest

设计：圆角方形 + 蓝色斜向渐变 + 白色首字母。
先按 1024px 画，再用 LANCZOS 缩到各尺寸，边缘才干净。

用法：
    python make_favicon.py            # 用默认的 "S"
    python make_favicon.py --letter 博
    python make_favicon.py --bg "#111827" --from "#60a5fa" --to "#2563eb"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

MASTER = 1024
MARGIN_RATIO = 0.06          # 四周留白，浏览器标签页里更好看
RADIUS_RATIO = 0.24          # 圆角半径（相对方块边长）
GLYPH_RATIO = 0.56           # 字母高度（相对方块边长）

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeuib.ttf",   # Segoe UI Bold
    r"C:\Windows\Fonts\arialbd.ttf",    # Arial Bold
    r"C:\Windows\Fonts\msyhbd.ttc",     # 微软雅黑 Bold（中文用）
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def pick_font(size: int, text: str) -> ImageFont.FreeTypeFont:
    """优先挑一个真的能画出这些字的字体。"""
    for path in FONT_CANDIDATES:
        if not Path(path).exists():
            continue
        try:
            font = ImageFont.truetype(path, size)
        except OSError:
            continue
        # 中文要用中文字体，否则会出现豆腐块
        if text.isascii() or Path(path).name.startswith(("msyh", "simhei")):
            return font
    # 全都不行就用默认位图字体兜底
    return ImageFont.load_default(size)


def gradient_square(size: int, c_from: tuple, c_to: tuple) -> Image.Image:
    """画一个斜向线性渐变的方块（先 1px 再放大，省算力）。"""
    grad = Image.new("RGB", (size, size))
    px = grad.load()
    for y in range(size):
        for x in range(size):
            # 左上 → 右下的投影比例
            t = (x + y) / (2 * (size - 1))
            px[x, y] = tuple(
                round(c_from[i] + (c_to[i] - c_from[i]) * t) for i in range(3)
            )
    return grad


def build_master(letter: str, c_from: tuple, c_to: tuple) -> Image.Image:
    """画一张 1024×1024 的母图：圆角方块 + 白色字母。"""
    canvas = Image.new("RGBA", (MASTER, MASTER), (0, 0, 0, 0))

    margin = round(MASTER * MARGIN_RATIO)
    side = MASTER - margin * 2
    radius = round(side * RADIUS_RATIO)

    # 渐变底
    grad = gradient_square(side, c_from, c_to).convert("RGBA")

    # 圆角蒙版
    mask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, side - 1, side - 1),
                                           radius=radius, fill=255)
    canvas.paste(grad, (margin, margin), mask)

    # 白色字母，按实际包围盒居中（不同字体的基线差异很大，必须量）
    target = round(side * GLYPH_RATIO)
    font = pick_font(target, letter)
    draw = ImageDraw.Draw(canvas)
    box = draw.textbbox((0, 0), letter, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    # 把包围盒的几何中心对齐到画布中心
    x = MASTER / 2 - w / 2 - box[0]
    y = MASTER / 2 - h / 2 - box[1]
    draw.text((x, y), letter, font=font, fill=(255, 255, 255, 255))

    return canvas


def find_site_root(start: Path) -> Path:
    """
    从脚本位置往上找，直到看见 hugo.toml —— 那就是站点根目录。
    这样脚本放在 tools/、.workbuddy-ai/tools/ 或任意子目录都能用。
    """
    for candidate in [start, *start.parents]:
        if (candidate / "hugo.toml").exists():
            return candidate
    return start


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None, help="输出目录，默认站点 static/")
    parser.add_argument("--letter", default="S", help="图标里的字符，默认 S")
    parser.add_argument("--from", dest="c_from", default="#60a5fa")
    parser.add_argument("--to", dest="c_to", default="#2563eb")
    parser.add_argument("--theme-color", default="#2563eb")
    parser.add_argument("--name", default="我的博客")
    args = parser.parse_args()

    site = find_site_root(Path(__file__).resolve().parent)
    out = Path(args.out) if args.out else site / "static"
    out.mkdir(parents=True, exist_ok=True)

    master = build_master(args.letter, hex_to_rgb(args.c_from), hex_to_rgb(args.c_to))

    targets = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "apple-touch-icon.png": 180,
        "android-chrome-192x192.png": 192,
        "android-chrome-512x512.png": 512,
    }
    for name, size in targets.items():
        img = master.resize((size, size), Image.LANCZOS)
        img.save(out / name, "PNG", optimize=True)
        print(f"  {name:<30} {size}x{size}")

    # .ico 要多尺寸打包，Windows 才会在大图标/小图标下都清晰
    ico = master.resize((256, 256), Image.LANCZOS)
    ico.save(out / "favicon.ico", format="ICO",
             sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"  {'favicon.ico':<30} 16/32/48/64/128/256")

    manifest = {
        "name": args.name,
        "short_name": args.name,
        "icons": [
            {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": args.theme_color,
        "background_color": "#ffffff",
        "display": "standalone",
    }
    (out / "site.webmanifest").write_text(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"  {'site.webmanifest':<30} name={args.name}")

    print(f"\n输出目录：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
