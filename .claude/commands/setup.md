---
description: Legge la consegna, crea o riusa setup.yaml e adatta il progetto all'esperienza
---

Prepara il progetto per l'esperienza in `docs/`. $ARGUMENTS

## 1. Consegna

Leggi tutto `docs/` (consegna, manuali). Se è vuota, chiedi la consegna.
Riassumi in poche righe: obiettivo, parti, e per ogni parte cosa si misura, cosa si calcola e con cosa si confronta. Segnala le parti solo qualitative e quelle in cui la consegna chiede di progettare qualcosa (scegliere componenti, portate, intervalli).

## 2. setup.yaml

Scheda breve di ciò che **non cambia** da un'esperienza all'altra, più due righe sull'esperienza. L'utente la modifica a mano: tienila corta, una riga per valore, niente spiegazioni.

- **Esiste** qui: leggila, non richiedere ciò che contiene.
- **Non esiste qui ma esiste `../setup.yaml`** (cartella del corso): copiala qui.
- **Non esiste**: fai le domande e creala.

Formato:

```yaml
# Scheda del setup: si modifica a mano, poi /setup riallinea il progetto.

corso:   NOME DEL CORSO
gruppo:  SIGLA                  # se il corso la usa
autori:                         # Nome Cognome, matricola
  - Nome Cognome, 1234567
python:  source .venv/bin/activate      # oppure: conda activate NOME

preferenze:                     # scelte dell'utente e richieste del docente, una per riga
  - ...

relazione:
  struttura: sezioni            # sezioni | per parte
  pdf: main                     # nome del PDF prodotto da latexmk

esperienza:
  titolo: "..."
  data: GG/MM/AAAA

strumenti:                      # incertezze dal manuale del modello esatto
  oscilloscopio:
    modello: MARCA MODELLO
    fonte: docs/FILE.pdf        # oppure titolo e link del documento
    V: 0.28 div
    t: 0.016 div
  multimetro:
    modello: MARCA MODELLO
    V_dc: 0.5 % + 3 digit
```

Regole per compilarla:

- Ogni strumento ha la sua `fonte`. Se il manuale non è in `docs/` e prendi le specifiche dalla rete, dillo subito all'utente con il link, prima di usarle.
- Dentro `strumenti` solo ciò che entra in un conto: specifiche di incertezza e caratteristiche che condizionano le misure (impedenze, bande). Un valore sconosciuto si scrive `TODO`: non inventarlo.
- `preferenze` raccoglie in forma breve ogni indicazione stabile su come lavorare: richieste del docente sulla relazione, scelte di stile, strumenti da usare (per esempio "circuiti disegnati con circuitikz", "grafici in scala logaritmica"). Scadenze e logistica non ci vanno.
- I valori dell'esperienza (componenti misurati, riferimenti, scelte di progetto) **non** stanno qui: vanno in `tools/config.py`.

Chiedi, in un solo messaggio, solo ciò che manca:

- voci `TODO` o assenti della scheda;
- titolo e data dell'esperienza;
- strumenti usati in questa esperienza e non ancora in elenco;
- grandezze preliminari già misurate e valori di riferimento;
- per ogni grandezza, **come viene letta**: strumento, forma (picco-picco, ampiezza, valore efficace; cursori o misura automatica), a mano o da file salvato dallo strumento.

Dopo averla creata, proponi di tenerne una copia in `../setup.yaml` per le prossime esperienze del corso.

## 3. Piano

Prima di scrivere codice, presenta all'utente per ogni parte, nell'ordine in cui si farà al banco:

- cosa si legge, con quale strumento e in quale forma;
- cosa si calcola e con cosa si confronta;
- come sarà il grafico (assi, scale, cosa viene sovrapposto).

Tutto ciò che la consegna chiede, riga per riga (anche le verifiche qualitative: andamenti, pendenze, confronti), e solo quello. Se pensi che serva altro (un fit, un parametro in più), proponilo qui come opzione. Aspetta l'approvazione.

## 3b. Preferenze

Applica ogni riga di `preferenze`. Se una richiede un pacchetto LaTeX o Python, aggiungilo (`latex/styles.tex`, ambiente di `python`) e verifica che la compilazione o l'analisi giri ancora. Se una preferenza contraddice `.claude/CLAUDE.md`, vale la preferenza.

## 4. Progetto

Solo se la consegna chiede di scegliere qualcosa. Proponi i valori **prima** che l'utente vada al banco:

- valori nominali disponibili (serie commerciali) e il conto che li giustifica;
- i vincoli che li limitano: resistenza d'uscita del generatore, impedenza d'ingresso e banda degli strumenti, capacità parassite, massimi dei componenti dal datasheet, portate;
- cosa cambia se il valore reale misurato si discosta dal nominale.

Aspetta la conferma dell'utente, poi riporta i valori scelti in `tools/config.py`, ciascuno con un commento che ne dice il motivo: servirà a scrivere le "Scelte di progetto" nella relazione.

## 5. Repository pulito

La cartella è una copia del template e ne porta la storia git. Al **primo** setup dell'esperienza va sostituita con una storia nuova:

- se `git log` non contiene alcun commit il cui messaggio inizia con `Setup:`, cancella `.git`, esegui `git init -b main` e, a fine setup, fai il primo commit con messaggio `Setup: <titolo dell'esperienza>`;
- se un commit `Setup:` esiste già, la storia è dell'esperienza: **non toccarla**.

## 6. Adattamento

- `tools/instruments.py`: una funzione per ogni strumento e grandezza usati, dai valori di `strumenti`;
- `tools/config.py`: valori di progetto, riferimenti e `BENCH_FIELDS` per le grandezze misurate una volta sola (componenti, impostazioni): le chiede il menu, non si scrivono a mano;
- `tools/partN.py`: uno per parte, con `FIELDS` e `analyze()`; aggiorna `PARTS` in `main.py`. I nomi dei campi dicono cosa si legge e dove ("resistore in serie al diodo", non "R del diodo"). Le grandezze salvate su file dallo strumento si leggono con `lab.load_table`;
- `latex/main.tex`: titolo, data, autori nella forma `Nome Cognome (matricola)`;
- `latex/src/`: la struttura scelta in `relazione` (vedi "Struttura" in `.claude/CLAUDE.md`).

## 7. Verifica

Con dati di prova controlla che l'analisi giri senza errori nell'ambiente indicato, poi rimuovi i dati di prova e i risultati generati.

## 8. procedura.md

Scrivi `procedura.md`: la scaletta che l'utente segue al banco, breve, in ordine di esecuzione.

- Prima i valori del banco (voce `b` del menu), poi una sezione per parte.
- Per ogni parte: cosa montare, come impostare gli strumenti, cosa leggere e dove, l'elenco dei punti da prendere (frequenze, tensioni), nell'ordine in cui il menu li chiede.
- Le letture si trascrivono con tutte le cifre del display.
- Uno o due controlli di plausibilità per parte ("se leggi X, controlla Y").
- A fine parte: lanciare l'analisi di quella parte prima di smontare.

Poi di' all'utente che il setup è pronto e di partire da `procedura.md`.
