---
description: Legge la consegna, crea o riusa setup.txt e adatta tools/ all'esperienza
---

Prepara il progetto per l'esperienza in `docs/`. $ARGUMENTS

## 1. Consegna

Leggi tutto `docs/` (consegna, manuali). Se è vuota, chiedi la consegna.
Riassumi in poche righe: obiettivo, parti, e per ogni parte cosa si misura, cosa si calcola e con cosa si confronta. Segnala le parti solo qualitative.

## 2. setup.txt

`setup.txt` è la scheda del setup: chi, con quali strumenti, con quali valori. È la fonte da cui si adattano `tools/` e `latex/main.tex`.

- **Esiste** in questa cartella: leggilo e non richiedere ciò che contiene.
- **Non esiste qui ma esiste `../setup.txt`** (cartella del corso): copialo qui e trattalo come sopra.
- **Non esiste**: fai le domande e crealo.

In tutti i casi chiedi, in un solo messaggio, solo ciò che manca o che questa esperienza cambia:

- blocchi stabili (di norma già presenti): corso, autori, ambiente Python, strumenti con marca, modello e specifiche di incertezza dal manuale;
- blocco `ESPERIENZA` (sempre da aggiornare): titolo, data, grandezze preliminari misurate, valori di riferimento, scelte di procedura che la consegna lascia aperte;
- strumenti usati in questa esperienza e non ancora in elenco.

Non inventare specifiche: se il manuale non è in `docs/` e l'utente non le fornisce, scrivi `DA DEFINIRE` e segnalalo.

Formato (testo semplice, allineato, leggibile a colpo d'occhio; una riga di spiegazione dove il valore non è ovvio):

```
SETUP
Aggiornato: AAAA-MM-GG

CORSO
  nome            ...
  anno            ...

AUTORI
  Nome Cognome              matricola

AMBIENTE
  python          conda env "NOME"      mai il Python di sistema
  analisi         conda run -n NOME python tools/main.py all
  relazione       latexmk               PDF in latex/build/main.pdf

STRUMENTI
  Oscilloscopio   MARCA MODELLO                     manuale: docs/FILE.pdf
    tensione      3 % lettura (+) 0.04 div          (+) = somma in quadratura
    tempo         0.04 div (+) 50 ppm lettura
  Multimetro      MARCA MODELLO
    tensione DC   0.5 % lettura + 3 digit

CONVENZIONI
  Z-test          compatibile se Z < 2

ESPERIENZA
  titolo          ...
  data            GG/MM/AAAA
  parti           1) ...   2) ...   3) ... (qualitativa)
  preliminari     R = 984 Ω       ponte, portata 2 kΩ, risoluzione 1 Ω
  riferimenti     V_gamma = 0.7 ± 0.1 V             datasheet 1N4148
```

Dopo averlo creato, proponi all'utente di tenerne una copia in `../setup.txt` per le prossime esperienze del corso.

## 3. Adattamento

Da `setup.txt` e dalla consegna:

- `tools/instruments.py`: una funzione per ogni strumento e grandezza usati;
- `tools/config.py`: grandezze preliminari e riferimenti;
- `tools/partN.py`: uno per parte, con `FIELDS` e `analyze()`; aggiorna `PARTS` in `main.py`;
- `latex/main.tex`: titolo, data, autori.

## 4. Verifica

Con dati di prova controlla che l'analisi giri senza errori nell'ambiente indicato, poi rimuovi i dati di prova e i risultati generati.

## 5. Consegna all'utente

L'elenco delle grandezze da misurare per parte, nell'ordine in cui il menu le chiede, con quanti punti servono e dove.
