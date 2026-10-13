"""
Valori dell'esperienza: scelte di progetto, grandezze preliminari, riferimenti.
DA ADATTARE. Tutto in unità SI.
"""

from uncertainties import ufloat

import instruments as ins
import lab
from lab import Field

# --- Scelte di progetto (valori nominali), ciascuna con il motivo ---
# R_NOM = 1e3      # [Ω] molto maggiore dei 50 Ω del generatore

# --- Valori del banco: misurati una volta sola, chiesti dalla voce "b" del menu ---
# Se l'esperienza non ne ha, lasciare BENCH_FIELDS = None.
BENCH_FILE = 'banco.txt'
BENCH_FIELDS = None
# BENCH_FIELDS = [
#     Field('R', 'Ω', sigma=ins.dmm_R),      # nome del componente, non della parte
# ]


def banco():
    """Valori del banco come dizionario nome -> ufloat."""
    try:
        return lab.load_once(BENCH_FILE, BENCH_FIELDS)
    except lab.LabError:
        raise lab.LabError("mancano i valori del banco: voce 'b' del menu.")


# --- Valori di riferimento (manuale, tabelle, consegna) ---
B_REF = 2.0                      # esatto: numero semplice
# G_REF = ufloat(9.806, 0.001)   # con incertezza
