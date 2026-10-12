---
description: Controllo finale di analisi e relazione prima della consegna
---

Controllo finale. $ARGUMENTS

1. Esegui l'analisi (`tools/main.py all` nell'ambiente di `setup.txt`) e compila con `latexmk` dalla cartella del progetto.
2. Verifica e riporta l'esito punto per punto:
   - nessun `[chiave?]` nel PDF (risultato richiamato ma non generato);
   - nessun riferimento `??`, nessun segnaposto (`TITOLO`, `AUTORI`, `CAPTION`, `GG/MM/AAAA`, `PARTE 1`);
   - titolo, data, autori e valori preliminari coincidono con `setup.txt`;
   - ogni numero nel testo coincide con `results.txt`; ogni tabella di misure con `data/`;
   - incertezze a non più di 2 cifre significative, unità presenti;
   - misure escluse (`#!`) dichiarate nel testo con il motivo;
   - nessun riferimento a Python o ai file del progetto;
   - struttura e regole del docente secondo il blocco `RELAZIONE` di `setup.txt`;
   - tono e contenuto secondo `.claude/CLAUDE.md`.
3. Correggi ciò che puoi; elenca ciò che richiede una decisione dell'utente.
