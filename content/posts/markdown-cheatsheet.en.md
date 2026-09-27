---
title: "Markdown Cheatsheet for Writing"
date: 2026-09-17
draft: false
summary: "This is all you need to remember for writing posts. Keep it around and look it up when you forget."
tags: ["Markdown", "Writing"]
categories: ["Site Notes"]
showTableOfContents: true
bilingual: true
---

The Markdown you actually need for blogging is a small subset. What follows covers about 95% of real use, and you can copy it straight out.

## Headings

The number of `#` marks the level: `#` is level one, `##` is level two. **In the body, start from level two** — level one is reserved for the post title.

```markdown
## This is a level-two heading
### This is a level-three heading
#### This is a level-four heading
```

## Emphasis

```markdown
**bold**
*italic*
~~strikethrough~~
`inline code`
```

Result: **bold**, *italic*, ~~strikethrough~~, `inline code`.

## Lists

Unordered lists use `-` or `*`; ordered lists use `1.`:

```markdown
- First item
- Second item
  - Nested item (indent two spaces)

1. First step
2. Second step
```

## Links and images

```markdown
[link text](https://example.com)
![image caption](image-url)
```

Images are best kept in a folder named after the post and referenced with a relative path, so they travel together with the post.

## Blockquotes

```markdown
> This is a quote.
> It can span several lines.
```

## Code blocks

Wrap the code in three backticks and name the language right after them — you get syntax highlighting and a copy button in the top-right corner:

````markdown
```python
def hello(name):
    print(f"Hello, {name}!")
```
````

## Tables

```markdown
| Left | Center | Right |
| :--- | :---: | ---: |
| cell | cell | cell |
```

## Horizontal rule

Three hyphens on their own line make a horizontal rule:

```markdown
---
```

## Two small tricks

**Line breaks**: a single newline in Markdown does not start a new line. To force one, put two spaces at the end of the line, or just leave a blank line to start a new paragraph.

**Special characters**: to show `*` or `#` literally instead of as syntax, put a backslash in front — write `\*`.

---

That is about all you need. You do not have to think about syntax while writing; it becomes second nature soon enough.
