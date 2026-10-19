---
name: lab:setup
description: >-
  Finalizza l'inizializzazione di un'esperienza di laboratorio dopo lab:init: legge le risposte
  dell'utente in proposta.md, chiede ciò che resta aperto, poi adatta analisi e relazione e scrive
  procedura.md da seguire al banco. Usare per /lab:setup, "ho risposto alla proposta",
  "finalizza il setup".
---

# lab:setup

Lavora nella cartella dell'esperienza. Segui `.claude/CLAUDE.md` del progetto e le regole di `setup.yaml`.

| Stato | Cosa fare |
|---|---|
| nessun `proposta.md` | l'esperienza non è inizializzata: rimanda a `/lab:init` e fermati |
| `proposta.md` con `Stato: in attesa di risposte` | procedi |
| `proposta.md` con `Stato: confermata` | setup già fatto: per cambiare qualcosa rimanda a `/lab:edit` e fermati |

1. **Leggi le risposte.** Vuoto = proposta accettata. Una risposta ambigua, o che apre una scelta nuova, diventa una nuova domanda nel file, nello stesso punto: lascia `Stato: in attesa di risposte`, di' all'utente cosa manca, che rilanci `/lab:setup`, e fermati. Le domande già risposte non si ripetono.
2. **Quando tutto è risposto**, applica:
   - `setup.yaml`; se una risposta chiede di aggiornare `../setup.yaml`, aggiornalo;
   - `tools/instruments.py`, `tools/config.py` (valori di progetto, ciascuno con il motivo; `BENCH_FIELDS` per i valori del banco), una `tools/partN.py` per parte e `PARTS` in `main.py`, nell'ordine del banco;
   - `latex/`: struttura scelta in `setup.yaml`, titolo, data, autori, pacchetti richiesti dalle `preferenze`, schemi dei circuiti;
   - `procedura.md`: la sezione "Procedura" di `proposta.md` con le risposte incorporate e senza domande.
3. **Verifica**: con dati inventati controlla che l'analisi giri nell'ambiente di `setup.yaml` e che `latexmk` compili; poi cancella dati di prova e risultati generati.
4. **Chiudi**: in `proposta.md` scrivi `Stato: confermata (GG/MM/AAAA)` e lasciala com'è (è il registro delle scelte e dei loro motivi, usato dalla relazione). Commit `Setup: <titolo>`.
5. **Di' all'utente** che si parte da `procedura.md` e che, se vuole, `/lab:relazione-init` scrive ora le parti della relazione che non dipendono dalle misure.
