---
title: "Markdown-konciso por skribado"
date: 2026-09-17
draft: false
summary: "Tion solan vi bezonas memori por blogi. Konservu tiun ĉi afiŝon kaj retrovu ĝin, kiam vi forgesos."
tags: ["Markdown", "Verkado"]
categories: ["Retejaj notoj"]
showTableOfContents: true
bilingual: true
---

La Markdown, kiun vi bezonas por blogi, estas vere malmulte. La sekvaĵo kovras proksimume 95 % de la okazoj kaj estas rekte kopiebla.

## Titoloj

La nombro de `#` montras la nivelon: `#` estas la unua nivelo, `##` la dua. **En la teksto komencu de la dua nivelo** — la unua estas rezervita por la artikola titolo.

```markdown
## Ĉi tio estas titolo de la dua nivelo
### Ĉi tio estas titolo de la tria nivelo
#### Ĉi tio estas titolo de la kvara nivelo
```

## Emfazo

```markdown
**grasa**
*kursiva*
~~forstrekita~~
`enlinia kodo`
```

Rezulto: **grasa**, *kursiva*, ~~forstrekita~~, `enlinia kodo`.

## Listoj

Senordaj listoj uzas `-` aŭ `*`, ordigitaj listoj uzas `1.`:

```markdown
- Unua ero
- Dua ero
  - Enigita ero (du spacoj antaŭe)

1. Unua paŝo
2. Dua paŝo
```

## Ligiloj kaj bildoj

```markdown
[ligila teksto](https://example.com)
![bilda priskribo](bilda adreso)
```

Bildojn plej bone metu en dosierujon samnoman kiel la artikolo kaj referencu per relativa vojo — tiel ili vojaĝas kune kun la artikolo.

## Citaĵoj

```markdown
> Ĉi tio estas citaĵo.
> Ĝi povas enhavi plurajn liniojn.
```

## Kodblokoj

Ĉirkaŭu la kodon per tri malantaŭaj apostrofoj kaj skribu la lingvonomon tuj post ili — la kodo aŭtomate reliefiĝos kaj supre dekstre aperos kopibutono:

````markdown
```python
def hello(name):
    print(f"Hello, {name}!")
```
````

## Tabeloj

```markdown
| Maldekstre | Centre | Dekstre |
| :--- | :---: | ---: |
| enhavo | enhavo | enhavo |
```

## Divida linio

Tri streketoj sur propra linio faras dividan linion:

```markdown
---
```

## Du malgrandaj trukoj

**Linrompo**: unuopa linrompo ne validas en Markdown. Por devigi ĝin, metu du spacojn ĉe la fino de la linio — aŭ simple lasu malplenan linion kaj komencu novan alineon.

**Specialaj signoj**: se vi volas, ke `*` aŭ `#` aperu laŭlitere anstataŭ kiel sintakso, metu antaŭ ĝin malantaŭan oblikvon, skribante `\*`.

---

Memoru ĉi tion kaj sufiĉas. Dum skribado vi ne devas konscie pensi pri la sintakso; ĝi mem enmemoriĝos per praktiko.
