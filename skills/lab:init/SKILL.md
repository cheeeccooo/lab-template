---
name: lab:init
description: >-
  Inizializza un'esperienza di laboratorio in una cartella che contiene solo il materiale
  (consegna, datasheet): applica il template, legge la consegna, aggiorna setup.yaml e scrive
  proposta.md con la prima stesura della procedura e le domande per l'utente. Rilanciata dopo
  che l'utente ha risposto in proposta.md, conferma le risposte, adatta analisi e relazione e
  scrive procedura.md. Fa tutto ciò che si può fare prima di andare in laboratorio.
  Usare per /lab:init, "inizializza l'esperienza", "prepara la cartella", "ho risposto alla proposta".
---

# lab:init

Lavora nella cartella corrente (la cartella dell'esperienza). Due fasi; la fase si riconosce dallo stato della cartella.

| Stato della cartella | Fase |
|---|---|
| nessun `.claude/CLAUDE.md` | **A** — applicare il template e scrivere `proposta.md` |
| `proposta.md` con `Stato: in attesa di risposte` | **B** — leggere le risposte |
| `proposta.md` con `Stato: confermata` | già inizializzata: fermati e rimanda a `/lab:setup` |

In ogni fase segui `.claude/CLAUDE.md` del progetto (dopo averlo copiato) e le regole di `setup.yaml`.

## Template

Il template è la cartella che contiene questa skill, due livelli sopra: `realpath "<cartella della skill>"/../..`. Controlla che contenga `.claude/CLAUDE.md` e `tools/lab.py`. Se non li trova, cerca `_template` risalendo dalla cartella corrente; se non lo trova, chiedi il percorso.

## Fase A

1. **Controlla** che la cartella contenga solo il materiale dell'esperienza. Se ci sono file che sembrano di un progetto (`tools/`, `latex/`, `.git/`), fermati e chiedi.
2. **Applica il template**:
   - sposta il materiale in `docs/` con nomi brevi e leggibili (`guida_E2.pdf`, `KSP2222A.pdf`);
   - copia il template senza la sua storia e senza le skill: `rsync -a --exclude .git --exclude skills --exclude .DS_Store "<template>/" ./`;
   - `git init -b main` e primo commit `Init: materiale e template`.
3. **Leggi la consegna** e tutto `docs/`.
4. **setup.yaml**: copia `../setup.yaml` se esiste. Compila ciò che si deduce: titolo, nome del PDF secondo la convenzione del corso, strumenti nuovi citati dalla consegna. Le specifiche mancanti: cercale nei documenti in `docs/`, poi in rete; ogni specifica ha la sua `fonte`, e quelle prese dalla rete si segnalano nella proposta. Non inventare: ciò che non trovi diventa una domanda.
5. **Scrivi `proposta.md`** (formato sotto) e fermati. Di' all'utente: rispondi nel file, poi rilancia `/lab:init`.

## Formato di proposta.md

Una procedura già pronta da seguire al banco, con le domande nel punto in cui servono. Breve, in ordine di esecuzione. Ogni domanda ha un numero, una proposta motivata (o "nessuna proposta") e lo spazio per la risposta.

```markdown
# Proposta — <titolo dell'esperienza>

Stato: in attesa di risposte

Rispondi dopo **Risposta:**. Vuoto = accetto la proposta. Le domande con "nessuna proposta" vanno risposte.
Poi rilancia `/lab:init`.

## Scheda

**D1.** Data dell'esperienza? — nessuna proposta
Risposta:

**D2.** Aggiungere l'oscilloscopio X alla scheda del corso `../setup.yaml`? — proposta: sì, servirà anche nelle prossime esperienze.
Risposta:

## Progetto

**D3.** Partitore di base: proposta R1 = 56 kΩ, R2 = 8.2 kΩ (valori commerciali). Motivo: V_B = 1.53 V … corrente nel partitore 10 volte quella di base nel caso peggiore h_fe = 50.
Risposta:

## Piano dell'analisi

Per ogni parte: cosa si legge e con quale strumento, cosa si calcola, con cosa si confronta, com'è il grafico.

**D4.** Approvi il piano? — proposta: sì.
Risposta:

## Procedura

### Valori del banco
- misurare R1, R2, R_C, R_E con il multimetro …

### Parte 1 — …
- montare …; impostare …; leggere …, con tutte le cifre del display
- punti: …
- controllo: se leggi …, controlla …
- a fine parte: analisi della parte, prima di smontare
```

Regole per le domande:
- **Solo ciò che serve davvero**: dati mancanti, scelte che la consegna lascia libere, specifiche non trovate, aggiornamenti della scheda del corso. Il resto lo decidi tu e lo scrivi nella procedura.
- **Ogni proposta ha il motivo**, breve: vincoli degli strumenti, limiti dei componenti dal datasheet, richieste della consegna, valori commerciali disponibili.
- **Il piano copre tutto ciò che la consegna chiede, riga per riga** (anche andamenti, pendenze, confronti qualitativi), e solo quello. Analisi in più si propongono come domanda separata, non si inseriscono nel piano.
- Una domanda per scelta: niente domande multiple nello stesso numero.

## Fase B

1. **Leggi le risposte.** Vuoto = proposta accettata. Una risposta ambigua, o che apre una scelta nuova, diventa una nuova domanda nel file, nello stesso punto: lascia `Stato: in attesa di risposte`, di' all'utente cosa manca e fermati. Le domande già risposte non si ripetono.
2. **Quando tutto è risposto**, applica:
   - `setup.yaml`; se una risposta chiede di aggiornare `../setup.yaml`, aggiornalo;
   - `tools/instruments.py`, `tools/config.py` (valori di progetto, ciascuno con il motivo; `BENCH_FIELDS` per i valori del banco), una `tools/partN.py` per parte e `PARTS` in `main.py`, nell'ordine del banco;
   - `latex/`: struttura scelta in `setup.yaml`, titolo, data, autori, pacchetti richiesti dalle `preferenze`, schemi dei circuiti;
   - `procedura.md`: la sezione "Procedura" di `proposta.md` con le risposte incorporate e senza domande.
3. **Verifica**: con dati inventati controlla che l'analisi giri nell'ambiente di `setup.yaml` e che `latexmk` compili; poi cancella dati di prova e risultati generati.
4. **Chiudi**: in `proposta.md` scrivi `Stato: confermata (GG/MM/AAAA)` e lasciala com'è (è il registro delle scelte e dei loro motivi, usato dalla relazione). Commit `Setup: <titolo>`.
5. **Di' all'utente** che si parte da `procedura.md` e che, se vuole, `/lab:relazione-init` scrive ora le parti della relazione che non dipendono dalle misure.
