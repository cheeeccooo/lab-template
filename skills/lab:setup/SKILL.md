---
name: lab:setup
description: >-
  Riallinea un'esperienza di laboratorio già inizializzata con lab:init quando qualcosa cambia
  rispetto al previsto (componenti diversi dal progetto, strumento diverso, punti o parti in più,
  setup.yaml modificato a mano): aggiorna analisi, procedura e schemi senza toccare le misure.
  Usare per /lab:setup, "è cambiato il circuito", "al banco c'è un altro strumento",
  "ho modificato setup.yaml", "riallinea il progetto".
---

# lab:setup

Lavora nella cartella dell'esperienza. Se non c'è `proposta.md` con `Stato: confermata`, l'esperienza non è inizializzata: rimanda a `/lab:init` e fermati.

1. **Capisci cosa è cambiato**: confronta `setup.yaml`, `proposta.md`, `procedura.md` e `tools/` con quanto ti dice l'utente; se non lo dice, chiediglielo in un solo messaggio.
2. **Aggiorna solo ciò che il cambiamento tocca**:
   - `setup.yaml` per strumenti e specifiche (con la `fonte`); se vale per tutto il corso, chiedi se aggiornare anche `../setup.yaml`;
   - `tools/` (strumenti, valori di progetto, campi, parti), mantenendo l'ordine del banco;
   - `procedura.md` e gli schemi in `latex/`;
   - in `proposta.md` aggiungi in fondo una sezione `## Modifiche` con data, cosa è cambiato e perché.
3. **Le misure non si toccano**: niente modifiche a `data/`. Se un cambiamento rende incompatibili le righe già inserite (colonne diverse), fermati e chiedi come procedere.
4. **Verifica** che l'analisi giri e la relazione compili, poi fai un commit che descrive il cambiamento.
