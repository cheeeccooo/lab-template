# Template di laboratorio

Punto di partenza per un'esperienza di laboratorio: analisi dati in Python e relazione in LaTeX, con un agente (Claude Code) che adatta tutto alla consegna.

## Requisiti

- **Python in un ambiente dedicato**, mai quello di sistema. Pacchetti in `requirements.txt` (`numpy`, `scipy`, `matplotlib`, `uncertainties`).
- **TeX Live** con `latexmk`.
- **Claude Code**, aperto nella cartella dell'esperienza.

## Nuova esperienza

1. Copia questa cartella e rinominala (es. `LabEM2_1`).
2. Metti la consegna e i manuali degli strumenti in `docs/`.
3. Se hai già un `setup.txt` del corso, mettilo nella cartella del corso (`../setup.txt`) o in quella dell'esperienza.
4. Apri Claude Code nella cartella e lancia `/setup`.

## Flusso

| Passo | Cosa fai | Cosa succede |
|---|---|---|
| `/setup` | rispondi alle domande | l'agente legge la consegna, crea o riusa `setup.txt`, adatta `tools/`, ti dice cosa misurare |
| misure | inserisci i valori dal menu | le incertezze si calcolano dalle specifiche degli strumenti e le righe finiscono in `data/` |
| `/relazione` | — | introduzione, apparato e metodi si possono scrivere mentre misuri; il resto dopo i dati |
| `/chiudi` | decidi sui punti aperti | controllo finale di numeri, segnaposto e stile |

## Comandi da terminale

Dalla cartella dell'esperienza, sempre uguali:

```sh
conda activate table          # una volta per terminale; l'ambiente è scritto in setup.txt
python tools/main.py          # menu: inserimento misure e analisi con grafici a schermo
python tools/main.py all      # tutte le analisi, senza finestre
latexmk                       # compila la relazione -> latex/build/main.pdf
```

## setup.txt

Scheda del setup, creata da `/setup` la prima volta: corso, autori, ambiente Python, strumenti con modello e specifiche di incertezza, e i valori dell'esperienza (titolo, data, grandezze preliminari, riferimenti).

- Se esiste, `/setup` non rifà le domande: chiede solo ciò che manca o che l'esperienza cambia.
- È la fonte dei valori: se qualcosa cambia, si corregge lì e si rilancia `/setup`.
- Tenerne una copia nella cartella del corso evita di ripetere autori e strumenti a ogni esperienza.

## Cartelle

```
setup.txt        scheda del setup
docs/            consegna e manuali (non versionati)
data/            misure, un file per parte
tools/           analisi: main.py, una partN.py per parte, instruments.py, config.py, lab.py
results.txt      risultati dell'analisi
latex/           relazione: main.tex, styles.tex, src/, plots/, images/, snippets.tex
CLAUDE.md        istruzioni e convenzioni per l'agente
```

## Dati

- Un file per parte, colonne separate da TAB, intestazione generata dall'analisi.
- Le misure non si correggono. Per escluderne una: `#!` a inizio riga e il motivo in fondo. Resta nel grafico come punto vuoto.

## Risultati nella relazione

Ogni analisi aggiorna `latex/results.tex`. Nel testo i numeri si richiamano, non si ricopiano:

```latex
$b = (\res{p1b})$ u.m., atteso \res{p1b:ref}, $Z = \res{p1b:z}$
```

Un risultato richiamato ma non generato compare nel PDF come `[chiave?]`.

## Bibliografia

Spenta di default. Per usarla: togliere il commento alle due righe `biblatex` in `latex/styles.tex` e a `\printbibliography` in `latex/main.tex`, poi aggiungere le voci in `latex/references.bib`.
