import numpy as np, torch, time
from mace.calculators import mace_off
from bench6_core import water_box
from multi_mace import MultiMACE
torch.set_num_threads(8)
c = mace_off(model="small", device="cpu", default_dtype="float64")
at = water_box(4); n = len(at)
solv, solu = at[list(range(3, n))], at[[0, 1, 2]]
at2 = water_box(4, seed=1)
systems = [at, solv, solu, at2]
mm = MultiMACE(c, systems)
pos = torch.cat([torch.tensor(a.positions) for a in systems])
E, F = mm.forces(pos)
worst = 0
for g, a in enumerate(systems):
    a = a.copy(); a.calc = c
    e0, f0 = a.get_potential_energy(), a.get_forces()
    s, t = mm.off[g], mm.off[g + 1]
    dE = abs(float(E[g]) - e0); dF = np.abs(F[s:t].numpy() - f0).max(); worst = max(worst, dF)
    print(f"system {g} ({len(a)} atoms): |dE| {dE:.2e} eV, max|dF| {dF:.2e} eV/A")
# move and re-evaluate (rebuild path)
pos2 = pos + 0.3 * torch.randn_like(pos) * 0.1
E2, F2 = mm.forces(pos2)
a = systems[0].copy(); a.positions = pos2[:n].numpy(); a.calc = c
print("after move sys0 max|dF|", np.abs(F2[:n].numpy() - a.get_forces()).max(), "rebuilds", mm.n_rebuild)
print("decoupling energy E_full - E_solv - E_solu (eV):", float(E[0] - E[1] - E[2]))
