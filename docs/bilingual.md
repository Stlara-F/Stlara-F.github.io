# 文章双语对照展示 · 实现计划

**本文是计划，尚未实现。** 需求：同一篇文章的多个语言版本可以**并排对照**阅读，
覆盖中英、中俄、中日等任意两种语言的组合，而不是一次只看一种。

文中标注「实测」的结论来自本仓库外的最小站点验证（Hugo 0.165.0 extended，三语
`zh-cn` / `en` / `ja`），验证方式见 §8。实现完成后，结论并入 `docs/i18n.md`，本文删除。

---

## 1. 方案选择

三条路，实测后选第一条。

| 方案 | 做法 | 客户端 JS | 页面体积 | 结论 |
| --- | --- | --- | --- | --- |
| **A 构建期嵌入** | 文章页在构建时把其他语言版本的正文一并渲染进 HTML，用 CSS 切换显示 | 0 | +（语言版本数 − 1）份正文，只落在开启对照的文章上 | **选它** |
| B 客户端拉取 | 读 `head` 里已有的 `<link rel="alternate">` 找到其他语言版本，点击时 fetch 并提取正文插入 | 约 100 行 | 不变 | 备选 |
| C 独立对照页 | 为每个语言对生成 `/posts/x/compare-zh-cn-en/` | 0 | 每对一份 | **实测不可行** |

**C 为什么不可行**（实测）：Hugo 的 content adapter 执行时站点尚未初始化，
`site.RegularPages` 直接让构建失败：

```
error calling RegularPages: this method cannot be called before the site is fully initialized
```

adapter 只能在构建前**凭空造**页面，看不到已有文章，也就拿不到「这篇文章有哪些语言版本」。
另一条路 `outputFormats` 同样不行——format 的输出路径是静态配置，不支持按语言对生成。

**选 A 的理由**：与项目既有取舍一致（本地化全在构建期完成、客户端 JS 为 0）；
失败在构建期暴露，而不是等读者点了才发现。B 作为备选——如果不想覆盖主题模板，
它是唯一不动模板的做法，代价是引入 JS，且依赖运行期的 HTML 结构稳定。

---

## 2. 数据结构

**不新增数据文件。** 只用两样已有的东西：

| 数据 | 来源 | 说明 |
| --- | --- | --- |
| 有哪些语言版本 | Hugo 的 `.Translations` | 同 basename 自动关联（见 `docs/i18n.md` §10 第一条分歧） |
| 各版本正文 | `.Translations` 里每一项的 `.Content` | 构建期已渲染好的 HTML |

**新增一个 front matter 字段**（可选，写在源文章里）：

```yaml
bilingual: true
```

- 不写 = 不生成对照。多语言文章默认仍是单栏，行为不变。
- `true` = 所有存在的语言版本都可对照，控件里出现「语言版本数 − 1」个选项。

**产物里的 DOM 结构**（由 partial 生成）：

```html
<div class="bi">
  <div class="bi-controls">
    <input type="radio" name="bi-view" id="bi-view-single" checked>
    <label for="bi-view-single">单栏</label>
    <input type="radio" name="bi-view" id="bi-view-en">
    <label for="bi-view-en">English</label>
    <input type="radio" name="bi-view" id="bi-view-ja">
    <label for="bi-view-ja">日本語</label>
  </div>
  <div class="bi-grid">
    <div class="bi-pane is-primary" data-lang="zh-cn">…本页正文…</div>
    <div class="bi-pane" data-lang="en">…英文正文…</div>
    <div class="bi-pane" data-lang="ja">…日文正文…</div>
  </div>
</div>
```

选项名取该语言 `[languages.<键名>].params.displayName`——与主题的语言切换组件同一来源，
加语言时不用另写一份名字。

---

## 3. 需要新增或修改的模块

| 文件 | 动作 | 说明 |
| --- | --- | --- |
| `layouts/_default/single.html` | **新增**（复制主题同名文件后改） | 主题的 139 行原样复制，只把 `{{ .Content }}` 换成条件 partial，约 3 行改动 |
| `layouts/partials/bilingual.html` | **新增** | 渲染控件与 pane；无 `.Translations` 或未开 `bilingual` 时输出空串 |
| `assets/css/custom.css` | 修改 | 对照布局：两栏、折行、深色模式 |
| `content/posts/<slug>/index.md` | 修改 | 加 `bilingual: true` |

**为什么必须复制整个 `single.html`**：Hugo 的模板覆盖是整文件替换，没有「在父模板里插一段」的机制；
Blowfish 也没在正文周围留扩展点——`single.html` 第 56 行直接是 `{{ .Content }}`。
这是项目硬约束里已经写明的代价：改主题模板就复制到站点根再改。

---

## 4. 渲染逻辑

**取哪些语言**：`.Translations` 给出除当前语言外的所有版本，按 `[languages]` 里的 `weight` 排。

**边界**：`.Translations` 为空（单语言文章）或未开 `bilingual` 时，partial 输出空串，
页面产物与改动前**逐字节相同**。这条最重要——它保证绝大多数文章不受影响。

**两种状态**：

| 状态 | 显示 |
| --- | --- |
| 单栏（默认） | 只显示主语言 pane |
| 对照 | 主语言 pane + 目标语言 pane，并排 |

**对齐策略——两栏各自独立，不做逐段配对。** 理由：段落配对要么靠 JS 操作 DOM，
要么靠构建期切分 HTML；后者用 `split .Content "</p>"` 只能近似实现，
列表、表格、代码块这些非 `<p>` 块会附到相邻段落上，切点不稳。
两栏独立是成熟对照工具的常见形态（并排、各自滚动），代价是译文长度差大时要来回找位置。

若以后确实需要逐段对齐，做法是模板里把两侧的 `<p>` 列表**交错输出**成同一个 CSS Grid 的单元格，
短的一侧补空单元格——网格自动两列，每行就是一对。这条路留在以后，不在本次范围。

**已知的冲突**：两侧正文在同一页，标题的 `id`（如 `<h2 id="安装">`）与脚注的 `id`（`#fn:1`）会重复，
浏览器只认第一个，对照侧的锚点跳转因此不可靠。本次接受这个限制——改写正文里的 ID
比它带来的收益风险更高。

---

## 5. 交互方式

**两个动作要分清**：

| 动作 | 是什么 | 入口 |
| --- | --- | --- |
| 语言切换 | 换一个语言看，一次一种 | 主题内置的语言菜单（`translations.html`） |
| 对照展示 | 同时看两种语言 | 本功能新增的控件 |

**控件**：正文上方的单选按钮组——「单栏 / English / 日本語」。radio + label 实现，
**零客户端 JS**，键盘 Tab 可达，选中项由 CSS 的 `:checked ~` 兄弟选择器驱动。

**默认状态**：单栏。对照是显式动作，不改默认阅读体验。

**窄屏**：`< 1024px` 折成上下堆叠，主语言在上。

**对照状态不可分享**：radio 的状态不进 URL，把地址发给别人打开的是单栏。
要可分享得靠 JS 写 hash 或查询参数——本次不做，理由是它会把「零客户端 JS」这个取舍打破，
而对照是临时的阅读动作，不是要分享的地址。

---

## 6. 约束条件

1. **覆盖主题模板**：`single.html` 复制到站点后与主题脱钩，主题升级要手动比对合并。
2. **页面体积**：开启对照的文章，HTML 增加「语言版本数 − 1」份正文。只对声明的文章生效。
3. **锚点与脚注 ID 重复**：见 §4。
4. **同站重复内容**：对照侧的正文与它自己的语言页内容相同。若在意，可在 pane 上加
   `data-nosnippet`；本次不做。
5. **中文 URL 基线不能变**：本功能不新增 URL，`tools/verify_i18n.py` 的基线断言应继续全过。
6. **宽度约束**：`.article-content` 带 `max-w-prose`，对照模式下要放宽，否则两栏各只有半幅。
7. **不引入依赖**：只用 Hugo 模板能力与 CSS，不加 JS 库。
8. **内容仍是两份文件**：对照不改变「一篇一个语言版本」的组织方式，
   不给内容文件增加内嵌多语言的写法。

---

## 7. 测试要点

| # | 测什么 | 期望 |
| --- | --- | --- |
| 1 | 单语言文章（无 `.Translations`） | 产物与改动前**逐字节相同**——最强的回归断言 |
| 2 | 多语言文章但未写 `bilingual` | 不渲染控件，产物与改动前相同 |
| 3 | 双语文章写了 `bilingual: true` | pane 数 = 2，控件选项 = 1 |
| 4 | 三语文章写了 `bilingual: true` | pane 数 = 3，控件选项 = 2，两两都能切 |
| 5 | 选项名 | 取 `displayName`，各语言按自己的叫法显示 |
| 6 | 窄屏 | `< 1024px` 折成上下 |
| 7 | 深色模式 | 两栏边界与文字对比度正常 |
| 8 | 键盘 | Tab 能到控件，方向键能换选项 |
| 9 | 锚点 | 对照打开时目录链接仍指向主语言侧，重复 ID 的行为符合预期 |
| 10 | 现有检查 | `python tools/check.py` 零警告；`python tools/verify_i18n.py` 29 项全过 |
| 11 | 构建 | `hugo --gc --minify --printPathWarnings` 无路径警告 |
| 12 | 体积 | 记录开启前后的 HTML 大小，确认增量与正文量级一致 |

---

## 8. 已实测的依据

在本仓库外的最小站点上验证（Hugo 0.165.0 extended，三语 `zh-cn` / `en` / `ja`，
两篇对照文章分别为 page bundle 的 `index.md` / `index.en.md` / `index.ja.md`）：

| 结论 | 怎么验的 |
| --- | --- |
| 模板里能取到其他语言版本的正文 | `{{ range .Translations }}{{ .Content }}{{ end }}` 在三种语言的页面里都取到了另外两份正文 |
| 语言版本两两可见 | 中文页拿到 en + ja，英文页拿到 zh-cn + ja，日文页拿到 zh-cn + en |
| `--minify` 不破坏对照结构 | minify 后 `data-lang` 与 pane 内容完好 |
| content adapter 看不到已有文章 | `_content.gotmpl` 里调 `site.RegularPages` → 构建失败，报 `this method cannot be called before the site is fully initialized` |
