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


class LabError(Exception):
    """Errore atteso (file vuoto, colonne sbagliate): si stampa senza traceback."""


# =====================================================
# DATI
# =====================================================

class Field:
    """Una grandezza misurata = una colonna (più la sua incertezza) del file dati.

    name  : nome della colonna, usato anche come chiave in load()
    unit  : unità di misura
    sigma : None            -> nessuna colonna di incertezza (es. indice, etichetta)
            numero          -> incertezza costante
            f(valore)       -> incertezza calcolata dal valore
            f(valore, x)    -> come sopra, con un parametro chiesto all'inserimento
    ask   : testo con cui chiedere x (es. 'scala verticale [V/div]')
    """

    def __init__(self, name, unit='', sigma=None, ask=None):
        self.name, self.unit, self.sigma, self.ask = name, unit, sigma, ask


def _columns(fields):
    cols = []
    for f in fields:
        cols.append(f"{f.name}[{f.unit}]" if f.unit else f.name)
        if f.sigma is not None:
            cols.append(f"s_{f.name}")
    return cols


def init_data(filename, fields, title=''):
    """Crea data/<filename> con l'intestazione delle colonne, se non esiste."""
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, 'w') as f:
        if title:
            f.write(f"# {title}\n")
        f.write("# Colonne separate da TAB. Per escludere una misura: '#!' a inizio riga"
                " e il motivo in fondo.\n")
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

    Le colonne con incertezza sono array di ufloat (usare nom() ed err() per i grafici).
    sort     : nome del campo su cui ordinare (None = ordine del file)
    excluded : True -> restituisce le righe escluse con '#!' invece di quelle valide
    """
    path = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(path):
        raise LabError(f"{filename} non esiste.")
    ncols = len(_columns(fields))
    rows = []
    with open(path) as f:
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
        if f.sigma is None:
            out[f.name] = arr[:, i]
            i += 1
        else:
            out[f.name] = unp.uarray(arr[:, i], arr[:, i + 1])
            i += 2
    if sort and len(arr):
        order = np.argsort(nom(out[sort]))
        out = {k: v[order] for k, v in out.items()}
    return out


def insert(filename, fields):
    """Inserimento interattivo: chiede i valori, calcola le incertezze, aggiunge la riga."""
    def ask(text):
        return float(input(f"  {text}: ").replace(',', '.'))

    print(f"\nInserimento in {filename}. Ctrl+C per finire.")
    while True:
        try:
            row = []
            for f in fields:
                v = ask(f"{f.name} [{f.unit}]" if f.unit else f.name)
                row.append(v)
                if f.sigma is None:
                    continue
                if callable(f.sigma):
                    row.append(f.sigma(v, ask('  ' + f.ask)) if f.ask else f.sigma(v))
                else:
                    row.append(float(f.sigma))
            line = "\t".join(f"{x:.6g}" for x in row)
            print("  -> " + line)
            if input("  Salvare? (s/n): ").strip().lower() == 's':
                with open(os.path.join(DATA_DIR, filename), 'a') as fh:
                    fh.write(line + "\n")
        except (KeyboardInterrupt, EOFError):
            print()
            return
        except ValueError as e:
            print(f"  Valore non valido ({e}). Riga scartata.")


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


def fit(model, x, y, p0, sy=None):
    """Fit non lineare di model(x, *p). Restituisce (parametri ufloat, chi2, gdl)."""
    from scipy.optimize import curve_fit
    if sy is None:
        sy = err(y)
    x, y, sy = nom(x), nom(y), np.asarray(sy, dtype=float)
    popt, pcov = curve_fit(model, x, y, p0=p0, sigma=sy, absolute_sigma=True)
    chi2 = float(np.sum(((y - model(x, *popt)) / sy) ** 2))
    return correlated_values(popt, pcov), chi2, len(x) - len(popt)


# =====================================================
# RISULTATI
# =====================================================

_results = []   # (chiave, testo LaTeX) della parte in esecuzione


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
