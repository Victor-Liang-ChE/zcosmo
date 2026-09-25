"""Flatten NIST ThermoML XML files into long-format tables.

Output tables:
  compounds.csv : file, orgnum, name, formula, inchikey, inchi, cas
  points.csv    : one row per (dataset, point, property) with all variable and
                  constraint values attached as JSON.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

from lxml import etree

NS = "{http://www.iupac.org/namespaces/ThermoML}"


def _t(el, path):
    x = el.find(path)
    return x.text.strip() if x is not None and x.text else None


def _leaf_name(el):
    """Return the text of the first leaf element (the enumerated name) below el."""
    for d in el.iter():
        if len(d) == 0 and d.text and d.text.strip():
            return etree.QName(d).localname, d.text.strip()
    return None, None


def parse_file(path: str):
    path = Path(path)
    try:
        root = etree.parse(str(path)).getroot()
    except Exception as e:  # malformed file
        return [], [], [(path.name, repr(e))]
    fid = path.name
    year = _t(root, f"{NS}Citation/{NS}yrPubYr")
    doi = _t(root, f"{NS}Citation/{NS}sDOI")
    comps = []
    for c in root.findall(f"{NS}Compound"):
        org = _t(c, f"{NS}RegNum/{NS}nOrgNum")
        comps.append(dict(
            file=fid, orgnum=org,
            name=_t(c, f"{NS}sCommonName"),
            formula=_t(c, f"{NS}sFormulaMolec"),
            inchikey=_t(c, f"{NS}sStandardInChIKey"),
            inchi=_t(c, f"{NS}sStandardInChI"),
            cas=_t(c, f"{NS}nCASRN") or _t(c, f"{NS}sCASName"),
            smiles=_t(c, f"{NS}sSmiles"),
        ))
    rows = []
    for ids, pm in enumerate(root.findall(f"{NS}PureOrMixtureData")):
        components = [_t(c, f"{NS}RegNum/{NS}nOrgNum") for c in pm.findall(f"{NS}Component")]
        phases = []
        for ph in pm.findall(f"{NS}PhaseID"):
            phases.append(dict(phase=_t(ph, f"{NS}ePhase"), org=_t(ph, f"{NS}RegNum/{NS}nOrgNum")))
        props = {}
        for p in pm.findall(f"{NS}Property"):
            num = _t(p, f"{NS}nPropNumber")
            grp = p.find(f"{NS}Property-MethodID/{NS}PropertyGroup")
            _, pname = _leaf_name(grp) if grp is not None else (None, None)
            # property name is ePropName specifically
            en = grp.find(f".//{NS}ePropName") if grp is not None else None
            if en is not None:
                pname = en.text.strip()
            method = grp.find(f".//{NS}eMethodName") if grp is not None else None
            smethod = grp.find(f".//{NS}sMethodName") if grp is not None else None
            props[num] = dict(
                prop=pname,
                prop_org=_t(p, f"{NS}Property-MethodID/{NS}RegNum/{NS}nOrgNum"),
                prop_phase=_t(p, f"{NS}PropPhaseID/{NS}ePropPhase"),
                prop_phase_org=_t(p, f"{NS}PropPhaseID/{NS}RegNum/{NS}nOrgNum"),
                method=(method.text.strip() if method is not None and method.text else None)
                or (smethod.text.strip() if smethod is not None and smethod.text else None),
            )
        constraints = []
        for c in pm.findall(f"{NS}Constraint"):
            ct = c.find(f"{NS}ConstraintID/{NS}ConstraintType")
            tag, name = _leaf_name(ct) if ct is not None else (None, None)
            constraints.append(dict(
                name=name, org=_t(c, f"{NS}ConstraintID/{NS}RegNum/{NS}nOrgNum"),
                phase=_t(c, f"{NS}ConstraintPhaseID/{NS}eConstraintPhase"),
                value=_t(c, f"{NS}nConstraintValue")))
        variables = {}
        for v in pm.findall(f"{NS}Variable"):
            num = _t(v, f"{NS}nVarNumber")
            vt = v.find(f"{NS}VariableID/{NS}VariableType")
            tag, name = _leaf_name(vt) if vt is not None else (None, None)
            variables[num] = dict(
                name=name, org=_t(v, f"{NS}VariableID/{NS}RegNum/{NS}nOrgNum"),
                phase=_t(v, f"{NS}VarPhaseID/{NS}eVarPhase"))
        for ip, nv in enumerate(pm.findall(f"{NS}NumValues")):
            vals = []
            for vv in nv.findall(f"{NS}VariableValue"):
                n = _t(vv, f"{NS}nVarNumber")
                d = dict(variables.get(n, {}))
                d["value"] = _t(vv, f"{NS}nVarValue")
                vals.append(d)
            for pv in nv.findall(f"{NS}PropertyValue"):
                n = _t(pv, f"{NS}nPropNumber")
                pr = props.get(n, {})
                unc = _t(pv, f".//{NS}nCombExpandUncertValue") or _t(pv, f".//{NS}nExpandUncertValue") \
                    or _t(pv, f".//{NS}nStdUncertValue")
                rows.append(dict(
                    file=fid, year=year, doi=doi, dataset=ids, point=ip,
                    ncomp=len(components), components="|".join(c or "" for c in components),
                    phases=json.dumps(phases), constraints=json.dumps(constraints),
                    variables=json.dumps(vals), prop=pr.get("prop"), prop_org=pr.get("prop_org"),
                    prop_phase=pr.get("prop_phase"), prop_phase_org=pr.get("prop_phase_org"),
                    method=pr.get("method"), value=_t(pv, f"{NS}nPropValue"), unc=unc))
    return comps, rows, []


def main(src: str, out: str):
    import pandas as pd
    files = sorted(str(p) for p in Path(src).rglob("*.xml"))
    comps, rows, errs = [], [], []
    with ProcessPoolExecutor() as ex:
        for c, r, e in ex.map(parse_file, files, chunksize=50):
            comps += c
            rows += r
            errs += e
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(comps).to_csv(out / "tml_compounds.csv", index=False)
    df = pd.DataFrame(rows)
    df.to_pickle(out / "tml_points.pkl")
    pd.DataFrame(errs, columns=["file", "error"]).to_csv(out / "tml_parse_errors.csv", index=False)
    print(f"files={len(files)} compounds={len(comps)} points={len(df)} errors={len(errs)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
