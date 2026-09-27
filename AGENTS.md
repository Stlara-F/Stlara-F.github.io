# 项目指令

个人博客：Hugo + Blowfish 主题，GitHub Actions 部署到 Pages。
面向使用者的说明都在 README.md，这里只写 agent 工作时要遵守的约定。

## 工作方式：交付最终状态，不记录过程

- 纠正 = 替换。新的要求覆盖旧要求：改配置、改文档时直接替换旧内容，
  不保留被推翻的写法、不追加"原来的说明"。
- 交付物只描述当前事实。代码注释、README、提交说明都只说
  "现在是什么、为什么这样"，不写"曾经错成什么样、后来怎么纠正的"。
- 提交说明写净变化（这次提交之后世界有什么不同），
  不用"修正 / 清除 / 整改 / 根治"这类过程叙事。
- 提交或发 PR 前做极简差异审查：逐块过 diff，凡是对应不上当前需求的
  代码、注释、文档、重构一律删掉。

## 会话收尾（每轮对话结束前）

- 任务清零：做完，或把进行中的长任务与下一步写入 `.zcode/tasks.md` 交接，不静默搁置。
- 工作区不留未处置的新文件：本机工具状态进 `.gitignore`，交付物本地提交，
  本会话的临时产物删除；不许有「未跟踪且未忽略」的文件。
- 后台任务停净；说过的下一步要么做完、要么入册。
- 以上自动决策；`git push` 与发布仍由用户触发（发布走 tools/publish.sh）。

## 项目事实（同一件事只认一处）

| 事实 | 唯一位置 |
| --- | --- |
| Hugo 版本号 | `.github/workflows/hugo.yml` 的 `HUGO_VERSION` |
| 允许的版本区间 | `themes/blowfish/config.toml` 的 `[module.hugoVersion]`，越界由 `tools/check.py` 拦 |
| 用法与个性化说明 | `README.md` |
| 各配置项含义 | `hugo.toml` 行内注释 |
| 语言集合 | `hugo.toml` 的 `[languages]` |
| i18n 规则（命名、目录、复用约束、编辑器两侧的分工） | `docs/i18n.md` |

## 硬约束（违反会直接坏）

- Hugo 必须 extended；本地版本要和 `HUGO_VERSION` 一致
- `baseURL` 结尾斜杠不能少；`timeZone = "Asia/Shanghai"` 不能删（删了当天的文章不显示）
- 主题 vendor 在 `themes/blowfish/`：要改模板就复制到站点根 `layouts/` 同路径再改，不直接动主题
- 社交链接的 email 只填明文地址，主题会自己补 `mailto:`
- `typeit` 短代码不可用：其依赖库不在主题里；要用时先从 Blowfish 上游恢复 `themes/blowfish/assets/lib/typeit/typeit.umd.js`
- `defaultContentLanguageInSubdir` 必须保持 `false`：中文地址是已上线的 `/posts/...`，翻成 `true` 会让它们全部搬家
- 语言代码的大小写分工不能混：`locale = "zh-CN"` 决定 `<html lang>` / `hreflang` / 主题文案的匹配；`[languages.zh-cn]` 的**键名**决定 URL 前缀。写成 `locale = "zh-cn"` 或 `[languages.zh-CN]` 都会错
- 内容的默认语言版本**不加语言后缀**（`about.md`，不是 `about.zh-cn.md`）
- `.workbuddy-ai/`、`.mimosa/` 是本机工具状态：不读、不提交、不写进任何交付物

## 常用命令

- 本地预览：`hugo server`
- 规范检查：`python tools/check.py`
- 构建验证：`hugo --gc --minify --printPathWarnings`
- 发布：`./tools/publish.sh "提交说明"`（自带检查与确认；只检查用 `--check`）
