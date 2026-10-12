"""
Parte 1 — ESEMPIO DA SOSTITUIRE: legge lineare y = a + b·x.

Ogni parte dell'esperienza è un file come questo, con:
  TITLE   : titolo breve
  DATA    : file in data/ riempito dal menu di inserimento; None se la parte è
            solo qualitativa o se legge file salvati da uno strumento
            (in quel caso: lab.load_table('nomefile.csv') dentro analyze)
  FIELDS  : grandezze misurate, nell'ordine delle colonne
  analyze : calcoli, confronti (lab.report) e grafici (lab.savefig)
e va aggiunta a PARTS in main.py.
"""

import matplotlib.pyplot as plt
import numpy as np

import config as cfg
import instruments as ins
import lab
from lab import Field

TITLE = "legge lineare"
DATA = 'data1.txt'
FIELDS = [
    Field('x', 'u.m.', sigma=ins.reading(0.1)),          # incertezza costante
    Field('y', 'u.m.', sigma=lambda v: ins.digital(v, pct=1, digits=1, res=0.01)),
    # con un parametro chiesto a ogni misura:
    # Field('V', 'V', sigma=ins.scope_V, ask='scala verticale [V/div]'),
]


def analyze():
    d = lab.load(DATA, FIELDS, sort='x')
    x, y = d['x'], d['y']

    a, b, chi2, gdl = lab.linfit(x, y)
    lab.report('p1a', 'a', a, 'u.m.')
    lab.report('p1b', 'b', b, '', ref=cfg.B_REF)
    print(f"  chi2/gdl = {chi2:.2g}/{gdl}")

    fig, ax = plt.subplots(figsize=(7, 5))
    lab.errorbar(ax, x, y, label='Dati')
    esclusi = lab.load(DATA, FIELDS, excluded=True)
    if len(esclusi['x']):
        lab.errorbar(ax, esclusi['x'], esclusi['y'], excluded=True)
    xm = np.linspace(lab.nom(x).min(), lab.nom(x).max(), 200)
    ax.plot(xm, a.n + b.n * xm, '-', label='Retta di best fit')
    ax.set_xlabel('x [u.m.]')
    ax.set_ylabel('y [u.m.]')
    ax.grid(True, ls=':')
    ax.legend()
    lab.savefig('part1')
