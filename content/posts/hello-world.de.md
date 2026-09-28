---
title: "Hallo Welt: Wie dieser Blog entstanden ist"
date: 2026-09-18
draft: false
summary: "Der erste richtige Beitrag. Ein Überblick über die technischen Entscheidungen hinter diesem Blog und warum er so aussieht, wie er aussieht."
tags: ["Hugo", "GitHub Pages"]
categories: ["Notizen zur Website"]
showTableOfContents: true
bilingual: true
---

Dies ist der erste Beitrag. Statt „Hello World" zu schreiben, lege ich lieber gleich offen, wie dieser Blog technisch aufgebaut ist — das lässt sich später gut nachschlagen.

## Technische Auswahl

| Bereich | Wahl | Warum |
| --- | --- | --- |
| Statischer Site-Generator | Hugo | In Go geschrieben, extrem schnell beim Bauen — selbst tausende Beiträge entstehen in Sekunden |
| Theme | Blowfish | Basiert auf Tailwind CSS, sieht von Anfang an gut aus und lässt Raum für eigene Stile |
| Hosting | GitHub Pages | Kostenlos, ohne Werbung, unterstützt HTTPS und eigene Domains |
| Versionsverwaltung | Git | Jeder Beitrag hat eine Versionsgeschichte, jeder Fehler lässt sich zurückrollen |

## Warum eine statische Website

Bei einem klassischen Blogsystem (etwa WordPress) muss der Server bei jedem Besuch eine Datenbank abfragen und eine Seite zusammenbauen. Eine statische Website erzeugt dagegen alle Seiten bereits beim Build als HTML-Dateien; Anfragen werden direkt beantwortet. Ohne Datenbank kann nichts langsam werden und unter Last nichts umfallen.

Der Preis dafür: Dynamische Funktionen (Kommentare, Likes, Besucherstatistiken) brauchen Drittanbieter-Dienste. Für einen persönlichen Blog lohnt sich dieser Kompromiss in der Regel.

---

In diesem Blog werde ich festhalten, was ich lerne und woran ich arbeite. Wenn auch du überlegst, dir einen eigenen Blog einzurichten, hoffe ich, dass dir das eine oder andere davon nützlich ist.
