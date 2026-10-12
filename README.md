# Template di laboratorio

Punto di partenza per un'esperienza di laboratorio di fisica: analisi dati in Python e relazione in LaTeX, con un agente di programmazione che legge la consegna e adatta il progetto.

## Requisiti

- **Python 3** in un ambiente virtuale (`venv` o conda), non quello di sistema.
- **TeX Live** con `latexmk`.
- **Un agente di programmazione.** Il template è predisposto per [Claude Code](https://claude.com/claude-code); con un altro agente vedi [Altri agenti](#altri-agenti).

## Installazione

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Con conda: `conda create -n lab python` e poi `pip install -r requirements.txt` nell'ambiente attivo.

## Nuova esperienza

1. Copia questa cartella e rinominala.
2. Metti la consegna e i manuali degli strumenti in `docs/`.
3. Se hai già un `setup.txt` di un'esperienza precedente, mettilo nella cartella superiore (`../setup.txt`).
4. Apri l'agente nella cartella e lancia `/setup`.

## Flusso

| Passo | Cosa fai | Cosa succede |
|---|---|---|
| `/setup` | rispondi alle domande | l'agente legge la consegna, crea o riusa `setup.txt`, ricrea il repository git pulito, adatta `tools/` e ti dice cosa misurare |
| misure | inserisci i valori dal menu | le incertezze si calcolano dalle specifiche degli strumenti e le righe finiscono in `data/` |
| `/relazione` | — | introduzione, apparato e metodi si possono scrivere mentre misuri; il resto dopo i dati |
| `/chiudi` | decidi sui punti aperti | controllo finale di numeri, segnaposto e stile |

## Comandi da terminale

Dalla cartella dell'esperienza, con l'ambiente attivo:

```sh
python tools/main.py          # menu: inserimento misure e analisi con grafici a schermo
python tools/main.py all      # tutte le analisi, senza finestre
latexmk                       # compila la relazione -> latex/build/main.pdf
```

## setup.txt

Scheda del setup, creata da `/setup` la prima volta: corso, autori con matricola, ambiente Python, strumenti con modello e specifiche di incertezza, e i valori dell'esperienza (titolo, data, grandezze preliminari, riferimenti).

- Se esiste, `/setup` non rifà le domande: chiede solo ciò che manca o che l'esperienza cambia.
- È la fonte dei valori: se qualcosa cambia, si corregge lì e si rilancia `/setup`.
- Una copia nella cartella superiore evita di ripetere autori e strumenti a ogni esperienza.

## Cartelle

```
setup.txt        scheda del setup
docs/            consegna e manuali (non versionati)
data/            misure, un file per parte
tools/           analisi: main.py, una partN.py per parte, instruments.py, config.py, lab.py
results.txt      risultati dell'analisi
latex/           relazione: main.tex, styles.tex, src/, plots/, images/, snippets.tex
.claude/         CLAUDE.md (istruzioni e convenzioni per l'agente) e i comandi
```

## Dati

- Un file per parte, colonne separate da TAB, intestazione generata dall'analisi.
- Le misure non si correggono. Per escluderne una: `#!` a inizio riga e il motivo in fondo. Resta nel grafico come punto vuoto.

## Risultati nella relazione

Ogni analisi aggiorna `latex/results.tex`. Nel testo i numeri si richiamano, non si ricopiano:

```latex
$b = (\res{p1b})$ u.m., atteso \res{p1b:ref}, $Z = \res{p1b:z}$
```

## Bibliografia

Spenta di default. Per usarla: togliere il commento alle due righe `biblatex` in `latex/styles.tex` e a `\printbibliography` in `latex/main.tex`, poi aggiungere le voci in `latex/references.bib`.

## Altri agenti

Le istruzioni stanno in `.claude/CLAUDE.md` e i tre comandi in `.claude/commands/`: sono file di testo e non dipendono da Claude. Con un altro agente:

- indicagli `.claude/CLAUDE.md` come file di istruzioni, o copialo dove l'agente lo cerca (per esempio `AGENTS.md` nella radice);
- al posto di `/setup`, `/relazione` e `/chiudi`, chiedigli di seguire il file corrispondente in `.claude/commands/`.

## Errori comuni

**`ModuleNotFoundError: No module named 'uncertainties'`**
L'ambiente virtuale non è attivo, o i pacchetti non ci sono: attivalo e ripeti `pip install -r requirements.txt`.

**`biber: extracting arm64 binary with lipo failed`** (macOS recenti, Apple Silicon, solo con la bibliografia attiva)
Il `biber` di TeX Live non riesce a estrarre la propria parte arm64. Estrarla a mano in una cartella che precede TeX Live nel `PATH`:

```sh
mkdir -p ~/.local/bin && lipo "$(kpsewhich -var-value SELFAUTOLOC)/biber" -thin arm64 -output ~/.local/bin/biber && chmod +x ~/.local/bin/biber
```

Se `which biber` non risponde `~/.local/bin/biber`, aggiungi `export PATH="$HOME/.local/bin:$PATH"` al profilo della shell.

**Nel PDF compare `[chiave?]`**
La relazione richiama un risultato che l'analisi non ha generato: rilancia `python tools/main.py all` e controlla il nome della chiave in `results.txt`.

**`latexmk` si ferma dopo un errore già corretto**
Cancella `latex/build/` e ricompila.

**`dataN.txt: attese N colonne, trovate M`**
Una riga del file dati non corrisponde ai `FIELDS` della parte: correggi la riga, o rigenera il file se i campi sono cambiati.
