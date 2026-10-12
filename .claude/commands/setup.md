---
description: Legge la consegna, crea o riusa setup.txt e adatta tools/ all'esperienza
---

Prepara il progetto per l'esperienza in `docs/`. $ARGUMENTS

## 1. Consegna

Leggi tutto `docs/` (consegna, manuali). Se è vuota, chiedi la consegna.
Riassumi in poche righe: obiettivo, parti, e per ogni parte cosa si misura, cosa si calcola e con cosa si confronta. Segnala le parti solo qualitative e quelle in cui la consegna chiede di progettare qualcosa (scegliere componenti, portate, intervalli).

## 2. setup.txt

`setup.txt` è la scheda del setup: chi, con quali strumenti, con quali valori. È la fonte da cui si adattano `tools/` e `latex/main.tex`.

- **Esiste** in questa cartella: leggilo e non richiedere ciò che contiene.
- **Non esiste qui ma esiste `../setup.txt`** (cartella del corso): copialo qui e trattalo come sopra.
- **Non esiste**: fai le domande e crealo.

In tutti i casi chiedi, in un solo messaggio, solo ciò che manca o che questa esperienza cambia:

- blocchi stabili (di norma già presenti): corso, autori con le rispettive matricole, ambiente Python, strumenti con marca, modello e specifiche di incertezza dal manuale, regole del docente per la relazione;
- blocco `ESPERIENZA` (sempre da aggiornare): titolo, data, grandezze preliminari misurate, valori di riferimento, scelte di procedura che la consegna lascia aperte;
- strumenti usati in questa esperienza e non ancora in elenco;
- per ogni grandezza, **come viene letta**: con quale strumento, in quale forma (picco-picco, ampiezza, valore efficace; cursori o misura automatica) e se a mano o da file salvato dallo strumento. Due strumenti possono dare la stessa grandezza in forme diverse.

Non inventare specifiche: se il manuale non è in `docs/` e l'utente non le fornisce, scrivi `DA DEFINIRE` e segnalalo.

Formato (testo semplice, allineato, leggibile a colpo d'occhio; una riga di spiegazione dove il valore non è ovvio):

```
SETUP
Aggiornato: AAAA-MM-GG

CORSO
  nome            ...
  anno            ...

AUTORI                                  uno per riga, con matricola
  Nome Cognome              1234567
  Nome Cognome              7654321

AMBIENTE
  python          venv .venv            oppure: conda env "NOME". Mai il Python di sistema
  attivazione     source .venv/bin/activate
  analisi         python tools/main.py all
  relazione       latexmk               PDF in latex/build/main.pdf

STRUMENTI
  Oscilloscopio   MARCA MODELLO                     manuale: docs/FILE.pdf
    tensione      3 % lettura (+) 0.04 div          (+) = somma in quadratura
    tempo         0.04 div (+) 50 ppm lettura
  Multimetro      MARCA MODELLO
    tensione DC   0.5 % lettura + 3 digit

CONVENZIONI
  Z-test          compatibile se Z < 2

RELAZIONE
  struttura       sezioni | per parte
  regole          ciò che chiede il docente (lunghezza, teoria sì/no, scadenza...)
  pdf             NOME_FILE.pdf         nome del PDF prodotto da latexmk

ESPERIENZA
  titolo          ...
  data            GG/MM/AAAA
  parti           1) ...   2) ...   3) ... (qualitativa)
  progetto        R = 1 kΩ, C = 10 nF   scelti per f_T ≈ 16 kHz; vedi motivazione
  preliminari     R = 984 Ω       ponte, portata 2 kΩ, risoluzione 1 Ω
  letture         V_in, V_out: oscilloscopio, picco-picco, cursori
  riferimenti     V_gamma = 0.7 ± 0.1 V             datasheet 1N4148
```

Dopo averlo creato, proponi all'utente di tenerne una copia in `../setup.txt` per le prossime esperienze del corso.

## 3. Progetto

Solo se la consegna chiede di scegliere qualcosa. Proponi i valori **prima** che l'utente vada al banco:

- valori nominali disponibili (serie commerciali) e il conto che li giustifica;
- i vincoli che li limitano: resistenza d'uscita del generatore, impedenza d'ingresso e banda degli strumenti, capacità parassite, massimi dei componenti dal datasheet, portate;
- cosa cambia se il valore reale misurato si discosta dal nominale.

Aspetta la conferma dell'utente, poi scrivi la scelta nella riga `progetto` di `setup.txt`.

## 4. Repository pulito

La cartella è una copia del template e ne porta la storia git. Al **primo** setup dell'esperienza va sostituita con una storia nuova:

- se `git log` non contiene alcun commit il cui messaggio inizia con `Setup:`, cancella `.git`, esegui `git init -b main` e, a fine setup, fai il primo commit con messaggio `Setup: <titolo dell'esperienza>`;
- se un commit `Setup:` esiste già, la storia è dell'esperienza: **non toccarla**.

## 5. Adattamento

Da `setup.txt` e dalla consegna:

- `tools/instruments.py`: una funzione per ogni strumento e grandezza usati;
- `tools/config.py`: grandezze preliminari e riferimenti;
- `tools/partN.py`: uno per parte, con `FIELDS` e `analyze()`; aggiorna `PARTS` in `main.py`. Le grandezze salvate su file dallo strumento si leggono con `lab.load_table`;
- `latex/main.tex`: titolo, data, autori nella forma `Nome Cognome (matricola)`;
- `latex/src/`: la struttura scelta in `RELAZIONE` (sei sezioni, oppure una copia di `_parte.tex` per parte).

## 6. Verifica

Con dati di prova controlla che l'analisi giri senza errori nell'ambiente indicato, poi rimuovi i dati di prova e i risultati generati.

## 7. Consegna all'utente

L'elenco delle grandezze da misurare per parte, nell'ordine in cui il menu le chiede, con quanti punti servono e dove.
