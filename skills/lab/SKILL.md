---
name: lab
description: >-
  Guida breve alla famiglia di skill per le esperienze di laboratorio (analisi in Python e
  relazione in LaTeX): mostra cosa fanno lab:init, lab:setup, lab:check, lab:edit,
  lab:relazione-init, lab:relazione e lab:chiudi e in che ordine si usano. Usare per /lab, "come si usano le
  skill del laboratorio", "da dove parto per una nuova esperienza".
---

# lab

Mostra all'utente il testo qui sotto, così com'è, e non fare altro.

---

**Skill per le esperienze di laboratorio**

Si lanciano dalla cartella dell'esperienza, in quest'ordine:

| Quando | Skill | Cosa fa |
|---|---|---|
| a casa, cartella con solo il materiale | `/lab:init` | applica il template, legge la consegna e scrive `proposta.md`: prima stesura della procedura, con domande e proposte motivate |
| a casa, dopo aver risposto in `proposta.md` | `/lab:setup` | conferma le risposte, prepara analisi e relazione, scrive `procedura.md`; la proposta accettata va in `docs/` |
| a casa, se vuoi | `/lab:relazione-init` | scrive le parti della relazione che non dipendono dalle misure |
| al banco | menu `python tools/main.py` | segui `procedura.md`: valori del banco, misure, `u` annulla, analisi; `Ctrl+C` interrompe e la riga a metà si riprende dopo |
| al banco, finita una parte | `/lab:check <parte>` | analisi della parte e confronto con l'atteso ricalcolato dai valori misurati: dice se si può smontare |
| quando cambia qualcosa | `/lab:edit <modifica>` | applica la modifica ad analisi, procedura e schemi; le misure non si toccano |
| dopo la presa dati | `/lab:relazione` | analisi completa e resto della relazione |
| prima della consegna | `/lab:chiudi` | controllo finale; `latexmk` produce il PDF |

**Come rispondere in `proposta.md`**: scrivi dopo `Risposta:`. Lasciare vuoto vuol dire accettare la proposta; le domande senza proposta richiedono una risposta.

**Scheda del corso**: `setup.yaml` nella cartella superiore (autori, strumenti, preferenze). `/lab:init` la copia nell'esperienza e chiede se aggiornarla quando cambia qualcosa che vale per tutto il corso.

Template e sorgenti delle skill: `Labs/_template` (le skill sono in `skills/`, non vengono copiate nelle esperienze).
