---
title: "Markdown-Kurzreferenz fürs Schreiben"
date: 2026-09-17
draft: false
summary: "Mehr musst du dir fürs Bloggen nicht merken. Behalte diesen Beitrag und schlag nach, wenn du etwas vergessen hast."
tags: ["Markdown", "Schreiben"]
categories: ["Notizen zur Website"]
showTableOfContents: true
bilingual: true
---

Für das Bloggen braucht man erstaunlich wenig Markdown. Das Folgende deckt etwa 95 % der Fälle ab und lässt sich direkt kopieren und anpassen.

## Überschriften

Die Anzahl der `#` gibt die Ebene an: `#` ist Ebene eins, `##` ist Ebene zwei. **Im Textkörper fängst du bei Ebene zwei an** — Ebene eins ist dem Artikeltitel vorbehalten.

```markdown
## Das ist eine Überschrift der Ebene zwei
### Das ist eine der Ebene drei
#### Das ist eine der Ebene vier
```

## Hervorhebung

```markdown
**fett**
*kursiv*
~~durchgestrichen~~
`Inline-Code`
```

Ergebnis: **fett**, *kursiv*, ~~durchgestrichen~~, `Inline-Code`.

## Listen

Aufzählungen nutzen `-` oder `*`, nummerierte Listen `1.`:

```markdown
- Erster Punkt
- Zweiter Punkt
  - Verschachtelter Punkt (zwei Leerzeichen davor)

1. Erster Schritt
2. Zweiter Schritt
```

## Links und Bilder

```markdown
[Linktext](https://example.com)
![Bildbeschreibung](Bildadresse)
```

Bilder gehören am besten in einen Ordner mit demselben Namen wie der Artikel und werden mit relativem Pfad eingebunden — so wandern sie mit dem Artikel mit.

## Zitate

```markdown
> Das ist ein Zitat.
> Es darf mehrere Zeilen haben.
```

## Codeblöcke

Umschließe den Code mit drei Backticks und schreibe die Sprache direkt dahinter — dann wird er automatisch hervorgehoben und oben rechts erscheint eine Kopierschaltfläche:

````markdown
```python
def hello(name):
    print(f"Hello, {name}!")
```
````

## Tabellen

```markdown
| Links | Mitte | Rechts |
| :--- | :---: | ---: |
| Inhalt | Inhalt | Inhalt |
```

## Trennlinie

Drei Bindestriche in einer eigenen Zeile ergeben eine Trennlinie:

```markdown
---
```

## Zwei kleine Kniffe

**Zeilenumbruch**: Ein einzelner Zeilenumbruch zählt in Markdown nicht als Umbruch. Erzwungen wird er mit zwei Leerzeichen am Zeilenende — oder du lässt einfach eine Leerzeile frei und beginnst einen neuen Absatz.

**Sonderzeichen**: Sollen `*` oder `#` wörtlich erscheinen und nicht als Syntax gelten, setzt du einen Backslash davor — also `\*`.

---

Das reicht im Wesentlichen aus. Beim Schreiben musst du nicht über die Syntax nachdenken; mit der Übung kommt sie von selbst.
