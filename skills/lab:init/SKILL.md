---
name: lab:init
description: >-
  Inizializza un'esperienza di laboratorio in una cartella che contiene solo il materiale
  (consegna, datasheet): applica il template, legge la consegna, aggiorna setup.yaml e scrive
  proposta.md con la prima stesura della procedura e le domande per l'utente. Dopo le risposte
  si prosegue con lab:setup. Usare per /lab:init, "inizializza l'esperienza", "prepara la cartella".
---

# lab:init

Lavora nella cartella corrente (la cartella dell'esperienza). Segui `.claude/CLAUDE.md` del progetto (dopo averlo copiato) e le regole di `setup.yaml`.

Se la cartella è già inizializzata (`.claude/CLAUDE.md` o `proposta.md` presenti), non rifare nulla: con `Stato: in attesa di risposte` rimanda a `/lab:setup`, con `Stato: confermata` a `/lab:edit`.

## Template

Il template è la cartella che contiene questa skill, due livelli sopra: `realpath "<cartella della skill>"/../..`. Controlla che contenga `.claude/CLAUDE.md` e `tools/lab.py`. Se non li trova, cerca `_template` risalendo dalla cartella corrente; se non lo trova, chiedi il percorso.

## Passi

1. **Controlla** che la cartella contenga solo il materiale dell'esperienza. Se ci sono file che sembrano di un progetto (`tools/`, `latex/`, `.git/`), fermati e chiedi.
2. **Applica il template**:
   - sposta il materiale in `docs/` con nomi brevi e leggibili (`guida_E2.pdf`, `KSP2222A.pdf`);
   - copia il template senza la sua storia e senza le skill: `rsync -a --exclude .git --exclude skills --exclude .DS_Store "<template>/" ./`;
   - `git init -b main` e primo commit `Init: materiale e template`.
3. **Leggi la consegna** e tutto `docs/`.
4. **setup.yaml**: copia `../setup.yaml` se esiste. Compila ciò che si deduce: titolo, nome del PDF secondo la convenzione del corso, strumenti nuovi citati dalla consegna. Le specifiche mancanti: cercale nei documenti in `docs/`, poi in rete; ogni specifica ha la sua `fonte`, e quelle prese dalla rete si segnalano nella proposta. Non inventare: ciò che non trovi diventa una domanda.
5. **Scrivi `proposta.md`** (formato sotto), fai un commit e fermati. Di' all'utente: rispondi nel file, poi lancia `/lab:setup`.

## Formato di proposta.md

Una procedura già pronta da seguire al banco, con le domande nel punto in cui servono. Breve, in ordine di esecuzione, leggibile a colpo d'occhio nell'anteprima Markdown:

- **matematica in `$...$`** (`$R_1 \parallel R_2$`, `$\dfrac{1}{2\pi R C}$`), mai formule in testo semplice;
- **una domanda = un blocco** con titolo proprio e tre paragrafi separati da righe vuote: Proposta, Motivo, Risposta;
- **il motivo è un elenco puntato**, una ragione per punto;
- **valori in tabella** quando sono più di due (componenti, punto di lavoro atteso, frequenze);
- sezioni separate da `---`.

```markdown
# Proposta — <titolo dell'esperienza>

Stato: in attesa di risposte

Scrivi accanto a **Risposta:**. Vuoto = accetto la proposta. Le domande con "nessuna proposta" vanno risposte.
Poi lancia `/lab:setup`.

---

## Scheda

### D1 · Data dell'esperienza

**Proposta:** nessuna

**Risposta:** 

---

## Progetto

| $V_{CC}$ | $R_E$ | $R_C$ |
|:---:|:---:|:---:|
| 12 V | 1 kΩ | 8.2 kΩ |

### D2 · Capacità d'ingresso

**Proposta:** $C_i = 220\ \text{nF}$

**Motivo:**
- $R_i = R_1 \parallel R_2 \parallel h_{fe} R_E \approx 7 – 8\ \text{k}\Omega$
- $f_T = \dfrac{1}{2\pi\,(R_s + R_i)\,C_i} \approx 100\ \text{Hz}$, come chiede la consegna
- valore commerciale

**Risposta:** 

---

## Piano dell'analisi

| Parte | Si legge | Si calcola e si confronta | Grafico |
|---|---|---|---|
| 1. … | … | … | … |

### D3 · Piano

**Proposta:** approvato così.

**Risposta:** 

---

## Procedura

### Valori del banco
- …

### Parte 1 — …
- montare …; impostare …; leggere …, con tutte le cifre del display
- **Controllo:** se leggi …, controlla …
- A fine parte: analisi della parte, prima di smontare.
```

Regole per le domande:
- **Solo ciò che serve davvero**: dati mancanti, scelte che la consegna lascia libere, specifiche non trovate, aggiornamenti della scheda del corso. Il resto lo decidi tu e lo scrivi nella procedura.
- **Ogni proposta ha il motivo**, breve: vincoli degli strumenti, limiti dei componenti dal datasheet, richieste della consegna, valori commerciali disponibili.
- **Il piano copre tutto ciò che la consegna chiede, riga per riga** (anche andamenti, pendenze, confronti qualitativi), e solo quello. Analisi in più si propongono come domanda separata, non si inseriscono nel piano.
- Una domanda per scelta: niente domande multiple nello stesso numero.
