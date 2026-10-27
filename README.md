# Template di laboratorio

Punto di partenza per un'esperienza di laboratorio di fisica: analisi dati in Python e relazione in LaTeX, con un agente di programmazione che legge la consegna e adatta il progetto.

## Requisiti

- **Python 3** in un ambiente virtuale (`venv` o conda), non quello di sistema.
- **TeX Live** con `latexmk`.
- **Un agente di programmazione.** Il template è predisposto per [Claude Code](https://claude.com/claude-code), con le skill in `skills/`; con un altro agente vedi [Altri agenti](#altri-agenti).

## Installazione

Una volta sola. Le skill (`/lab`, `/lab:init`, …) si collegano tra le skill utente di Claude Code:

```sh
./skills/install.sh
```

Sono collegamenti alla cartella `skills/` del template: modificarle qui le aggiorna ovunque, e non vengono copiate nelle esperienze.

Python, con `venv` dalla cartella dell'esperienza:

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

1. Crea la cartella dell'esperienza e mettici solo il materiale: consegna, datasheet, manuali.
2. Se hai la scheda del corso, tienila nella cartella superiore (`../setup.yaml`).
3. Apri Claude Code nella cartella e lancia `/lab:init`: applica il template e scrive `proposta.md`.
4. Rispondi in `proposta.md` (dopo **Risposta:**; vuoto = accetto la proposta) e lancia `/lab:setup`.

`/lab` mostra in breve tutti i passi.

## Flusso

| Quando | Cosa | Cosa succede |
|---|---|---|
| a casa | `/lab:init` | template applicato; `proposta.md`: prima stesura della procedura con domande e proposte motivate |
| a casa | rispondi in `proposta.md`, poi `/lab:setup` | risposte confermate; analisi e relazione predisposte; `procedura.md` pronta |
| a casa | `/lab:relazione-init` | parti della relazione che non dipendono dalle misure |
| al banco | segui `procedura.md` e il menu | valori del banco, poi una parte alla volta; il menu propone i punti previsti in ordine |
| finita una parte | `/lab:check <parte>` | analisi della parte e confronto con l'atteso: dice se si può smontare |
| se cambia qualcosa | `/lab:edit <modifica>` | la modifica applicata ad analisi, procedura e schemi; le misure non si toccano |
| dopo le misure | `/lab:relazione` | analisi completa e resto della relazione |
| prima della consegna | `/lab:chiudi` | controllo finale di numeri, segnaposto e stile |

## Comandi da terminale

Dalla cartella dell'esperienza:

```sh
source .venv/bin/activate     # oppure: conda activate lab
python tools/main.py          # menu: valori del banco, misure, annulla, analisi
python tools/main.py all      # tutte le analisi, senza finestre
latexmk                       # compila la relazione -> latex/build/<nome>.pdf
```

## setup.yaml

Scheda breve in YAML, creata da `/lab:init` la prima volta e pensata per essere modificata a mano: corso, autori con matricola, ambiente Python, preferenze, struttura e nome del PDF della relazione, titolo e data dell'esperienza, strumenti con le specifiche di incertezza.

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

- `/lab:init` copia quella del corso e chiede solo ciò che manca o che l'esperienza cambia; se qualcosa vale per tutto il corso, chiede se aggiornare anche quella.
- Se qualcosa cambia, si corregge lì e si lancia `/lab:edit`.
- I valori della singola esperienza (componenti misurati, riferimenti) non stanno qui ma in `tools/config.py`.
- Una copia nella cartella superiore evita di ripetere autori e strumenti a ogni esperienza.

## Cartelle

```
setup.yaml       scheda del setup
proposta.md      domande, proposte e risposte: registro delle scelte
procedura.md     scaletta da seguire al banco, scritta da /lab:setup
docs/            consegna e manuali (non versionati)
data/            misure, un file per parte
tools/           analisi: main.py, una partN.py per parte, instruments.py, config.py, lab.py
results.txt      risultati dell'analisi
latex/           relazione: main.tex, styles.tex, src/, plots/, images/, snippets.tex
.claude/         CLAUDE.md: istruzioni e convenzioni per l'agente
skills/          le skill lab* (solo nel template, non nelle esperienze)
```

## Dati

- Misure inserite a mano: un file per parte, colonne separate da TAB. Il file contiene solo le letture e i loro parametri (per esempio la scala); le incertezze si calcolano a ogni analisi dalle specifiche degli strumenti.
- `Ctrl+C` a metà riga chiede se tenere i valori già inseriti: al prossimo inserimento si riprende da lì.
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

Istruzioni e skill sono file di testo e non dipendono da Claude. Con un altro agente:

- indicagli `.claude/CLAUDE.md` come file di istruzioni, o copialo dove l'agente lo cerca (per esempio `AGENTS.md` nella radice);
- al posto di `/lab:init`, `/lab:setup`, `/lab:check`, ecc., chiedigli di seguire il `SKILL.md` corrispondente in `skills/` del template.

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
