# Read-only tabulation of STORED LLE flags (no model call, no rescoring). Same arithmetic as job 27.
P="$HOME/Projects/BIP Free Predictive Modeling"; cd "$P" || exit 1
source /opt/miniconda3/etc/profile.d/conda.sh; conda activate zcosmo
shasum -a 256 results/predictions/lle_negatives.csv results/predictions/*__lle__all.csv
python - <<'PY'
import pandas as pd, numpy as np
neg=pd.read_csv('results/predictions/lle_negatives.csv'); print('neg cols', list(neg.columns)); print('neg split counts', neg.split.value_counts().to_dict())
n=neg[neg.split!='train']
for m in ['unifac_do','cosmosac2010','cosmosac_dsp','Z0','Z0e','Z0s','Z0x','Z0w','hanna']:
    try: d=pd.read_csv(f'results/predictions/{m}__lle__all.csv')
    except FileNotFoundError: print(m,'no lle predictions'); continue
    print(m,'split counts',d.split.value_counts().to_dict())
    d=d[d.split!='train']
    s=np.where(d.c1<d.c2,d.c1+'|'+d.c2,d.c2+'|'+d.c1)
    g=d.groupby(s).pred_split.mean()>0.5; rec=g.mean()
    col=f'fp_{m}'
    if col in n: fp=n[col].mean(); nn=int(n[col].notna().sum()); fps=int(n[col].sum())
    else: fp=float('nan'); nn=0; fps=-1
    print(f'{m} pos_pairs {len(g)} detected {int(g.sum())} recall {rec:.4f} | neg n {nn} fp_count {fps} fp {fp:.4f} | bal {(rec+1-fp)/2:.4f}')
PY
