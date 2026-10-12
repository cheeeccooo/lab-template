"""
Entry point.

Da eseguire nell'ambiente Python di setup.txt, mai con quello di sistema.

  python tools/main.py          menu interattivo (inserimento dati, analisi con grafici a schermo)
  python tools/main.py all      tutte le analisi, senza finestre
  python tools/main.py part1    una sola parte, senza finestre

Ogni analisi aggiorna results.txt, latex/results.tex e latex/plots/.
"""

import sys

import matplotlib

INTERACTIVE = len(sys.argv) == 1
if not INTERACTIVE:
    matplotlib.use('Agg')

import lab
import part1

# DA ADATTARE: una voce per ogni parte dell'esperienza.
PARTS = [part1]


def menu():
    lab.SHOW = True
    with_data = [p for p in PARTS if p.DATA]
    while True:
        print("\n=== Analisi dati ===")
        for i, p in enumerate(PARTS, 1):
            print(f"  {i}) {p.TITLE}")
        print("  a) tutte le parti")
        print("  i) inserisci misure")
        print("  0) esci")
        c = input("Scelta: ").strip().lower()
        if c == '0':
            return
        if c == 'a':
            for p in PARTS:
                lab.run(p)
        elif c == 'i':
            for i, p in enumerate(with_data, 1):
                print(f"  {i}) {p.DATA} — {p.TITLE}")
            k = input("File: ").strip()
            if k.isdigit() and 1 <= int(k) <= len(with_data):
                p = with_data[int(k) - 1]
                lab.insert(p.DATA, p.FIELDS)
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
