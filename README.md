# Template di laboratorio

Punto di partenza per un'esperienza di laboratorio di fisica: analisi dati in Python e relazione in LaTeX, con un agente di programmazione che legge la consegna e adatta il progetto.

## Requisiti

- **Python 3** in un ambiente virtuale (`venv` o conda), non quello di sistema.
- **TeX Live** con `latexmk`.
- **Un agente di programmazione.** Il template è predisposto per [Claude Code](https://claude.com/claude-code); con un altro agente vedi [Altri agenti](#altri-agenti).

## Installazione

Una volta sola. Con `venv`, dalla cartella dell'esperienza:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Con conda, un ambiente riusabile per tutte le esperienze:

```sh
conda create -n lab python
conda activate lab
pip install -r requirements.txt
```

A ogni nuovo terminale va riattivato l'ambiente: `source .venv/bin/activate` oppure `conda activate lab`.

## Nuova esperienza

1. Copia questa cartella e rinominala.
2. Metti la consegna e i manuali degli strumenti in `docs/`.
3. Se hai già un `setup.yaml` di un'esperienza precedente, mettilo nella cartella superiore (`../setup.yaml`).
4. Apri l'agente nella cartella e lancia `/setup`.

## Flusso

| Passo | Cosa fai | Cosa succede |
|---|---|---|
| `/setup` | rispondi alle domande e approvi il piano | l'agente legge la consegna, crea o riusa `setup.yaml`, ti fa approvare cosa misurare, calcolare e graficare, adatta `tools/` e scrive `procedura.md` |
| misure | segui `procedura.md` e inserisci dal menu | prima i valori del banco, poi una parte alla volta, con l'analisi subito dopo ogni parte |
| `/relazione` | — | introduzione, apparato e metodi si possono scrivere mentre misuri; il resto dopo i dati |
| `/chiudi` | decidi sui punti aperti | controllo finale di numeri, segnaposto e stile |

## Comandi da terminale

Dalla cartella dell'esperienza:

```sh
source .venv/bin/activate     # oppure: conda activate lab
python tools/main.py          # menu: valori del banco, misure, annulla, analisi
python tools/main.py all      # tutte le analisi, senza finestre
latexmk                       # compila la relazione -> latex/build/<nome>.pdf
```

## setup.yaml

Scheda breve in YAML, creata da `/setup` la prima volta e pensata per essere modificata a mano: corso, autori con matricola, ambiente Python, preferenze, struttura e nome del PDF della relazione, titolo e data dell'esperienza, strumenti con le specifiche di incertezza.

```yaml
autori:
  - Nome Cognome, 1234567
python: conda activate lab
preferenze:
  - relazione senza teoria
  - circuiti disegnati con circuitikz
relazione:
  struttura: per parte
  pdf: Mar12_E1
```

`preferenze` è il posto per ogni indicazione stabile su come lavorare (richieste del docente, scelte di stile, pacchetti da usare): l'agente le applica a ogni passo.

- Se esiste, `/setup` non rifà le domande: chiede solo ciò che manca o che l'esperienza cambia.
- Se qualcosa cambia, si corregge lì e si rilancia `/setup`.
- I valori della singola esperienza (componenti misurati, riferimenti) non stanno qui ma in `tools/config.py`.
- Una copia nella cartella superiore evita di ripetere autori e strumenti a ogni esperienza.

## Cartelle

```
setup.yaml       scheda del setup
procedura.md     scaletta da seguire al banco, scritta da /setup
docs/            consegna e manuali (non versionati)
data/            misure, un file per parte
tools/           analisi: main.py, una partN.py per parte, instruments.py, config.py, lab.py
results.txt      risultati dell'analisi
latex/           relazione: main.tex, styles.tex, src/, plots/, images/, snippets.tex
.claude/         CLAUDE.md (istruzioni e convenzioni per l'agente) e i comandi
```

## Dati

- Misure inserite a mano: un file per parte, colonne separate da TAB. Il file contiene solo le letture e i loro parametri (per esempio la scala); le incertezze si calcolano a ogni analisi dalle specifiche degli strumenti.
- `u` nel menu annulla l'ultima modifica ai dati (riga inserita o valori del banco riscritti); ripetuto, torna indietro di più passi.
- File salvati dagli strumenti (CSV dell'oscilloscopio, acquisizioni): si mettono in `data/` così come sono.
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
