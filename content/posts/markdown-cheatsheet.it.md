---
title: "Prontuario Markdown per scrivere"
date: 2026-09-17
draft: false
summary: "Per scrivere sul blog non serve ricordare altro. Tieni questo articolo e consultalo quando dimentichi qualcosa."
tags: ["Markdown", "Scrittura"]
categories: ["Note sul sito"]
showTableOfContents: true
bilingual: true
---

Il Markdown che serve per tenere un blog è davvero poco. Quello che segue copre circa il 95% dei casi e si può copiare direttamente.

## Titoli

Il numero di `#` indica il livello: `#` è il primo livello, `##` il secondo. **Nel corpo del testo parti dal secondo livello** — il primo è riservato al titolo dell'articolo.

```markdown
## Questo è un titolo di secondo livello
### Questo è un titolo di terzo livello
#### Questo è un titolo di quarto livello
```

## Enfasi

```markdown
**grassetto**
*corsivo*
~~barrato~~
`codice in linea`
```

Risultato: **grassetto**, *corsivo*, ~~barrato~~, `codice in linea`.

## Elenchi

Gli elenchi puntati usano `-` o `*`, quelli numerati `1.`:

```markdown
- Primo elemento
- Secondo elemento
  - Elemento annidato (due spazi davanti)

1. Primo passo
2. Secondo passo
```

## Link e immagini

```markdown
[testo del link](https://example.com)
![descrizione dell'immagine](indirizzo dell'immagine)
```

Le immagini conviene tenerle in una cartella con lo stesso nome dell'articolo e richiamarle con un percorso relativo: così seguono l'articolo.

## Citazioni

```markdown
> Questa è una citazione.
> Può andare su più righe.
```

## Blocchi di codice

Racchiudi il codice tra tre backtick e scrivi subito dopo il nome del linguaggio: la sintassi viene evidenziata da sola e in alto a destra compare un pulsante di copia.

````markdown
```python
def hello(name):
    print(f"Hello, {name}!")
```
````

## Tabelle

```markdown
| A sinistra | Al centro | A destra |
| :--- | :---: | ---: |
| contenuto | contenuto | contenuto |
```

## Linea di separazione

Tre trattini su una riga da soli formano una linea di separazione:

```markdown
---
```

## Due piccoli trucchi

**A capo**: in Markdown un singolo a capo non conta. Per imporlo, metti due spazi a fine riga — oppure lascia semplicemente una riga vuota e inizia un nuovo paragrafo.

**Caratteri speciali**: se vuoi che `*` o `#` compaiano alla lettera invece che come sintassi, mettici davanti una barra rovesciata, scrivendo `\*`.

---

Questo basta e avanza. Mentre scrivi non devi pensare alla sintassi: viene da sé.
