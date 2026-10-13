"""
Entry point.

Da eseguire nell'ambiente Python di setup.yaml, mai con quello di sistema.

  python tools/main.py          menu interattivo (valori del banco, misure, analisi con grafici a schermo)
  python tools/main.py all      tutte le analisi, senza finestre
  python tools/main.py part1    una sola parte, senza finestre

Ogni analisi aggiorna results.txt, latex/results.tex e latex/plots/.
"""

import sys

import matplotlib

INTERACTIVE = len(sys.argv) == 1
if not INTERACTIVE:
    matplotlib.use('Agg')

import config as cfg
import lab
import part1

# DA ADATTARE: una voce per ogni parte, nell'ordine in cui si svolgono al banco.
PARTS = [part1]


def _choose(parts):
    """Fa scegliere un file dati tra quelli delle parti."""
    for i, p in enumerate(parts, 1):
        print(f"  {i}) {p.DATA} — {p.TITLE}")
    k = input("File: ").strip()
    return parts[int(k) - 1] if k.isdigit() and 1 <= int(k) <= len(parts) else None


def menu():
    """Voci nell'ordine in cui servono al banco: valori preliminari, misure, analisi."""
    lab.SHOW = True
    with_data = [p for p in PARTS if p.DATA]
    bench = getattr(cfg, 'BENCH_FIELDS', None)
    while True:
        print("\n=== Esperienza ===")
        if bench:
            print("  b) valori del banco (componenti, impostazioni)")
        print("  i) inserisci misure")
        print("  u) annulla l'ultima misura inserita")
        for i, p in enumerate(PARTS, 1):
            print(f"  {i}) analisi: {p.TITLE}")
        print("  a) analisi di tutte le parti")
        print("  0) esci")
        c = input("Scelta: ").strip().lower()
        if c == '0':
            return
        if c == 'b' and bench:
            lab.insert_once(cfg.BENCH_FILE, bench, "Valori del banco")
        elif c == 'i':
            p = _choose(with_data)
            if p:
                lab.insert(p.DATA, p.FIELDS)
        elif c == 'u':
            p = _choose(with_data)
            if p:
                lab.undo(p.DATA)
        elif c == 'a':
            for p in PARTS:
                lab.run(p)
        elif c.isdigit() and 1 <= int(c) <= len(PARTS):
            lab.run(PARTS[int(c) - 1])
        else:
            print("Scelta non valida.")


def main():
    for p in PARTS:
        if p.DATA:
            lab.init_data(p.DATA, p.FIELDS, p.TITLE)
    if INTERACTIVE:
        menu()
        return
    names = {p.__name__: p for p in PARTS}
    for arg in sys.argv[1:]:
        if arg == 'all':
            for p in PARTS:
                lab.run(p)
        elif arg in names:
            lab.run(names[arg])
        else:
            sys.exit(f"Argomento sconosciuto: {arg}. Usare: all, {', '.join(names)}")


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
