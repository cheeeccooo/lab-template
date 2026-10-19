---
name: lab:relazione
description: >-
  Dopo la presa dati: esegue l'analisi completa dell'esperienza di laboratorio e scrive le parti
  della relazione che dipendono dalle misure (misure, risultati, conclusioni, sommario),
  completando quelle già scritte da lab:relazione-init. Usare per /lab:relazione,
  "scrivi la relazione", "ho finito le misure".
---

# lab:relazione

Lavora nella cartella dell'esperienza. Segui le regole della sezione "Relazione" di `.claude/CLAUDE.md` e le `preferenze` di `setup.yaml`.

1. **Analisi**: esegui `tools/main.py all` con l'interprete dell'ambiente di `setup.yaml`. Controlla che ogni parte abbia dati e risultati; le parti senza dati restano vuote e lo dici all'utente.
2. **Parti senza dati**: se mancano (non è stato lanciato `/lab:relazione-init`), scrivile ora con le stesse regole.
3. **Scrivi** misure, risultati con un commento breve, conclusioni e sommario.
   - Tabelle, figure e schemi da `latex/snippets.tex`; risultati solo con `\res{chiave}`.
   - Misure escluse con `#!`: dichiarate con il motivo.
   - Ogni richiesta della consegna ha la sua misura, il suo risultato e, se serve, il suo grafico.
   - Parti qualitative: foto o schermate da `latex/images/`; se mancano, chiedile.
4. Compila con `latexmk` e correggi errori e riferimenti non risolti.
5. **Rileggi** il testo contro la sezione "Relazione" di `.claude/CLAUDE.md` e taglia ciò che non la rispetta. Fai un commit e proponi `/lab:chiudi`.
