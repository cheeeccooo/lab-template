---
name: lab:relazione-init
description: >-
  Scrive, prima della presa dati, le parti della relazione di laboratorio che non dipendono dalle
  misure: introduzione, scelte di progetto motivate, apparato e procedura, schemi dei circuiti.
  Usare per /lab:relazione-init, "comincia la relazione", "scrivi intanto le parti senza dati".
---

# lab:relazione-init

Lavora nella cartella dell'esperienza, inizializzata con `/lab:init` (`proposta.md` con `Stato: confermata`). Segui le regole della sezione "Relazione" di `.claude/CLAUDE.md` e le `preferenze` di `setup.yaml`.

1. **Fonti**: consegna in `docs/`, `setup.yaml`, `proposta.md` (scelte e loro motivi), `procedura.md`, `tools/config.py`.
2. **Scrivi**, secondo la struttura di `setup.yaml`:
   - `sezioni`: introduzione, apparato, metodi;
   - `per parte`: introduzione breve e, per ogni parte, scelte di progetto e apparato e procedura.
3. **Non scrivere** nulla che dipenda dalle misure: niente sommario, misure, risultati, conclusioni. I valori misurati dei componenti si richiamano con `\res{...}` anche se non ci sono ancora: compariranno come `[chiave?]` fino all'analisi.
4. Schemi da `latex/snippets.tex`, secondo le `preferenze`.
5. Compila con `latexmk`, correggi gli errori e fai un commit. Di' all'utente che il resto si scrive con `/lab:relazione` dopo la presa dati.
