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
| 5, Hsieh et al. | Fluid Phase Equilib. 2014, 367, 109-116 | https://doi.org/10.1016/j.fluid.2014.01.032 | A corrigendum exists at 384, 14-15, DOI 10.1016/j.fluid.2014.10.019. Its author-institution record is verified; original publisher text and implications remain outstanding. |
| 6, Bell et al. | J. Chem. Theory Comput. 2020, 16(4), 2635-2646 | https://pubs.acs.org/doi/abs/10.1021/acs.jctc.9b01016 | Complete citation verified at ACS. Its 2,261-compound distribution count is distinct from the project's reported 2,259-entry inventory. |
| 7, Gmehling et al. | Ind. Eng. Chem. Res. 1993, 32(1), 178-193 | https://doi.org/10.1021/ie00013a024 | Cite the actual 2016 parameter update as well; the 1993 paper alone does not identify the DOUFIP2016 software table. |
| 8, Hoffmann et al. | Nat. Commun. 2026, 17, 3485; published 14 April 2026 | https://www.nature.com/articles/s41467-026-71430-y | Publisher gives 824,481 data points. The project still needs its deployed weight/version receipt and row-overlap scope; publication metadata does not recover those. |
| 9, Frenkel et al. | Part 1 is J. Chem. Eng. Data 2003, 48(1), 2-13 | https://pubs.acs.org/doi/abs/10.1021/je025645o | Replace the draft's unspecific 2006, 51, 1504 series placeholder with this identified Part 1 article. Online December 2002 does not change the 2003 issue citation. |
| 10, Herington | The draft identifies J. Inst. Petrol. 1951, 37, 457 | No original publisher record recovered | Keep explicitly provisional. Title and complete range need a primary archival record; do not manufacture a DOI. A later paper citing these coordinates is not the original source. |
| 11, Onsager | J. Am. Chem. Soc. 1936, 58(8), 1486-1493 | https://doi.org/10.1021/ja01299a050 | Complete DOI and range; the implementation's convention needs its own code citation. |
| 12, Wertheim I-IV | 1984, 35, 19-34 and 35-47; 1986, 42, 459-476 and 477-492 | https://doi.org/10.1007/BF01017362 ; https://doi.org/10.1007/BF01017363 ; https://doi.org/10.1007/BF01127721 ; https://doi.org/10.1007/BF01127722 | Replace the incomplete parenthetical series reference with explicit I-IV identities. These papers do not validate the project's particular site mapping or inversion. |
| 13, Caldeweyher et al. | J. Chem. Phys. 2019, 150(15), 154122, DOI 10.1063/1.5090222 | https://www.cambridge.org/engage/chemrxiv/article-details/60c74060f96a006646286291 | Author preprint/version-of-record link supports identity. Direct AIP publisher retrieval was unsuccessful, so direct publisher verification stays open. Do not cite a preprint DOI as the final journal DOI. |
| 14, Bannwarth et al. | J. Chem. Theory Comput. 2019, 15(3), 1652-1671 | https://doi.org/10.1021/acs.jctc.8b01176 | Complete GFN2-xTB title, DOI and range; actual tblite/geometry versions are separate provenance. |
| 15, Grimme | Chem. Eur. J. 2012, 18(32), 9955-9964 | https://doi.org/10.1002/chem.201200497 | Complete range and DOI. Do not treat model quasi-RRHO thermochemistry as a measured liquid entropy. |
| 16, Sun et al. | J. Chem. Phys. 2020, 153(2), 024109 | https://doi.org/10.1063/5.0006074 | Complete citation. A package paper does not specify the pinned PySCF 2.14.0 source used in later diagnostics. |
| 17, Boys and Bernardi | Mol. Phys. 1970, 19(4), 553-566 | https://doi.org/10.1080/00268977000101561 | Use the original DOI and publication year, not a later reprint or digitization. |
| Added 18, Constantinescu and Gmehling | J. Chem. Eng. Data 2016, 61(8), 2738-2748 | https://doi.org/10.1021/acs.jced.6b00136 | Identify the 2016 update; also record the installed thermo parameter-table revision from existing execution receipts. |

The corrigendum author record is
https://scholars.ncu.edu.tw/zh/publications/corrigendum-to-considering-the-dispersive-interactions-in-the-cos/ .
No correction's uninspected contents are asserted here. The complete reference audit uses publisher
records where accessible and labels the remaining author-record-only or unrecovered identities.

The submission archive should also identify the already-used MACE-OFF23 weight file and its corresponding
primary publication, along with exact model/software/data versions for PySCF, D4, GFN2-xTB/tblite, RDKit,
pyberny, thermo/ugropy, HANNA and the ThermoML snapshot. Method citations for the chosen basis/functional
and numerical integration belong in the supplement. These items must be taken from existing execution
receipts; R17 does not invent a package version, generate new chemistry or certify an absent model hash.
This is a finite editorial checklist, not a proposal to acquire a new validation dataset.

## Figure inventory

All five captioned PNG files exist under manuscript/figures at the pinned R17 base. The GitHub tree and
file metadata were checked, not their pixels or private underlying arrays. There is no caption-only
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
