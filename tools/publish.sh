#!/usr/bin/env bash
# ============================================================
#  发布脚本：检查 -> 提交 -> 推送
#
#  用法（在 Git Bash 里，进到博客目录后执行）：
#
#    ./tools/publish.sh "写了一句什么"   # 检查 + 提交 + 推送
#    ./tools/publish.sh                 # 不写说明，会提示你输入
#    ./tools/publish.sh --check         # 只检查，不提交
#
#  它会先跑 tools/check.py。只要有一个「错误」就不让你提交，
#  避免把坏掉的配置推上去、让线上构建失败。
#  警告不会拦你，但会显示出来。
# ============================================================

set -euo pipefail

# ---------------------------------------------------------- 定位仓库根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

# ---------------------------------------------------------- 找 Python
PY=""
for c in python3 python py; do
    if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
    echo "找不到 Python，无法运行规范检查。装好 Python 再试，"
    echo "或者临时用 git 手动提交（不推荐）。"
    exit 1
fi

# ---------------------------------------------------------- 解析参数
MODE="publish"
MSG=""
while [ $# -gt 0 ]; do
    case "$1" in
        --check)   MODE="check"; shift ;;
        -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
        *)         MSG="$1"; shift ;;
    esac
done

# ---------------------------------------------------------- 环境自检
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "当前目录不是 git 仓库：$ROOT"
    exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "仓库目录：$ROOT"
echo "当前分支：$BRANCH"

if [ "$BRANCH" != "main" ]; then
    echo
    echo "你现在不在 main 分支上。"
    echo "只有 main 分支的内容会发布到线上，推别的分支不会更新站点。"
    read -r -p "仍然继续？(y/N) " ans
    [ "$ans" = "y" ] || { echo "已取消"; exit 0; }
fi

# ---------------------------------------------------------- 第一步：检查
echo
echo "── 第一步：规范检查 ────────────────────────────"
if ! "$PY" tools/check.py; then
    echo
    echo "检查没通过，已停止提交。按上面的提示改好再来一次。"
    exit 1
fi

if [ "$MODE" = "check" ]; then
    echo
    echo "只检查模式，到此结束（没有提交任何东西）。"
    exit 0
fi

# ---------------------------------------------------------- 第二步：看改动
echo
echo "── 第二步：待提交的改动 ────────────────────────"
if [ -z "$(git status --porcelain)" ]; then
    echo "没有任何改动，不需要提交。"
    exit 0
fi
git status --short

# ---------------------------------------------------------- 第三步：提交
echo
if [ -z "$MSG" ]; then
    read -r -p "写一句提交说明（说明这次改了什么）： " MSG
    if [ -z "$MSG" ]; then
        echo "提交说明不能为空，已取消。"
        exit 0
    fi
fi

echo
echo "提交说明：$MSG"
read -r -p "确认提交？(y/N) " ans
[ "$ans" = "y" ] || { echo "已取消"; exit 0; }

git add -A
git commit -m "$MSG"

# ---------------------------------------------------------- 第四步：推送
echo
echo "── 第三步：推送到 GitHub ───────────────────────"
git push

echo
echo "完成。GitHub Actions 大约 1 分钟后部署完，"
echo "可以去这里看进度：https://github.com/Stlara-F/Stlara-F.github.io/actions"
