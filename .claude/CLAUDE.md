# Laboratorio — istruzioni per l'agente

Ricevi la consegna di un'esperienza in `docs/`. La leggi, chiedi all'utente ciò che manca, adatti gli strumenti di analisi in `tools/` e scrivi la relazione in `latex/`.

## Fasi

| Fase | Chi | Cosa |
|---|---|---|
| 1. Inizializzazione, a casa | `/lab:init` (due volte) | applica il template; scrive `proposta.md` con domande e proposte; dopo le risposte adatta `tools/` e `latex/` e scrive `procedura.md` |
| 2. Relazione senza dati, a casa | `/lab:relazione-init` | introduzione, scelte di progetto, apparato e procedura |
| 3. Misure, al banco | utente | segue `procedura.md` e inserisce dal menu di `tools/main.py`: valori del banco, poi una parte alla volta, con l'analisi della parte prima di smontare |
| 4. Cambiamenti | `/lab:setup` | riallinea analisi, procedura e schemi se qualcosa cambia rispetto al previsto |
| 5. Relazione | `/lab:relazione` | analisi completa e resto della relazione |
| 6. Chiusura | `/lab:chiudi` | compila e verifica |

Le skill sono nel template (`skills/`), non nel progetto: `/lab` ne dà una guida breve.

## Regole

- **In dubbio, chiedi.** Non improvvisare su procedura, strumenti o valori.
- **Fai ciò che la consegna chiede, non di più.** Fit, parametri, test e grafici che la consegna non chiede si propongono all'utente, non si aggiungono.
- **Non inventare nulla**: né misure, né specifiche degli strumenti, né valori di riferimento. Se manca un dato, chiedilo.
- **Le misure non si modificano.** Una misura sbagliata si esclude con `#!` a inizio riga e il motivo in fondo; resta nel grafico come punto vuoto e va dichiarata nella relazione.
- **Le incertezze vengono dal manuale dello strumento** (marca e modello esatti): il limite dichiarato si usa come σ. Una stima a occhio va dichiarata come tale. Le σ non si ritoccano dopo aver visto un risultato; il χ² si riporta solo se richiesto.
- **Mai il Python di sistema.** Usa l'interprete dell'ambiente indicato in `setup.yaml` (voce `python`); se manca un pacchetto, installalo lì.
- **Le `preferenze` di `setup.yaml` valgono sempre**, anche contro le convenzioni di questo file.
- **Adatta tutto all'esperienza.** Numero di parti, colonne, formule, grafici e struttura della relazione seguono la consegna, non il template.

## File

```
setup.yaml            scheda del setup: corso, autori, ambiente, preferenze, strumenti
proposta.md           domande, proposte e risposte: registro delle scelte e dei loro motivi
procedura.md          scaletta da seguire al banco, scritta da /lab:init
docs/                 consegna, manuali degli strumenti
data/banco.txt        valori misurati una volta sola (componenti, impostazioni)
data/dataN.txt        letture inserite a mano; solo valori e parametri, le incertezze si calcolano al caricamento
data/*.csv            file salvati dagli strumenti, letti con lab.load_table
tools/main.py         menu e riga di comando; elenco PARTS
tools/partN.py        una parte: TITLE, DATA, FIELDS, analyze()
tools/instruments.py  incertezze degli strumenti usati
tools/config.py       valori dell'esperienza: grandezze preliminari, progetto, riferimenti
tools/lab.py          libreria condivisa: non dipende dall'esperienza
results.txt           risultati leggibili, aggiornati a ogni analisi
latex/results.tex     gli stessi risultati come \res{chiave}
latex/plots/          grafici generati       latex/images/  foto e schemi
latex/snippets.tex    schemi di tabelle e figure da copiare
```

- `part1.py` è un esempio: sostituiscilo. Una parte solo qualitativa ha `DATA = None`.
- Le parti in `PARTS` e i campi in `FIELDS` seguono l'ordine in cui si lavora al banco.
- Se serve una funzione generale che manca, aggiungila a `lab.py`.
- `setup.yaml` è la fonte per autori, titolo, data e specifiche degli strumenti: `instruments.py` e `main.tex` devono coincidere con esso.
- Dipendenze in `requirements.txt`.
- Compilazione: `latexmk` dalla cartella del progetto. Il PDF esce in `latex/build/` con il nome della voce `pdf` di `setup.yaml` (default `main.pdf`).

## Relazione

Le `preferenze` di `setup.yaml` prevalgono su quanto segue.

**Tono**
- Essenziale e concisa: il verbale di ciò che si è fatto e trovato.
- Linguaggio semplice, da studente universitario. Terza persona o impersonale.
- Niente riempitivi: avverbi e aggettivi che non aggiungono informazione, frasi di raccordo, premesse.
- Niente frasi sull'esperienza in sé ("l'esperienza serve a…"): si apre con ciò che si studia.
- Niente metafore, enfasi o termini altisonanti.

**Contenuto**
- Teoria: solo le formule usate nell'analisi, ciascuna con una riga di spiegazione.
- Niente teoria di statistica o di analisi dati: il metodo si nomina (media pesata, fit lineare, Z-test), non si spiega.
- Niente riferimenti a Python, script, programmi o file del progetto.
- Uno scostamento non compatibile con l'atteso ha una causa fisica o strumentale indicata, oppure si dichiara che non è stata individuata. Un risultato compatibile non si giustifica.
- Solo ciò che si è misurato o fatto: niente stime di effetti non misurati, dettagli di cablaggio, elenchi di ciò che non si è fatto.

**Numeri**
- Incertezze con al massimo 2 cifre significative; il valore si arrotonda alla stessa cifra.
- Ogni risultato si richiama con `\res{chiave}`: non si ricopia a mano.
- Unità sempre indicate, con `siunitx`.
- Le tabelle delle misure riportano i valori di `data/`.

**Struttura** (scelta in `setup.yaml`)
- `sezioni`: sommario, introduzione, apparato, metodi, misure, analisi dati, conclusioni; l'analisi è divisa per parte.
- `per parte`: sommario, introduzione breve, una sezione per parte, conclusioni brevi.
  - Sommario: 3-5 frasi con i risultati numerici principali.
  - Introduzione: cosa si studia, elenco delle parti, criterio di confronto. Niente teoria. Si parte da `1_Introduction.tex` togliendo i paragrafi delle formule.
  - Ogni parte (modello `latex/src/_parte.tex`): scelte di progetto (il motivo, senza percentuali stimate), apparato e procedura, misure, risultati con un commento breve a ciò che si osserva.
  - Conclusioni: risultati finali in riga e poche osservazioni generali. Si parte da `6_Conclusions.tex`.
  - I file delle sezioni 2-5 si tolgono.
- **Scelte di progetto**: quando la consegna lascia liberi elementi o valori, ogni scelta va riportata e motivata nella parte a cui appartiene.
- Figure e tabelle restano nel punto in cui sono citate (`[H]`). I grafici occupano quasi tutta la larghezza del testo.
- Una sezione o un paragrafo senza contenuto si toglie.
