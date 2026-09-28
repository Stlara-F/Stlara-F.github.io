---
title: "Mémo Markdown pour écrire"
date: 2026-09-17
draft: false
summary: "C'est tout ce qu'il faut retenir pour écrire des articles. Gardez ce mémo et consultez-le en cas d'oubli."
tags: ["Markdown", "Rédaction"]
categories: ["Notes sur le site"]
showTableOfContents: true
bilingual: true
---

Le Markdown nécessaire pour tenir un blog est en réalité très réduit. Ce qui suit couvre environ 95 % des cas et peut se copier tel quel.

## Titres

Le nombre de `#` indique le niveau : `#` est le niveau un, `##` le niveau deux. **Dans le corps du texte, partez du niveau deux** — le niveau un est réservé au titre de l'article.

```markdown
## Ceci est un titre de niveau deux
### Ceci est un titre de niveau trois
#### Ceci est un titre de niveau quatre
```

## Mise en forme

```markdown
**gras**
*italique*
~~barré~~
`code en ligne`
```

Rendu : **gras**, *italique*, ~~barré~~, `code en ligne`.

## Listes

Les listes à puces utilisent `-` ou `*`, les listes numérotées `1.` :

```markdown
- Premier élément
- Deuxième élément
  - Élément imbriqué (deux espaces devant)

1. Première étape
2. Deuxième étape
```

## Liens et images

```markdown
[texte du lien](https://example.com)
![légende de l'image](adresse de l'image)
```

Les images ont intérêt à être placées dans un dossier portant le nom de l'article et appelées par un chemin relatif : elles suivent ainsi l'article.

## Citations

```markdown
> Ceci est une citation.
> Elle peut tenir sur plusieurs lignes.
```

## Blocs de code

Entourez le code de trois accents graves et indiquez le langage juste après — la coloration s'applique automatiquement et un bouton de copie apparaît en haut à droite :

````markdown
```python
def hello(name):
    print(f"Hello, {name}!")
```
````

## Tableaux

```markdown
| À gauche | Centré | À droite |
| :--- | :---: | ---: |
| contenu | contenu | contenu |
```

## Séparateur

Trois tirets sur une ligne à part forment un séparateur :

```markdown
---
```

## Deux petites astuces

**Saut de ligne** : un simple retour à la ligne ne compte pas en Markdown. Pour l'imposer, tapez deux espaces en fin de ligne — ou laissez simplement une ligne vide pour commencer un nouveau paragraphe.

**Caractères spéciaux** : pour afficher `*` ou `#` littéralement plutôt que comme balise, faites-les précéder d'une barre oblique inversée, en écrivant `\*`.

---

Voilà l'essentiel. Inutile de penser à la syntaxe en écrivant ; à force d'écrire, elle se retient d'elle-même.
