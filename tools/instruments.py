"""
Incertezze strumentali. DA ADATTARE: una funzione per ogni strumento e grandezza
usati nell'esperienza, con le specifiche del manuale del modello esatto.

Ogni funzione restituisce σ. I contributi indipendenti si sommano in quadratura.
"""

import numpy as np


# =====================================================
# MODELLI GENERICI
# =====================================================

def digital(value, pct, digits, res):
    """Strumento digitale: ±(pct % della lettura + digits · risoluzione).

    res : valore dell'ultima cifra del display sulla portata usata
    """
    return float(np.hypot(pct / 100.0 * abs(value), digits * res))


def analog(full_scale, klass):
    """Strumento analogico: classe (in %) per il fondo scala."""
    return klass / 100.0 * full_scale


def reading(res):
    """Sola risoluzione di lettura (righello, cronometro, display senza specifiche)."""
    return res / np.sqrt(12.0)


# =====================================================
# STRUMENTI DELL'ESPERIENZA  (esempi da sostituire)
# =====================================================

# def dmm_V(V, res):
#     """Tensione DC, multimetro MARCA MODELLO: ±(0.5 % + 3 digit)."""
#     return digital(V, pct=0.5, digits=3, res=res)
