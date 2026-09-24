# 我的博客

用 [Hugo](https://gohugo.io/) 建站，主题是 [Blowfish](https://blowfish.page/)，托管在 GitHub Pages 上。
线上地址：**https://stlara-f.github.io/**

---

## 目录速览

```
blog/
├── hugo.toml              站点配置（标题、配色、菜单、作者信息都在这里改）
├── content/               所有内容
│   ├── _index.md          首页顶部那段文字
│   ├── about.md           关于页
│   └── posts/             文章都放这里
├── assets/
│   ├── css/custom.css     自定义样式，改外观主要改这个文件
│   └── img/avatar.svg     头像
├── static/                原样复制到网站根目录的文件（站点图标在这里）
├── archetypes/default.md  新建文章时套用的模板
├── layouts/               覆盖主题模板用（现在是空的）
├── themes/blowfish/       主题本体（一般不用动）
├── tools/                 检查、发布、生成图标的小脚本
├── public/                构建产物，自动生成，不用管也不用提交
└── .github/workflows/     自动部署脚本
```

两处容易误会的地方：

- `assets/` 下的文件会走 Hugo 的打包管线（按内容加指纹、压缩之后再发布），
  `static/` 下的则是原样复制。所以自定义样式要放 `assets/css/`，不是 `static/`。
- 文章有两种形式：单个 `.md` 文件，或者同名文件夹（`content/posts/文章名/index.md`，
  图片视频和它放在一起）。两者生成的网址完全一样，放媒体时用后者更方便。

---

## 个性化清单（把占位符换成你自己的）

下面这几处现在还是占位内容，**改完提交推送就会自动生效**。大多集中在 `hugo.toml`：

| 想改什么 | 位置（在 `hugo.toml` 里搜） | 现在是什么 |
| --- | --- | --- |
| 站点标题（浏览器标签页 + 页头） | `title =` | `我的博客` |
| 页脚署名 + 文章底部作者卡片 | `[params.author]` → `name =` | `你的名字` |
| 作者卡片里的一句话 | `[params.author]` → `headline =` | `在这里写一句话介绍自己` |
| 作者卡片里的详细介绍 | `[params.author]` → `bio =` | `这里可以写两三句更详细的自我介绍…` |
| 作者头像 | `[params.author]` → `image =` | `img/avatar.svg`（文件在 `assets/img/` 下） |
| 社交链接 | `[params.author]` → `links` | 空数组，写法见下一节 |
| 关于页正文 | `content/about.md` | 示例内容 |
| 首页顶部那段话 | `content/_index.md` | 示例内容。它不设 `title`——设了正文上方会多出一个大标题 |

### 改社交链接

`hugo.toml` 里现在只有一行 `links = []`。把这行**整行替换**成下面这样：

```toml
  links = [
    { github = "https://github.com/你的用户名" },
    { x-twitter = "https://x.com/你的用户名" },
    { email = "你的邮箱" },
  ]
```

两个约定：

- 等号左边的名字就是图标名，取值见 `themes/blowfish/assets/icons/` 下的文件名。
  写错了不会报错，只是那个图标不显示（`tools/check.py` 会替你查出来）。
- `email` 只填邮箱本身。主题会自己编码，带上 `mailto:` 前缀会变成 `mailto:mailto:…`。

改完本地看一眼（见下面「一、本地预览」）：

```bash
hugo server
```

### 换站点图标

图标在 `static/` 下（16/32/ico/apple-touch/android + `site.webmanifest`）。
现在用的是蓝色圆角方块 + 白色字母 **S**。

想换字母或换配色，用这个脚本重新生成一整套：

```bash
# 换字母
python tools/make_favicon.py --letter 博

# 换配色（斜向渐变的两端 + 浏览器主题色）
python tools/make_favicon.py \
    --from "#f472b6" --to "#db2777" --theme-color "#db2777"

# 换标签页里的名字
python tools/make_favicon.py --name "我的博客"
```

> 提示：16×16 是浏览器标签页的实际尺寸，**只有笔画少的字形能认出来**。
> 单个大写字母最稳；中文单字建议选笔画少的（如「一」「山」），
> 像「博」这种十几笔的在小尺寸下会糊成一团。

---

## 一、本地预览

打开终端，进入博客目录后运行：

```bash
hugo server
```

然后浏览器打开 **http://localhost:1313**。

这个服务会一直开着并监听文件变化，你改了文章或配置，保存后浏览器会自动刷新。想停止就按 `Ctrl + C`。

---

## 二、写一篇新文章

在 `content/posts/` 下新建一个 `.md` 文件，例如 `my-first-note.md`。

**文件名会变成网址**，所以用英文加短横线——中文和空格会在网址里变成一串百分号编码。

也可以用命令生成（会自动带上模板，日期也会自动填好）：

```bash
hugo new content content/posts/my-first-note.md
```

> 路径要带上 `content/` 前缀。

文件开头这段叫「front matter」，用来描述这篇文章：

```yaml
---
title: "文章标题"
date: 2026-09-18
draft: false
summary: "一句话摘要，会显示在文章列表里"
tags: ["标签一", "标签二"]
categories: ["分类名"]
---
```

几个关键字段：

| 字段 | 说明 |
| --- | --- |
| `title` | 文章标题，必填 |
| `date` | 发布日期，格式 `年-月-日` |
| `draft` | `true` 是草稿（线上不显示），`false` 才正式发布 |
| `summary` | 摘要，留空则自动截取正文开头 |
| `tags` / `categories` | 标签和分类，会自动生成对应的归档页 |

正文语法看这篇就够了：[Markdown 写作速查表](content/posts/markdown-cheatsheet.md)。

### 内容的三种状态

除了 `draft`，还能用两个日期字段控制文章什么时候上线、什么时候下线。都是 Hugo 自带的行为，不需要额外配置：

| 想要的效果 | 怎么写 | 结果 |
| --- | --- | --- |
| 草稿，先不发布 | `draft: true` | 线上不生成；本地 `hugo server -D` 能看到 |
| 定时发布 | 加 `publishDate: 2026-10-01` | 这个时间点之前的构建都不生成它 |
| 到期自动下架 | 加 `expiryDate: 2026-12-31` | 过了这个时间点就不再生成，文件还留着 |

三者都是**构建时判断**。本站只在推送时构建，所以定时发布不是到点自己跳出来，
而是到点之后的**下一次推送**才出现——写年终总结这类文章时会用到。

---

## 三、改外观

### 换个配色（最简单）

打开 `hugo.toml`，找到 `colorScheme`，换成下面任意一个：

```
autumn  avocado  bloody  blowfish  burufugu  congo  fire  forest
github  marvel   neon    noir      ocean     one-light  princess  slate  terminal
```

改完保存，浏览器会自动刷新。

### 深度定制样式

打开 `assets/css/custom.css`。这个文件在主题样式**之后**加载，所以写在这里的规则会覆盖主题默认值。文件里已经准备好 6 段可直接用的例子（换主色、换字体、调圆角、中文行高、深色模式专属样式、隐藏元素），把注释去掉就能生效。

### 改主题的页面结构

想改 HTML 结构的话：把 `themes/blowfish/layouts/` 里对应的文件，复制到**站点根目录**的 `layouts/` 下的相同路径，再改复制出来的那份。Hugo 会优先使用站点根目录的版本，这样主题升级时你的改动不会被覆盖。

### 其他常用开关

`hugo.toml` 的 `[params]` 下面每一行都带注释，改的时候就在旁边。最常动的几个：

- `defaultAppearance` — 默认明色还是暗色
- `[params.homepage] layout` — 首页样式：`page`（博客列表）/ `profile`（个人名片）/ `hero` / `card` / `background`
- `[params.article] showTableOfContents` — 是否显示文章目录
- `[params.article] sharingLinks` — 文末分享按钮

---

## 四、发布上线

仓库已经建好，Pages 也配好了。日常更新只有一条命令。

### 每次更新

**推荐用发布脚本**，它会在提交前先检查一遍，有问题就不让你提交：

```bash
./tools/publish.sh "新增文章：xxx"
```

流程是：规范检查 → 显示改动 → 让你确认 → 提交 → 推送。

只想看看有没有问题、不提交：

```bash
./tools/publish.sh --check
```

也可以自己敲 git 命令，只是**少了一道检查**：

```bash
git add .
git commit -m "新增文章：xxx"
git push
```

推上去之后，GitHub 会自动重新构建并发布，一两分钟后线上就更新了。

### 规范检查在查什么

`tools/check.py` 是本地和 CI 共用的**同一个脚本**，所以不会出现
「本地过了、线上挂了」这种两边规则对不上的情况。

查这些（**错误会阻断提交，警告只是提醒**）：

| 类别 | 查什么 |
| --- | --- |
| 配置 | `hugo.toml` 是不是合法 TOML（顺带抓「同一个键写两遍」）、`baseURL` 是不是还写着 example.com、`timeZone` 在不在、主题目录完不完整 |
| 版本 | 工作流钉住的 Hugo 版本有没有越出主题声明的区间 |
| 社交链接 | 图标名在主题里有没有对应文件、email 有没有误写 `mailto:` 前缀 |
| 菜单 | 每一项有没有 name 和 url |
| 内容 | front matter 的 title / date 在不在、draft 是不是 true/false |
| 图标 | `site.webmanifest` 引用的文件存不存在 |
| 仓库 | 构建产物（public/）有没有被误提交 |

这张表是分类概览；具体判据以脚本为准，改了脚本就顺手对一下。

单独跑：

```bash
python tools/check.py    # 有问题退出码 1
```

### 线上做了哪些检查

`.github/workflows/hugo.yml` 分三段，按顺序跑：

1. **规范检查** —— 跑 `tools/check.py`，再用 actionlint 把工作流文件自己也查一遍
2. **构建站点** —— 装 Hugo、构建、确认产物里有 `index.html`，
   且首页的 canonical 地址和站点真实网址一致
3. **发布上线** —— 只有推送到 main 才跑

提 PR 时只跑前两段，不会发布，这样能在合并前发现问题。

### Pages 的 Source：GitHub Actions

仓库 **Settings → Pages → Build and deployment → Source** 现在选的是 **GitHub Actions**。

被改成「Deploy from a branch」的话，GitHub 会另外跑一条内置的
`pages build and deployment`，用 **Jekyll** 去构建这个仓库。这是 Hugo 站点，Jekyll 建不了：

```
Liquid Exception: Invalid Date: '{}' is not a valid datetime.
ERROR: YOUR SITE COULD NOT BE BUILT:
```

结果就是每次提交都多一个红叉，而真正决定线上内容的
`部署博客到 GitHub Pages` 那条工作流其实是好的。

确认现在是哪种：

```bash
gh api repos/Stlara-F/Stlara-F.github.io/pages --jq '.build_type'
# "workflow" = 正确（由 Actions 部署）
# "legacy"   = 还在按分支构建，需要去设置里改
```

---

## 五、常见问题

**文章没显示出来？**
按顺序检查三件事：`draft` 是不是还是 `true`；`date` 是不是写成了未来的日期；有没有写 `publishDate` 或 `expiryDate` 把时间卡在范围外。

**`hugo` 命令找不到？**
关掉终端重新开一个（PATH 要新开终端才生效）。

**网址里的中文变成乱码？**
文章文件名用英文。标题写中文没问题；文件名用中文的话，网址里会出现一串百分号编码。

**推送时报 `Repository not found`？**
按顺序查两件事：

1. **仓库建了没有。** 打开 `https://github.com/你的用户名/你的用户名.github.io`，如果是 404，说明仓库还没创建，或者名字拼错了（名字要严格写成 `用户名.github.io`，区分大小写）。
2. **登录的是不是本人。** GitHub 对「你没有权限的仓库」统一返回 404 而不是 403，所以**用错账号登录也会报这个错**。在文件管理器地址栏输入 `%USERPROFILE%` 回车，用记事本打开里面的 `.git-credentials`，看看 `@github.com` 前面的用户名是不是你。不是的话，把那一行删掉，重新推送时就会重新弹登录窗口。

**推送时弹出的登录窗口是什么？**
那是 Git Credential Manager，选 **Sign in with your browser**，在浏览器里登录你的 GitHub 账号并授权即可。

**提交记录里的作者名字不对？**
检查 `git config user.name` 和 `git config user.email`。改完执行一次
`git commit --amend --reset-author --no-edit` 修正最近一次提交。

**样式改了没反应？**
浏览器强制刷新一下（`Ctrl + F5`）。如果还不行，确认改的是 `assets/css/custom.css` 而不是主题目录里的文件。

**代码块在浅色模式下看不清（浅底浅字）？**
检查 `hugo.toml` 里的 `[markup.highlight] noClasses` 是不是 `false`。改成 `true` 的话，Hugo 会把配色直接写死进 HTML，深色和浅色就只能共用一套颜色了。

**想换主题怎么办？**
`hugo.toml` 里的 `theme` 改成新主题目录名，并把新主题放进 `themes/`。不同主题的配置项完全不同，需要重新配。

---

## 技术备忘

- Hugo 版本由 `.github/workflows/hugo.yml` 的 `HUGO_VERSION` 决定，本地装同一个版本
- 允许的上限由主题声明，位置是 `themes/blowfish/config.toml` 的 `[module.hugoVersion]`。
  越界时 Hugo 只发一条警告、构建照样成功，所以这件事由 `tools/check.py` 来拦
- 主题：Blowfish（内置在 `themes/blowfish/`，不是 submodule，可以直接改）
- 部署方式：GitHub Actions，构建产物自动发布到 Pages
