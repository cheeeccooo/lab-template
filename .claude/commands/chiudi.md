---
description: Controllo finale di analisi e relazione prima della consegna
---

Controllo finale. $ARGUMENTS

1. Esegui l'analisi (`tools/main.py all` nell'ambiente di `setup.yaml`) e compila con `latexmk` dalla cartella del progetto.
2. Verifica e riporta l'esito punto per punto:
   - nessun `[chiave?]` nel PDF (risultato richiamato ma non generato);
   - nessun riferimento `??`, nessun segnaposto (`TITOLO`, `AUTORI`, `CAPTION`, `GG/MM/AAAA`, `PARTE 1`);
   - titolo, data e autori coincidono con `setup.yaml`;
   - ogni numero nel testo coincide con `results.txt`; ogni tabella di misure con `data/`;
   - incertezze a non più di 2 cifre significative, unità presenti;
   - misure escluse (`#!`) dichiarate nel testo con il motivo;
   - ogni elemento o valore scelto dal gruppo è motivato;
   - ogni richiesta della consegna ha la sua misura, il suo risultato e, se serve, il suo grafico;
   - nulla che la consegna non chiede e l'utente non ha approvato;
   - nessun riferimento a Python o ai file del progetto;
   - struttura e `preferenze` di `setup.yaml` rispettate;
   - tono e contenuto secondo `.claude/CLAUDE.md`.
3. Correggi ciò che puoi; elenca ciò che richiede una decisione dell'utente.
