# Template di laboratorio

Esperienze di laboratorio di fisica, dalla consegna alla relazione: analisi dati in Python e relazione in LaTeX, preparate da un agente di programmazione ([Claude Code](https://claude.com/claude-code)).

Tu porti in laboratorio la consegna; l'agente la legge, ti prepara la procedura da seguire al banco, calcola le incertezze dalle specifiche degli strumenti, fa i grafici e scrive la relazione con le regole del tuo corso.

## Guida rapida

Funziona su macOS e Linux. Su Windows serve [WSL](https://learn.microsoft.com/windows/wsl/install).

### 1. Installa i programmi (una volta sola)

| Programma | A cosa serve | Dove si scarica |
|---|---|---|
| Python 3 | analisi dei dati | [python.org](https://www.python.org/downloads/) |
| TeX Live (o MacTeX su Mac) | relazione in PDF | [tug.org/texlive](https://tug.org/texlive/) · [tug.org/mactex](https://tug.org/mactex/) |
| Claude Code | l'agente che fa il lavoro | [claude.com/claude-code](https://claude.com/claude-code) |
| Git | scaricare il template | già presente su Mac e Linux; altrimenti [git-scm.com](https://git-scm.com/) |

### 2. Scarica il template e attiva le skill (una volta sola)

Apri il Terminale e incolla:

```sh
git clone https://github.com/UTENTE/REPO.git ~/lab-template
cd ~/lab-template
./skills/install.sh
python3 -m venv ~/.venv-lab
source ~/.venv-lab/bin/activate
pip install -r requirements.txt
```

- `install.sh` rende disponibili in Claude Code i comandi `/lab`, `/lab:init`, `/lab:setup`, …
- `~/.venv-lab` è l'ambiente Python usato da tutte le esperienze: il Python di sistema resta pulito.
- Non spostare né cancellare `~/lab-template`: i comandi lo usano ogni volta.

### 3. Prepara le cartelle

Una cartella per il corso, dentro una cartella per ogni esperienza:

```
Laboratorio/          cartella del corso
├── setup.yaml        scheda del corso: la crea /lab:init la prima volta
├── E1/               un'esperienza: dentro metti solo la consegna e i datasheet
└── E2/
```

### 4. Prima di andare in laboratorio

```sh
cd Laboratorio/E1
claude
```

In Claude Code:

1. scrivi `/lab:init`: prepara la cartella e scrive `proposta.md`, con la procedura e alcune domande;
2. apri `proposta.md` e rispondi accanto a **Risposta:** (vuoto = va bene la proposta);
3. scrivi `/lab:setup`: prepara tutto e scrive `procedura.md`, la scaletta per il banco.

La prima volta ti chiede autori, matricole e strumenti del corso, e li salva in `../setup.yaml` per le esperienze successive.

### 5. In laboratorio e dopo

```sh
source ~/.venv-lab/bin/activate
python tools/main.py
```

1. Segui `procedura.md` e inserisci le misure dal menu; `u` annulla l'ultima, `Ctrl+C` interrompe e poi si riprende da lì.
2. Finita una parte, in Claude Code: `/lab:check 1` (2, 3, …) ti dice se puoi smontare.
3. Finite le misure: `/lab:relazione`, poi `/lab:chiudi`.
4. Il PDF si compila con `latexmk` e si trova in `latex/build/`.

`/lab` in Claude Code riassume tutti i passi.

## Tutti i comandi

| Quando | Cosa | Cosa succede |
|---|---|---|
| a casa | `/lab:init` | template applicato; `proposta.md`: prima stesura della procedura con domande e proposte motivate |
| a casa | rispondi in `proposta.md`, poi `/lab:setup` | risposte confermate, proposta accettata spostata in `docs/`; analisi e relazione predisposte; `procedura.md` pronta |
| a casa | `/lab:relazione-init` | parti della relazione che non dipendono dalle misure |
| al banco | segui `procedura.md` e il menu | valori del banco, poi una parte alla volta; il menu ricorda il prossimo punto previsto |
| finita una parte | `/lab:check <parte>` | analisi della parte e confronto con l'atteso: dice se si può smontare |
| se cambia qualcosa | `/lab:edit <modifica>` | la modifica applicata ad analisi, procedura e schemi; le misure non si toccano |
| dopo le misure | `/lab:relazione` | analisi completa e resto della relazione |
| prima della consegna | `/lab:chiudi` | controllo finale di numeri, segnaposto e stile |

## Comandi da terminale

Dalla cartella dell'esperienza:

```sh
source ~/.venv-lab/bin/activate
python tools/main.py          # menu: valori del banco, misure, annulla, analisi
python tools/main.py all      # tutte le analisi, senza finestre
latexmk                       # compila la relazione -> latex/build/<nome>.pdf
```

## setup.yaml

Scheda breve in YAML, creata da `/lab:init` la prima volta e pensata per essere modificata a mano: corso, autori con matricola, ambiente Python, preferenze, struttura e nome del PDF della relazione, titolo e data dell'esperienza, strumenti con le specifiche di incertezza.

```yaml
autori:
  - Nome Cognome, 1234567
python: source ~/.venv-lab/bin/activate
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
proposta.md      domande da rispondere; accettata, va in docs/ come registro delle scelte
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
L'ambiente Python non è attivo: `source ~/.venv-lab/bin/activate`. Se l'errore resta, ripeti `pip install -r requirements.txt` dalla cartella del template.

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

**`/lab:init` non esiste in Claude Code**
Le skill non sono collegate: dalla cartella del template lancia `./skills/install.sh` e riapri Claude Code.

**Preferisco conda a venv**
Va bene anche un ambiente conda al posto di `~/.venv-lab`: crealo con `conda create -n lab python`, attivalo con `conda activate lab` e scrivi quel comando nella voce `python` di `setup.yaml`.
