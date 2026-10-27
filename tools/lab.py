"""
Libreria condivisa: dati, incertezze, statistica, grafici, risultati.

NON si adatta all'esperienza. Ciò che cambia da un'esperienza all'altra sta in
instruments.py, config.py e nei part*.py.
"""

import contextlib
import io
import os
import sys
import warnings

import numpy as np
from uncertainties import correlated_values, ufloat
from uncertainties import unumpy as unp

warnings.filterwarnings('ignore', message='Using UFloat objects with std_dev==0')

ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(ROOT, 'data')
PLOTS_DIR   = os.path.join(ROOT, 'latex', 'plots')
RESULTS_TXT = os.path.join(ROOT, 'results.txt')
RESULTS_TEX = os.path.join(ROOT, 'latex', 'results.tex')

SHOW  = False   # True: apre la finestra del grafico dopo averlo salvato
Z_MAX = 2.0     # soglia di compatibilità dello Z-test


_results = []   # (chiave, testo LaTeX) della parte in esecuzione


class LabError(Exception):
    """Errore atteso (file vuoto, colonne sbagliate): si stampa senza traceback."""


# =====================================================
# DATI
# =====================================================

class Field:
    """Una grandezza letta = una colonna del file dati (più, se serve, il suo parametro).

    name  : nome della colonna, usato anche come chiave in load()
    unit  : unità di misura
    sigma : None            -> nessuna incertezza (es. indice, etichetta, impostazione)
            numero          -> incertezza costante
            f(valore)       -> incertezza calcolata dal valore
            f(valore, x)    -> come sopra, con un parametro x letto insieme al valore
    ask   : testo con cui chiedere x (es. 'scala verticale [V/div]')
    label : cosa è la grandezza, in poche parole (es. 'ingresso, picco-picco, CH1'):
            compare quando si inserisce e nell'intestazione del file

    Nel file si salvano solo le letture e i parametri: l'incertezza si calcola a ogni
    caricamento, quindi cambiare una funzione di instruments.py aggiorna tutti i dati.
    """

    def __init__(self, name, unit='', sigma=None, ask=None, label=''):
        self.name, self.unit, self.sigma, self.ask, self.label = name, unit, sigma, ask, label

    def prompt(self):
        text = self.name + (f" — {self.label}" if self.label else '')
        return f"{text} [{self.unit}]" if self.unit else text

    def error(self, value, par=None):
        if self.sigma is None:
            return None
        if callable(self.sigma):
            return float(self.sigma(value, par) if self.ask else self.sigma(value))
        return float(self.sigma)


def _columns(fields):
    cols = []
    for f in fields:
        cols.append(f"{f.name}[{f.unit}]" if f.unit else f.name)
        if f.ask:
            cols.append(f"p_{f.name}")
    return cols


def _path(filename):
    return os.path.join(DATA_DIR, filename)


def init_data(filename, fields, title=''):
    """Crea data/<filename> con l'intestazione delle colonne, se non esiste."""
    if os.path.exists(_path(filename)):
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_path(filename), 'w') as f:
        if title:
            f.write(f"# {title}\n")
        f.write("# Solo letture, separate da TAB (p_ = parametro della lettura, es. scala)."
                " Per escludere una misura: '#!' a inizio riga e il motivo in fondo.\n")
        for fl in fields:
            if fl.label:
                f.write(f"#   {fl.name}: {fl.label}" + (f"; p_{fl.name}: {fl.ask}" if fl.ask else '') + "\n")
        f.write("# " + "\t".join(_columns(fields)) + "\n")


def _parse(line, ncols, filename, trailing_text=False):
    tokens = line.split('#')[0].split()
    if trailing_text:               # riga esclusa: dopo i numeri c'è il motivo
        tokens = tokens[:ncols]
    try:
        row = [float(x.replace(',', '.')) for x in tokens]
    except ValueError:
        raise LabError(f"{filename}: riga non numerica: {line.strip()!r}")
    if len(row) != ncols:
        raise LabError(f"{filename}: attese {ncols} colonne, trovate {len(row)}: {line.strip()!r}")
    return row


def load(filename, fields, sort=None, excluded=False):
    """Legge data/<filename> e restituisce un dizionario nome -> colonna.

    Le colonne con incertezza sono array di ufloat (usare nom() ed err() per i grafici);
    il parametro di una lettura è disponibile come 'p_<nome>'.
    sort     : nome del campo su cui ordinare (None = ordine del file)
    excluded : True -> restituisce le righe escluse con '#!' invece di quelle valide
    """
    if not os.path.isfile(_path(filename)):
        raise LabError(f"{filename} non esiste.")
    ncols = len(_columns(fields))
    rows = []
    with open(_path(filename)) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if s.startswith('#!'):
                if excluded:
                    rows.append(_parse(s[2:], ncols, filename, trailing_text=True))
            elif not s.startswith('#') and not excluded:
                rows.append(_parse(s, ncols, filename))
    if not rows and not excluded:
        raise LabError(f"{filename} è vuoto: inserire le misure.")
    arr = np.array(rows, dtype=float).reshape(-1, ncols)

    out, i = {}, 0
    for f in fields:
        v = arr[:, i]
        p = arr[:, i + 1] if f.ask else [None] * len(v)
        i += 2 if f.ask else 1
        if f.ask:
            out[f"p_{f.name}"] = np.array(p)
        if f.sigma is None:
            out[f.name] = v
        else:
            out[f.name] = unp.uarray(v, [f.error(x, q) for x, q in zip(v, p)])
    if sort and len(arr):
        order = np.argsort(nom(out[sort]))
        out = {k: v[order] for k, v in out.items()}
    return out


def load_once(filename, fields):
    """Scheda a riga unica (insert_once): dizionario nome -> valore (ufloat se ha incertezza)."""
    return {k: v[0] for k, v in load(filename, fields).items()}


def load_table(filename, usecols=None, delimiter=None):
    """Legge un file grezzo di uno strumento (CSV dell'oscilloscopio, acquisizione...)
    da data/<filename>. Restituisce un array 2D con le sole righe numeriche:
    intestazioni e righe di testo vengono saltate.

    usecols   : indici delle colonne da tenere (None = tutte)
    delimiter : separatore (None = riconosciuto tra ',' ';' TAB e spazi)
    """
    if not os.path.isfile(_path(filename)):
        raise LabError(f"{filename} non esiste.")
    rows = []
    with open(_path(filename), errors='replace') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            sep = delimiter or next((d for d in (';', '\t', ',') if d in s), None)
            tokens = [t.strip() for t in (s.split(sep) if sep else s.split())]
            if usecols is not None:
                if max(usecols) >= len(tokens):
                    continue
                tokens = [tokens[i] for i in usecols]
            try:
                rows.append([float(t) for t in tokens])
            except ValueError:
                continue
    if not rows:
        raise LabError(f"{filename}: nessuna riga numerica.")
    n = len(rows[0])
    return np.array([r for r in rows if len(r) == n])


DRAFT_DIR = os.path.join(DATA_DIR, '.bozza')


class _Interrupted(Exception):
    """Ctrl+C a metà riga: porta con sé i valori già inseriti."""

    def __init__(self, done):
        self.done = done


def _draft_path(filename):
    return os.path.join(DRAFT_DIR, filename + '.json')


def _save_draft(filename, done):
    import json
    os.makedirs(DRAFT_DIR, exist_ok=True)
    with open(_draft_path(filename), 'w') as f:
        json.dump(done, f)


def _take_draft(filename, fields):
    """Riga interrotta in sospeso: la mostra e chiede se riprenderla. Restituisce i valori o []."""
    import json
    path = _draft_path(filename)
    if not os.path.isfile(path):
        return []
    with open(path) as f:
        done = json.load(f)
    os.remove(path)
    shown = ",  ".join(f"{fl.name} = {v:g}" for fl, (v, _) in zip(fields, done))
    nxt = fields[len(done)].name if len(done) < len(fields) else 'conferma'
    if input(f"  Riga interrotta: {shown}. Riprendere da {nxt}? (s/n): ").strip().lower() == 's':
        return done
    return []


def _ask_row(fields, done=None):
    """Chiede una riga, ripartendo dai valori già inseriti in `done` (lista di (valore, parametro)).
    Restituisce (valori da salvare, riepilogo con le incertezze). Ctrl+C -> _Interrupted."""
    def ask(text):
        return float(input(f"  {text}: ").replace(',', '.'))

    done = list(done or [])
    try:
        for k, f in enumerate(fields):
            if k < len(done):
                continue
            v = ask(f.prompt())
            p = ask('  ' + f.ask) if f.ask else None
            done.append((v, p))
    except (KeyboardInterrupt, EOFError):
        raise _Interrupted(done)
    row, summary = [], []
    for f, (v, p) in zip(fields, done):
        row += [v] if p is None else [v, p]
        s = f.error(v, p)
        summary.append(f"{f.name} = {v:g}" + (f" ± {s:.2g}" if s is not None else ''))
    return row, ",  ".join(summary), done


def _interrupted(filename, done):
    """Ctrl+C: se la riga era iniziata chiede se tenerla in sospeso per riprenderla da lì."""
    print()
    if done:
        try:
            keep = input("  Riga a metà: tenere i valori inseriti e riprendere da qui la prossima volta? (s/n): ")
        except (KeyboardInterrupt, EOFError):
            keep = 'n'
        if keep.strip().lower() == 's':
            _save_draft(filename, done)
            print("  Riga in sospeso salvata.")


def _remaining(filename, fields, plan):
    """Punti previsti (valori del primo campo) non ancora presenti nel file."""
    if not plan:
        return []
    try:
        have = nom(load(filename, fields)[fields[0].name])
    except LabError:
        have = []
    return [x for x in plan if not any(abs(h - x) <= 1e-9 * max(abs(x), 1) for h in have)]


def insert(filename, fields, plan=None):
    """Inserimento interattivo: chiede le letture, mostra le incertezze, aggiunge la riga.

    plan : valori previsti del primo campo (es. le frequenze di procedura.md): a ogni riga si
           ricorda il primo non ancora misurato; il valore si scrive comunque a mano.
    Ctrl+C a metà riga chiede se tenerla in sospeso; alla ripresa si riparte da lì.
    """
    print(f"\nInserimento in {filename}. Ctrl+C per interrompere.")
    done = _take_draft(filename, fields)
    while True:
        todo = _remaining(filename, fields, plan)
        if plan:
            if not todo and not done:
                print("  Tutti i punti previsti sono inseriti.")
            elif todo:
                print(f"\n  Prossimo punto previsto: {fields[0].name} = {todo[0]:g}"
                      f"  ({len(plan) - len(todo) + 1} di {len(plan)})")
        try:
            row, summary, done = _ask_row(fields, done)
            print("  -> " + summary)
            ans = input("  Salvare? (s/n): ").strip().lower()
        except _Interrupted as e:
            _interrupted(filename, e.done)
            return
        except (KeyboardInterrupt, EOFError):
            _interrupted(filename, done)
            return
        except (ValueError, LabError) as e:
            print(f"  Valore non valido ({e}). Riga scartata.")
            done = []
            continue
        if ans == 's':
            _snapshot(filename)
            with open(_path(filename), 'a') as fh:
                fh.write("\t".join(f"{x:.10g}" for x in row) + "\n")
        done = []


def insert_once(filename, fields, title=''):
    """Scheda a riga unica (es. valori dei componenti sul banco): chiede ogni campo una
    volta e riscrive data/<filename>. Si rilegge con load_once(). Interrompibile come insert()."""
    done = _take_draft(filename, fields)
    if not done:
        try:
            old = load_once(filename, fields)
            print(f"\n{filename} contiene già:")
            for f in fields:
                print(f"  {f.name} = {fmt(old[f.name])} {f.unit}".rstrip())
            if input("Sovrascrivere? (s/n): ").strip().lower() != 's':
                return
        except LabError:
            pass
    print(f"\nInserimento in {filename}. Ctrl+C per interrompere.")
    try:
        row, summary, done = _ask_row(fields, done)
        print("  -> " + summary)
        ans = input("  Salvare? (s/n): ").strip().lower()
    except _Interrupted as e:
        _interrupted(filename, e.done)
        return
    except (KeyboardInterrupt, EOFError):
        _interrupted(filename, done)
        return
    except (ValueError, LabError) as e:
        print(f"  Valore non valido ({e}). Nulla è stato salvato.")
        return
    if ans != 's':
        return
    _snapshot(filename)
    if os.path.exists(_path(filename)):
        os.remove(_path(filename))
    init_data(filename, fields, title)
    with open(_path(filename), 'a') as fh:
        fh.write("\t".join(f"{x:.10g}" for x in row) + "\n")


UNDO_DIR = os.path.join(DATA_DIR, '.undo')


def _snapshot(filename):
    """Salva lo stato di data/<filename> prima di una modifica fatta dal menu."""
    os.makedirs(UNDO_DIR, exist_ok=True)
    n = 1 + max([int(x.split('_', 1)[0]) for x in os.listdir(UNDO_DIR)] or [0])
    with open(os.path.join(UNDO_DIR, f"{n:04d}_{filename}"), 'w') as out:
        if os.path.isfile(_path(filename)):
            with open(_path(filename)) as f:
                out.write(f.read())


def undo():
    """Annulla l'ultima modifica fatta dal menu (riga inserita o scheda del banco riscritta).
    Si può ripetere per tornare indietro di più passi."""
    snaps = sorted(os.listdir(UNDO_DIR)) if os.path.isdir(UNDO_DIR) else []
    if not snaps:
        print("  Niente da annullare.")
        return
    snap = os.path.join(UNDO_DIR, snaps[-1])
    filename = snaps[-1].split('_', 1)[1]
    with open(snap) as f:
        before = f.read()
    now = open(_path(filename)).read() if os.path.isfile(_path(filename)) else ''
    gone = [l for l in now.splitlines() if l not in before.splitlines()]
    back = [l for l in before.splitlines() if l not in now.splitlines()]
    print(f"  Ultima modifica: {filename}")
    for l in gone:
        print(f"    toglie:     {l}")
    for l in back:
        print(f"    ripristina: {l}")
    if input("  Annullare? (s/n): ").strip().lower() != 's':
        return
    with open(_path(filename), 'w') as f:
        f.write(before)
    os.remove(snap)
    print("  Annullato.")


def nom(x):
    """Valori centrali di un ufloat o di un array di ufloat."""
    return unp.nominal_values(x)


def err(x):
    """Incertezze di un ufloat o di un array di ufloat."""
    return unp.std_devs(x)


# =====================================================
# STATISTICA
# =====================================================

def z_test(a, b):
    """Z = |a - b| / sqrt(σa² + σb²). a, b: ufloat o numeri."""
    s = float(np.hypot(err(a), err(b)))
    return float('nan') if s == 0 else abs(float(nom(a)) - float(nom(b))) / s


def weighted_mean(values):
    """Media pesata (pesi 1/σ²) di una sequenza di ufloat."""
    w = 1.0 / err(values) ** 2
    return ufloat(np.sum(w * nom(values)) / np.sum(w), 1.0 / np.sqrt(np.sum(w)))


def linfit(x, y, sy=None):
    """Retta y = a + b·x ai minimi quadrati pesati. Restituisce (a, b, chi2, gdl).

    y può essere un array di ufloat: in tal caso sy = le sue incertezze.
    """
    if sy is None:
        sy = err(y)
    x, y, sy = nom(x), nom(y), np.asarray(sy, dtype=float)
    w = 1.0 / sy ** 2
    M = np.array([[np.sum(w), np.sum(w * x)], [np.sum(w * x), np.sum(w * x * x)]])
    cov = np.linalg.inv(M)
    a, b = cov @ np.array([np.sum(w * y), np.sum(w * x * y)])
    chi2 = float(np.sum(((y - a - b * x) / sy) ** 2))
    ua, ub = correlated_values([a, b], cov)
    return ua, ub, chi2, len(x) - 2


def fit(model, x, y, p0, sy=None, key=None):
    """Fit non lineare di model(x, *p). Restituisce (parametri ufloat, chi2, gdl).

    key : se dato, registra chi2 e gdl per la relazione come \\res{key:chi2} e \\res{key:gdl}.
    """
    from scipy.optimize import curve_fit
    if sy is None:
        sy = err(y)
    x, y, sy = nom(x), nom(y), np.asarray(sy, dtype=float)
    popt, pcov = curve_fit(model, x, y, p0=p0, sigma=sy, absolute_sigma=True)
    chi2 = float(np.sum(((y - model(x, *popt)) / sy) ** 2))
    gdl = len(x) - len(popt)
    if key:
        _results.append((f"{key}:chi2", f"{chi2:.2g}"))
        _results.append((f"{key}:gdl", str(gdl)))
    return correlated_values(popt, pcov), chi2, gdl


# =====================================================
# RISULTATI
# =====================================================

def fmt(x):
    """Testo 'valore ± incertezza' con 2 cifre significative sull'incertezza."""
    if hasattr(x, 'std_dev') and x.std_dev > 0:
        return f"{x:.2uP}".replace('±', ' ± ')
    return f"{float(nom(x)):.4g}"


def _tex(x):
    if hasattr(x, 'std_dev') and x.std_dev > 0:
        return f"{x:.2uL}"
    s = f"{float(nom(x)):.4g}"
    if 'e' in s:
        m, e = s.split('e')
        s = f"{m} \\times 10^{{{int(e)}}}"
    return s


def report(key, label, value, unit='', ref=None):
    """Stampa un risultato e lo registra per la relazione.

    key : nome con cui richiamarlo in LaTeX: \\res{key}, \\res{key:ref}, \\res{key:z}
    ref : valore atteso (ufloat o numero) -> aggiunge lo Z-test
    Convertire PRIMA il valore nell'unità in cui va riportato (es. value * 1e3).
    """
    print(f"  {label} = {fmt(value)} {unit}".rstrip())
    _results.append((key, _tex(value)))
    if ref is None:
        return
    z = z_test(value, ref)
    _results.append((f"{key}:ref", _tex(ref)))
    if np.isnan(z):
        print(f"    atteso {fmt(ref)} {unit}".rstrip())
        return
    esito = 'compatibile' if z < Z_MAX else 'NON compatibile'
    print(f"    atteso {fmt(ref)} {unit}".rstrip() + f"  ->  Z = {z:.2f}  ({esito})")
    _results.append((f"{key}:z", f"{z:.2f}"))


def _write_section(path, name, body, mark):
    """Sostituisce la sezione `name` del file, lasciando intatte le altre."""
    head = f"{mark}=== "
    sections, current = {}, None
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if line.startswith(head):
                    current = line[len(head):].split(' ===')[0]
                    sections[current] = ''
                elif current is not None:
                    sections[current] += line
    sections[name] = body.strip('\n') + '\n\n'
    with open(path, 'w') as f:
        for k in sorted(sections):
            f.write(f"{head}{k} ===\n{sections[k]}")


class _Tee(io.StringIO):
    def write(self, s):
        sys.__stdout__.write(s)
        return super().write(s)


def run(part):
    """Esegue part.analyze() e aggiorna results.txt e latex/results.tex."""
    name = part.__name__
    _results.clear()
    buf = _Tee()
    print(f"\n--- {name}: {part.TITLE} ---")
    try:
        with contextlib.redirect_stdout(buf):
            part.analyze()
    except LabError as e:
        print(f"  {e}")
        return
    _write_section(RESULTS_TXT, f"{name}: {part.TITLE}", buf.getvalue(), '# ')
    _write_section(RESULTS_TEX, name,
                   "\n".join(f"\\resdef{{{k}}}{{{v}}}" for k, v in _results), '% ')


# =====================================================
# GRAFICI
# =====================================================

def errorbar(ax, x, y, excluded=False, **kw):
    """ax.errorbar che accetta array di ufloat. excluded=True: punti vuoti grigi."""
    style = dict(fmt='o', ms=4, capsize=3)
    if excluded:
        style.update(mfc='none', color='gray', label='Esclusi')
    style.update(kw)
    xe, ye = err(x), err(y)
    return ax.errorbar(nom(x), nom(y), xerr=xe if np.any(xe) else None,
                       yerr=ye if np.any(ye) else None, **style)


def savefig(name):
    """Salva la figura corrente in latex/plots/<name>.png."""
    import matplotlib.pyplot as plt
    os.makedirs(PLOTS_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f"{name}.png"), dpi=200)
    print(f"  grafico: latex/plots/{name}.png")
    if SHOW:
        plt.show()
    plt.close()
