"""Render only Figures 2 and 3 from pinned public, precomputed quantities.

No prediction files, model imports, bootstrap or new thermodynamic scores.
Original image files are never overwritten. Raster equality is not claimed.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
import math
from pathlib import Path
from r17_audit import BASE, ROOT, blob, fresh_output, require, sha

INPUTS = {
    'results/qc/hb_constants_per_dimer.csv': 'bd249aaf7ad01e5fd70a7357766c6db6e5cf1307',
    'results/qc/hb_constants_by_class.csv': 'fe225ee279fd80fc599c871955011370ddafb5e0',
    'results/scorecard_test_main7.json': 'aee303792afcdff48e90aa74d074802a3bb7596b',
}
CLASSES = ('OH-OH', 'OH-OT', 'OT-OT')
MODELS = ('unifac_do', 'cosmosac2010', 'cosmosac_dsp', 'Z0', 'Z0e', 'Z0s', 'Z0x')
FITTED = (4013.78, 3016.43, 932.31)
NAMES = ('UNIFAC-Do', 'COSMO-SAC 2010', 'COSMO-SAC-dsp', 'Z0', 'Z0e', 'Z0s', 'Z0x')


def positive(value: object) -> float:
    value = float(value)
    require(math.isfinite(value) and value > 0, 'invalid stored plot quantity')
    return value


def figure2_data(per_dimer: bytes, classes: bytes) -> dict:
    """Use stored class means, not a newly fitted/re-estimated parameter."""
    rows = list(csv.DictReader(io.StringIO(per_dimer.decode())))
    means = list(csv.DictReader(io.StringIO(classes.decode())))
    require(len(rows) == 17 and len(means) == 3, 'HB table dimensions changed')
    require(len({r['label'] for r in rows}) == 17, 'duplicate dimer identity')
    require({r['cls'] for r in means} == set(CLASSES), 'HB class identities changed')
    groups = {c: [positive(r['c_hb']) for r in rows if r['cls'] == c] for c in CLASSES}
    counts = [len(groups[c]) for c in CLASSES]
    require(counts == [5, 7, 5], 'dimer-class counts changed')
    by = {r['cls']: r for r in means}
    require([int(by[c]['count']) for c in CLASSES] == counts, 'stored class count mismatch')
    return dict(classes=list(CLASSES), groups=groups,
                means=[positive(by[c]['mean']) for c in CLASSES], fitted=list(FITTED), count=17)


def figure3_data(scorecard: bytes) -> dict:
    data = json.loads(scorecard)
    require(data['split'] == 'test', 'wrong scorecard split')
    require(set(data['models']) == set(MODELS), 'main7 comparator list changed')
    idac, vle = data['tables']['idac'], data['tables']['vle']
    require(idac['n_points'] == 708 and idac['n_systems'] == 163 and vle['n_points'] == 9432,
            'main7 plot denominators changed')
    return dict(models=list(MODELS), labels=list(NAMES),
                IDAC=[positive(idac[m]['MAE_ln_gamma_inf']) for m in MODELS],
                VLE=[positive(vle[m]['AAD_P_pct']) for m in MODELS],
                IDAC_rows=708, IDAC_systems=163, VLE_rows=9432)


def render2(data: dict, filename: Path) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    for i, cls in enumerate(data['classes']):
        # Fixed offsets distinguish points. They do not encode another observation.
        values = data['groups'][cls]
        n = len(values)
        offsets = [0.0] if n == 1 else [-0.10 + 0.20 * j / (n - 1) for j in range(n)]
        ax.scatter([i + off for off in offsets], values, s=26,
                   label='Dimer estimates' if i == 0 else None)
    ax.scatter(range(3), data['means'], marker='_', s=700, linewidths=2.4, label='Stored class mean')
    ax.scatter(range(3), data['fitted'], marker='D', s=55, label='COSMO-SAC 2010')
    ax.set_xticks(range(3), data['classes'])
    ax.set_ylabel(r'$c_{HB}$ (kcal $\mathrm{\AA}^4$ mol$^{-1}$ e$^{-2}$)')
    ax.set_title('Historical hydrogen-bond coefficients')
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)


def render3(data: dict, filename: Path) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    for name, x, y in zip(data['labels'], data['IDAC'], data['VLE']):
        ax.scatter([x], [y], s=45)
        ax.annotate(name, (x, y), xytext=(5, 5), textcoords='offset points', fontsize=9)
    ax.set_xlabel(r'IDAC MAE in $\ln\gamma^\infty$ (708 observations)')
    ax.set_ylabel('VLE pressure AAD, % (9,432 observations)')
    ax.set_title('Stored main7 point estimates, property-specific subsets')
    ax.margins(x=0.2, y=0.15)
    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)


def run(root: Path, out: Path) -> None:
    root = root.resolve()
    inputs = {}
    for path, expected in INPUTS.items():
        target = (root / path).resolve()
        require(target.is_relative_to(root), 'input symlink leaves checkout')
        data = target.read_bytes()
        require(blob(data) == expected, 'pinned public plot input differs: ' + path)
        inputs[path] = data
    h = figure2_data(inputs['results/qc/hb_constants_per_dimer.csv'],
                     inputs['results/qc/hb_constants_by_class.csv'])
    t = figure3_data(inputs['results/scorecard_test_main7.json'])
    output = fresh_output(out, root)
    render2(h, output / 'fig2_hbond_constants.png')
    render3(t, output / 'fig3_tradeoff.png')
    receipt = dict(base=BASE, inputs={p: dict(git_blob=blob(b), sha256=sha(b)) for p, b in inputs.items()},
                   outputs={p.name: sha(p.read_bytes()) for p in sorted(output.glob('*.png'))},
                   new_model_calls=0, new_scores_computed=False, pixels_equal_to_archived=False)
    (output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('Rendered Figures 2 and 3 from stored public quantities. Originals unchanged.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    run(args.root, args.out)
