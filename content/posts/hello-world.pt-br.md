---
title: "Hello World: como este blog foi construído"
date: 2026-09-18
draft: false
summary: "O primeiro post de verdade. Um resumo das escolhas técnicas por trás deste blog e do motivo de ele ter a cara que tem."
tags: ["Hugo", "GitHub Pages"]
categories: ["Notas sobre o site"]
showTableOfContents: true
bilingual: true
---

Este é o primeiro post. Em vez de escrever "Hello World", prefiro logo explicar como este blog é montado — vai ser útil para rever depois.

## Escolhas técnicas

| Parte | Escolha | Por quê |
| --- | --- | --- |
| Gerador de site estático | Hugo | Escrito em Go, compila extremamente rápido — milhares de posts levam segundos |
| Tema | Blowfish | Baseado em Tailwind CSS, bonito de fábrica e deixa espaço para estilos personalizados |
| Hospedagem | GitHub Pages | Grátis, sem anúncios, com suporte a HTTPS e domínio próprio |
| Controle de versão | Git | Cada post tem histórico e qualquer erro pode ser desfeito |

## Por que um site estático

Num sistema de blog tradicional (como o WordPress), a cada visita o servidor precisa consultar um banco de dados e montar a página. Num site estático, todas as páginas já são geradas como arquivos HTML durante o build, e as requisições são respondidas diretamente. Sem banco de dados, não há o que ficar lento nem o que cair sob carga.

O preço disso: funcionalidades dinâmicas (comentários, curtidas, estatísticas de acesso) dependem de serviços de terceiros. Para um blog pessoal, esse custo costuma valer a pena.

---

A partir daqui vou usar este blog para registrar o que aprendo e no que trabalho. Se você também está pensando em montar um blog seu, espero que algo aqui seja útil.
