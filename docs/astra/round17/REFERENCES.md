# R17 bibliography and figure-source audit

This is an editorial audit, not a new literature-selected model. Bibliographic identity and the contents
of a paper are different checks. A publisher metadata record can establish a DOI and page range without
validating every scientific claim attributed to the paper. The original reference numbers are retained.
Issue-publication years are used instead of later digitization dates or earlier online dates.

| Reference | Metadata established | Primary location | Remaining issue / manuscript action |
|---|---|---|---|
| 1, Klamt | J. Phys. Chem. 1995, 99(7), 2224-2235 | https://doi.org/10.1021/j100007a062 | Expand title and pages. Do not use the website's 2002 digitization date as the publication year. |
| 2, Lin and Sandler | Ind. Eng. Chem. Res. 2002, 41(5), 899-913 | https://doi.org/10.1021/ie001047w | Add DOI and the related 2004 correction, 43(5), 1322, https://doi.org/10.1021/ie0308689. No inference that current 2010 code is affected without checking its equations. |
| 3, Mullins et al. | Ind. Eng. Chem. Res. 2006, 45(12), 4389-4415 | https://doi.org/10.1021/ie060370h | Add full range and DOI; distinguish this database publication from the project's UD inventory. |
| 4, Hsieh et al. | Fluid Phase Equilib. 2010, 297(1), 90-97 | https://doi.org/10.1016/j.fluid.2010.06.011 | Add exact DOI/range; model constants remain those of the pinned implementation. |
| 5, Hsieh et al. | Fluid Phase Equilib. 2014, 367, 109-116 | https://doi.org/10.1016/j.fluid.2014.01.032 | Corrigendum Fluid Phase Equilib. 2014, 384, 14-15, DOI 10.1016/j.fluid.2014.10.019, confirmed by the Crossref record deposited by Elsevier (closeout 2026-10-08). Its text (author copy at https://mb.uni-paderborn.de/fileadmin-mb/tdy/Publikationen/Veroeffentlichungen/COSMO-SAC-dsp.pdf) gives w = 0.27027, the value in the pinned implementation, corrects a Table 2 label and changes one Table 5 error entry. No manuscript result uses the corrected entries. Resolved. |
| 6, Bell et al. | J. Chem. Theory Comput. 2020, 16(4), 2635-2646 | https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b01016 | Complete citation verified at ACS. Its 2,261-compound distribution count is distinct from the project's reported 2,259-entry inventory. |
| 7, Gmehling et al. | Ind. Eng. Chem. Res. 1993, 32(1), 178-193 | https://doi.org/10.1021/ie00013a024 | Cite the actual 2016 parameter update as well; the 1993 paper alone does not identify the DOUFIP2016 software table. |
| 8, Hoffmann et al. | Nat. Commun. 2026, 17, 3485; published 14 April 2026 | https://www.nature.com/articles/s41467-026-71430-y | Publisher gives 824,481 data points. Deployed version recovered at closeout: github.com/marco-hoffmann/HANNA commit 6fe873c, cloned 2026-09-24, clean tree, ten ensemble weight files with aggregate SHA-256 ee0b38d3... (round17/RESULTS.md). Row overlap with the benchmark stays unresolved and is stated as such. |
| 9, Frenkel et al. | Part 1 is J. Chem. Eng. Data 2003, 48(1), 2-13 | https://pubs.acs.org/doi/abs/10.1021/je025645o | Replace the draft's unspecific 2006, 51, 1504 series placeholder with this identified Part 1 article. Online December 2002 does not change the 2003 issue citation. |
| 10, Herington | J. Inst. Pet. 1951, 37, 457-470, "Tests for the Consistency of Experimental Isobaric Vapor-Liquid Equilibrium Data" | NIST TRC ThermoData Engine reference list, https://trc.nist.gov/TDE/Help/TDE103a_v2_2/References.htm | The 1951 journal has no DOI and no online publisher record. The NIST TRC list is a curated bibliographic source independent of the draft; the manuscript cites title and range from it and says so. Resolved as far as the record allows. |
| 11, Onsager | J. Am. Chem. Soc. 1936, 58(8), 1486-1493 | https://doi.org/10.1021/ja01299a050 | Complete DOI and range; the implementation's convention needs its own code citation. |
| 12, Wertheim I-IV | 1984, 35, 19-34 and 35-47; 1986, 42, 459-476 and 477-492 | https://doi.org/10.1007/BF01017362 ; https://doi.org/10.1007/BF01017363 ; https://doi.org/10.1007/BF01127721 ; https://doi.org/10.1007/BF01127722 | Replace the incomplete parenthetical series reference with explicit I-IV identities. These papers do not validate the project's particular site mapping or inversion. |
| 13, Caldeweyher et al. | J. Chem. Phys. 2019, 150(15), 154122, DOI 10.1063/1.5090222 | https://www.cambridge.org/engage/chemrxiv/article-details/60c74060f96a006646286291 | Confirmed at closeout by the Crossref record deposited by AIP Publishing: volume 150, issue 15, article 154122, issued 2019-04-21, seven authors Caldeweyher, Ehlert, Hansen, Neugebauer, Spicher, Bannwarth, Grimme. The manuscript lists all seven. Resolved. |
| 14, Bannwarth et al. | J. Chem. Theory Comput. 2019, 15(3), 1652-1671 | https://doi.org/10.1021/acs.jctc.8b01176 | Complete GFN2-xTB title, DOI and range; actual tblite/geometry versions are separate provenance. |
| 15, Grimme | Chem. Eur. J. 2012, 18(32), 9955-9964 | https://doi.org/10.1002/chem.201200497 | Complete range and DOI. Do not treat model quasi-RRHO thermochemistry as a measured liquid entropy. |
| 16, Sun et al. | J. Chem. Phys. 2020, 153(2), 024109 | https://doi.org/10.1063/5.0006074 | Complete citation. A package paper does not specify the pinned PySCF 2.14.0 source used in later diagnostics. |
| 17, Boys and Bernardi | Mol. Phys. 1970, 19(4), 553-566 | https://doi.org/10.1080/00268977000101561 | Use the original DOI and publication year, not a later reprint or digitization. |
| Added 18, Constantinescu and Gmehling | J. Chem. Eng. Data 2016, 61(8), 2738-2748 | https://doi.org/10.1021/acs.jced.6b00136 | Identify the 2016 update. Installed implementation: thermo 0.6.1 with the DOUFIP2016 table present (job 421). Resolved. |
| Added 19, Kovács et al. (MACE-OFF) | J. Am. Chem. Soc. 2025, 147(21), 17598-17611 | https://doi.org/10.1021/jacs.4c07099 | Crossref-confirmed. The simulations used `mace_off(model="small")` (MACE-OFF23 small) on cloud GPUs; no local weight file was kept, so the loader call is the recorded identity. |

The corrigendum author record is
https://scholars.ncu.edu.tw/zh/publications/corrigendum-to-considering-the-dispersive-interactions-in-the-cos/ .
No correction's uninspected contents are asserted here. The complete reference audit uses publisher
records where accessible and labels the remaining author-record-only or unrecovered identities.

Closeout, 2026-10-08. Software and data versions were read from the Mac environment (queue job 421)
and are listed in the manuscript's data-availability section: Python 3.11.16, PySCF 2.14.0, pyberny
0.7.0, RDKit 2026.3.6, dftd4 4.2.0, tblite 0.7.0, xtb 6.4.1, thermo 0.6.1, chemicals 1.5.2, ugropy
3.2.0, NumPy 2.4.6, SciPy 1.17.1, pandas 3.0.6, PyTorch 2.13.0, mace-torch 0.3.16, ASE 3.29.0 and
Matplotlib 3.11.2. These are the versions present at closeout; packages were updated during the project
and the manuscript says so. The ThermoML input is the five-journal TRC archive (2020 snapshot) with
benchmark split SHA-256 d414402911946b14165a168ce40b8c00694d52de245adb6451fb6f65d7a2ffb6. No package
version or model hash was invented; the MACE-OFF23 weights are identified by loader call only.

## Figure inventory

All five captioned PNG files exist under manuscript/figures at the pinned R17 base. At closeout the
pixels of Figures 1, 4 and 5 were inspected and each was paired with its stored inputs read-only (jobs
424 and 426; details in round17/RESULTS.md). The committed bytes equal the files on the Mac. There is no caption-only
figure among those five. No additional P54 or LV1 figure is asserted to exist.

| Figure | Committed file | Git blob | Bytes | What can be done without scoring |
|---|---|---|---:|---|
| 1 | fig1_idac_parity_test.png | 72659886f5d3b451cf00adfe536a3715b1d6553a | 164834 | Export existing image. Original regeneration needs the exact historical private prediction CSVs and mask; no regenerated MAE in R17. |
| 2 | fig2_hbond_constants.png | c22a980ff1e3266e8865b84a2bac9c9deebe6367 | 36908 | Render from committed per-dimer and stored class-mean CSVs using r17_figures.py. |
| 3 | fig3_tradeoff.png | 62205ae989a86687abf91d99bdd9b1010d7cb46a | 45885 | Render stored main7 IDAC and VLE means using r17_figures.py, with each axis's own denominator. |
| 4 | fig4_lle_detection.png | 03560344877b0867a97b806b7014ebb477a7d8b5 | 44921 | Export existing image. Original private positive/negative arrays are needed for provenance; one operating point per model is not a full ROC curve. |
| 5 | fig5_error_map.png | 78e50e66d2dc842667e0ed5aa2a9e42a42a7fece | 78089 | Export existing image. Committed family aggregates are not certified to have the original figure's common mask, so do not relabel an alternative rendering as an exact regeneration. |

The old scripts/make_figures.py reads private prediction files at module import before the public-only
figure sections. It can also recompute metrics and silently skip absent model inputs. It is therefore
not the zero-score regeneration command for R17. The isolated helper reads only three fixed public
files and writes Figures 2 and 3 into a fresh external directory. It promises data-source fidelity,
not pixel identity with the original plotting environment. Exporting Figures 1, 4 and 5 from the Git
object preserves their exact original bytes but does not replace their pending source-array audit.
