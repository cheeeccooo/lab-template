---
name: lab:check
description: >-
  Controllo al banco dopo aver finito una parte di un'esperienza di laboratorio, prima di smontare:
  esegue l'analisi della parte, ricalcola i valori attesi dai componenti misurati e confronta con
  "Alla fine hai" di procedura.md; dice cosa rifare o aggiungere. Usare per /lab:check <parte>,
  "ho finito la parte 2", "controlla le misure", "posso smontare?".
---

# lab:check

Parte da controllare: $ARGUMENTS (numero o nome; se manca, l'ultima parte con dati nuovi in `data/`).

Lavora nella cartella dell'esperienza. Risposta breve: l'utente è al banco. Non modificare `data/`.

1. **Esegui l'analisi della parte** (`tools/main.py partN` con l'interprete dell'ambiente di `setup.yaml`). Se fallisce per un errore nei dati (colonne, valori non numerici), di' quale riga correggere.
2. **Valori attesi dai valori misurati**: ricalcolali dai componenti del banco (`data/banco.txt`), non dai nominali della consegna o di `procedura.md`. Se il banco non è ancora inserito, dillo: è il primo passo.
3. **Confronta** con il riquadro "Alla fine hai" della parte in `procedura.md`, punto per punto, e con i controlli della procedura:
   - ogni punto previsto è inserito (frequenze, tensioni, righe del banco);
   - i risultati sono compatibili con gli attesi ricalcolati;
   - nessuna riga anomala (fuori andamento, valore fuori scala, segno sbagliato);
   - schermate e file richiesti sono salvati in `latex/images/` o `data/`.
4. **Rispondi** con un elenco, nell'ordine dei passi della parte:
   - ✓ ciò che va bene, con il numero che lo mostra;
   - ✗ ciò che manca o non torna, con l'azione da fare al banco (ripetere quel punto, aggiungere punti tra X e Y, controllare un collegamento);
   - in fondo: **si può smontare** oppure **prima di smontare: …**.
5. Una riga anomala non si cancella e non si corregge: proponi di rimisurarla, o di escluderla con `#!` e il motivo se l'utente lo decide.
