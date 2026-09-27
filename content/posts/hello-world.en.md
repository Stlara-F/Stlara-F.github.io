---
title: "Hello World: How This Blog Was Built"
date: 2026-09-18
draft: false
summary: "The first real post. A rundown of the technical choices behind this blog, and why it looks the way it does."
tags: ["Hugo", "GitHub Pages"]
categories: ["Site Notes"]
showTableOfContents: true
---

This is the first post. Rather than writing "Hello World", I would rather lay out how this blog is put together — it will be handy to look back on later.

## Technical choices

| Part | Choice | Why |
| --- | --- | --- |
| Static site generator | Hugo | Written in Go, extremely fast to build — thousands of posts still take seconds |
| Theme | Blowfish | Built on Tailwind CSS, good-looking out of the box, and leaves room for custom styles |
| Hosting | GitHub Pages | Free, no ads, supports HTTPS and custom domains |
| Version control | Git | Every post has a history, and any mistake can be rolled back |

## Why a static site

With a traditional blog system (WordPress, say), every visit makes the server query a database and assemble a page. A static site generates all pages into HTML files at build time, so requests are served directly. No database means it cannot get slow or fall over under load.

The trade-off: dynamic features (comments, likes, view counts) need third-party services. For a personal blog, that trade-off is usually worth it.

---

Going forward I will use this blog to record things I learn and work on. If you are thinking about building a blog of your own, I hope some of this is useful.
