"""
Grandezze fisse dell'esperienza: valori preliminari misurati una volta sola
(componenti, masse, lunghezze...) e valori di riferimento per i confronti.
DA ADATTARE. Tutto in unità SI, come ufloat(valore, incertezza).
"""

from uncertainties import ufloat

import instruments as ins

# --- Grandezze preliminari (misurate) ---
# R = ufloat(984.0, ins.digital(984.0, pct=1, digits=1, res=1.0))   # [Ω]

# --- Valori di riferimento (manuale, tabelle, consegna) ---
B_REF = 2.0                      # esatto: numero semplice
# G_REF = ufloat(9.806, 0.001)   # con incertezza
