source /opt/miniconda3/etc/profile.d/conda.sh; conda activate zcosmo
export PYTHONPATH=src
python -m zcosmo.metrics unifac_do cosmosac2010 Z0x Z0w --split test --ref Z0x --tag z0w 2>&1 | grep -v -i warn | grep -E "^## |^\| (Z0w|Z0x|cosmosac2010|unifac_do) "
python - <<'PY'
import pandas as pd, numpy as np
neg=pd.read_csv('results/predictions/lle_negatives.csv'); n=neg[neg.split!='train']
for m in ['cosmosac2010','Z0x','Z0w']:
    d=pd.read_csv(f'results/predictions/{m}__lle__all.csv'); d=d[d.split!='train']
    s=np.where(d.c1<d.c2,d.c1+'|'+d.c2,d.c2+'|'+d.c1)
    rec=(d.groupby(s).pred_split.mean()>0.5).mean(); fp=n[f'fp_{m}'].mean()
    print(m,'LLE test recall',round(rec,2),'fp',round(fp,3),'bal',round((rec+1-fp)/2,3))
PY
