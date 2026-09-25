"""Modified UNIFAC (Dortmund) baseline via ugropy group assignment + thermo."""
from __future__ import annotations

from functools import lru_cache

import numpy as np
from thermo.unifac import DOUFSG, DOUFIP2016, UNIFAC

_NAME2ID = {}
for k, v in DOUFSG.items():
    _NAME2ID.setdefault(v.group.replace(" ", "").upper(), k)
_NAME2ID["HCO"] = 20  # aldehyde CHO


@lru_cache(maxsize=None)
def dortmund_groups(smiles: str):
    from ugropy import Groups
    try:
        g = Groups(smiles, "smiles").dortmund.subgroups
    except Exception:
        return None
    if not g:
        return None
    out = {}
    for name, n in g.items():
        k = _NAME2ID.get(name.replace(" ", "").upper())
        if k is None:
            return None
        out[k] = out.get(k, 0) + n
    return out


def _has_params(groups_list):
    mains = {DOUFSG[k].main_group_id for g in groups_list for k in g}
    for a in mains:
        for b in mains:
            if a != b and (a not in DOUFIP2016 or b not in DOUFIP2016[a]):
                return False
    return True


class UnifacBinary:
    def __init__(self, smiles1, smiles2):
        g1, g2 = dortmund_groups(smiles1), dortmund_groups(smiles2)
        self.ok = g1 is not None and g2 is not None and _has_params([g1, g2])
        self.groups = [g1, g2]

    def lngamma(self, T, x):
        if not self.ok:
            return np.full(2, np.nan)
        x = np.clip(np.asarray(x, float), 1e-12, 1)
        x = x / x.sum()
        m = UNIFAC.from_subgroups(T=T, xs=list(x), chemgroups=self.groups, version=1,
                                  interaction_data=DOUFIP2016, subgroups=DOUFSG)
        return np.log(np.array(m.gammas()))

    def lngamma_inf(self, T, solute_index=0):
        x = np.array([1e-10, 1 - 1e-10]) if solute_index == 0 else np.array([1 - 1e-10, 1e-10])
        return self.lngamma(T, x)[solute_index]
