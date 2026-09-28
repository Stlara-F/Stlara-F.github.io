---
title: "Guia rápido de Markdown para escrever"
date: 2026-09-17
draft: false
summary: "É só disso que você precisa lembrar para escrever no blog. Guarde este post e consulte quando esquecer."
tags: ["Markdown", "Escrita"]
categories: ["Notas sobre o site"]
showTableOfContents: true
bilingual: true
---

O Markdown necessário para manter um blog é muito pouco. O que vem a seguir cobre cerca de 95% dos casos e pode ser copiado direto.

## Títulos

A quantidade de `#` indica o nível: `#` é o nível um, `##` é o nível dois. **No corpo do texto, comece pelo nível dois** — o nível um fica reservado para o título do post.

```markdown
## Este é um título de nível dois
### Este é um título de nível três
#### Este é um título de nível quatro
```

## Ênfase

```markdown
**negrito**
*itálico*
~~riscado~~
`código em linha`
```

Resultado: **negrito**, *itálico*, ~~riscado~~, `código em linha`.

## Listas

Listas com marcadores usam `-` ou `*`; listas numeradas usam `1.`:

```markdown
- Primeiro item
- Segundo item
  - Item aninhado (dois espaços à frente)

1. Primeiro passo
2. Segundo passo
```

## Links e imagens

```markdown
[texto do link](https://example.com)
![descrição da imagem](endereço da imagem)
```

Vale guardar as imagens numa pasta com o mesmo nome do post e referenciá-las por caminho relativo: assim elas viajam junto com o post.

## Citações

```markdown
> Isto é uma citação.
> Pode ocupar várias linhas.
```

## Blocos de código

Envolva o código em três crases e escreva o nome da linguagem logo depois — a sintaxe é destacada automaticamente e um botão de copiar aparece no canto superior direito:

````markdown
```python
def hello(name):
    print(f"Hello, {name}!")
```
````

## Tabelas

```markdown
| À esquerda | Centralizado | À direita |
| :--- | :---: | ---: |
| conteúdo | conteúdo | conteúdo |
```

## Linha divisória

Três hífens sozinhos numa linha formam uma linha divisória:

```markdown
---
```

## Dois truques pequenos

**Quebra de linha**: no Markdown, uma quebra simples não conta. Para forçá-la, deixe dois espaços no fim da linha — ou simplesmente pule uma linha para começar outro parágrafo.

**Caracteres especiais**: para que `*` ou `#` apareçam literalmente em vez de virarem sintaxe, coloque uma barra invertida antes — escreva `\*`.

---

Com isso já dá para o gasto. Na hora de escrever não é preciso pensar na sintaxe; com a prática ela vem sozinha.
