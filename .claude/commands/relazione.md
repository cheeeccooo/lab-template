---
description: Scrive la relazione in latex/src seguendo le convenzioni di .claude/CLAUDE.md
---

Scrivi la relazione. $ARGUMENTS

1. Controlla quali parti hanno già misure in `data/` e risultati in `results.txt`.
2. **Senza dati** si scrivono le parti che non dipendono dalle misure: introduzione, apparato e metodi, oppure introduzione, scelte di progetto, circuito e procedura di ogni parte, secondo la struttura in `setup.yaml`.
3. **Con i dati**: esegui l'analisi (`tools/main.py all` nell'ambiente di `setup.yaml`), poi scrivi misure, risultati, conclusioni e sommario. Le parti ancora senza dati restano vuote: dillo all'utente.
4. Segui le `preferenze` di `setup.yaml`. Tabelle, figure e schemi da `latex/snippets.tex`. Risultati solo con `\res{chiave}`.
5. Parti qualitative: foto o schermate da `latex/images/`; se mancano, chiedile.
6. Compila con `latexmk` dalla cartella del progetto e correggi errori e riferimenti non risolti.
7. Rileggi il testo contro la sezione "Relazione" di `.claude/CLAUDE.md` e taglia ciò che non la rispetta.
