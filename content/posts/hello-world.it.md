---
title: "Hello World: come è fatto questo blog"
date: 2026-09-18
draft: false
summary: "Il primo articolo vero. Una panoramica delle scelte tecniche alla base di questo blog e del perché ha l'aspetto che ha."
tags: ["Hugo", "GitHub Pages"]
categories: ["Note sul sito"]
showTableOfContents: true
bilingual: true
---

Questo è il primo articolo. Più che scrivere «Hello World», preferisco spiegare subito com'è costruito tecnicamente questo blog — sarà utile da rileggere in futuro.

## Scelte tecniche

| Parte | Scelta | Perché |
| --- | --- | --- |
| Generatore di siti statici | Hugo | Scritto in Go, velocissimo nella compilazione — anche migliaia di articoli si costruiscono in pochi secondi |
| Tema | Blowfish | Basato su Tailwind CSS, bello fin da subito e con spazio per stili personalizzati |
| Hosting | GitHub Pages | Gratuito, senza pubblicità, supporta HTTPS e domini personalizzati |
| Controllo di versione | Git | Ogni articolo ha una cronologia e qualsiasi errore si può annullare |

## Perché un sito statico

Con un sistema di blog tradizionale (per esempio WordPress), a ogni visita il server deve interrogare un database e assemblare una pagina. Un sito statico genera invece tutte le pagine come file HTML già in fase di build: le richieste vengono servite direttamente e, senza database, non c'è nulla che possa rallentare o crollare sotto carico.

La contropartita: le funzionalità dinamiche (commenti, like, statistiche di visita) richiedono servizi di terze parti. Per un blog personale questo compromesso di solito ne vale la pena.

---

Da qui in avanti userò questo blog per annotare ciò che imparo e su cui lavoro. Se anche tu stai pensando di creare un blog tutto tuo, spero che qualcosa di tutto questo ti sia utile.
