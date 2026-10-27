---
name: lab:chiudi
description: >-
  Controllo finale di un'esperienza di laboratorio prima della consegna: rilancia analisi e
  compilazione e verifica numeri, segnaposto, richieste della consegna, preferenze e stile della
  relazione. Usare per /lab:chiudi, "controllo finale", "è pronta da consegnare?".
---

# lab:chiudi

Lavora nella cartella dell'esperienza.

1. Esegui l'analisi (`tools/main.py all` nell'ambiente di `setup.yaml`) e compila con `latexmk`.
2. Verifica e riporta l'esito punto per punto:
   - nessun `[chiave?]` nel PDF (risultato richiamato ma non generato);
   - nessun riferimento `??`, nessun segnaposto (`TITOLO`, `AUTORI`, `CAPTION`, `GG/MM/AAAA`, `PARTE 1`);
   - titolo, data e autori coincidono con `setup.yaml`;
   - ogni numero nel testo coincide con `results.txt`; ogni tabella di misure con `data/`;
   - incertezze a non più di 2 cifre significative, unità presenti;
   - misure escluse (`#!`) dichiarate nel testo con il motivo;
   - ogni scelta del gruppo è motivata, coerente con `docs/proposta.md`;
   - ogni richiesta della consegna ha la sua misura, il suo risultato e, se serve, il suo grafico;
   - nulla che la consegna non chiede e l'utente non ha approvato;
   - nessun riferimento a Python o ai file del progetto;
   - struttura e `preferenze` di `setup.yaml` rispettate;
   - tono e contenuto secondo `.claude/CLAUDE.md`.
3. Correggi ciò che puoi; elenca ciò che richiede una decisione dell'utente. Fai un commit con le correzioni.
