# Laboratorio — istruzioni per l'agente

Ricevi la consegna di un'esperienza in `docs/`. La leggi, chiedi all'utente ciò che manca, adatti gli strumenti di analisi in `tools/` e scrivi la relazione in `latex/`.

## Fasi

| Fase | Chi | Cosa |
|---|---|---|
| 1. Setup | agente, `/setup` | legge la consegna, crea o riusa `setup.txt`, propone il progetto se richiesto, ricrea il repository pulito, adatta `tools/` |
| 2. Misure | utente | inserisce le misure dal menu di `tools/main.py` |
| 3. Analisi | agente | `tools/main.py all`, controlla i risultati |
| 4. Relazione | agente, `/relazione` | scrive `latex/src/`; le parti senza dati si possono scrivere durante la fase 2 |
| 5. Chiusura | agente, `/chiudi` | compila e verifica |

## Regole

- **In dubbio, chiedi.** Non improvvisare su procedura, strumenti o valori.
- **Fai il minimo che serve**, nel modo più diretto.
- **Non inventare nulla**: né misure, né specifiche degli strumenti, né valori di riferimento. Se manca un dato, chiedilo.
- **Le misure non si modificano.** Una misura sbagliata si esclude con `#!` a inizio riga e il motivo in fondo; resta nel grafico come punto vuoto e va dichiarata nella relazione.
- **Le incertezze vengono dal manuale dello strumento** (marca e modello esatti), non da percentuali stimate. Una stima a occhio va dichiarata come tale.
- **Mai il Python di sistema.** Usa l'ambiente indicato in `setup.txt` (blocco `AMBIENTE`); se manca un pacchetto, installalo lì.
- **Adatta tutto all'esperienza.** Numero di parti, colonne, formule, grafici e struttura della relazione seguono la consegna, non il template.

## File

```
setup.txt             scheda del setup: autori e matricole, ambiente, strumenti, valori dell'esperienza
docs/                 consegna, manuali degli strumenti
data/dataN.txt        misure inserite a mano; l'intestazione è generata da FIELDS
data/*.csv            file salvati dagli strumenti, letti con lab.load_table
tools/main.py         menu e riga di comando; elenco PARTS
tools/partN.py        una parte: TITLE, DATA, FIELDS, analyze()
tools/instruments.py  incertezze degli strumenti usati
tools/config.py       grandezze preliminari e valori di riferimento
tools/lab.py          libreria condivisa: non dipende dall'esperienza
results.txt           risultati leggibili, aggiornati a ogni analisi
latex/results.tex     gli stessi risultati come \res{chiave}
latex/plots/          grafici generati       latex/images/  foto e schemi
latex/snippets.tex    schemi di tabelle e figure da copiare
```

- `part1.py` è un esempio: sostituiscilo. Una parte solo qualitativa ha `DATA = None`.
- Se serve una funzione generale che manca, aggiungila a `lab.py`.
- `setup.txt` è la fonte: `instruments.py`, `config.py` e `main.tex` devono coincidere con esso. Se un valore cambia, aggiorna prima `setup.txt`.
- Dipendenze in `requirements.txt`.
- Compilazione: `latexmk` dalla cartella del progetto. Il PDF esce in `latex/build/` con il nome della riga `pdf` di `setup.txt` (default `main.pdf`).

## Relazione

Le regole del docente nel blocco `RELAZIONE` di `setup.txt` prevalgono su quelle qui sotto.

**Tono**
- Essenziale e concisa: il verbale di ciò che si è fatto e trovato.
- Linguaggio semplice, da studente universitario. Terza persona o impersonale.
- Niente riempitivi: avverbi e aggettivi che non aggiungono informazione, frasi di raccordo, premesse.
- Niente metafore, enfasi o termini altisonanti.

**Contenuto**
- Teoria: solo le formule usate nell'analisi, ciascuna con una riga di spiegazione.
- Niente teoria di statistica o di analisi dati: il metodo si nomina (media pesata, fit lineare, Z-test), non si spiega.
- Niente riferimenti a Python, script, programmi o file del progetto.
- Ogni scostamento dal valore atteso ha una causa fisica o strumentale indicata, oppure si dichiara che non è stata individuata.

**Numeri**
- Incertezze con al massimo 2 cifre significative; il valore si arrotonda alla stessa cifra.
- Ogni risultato si richiama con `\res{chiave}`: non si ricopia a mano.
- Unità sempre indicate, con `siunitx`.
- Le tabelle delle misure riportano i valori di `data/`.

**Struttura** (scelta in `setup.txt`)
- `sezioni`: introduzione, apparato, metodi, misure, analisi dati, conclusioni; l'analisi è divisa per parte. File in `latex/src/`.
- `per parte`: una sezione per parte con circuito e procedura, misure, risultati; niente introduzione teorica. Modello in `latex/src/_parte.tex`; i file delle sei sezioni si tolgono.
- Una sezione o un paragrafo senza contenuto si toglie.
