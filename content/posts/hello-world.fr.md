---
title: "Bonjour le monde : les coulisses de ce blog"
date: 2026-09-18
draft: false
summary: "Le premier véritable article. Un tour d'horizon des choix techniques de ce blog et des raisons de son apparence actuelle."
tags: ["Hugo", "GitHub Pages"]
categories: ["Notes sur le site"]
showTableOfContents: true
bilingual: true
---

Voici le premier article. Plutôt que d'écrire « Hello World », je préfère détailler d'emblée comment ce blog est construit — cela me sera utile pour y revenir plus tard.

## Choix techniques

| Élément | Choix | Pourquoi |
| --- | --- | --- |
| Générateur de site statique | Hugo | Écrit en Go, extrêmement rapide à compiler — des milliers d'articles se construisent en quelques secondes |
| Thème | Blowfish | Basé sur Tailwind CSS, joli dès l'installation et laisse la place aux styles personnalisés |
| Hébergement | GitHub Pages | Gratuit, sans publicité, prend en charge HTTPS et les domaines personnalisés |
| Gestion de versions | Git | Chaque article possède son historique, et toute erreur peut être annulée |

## Pourquoi un site statique

Avec un système de blog traditionnel (WordPress, par exemple), chaque visite oblige le serveur à interroger une base de données et à assembler une page. Un site statique génère toutes les pages sous forme de fichiers HTML dès l'étape de construction : les requêtes sont servies directement, et sans base de données, rien ne peut ralentir ni tomber en panne sous la charge.

La contrepartie : les fonctions dynamiques (commentaires, likes, statistiques de visite) nécessitent des services tiers. Pour un blog personnel, ce compromis en vaut généralement la peine.

---

J'utiliserai ce blog pour consigner ce que j'apprends et sur quoi je travaille. Si vous envisagez vous aussi de créer votre propre blog, j'espère que ces lignes vous seront utiles.
