Z-COSMO round 14: test the dielectric ingredient before committing to a liquid-permittivity campaign

Reference: `Victor-Liang-ChE/zcosmo`, main at `864aaac1e85eda31a43f24e856770c7f56ccb760`. The supplied patches add isolated review helpers and proposed documentation. They change no production solver, dielectric table or profile. P35's explanatory closeout remains intact. The requested main question is reopened separately. This report distinguishes proposed registered work from calculations actually executed here. [S1–S5]

| Rank | ID | Target / class | Mechanism and budget | Expected saving or speed-up | Effort |
|---:|---|---|---|---|---|
| 1 | P51 | `scripts/r14_dielectric.py`; E source, exposure and ingredient audit | Verify the public reference, freeze exact identity/state rules, and assess existing Onsager values before any phase-equilibrium score. Zero SCF and zero activity-model calls. | Avoids treating an unverified ingredient or an exposed dataset as a new physical validation. No solver acceleration claimed. | Low |
| 2 | P52 | `scripts/r14_oracle.py`; A experimental-input diagnostic with E integrity checks | One private Mac VLE comparison, at most 100 systems and ten observations per system, with baseline, experimental-ε and COSMO-SAC 2010 arms. At most 3,000 model requests and 7,200 serial seconds. | Tests practical leverage before a pilot costing tens of GPU-hours or a portfolio campaign costing thousands. Savings are avoided-work scenarios, not measured acceleration. | Moderate |
| 3 | P53 | `docs/astra/round14/STATUS_PROPOSED.md`; E reporting | Record the actual screening hypothesis, exposure and current-source association concern. Prepare the paper in parallel with the bounded checks. | Zero new physical computations; preserves the value of the existing results. | Low |
| Shared | H14, REG14 | Portable tests and prospective registration | Forty-five software tests and exact application/check commands. | No new scientific result or acceptance is implied by a software pass. | Low |
| Assessed, not authorized | Correlated-liquid ε, a new association architecture, direct simulation γ | A physical research alternatives | Compare the concrete designs and costs below. Native budget under these patches is zero. | No justified full-portfolio improvement forecast yet. | High to very high |

The ranking is by the value of the decision per unit of effort, rather than a fabricated probability of removing a particular number of VLE percentage points. The P51/P52 avoided-cost estimates overlap and must not be added. A dielectric investigation is worth a bounded check. The current evidence does not justify promising that it closes the VLE gap, and it does not justify launching roughly 740 liquid simulations now.

The premise needs a sign check

On the main7 IDAC common subset, Z0x's MAE is 0.762 against 0.815 for COSMO-SAC 2010 and 0.446 for UNIFAC Dortmund, on 708 observations in 163 systems. For HE on 6,311 common observations, Z0x is at 522 J/mol against 399 for COSMO-SAC 2010 and 314 for UNIFAC. This is a tradeoff across properties, not an overall superiority claim. The new check should preserve the existing IDAC/LLE evidence while addressing the VLE limitation. [S3]

The main7 comparison is 14.15% VLE AAD for Z0x versus 8.62% for COSMO-SAC 2010, a 5.53 percentage-point difference on 9,432 common observations. The 2017–2019 temporal common subset is different: 9.47% versus 7.28% on 7,722 observations. Neither comparison should be combined with the later Z0w3 denominators or the glycol-only score. The original test split and temporal set have both informed subsequent development. [S2–S4]

Current Z0x uses

\[
 c_{ES}(x)=c_0 f(\epsilon(x)),\qquad
 f(\epsilon)=\frac{\epsilon-1}{\epsilon+1/2}
             =1-\frac{3/2}{\epsilon+1/2},\qquad
 f'(\epsilon)=\frac{3/2}{(\epsilon+1/2)^2}>0.
\]

Thus raising the stored ε increases the electrostatic coefficient toward its conductor value. The historical improvement from conductor Z0 to Z0e and then composition-dependent Z0x does not establish that raising water's or methanol's ε improves VLE. Z0s obtained lower VLE error by a different, train-selected optical-screening choice, with worse IDAC. It is not an experimentally unselected physical answer to this question. [S2–S4, S6]

Using the stored water value 52.9379836613 and the prompt's approximate experimental value 78, f changes from 0.97193008 to 0.98089172: a 0.922% increase in c_ES. Methanol, 24.4472235738 to approximately 33, gives 0.93987307 to 0.95522388, a 1.633% increase. These arithmetic probes use already-exposed approximate values. They are not the proposed reference benchmark and did not generate a new ε estimate. They also are not bounds on ln γ or pressure. [S6, S7]

There is more possible leverage in low-to-moderate permittivities and in a mixture's composition derivative. With the unchanged volume mixing rule,

\[
 \epsilon(x)=\frac{xV_1\epsilon_1+(1-x)V_2\epsilon_2}{xV_1+(1-x)V_2},\qquad
 \epsilon'(x)=\frac{V_1V_2(\epsilon_1-\epsilon_2)}{[xV_1+(1-x)V_2]^2}.
\]

Replacing ε must update both c_ES and its derivative. A helper that changes only an energy coefficient while leaving the old composition derivative can break the intended excess-Gibbs construction. P52 changes the instance's two ε values before its first query; both existing code paths then read those values. It retains the current volume rule and all other constants. [S6]

The source gives c₀ = 12,226.2353 in its COSMO units. The fitted 2010 electrostatic coefficient at 298.15 K is about 8,197.2422. Equating only those coefficients would require f ≈ 0.67046, equivalent to ε ≈ 4.05185 in this particular mapping. That is an algebraic comparison, not a proposal to use ε = 4, a fit or a universal liquid value. It highlights a separate issue: accurate macroscopic bulk permittivity does not by itself validate the mapping to a local segment-contact coefficient. [S6, S8]

The current Onsager estimate has several ingredients that can compensate for one another: an xTB dipole evaluated at one MMFF geometry, D4 polarizability and inverse COSMO cavity volume as number density. The missing orientational correlation is only one approximation. The stored table also contains highly polar aprotic and nominally nonpolar molecules, so a water/methanol-only diagnosis cannot establish a uniform bias. The full reference-matched census is deliberately left for P51 rather than inferred from the table's first entries. [S7]

What a defensible correlated ε would require

For a fixed-volume, isotropic liquid with an explicitly defined electric-field coupling, a useful starting point is

\[
 H(R,E)=H_0(R)-M_0(R)\cdot E-\tfrac12 E\cdot\alpha_{cell}(R)E+O(E^3).
\]

Differentiating its equilibrium partition function at zero field gives

\[
 \epsilon_{ab}=\delta_{ab}+\frac{1}{\epsilon_0 V}
 \left[\langle\alpha_{cell,ab}\rangle+
 \frac{\operatorname{Cov}(M_{0,a},M_{0,b})}{k_BT}\right].
\]

For an isotropic sample the scalar value uses one third of the trace. The fluctuation formula must correspond to the electrostatic boundary condition, ordinarily conducting or tin-foil conditions for the usual periodic expression. A simulation's boundary-dependent total-dipole fluctuation is not automatically the infinite-liquid Kirkwood correlation factor. [U1]

This derivation also clarifies the dipole-model issue. Adding a stated postprocessed dipole observable to a zero-field potential defines a field-dependent model when its coupling is specified. It is meaningful to measure that model's response. It is a separate question whether it represents a real liquid. Energy/force accuracy at zero field and a reasonable hydrogen-bond count do not validate that field coupling.

| Option | Stated physical model | Defensible use and principal limitations |
|---|---|---|
| Fixed-monomer dipoles on existing MACE trajectories | Obtain a gas-phase dipole vector for each neutral reference molecule without experimental fitting. Rotate the fixed vector with each molecule's proper body-frame orientation; sum vectors to obtain M. Specify the electronic field-response term once. | Cheapest correlation-sensitive A diagnostic. It omits environment-induced dipole changes and internal-coordinate dependence. Methanol's internal OH motion makes a rigid-body approximation testable rather than automatically adequate. It is not a validated liquid ε merely because the trajectory is first-principles-trained. |
| Instantaneous molecular or local-environment dipole model | Use whole-molecule geometry-dependent xTB dipole vectors, or a separately validated equivariant dipole/polarizability model trained solely on electronic-structure labels. Specify how environmental induction and intermolecular charge transfer enter. | Stronger candidate, with explicit dipole-label cost. Isolated-molecule xTB still omits environmental polarization. Arbitrarily cut clusters have artificial boundaries; embedded/periodic labels need their own convergence study. No verified ready-to-run bulk dipole model for this project's teacher has been supplied here. |
| Kirkwood–Fröhlich with a simulated correlation factor | Evaluate a bulk, boundary-corrected orientational correlation factor, a separately specified permanent dipole convention, number density and ε∞. | Defensible only with mutually consistent conventions. It is not valid to insert an uncorrected finite-box dipole ratio and then add electronic polarization a second time. |
| Cluster or dimer QM g estimate | Integrate orientational correlations with a specified liquid pair-distribution or cluster-statistical model. | A dimer minimum or its binding energy alone does not determine bulk g. Coordination, competing orientations, many-body polarization and long-range correlations are missing. A small-cluster rule is an additional A closure, not a uniquely first-principles replacement for Onsager. |

In a fixed-length permanent-dipole convention, the relevant bulk quantity has the form

\[
 g_K=1+\frac{1}{N\mu_0^2}\sum_{i\ne j}
       \langle\boldsymbol\mu_i\cdot\boldsymbol\mu_j\rangle
\]

with the appropriate bulk limit and boundary convention. Parallel association can increase it, while antiparallel structure can decrease it. A bonded-donor fraction of 0.87 supplies neither the dot products nor the collective correlation integral. Choosing a multiplicative g from experimental ε would be fitting the ingredient, which is outside the proposed fit-free candidate rules.

The Kirkwood–Fröhlich relation, under its own permanent-dipole and optical-response assumptions, is

\[
 \frac{(\epsilon-\epsilon_\infty)(2\epsilon+\epsilon_\infty)}
      {\epsilon(\epsilon_\infty+2)^2}
 =\frac{n\mu_0^2g_K}{9\epsilon_0k_BT}.
\]

The helper implements its positive quadratic root for algebra tests. This does not implement or validate a simulator for g_K. The current Onsager source corresponds to the g_K = 1 version of this algebra, with its own Clausius–Mossotti estimate of ε∞. [S7]

Electronic polarization needs one convention throughout. For the explicit field-response model above, the covariance contains the zero-field total dipole, including any environment-induced part represented by M₀. The α term represents the additional response to the applied field. Adding that derivative once is different from adding another empirical optical correction to an already complete susceptibility. A KF local-field transformation and a separately added D4/Clausius–Mossotti contribution cannot be stacked without a derivation. Conversely, deleting every polarization contribution on the theory that “COSMO already includes it” is also unjustified: the profile generation and the bulk-field response play different roles. Keep conductor profiles fixed during an ε test; do not recompute finite-ε profiles and rescale their interaction a second time in the same intervention.

The smallest physical pilot I would consider after the zero-QC tasks is four liquids, water, methanol, acetonitrile and benzene. The last two prevent the exercise from becoming a correction selected only for hydrogen-bond donors. Start with a declared field/dipole model, not just a list of charges. A fixed-vector model can be a feasibility screen, but needs comparison with geometry-dependent dipole vectors on independently selected snapshots before its ε is treated as an ingredient candidate. A more complete model needs independent condensed-environment labels as well. Those are physical acceptance data, not ThermoML selection targets.

For any such pilot, retain two independent seeds and two sizes, for example 64 and 128 molecules. Equilibrate at the model's own pressure/density, then use a clearly defined NVT production ensemble for the displayed response formula. A proposed allocation is 50 ps equilibration and 500 ps production per trajectory at 0.5 fs. This is a capped trial, not a claim of convergence. Require a stable liquid and complete molecular connectivity, molecule-whole dipoles, removal of the sample mean, and finite-size/replica agreement within 10% plus their estimated uncertainty. Require relative statistical uncertainty no larger than 10%, and convergence of blocked estimates of the collective variance rather than only the mean energy or hydrogen-bond fraction. A failed or inconclusive member blocks pilot acceptance. The number of saved frames is not the number of independent variance samples.

Density agreement in the old teacher does not satisfy these conditions. Its short trajectories were registered for a structural association referee. Its water density is about 10% high; that directly changes number density and can also change orientational correlations. The current `MultiMACE` is an energy/force evaluator with fixed cell arrays and minimum-image assumptions. Its L > 2(r_cut + skin) condition and cell/neighbor rebuilding must remain valid during any future volume change. Simply modifying a box-length scalar is not a validated NPT implementation. The archived teacher's registration and current batching/TI code were inspected, but the exact historical `md_liquid_v4.py` NPT driver was not recovered through the connector in this review. Its source and trajectory provenance must be frozen before reuse; I do not claim it is absent from the maintainer's private holdings. [S4, S9]

Temperature must also be explicit. The present table is at 298.15 K but is used as a constant over the activity model's temperature range. A new ε(T) changes excess enthalpy through dε/dT and may require density and population changes. Three temperatures are not automatically sufficient near a transition. The first P52 diagnostic therefore substitutes experimental ε at 298.15 K and keeps it constant, isolating the same ingredient convention. It neither extrapolates a source correlation into an invalid liquid range nor claims an ε(T) correction to HE.

Free-compute sizing, not a portfolio promise

Four liquids times two sizes times two seeds gives 16 trajectories. At 550 ps total and 0.5 fs, each requires 1.1 million steps, or 17.6 million system-steps overall. Assuming an amortized 3–10 ms per system-step gives 14.7–48.9 GPU-hours, before dipole labels, extra convergence controls, packing failures or data transfer. This bracket is a scenario informed by the old batching measurements, not a new benchmark of those particular liquids and sizes. Individual-atom counts and graph sizes differ, so the favorable small-water throughput cannot be applied universally. [S9, S10]

Applying the same two-size/two-seed trial to 740 compounds gives 3.256 billion system-steps, or approximately 2,713–9,044 GPU-hours at the same assumed costs. At an assumed available 30 GPU-hours per week, that alone is about 90–301 weeks. Three independent temperatures roughly triple the dynamics allocation. The quota is the project's stated planning allowance, not a verified guarantee of future availability. Several compounds do not form a stable neutral liquid at 298 K and ambient pressure, so a blanket run also lacks a universal physical state definition.

Dipole labeling can be the dominant extra cost. Four fixed reference vectors cost only four small molecular calculations, but give the weakest response model. Evaluating every molecule in 5,000 saved configurations for the above pilot would require 7.68 million isolated-molecule dipole evaluations. Even a 0.01-second amortized label would add about 21 hours, and a 0.1-second label about 213 hours, before accounting for model error. An electronic-label-trained predictor can reduce inference cost but introduces a separate training and transfer-validation project. These are additional scenario calculations, not measured xTB timings.

A justified subset rule would therefore be explicit: only the four predeclared pilot liquids can ever receive pilot values after independent validation; every other key retains its original stored ε. Failed pilot output is not silently mixed with successful output. A rollout to another chemical class requires a new applicability and validation decision. No per-molecule choice between candidate and Onsager is made by whichever experimental error is lower.

P51: the ingredient benchmark before phase-equilibrium scoring

The verified public source is the CRC-derived liquid-permittivity table in `CalebBell/chemicals`, pinned to commit `e79047588b30cfabc564c79fb26d760c746877d7`, with Git blob `bf12ffba51b478a021acc6ed58778c04deb9b988`. The exact source path and retrieval URL are embedded in the helper. The official library documentation describes the liquid data and its polynomial representation. The repository file's schema was retrieved and inspected. The full source/reference join and its errors have not been computed here. [U2]

| Source | Verified location and content | Limit of what is established |
|---|---|---|
| Liquid static-permittivity compilation | [Pinned TSV](https://github.com/CalebBell/chemicals/blob/e79047588b30cfabc564c79fb26d760c746877d7/chemicals/Electrolytes/Permittivity%20%28Dielectric%20Constant%29%20of%20Liquids.tsv), [official module documentation](https://chemicals.readthedocs.io/chemicals.permittivity.html) | CAS, reference T and ε, polynomial coefficients and valid ranges. A compilation with fitted interpolations, not a new ab initio source. Row-level original laboratory provenance and uncertainty are not fully supplied by this TSV. |
| Water reference | [IAPWS release on static dielectric constant](https://iapws.org/relguide/Dielec.html) | A scientific reference formulation for water, not a fit-free candidate input. It is supplementary context, not an alternative source selected after seeing the CRC comparison. |
| NIST ThermoML archive | [NIST data record](https://data.nist.gov/od/id/mds2-2422), [TRC archive](https://trc.nist.gov/ThermoML/) | The documented 2020 collection includes publications through 2019. I did not verify a newer bulk export with post-2019 coverage. A current webpage date is not evidence of new measurements. |
| Post-2019 VLE acquisition candidate | [2023 ethyl-acetate/methylcyclohexane study record](https://acs.figshare.com/articles/journal_contribution/Separation_of_Azeotropic_Mixtures_of_Ethyl_Acetate_Methylcyclohexane_Vapor_Liquid_Equilibrium_Measurements/22331073), [record API](https://api.figshare.com/v2/articles/22331073) | Public study/supporting-material metadata, with a description of VLE measurements. Its abstract contains numerical information and has been exposed during this review. Individual machine-readable measurement rows and their eligibility have not been verified. It is not a certified blind benchmark. |

The distinction between independent property and independent evidence matters. Static permittivity is a different response from VLE/HE/IDAC, so comparing against it is a legitimate ingredient test. That does not prove disjoint laboratories, papers, chemical systems or earlier developer exposure. Handbook compilations may share source papers or materials with other thermophysical datasets. Inspecting water and methanol beforehand is also real exposure. P51 records these limitations. Neither the repository's absence of a prior ε score nor the public availability of a table proves statistical independence.

Identity matching is deliberately conservative. Each exact stored InChIKey must resolve through the existing project UD index to one checksum-valid CAS, that CAS to one project key, and that CAS to one source entry. Ambiguous stereochemistry, missing identifiers and duplicate reference CAS values are not resolved by choosing the closest ε or a chemical-name synonym. The ingredient matching rule is intentionally stricter than the existing unique-connectivity sigma-profile fallback. All exclusions remain visible in the coverage report.

At 298.15 K, use the source polynomial only inside its stated range; otherwise require a tabulated point within 0.10 K. The helper requires A/B and interprets absent higher-order terms as zero under the documented polynomial convention. A liquid value at 293.2 K is not silently called a 298.15 K reference. No critical-state, solid or gas value is inferred from a compound's name. Values with missing or invalid stored ε stay in the accounting, and a reference-matched invalid stored value blocks the complete aggregate.

The primary error is equal-compound mean |ln(ε_model/ε_ref)|. Report median log error and signed log bias, along with mean/max relative ε errors and mean |f_model−f_ref|. The f metric captures screening sensitivity that a raw ε error can obscure. No one metric substitutes for the pressure calculation.

For a future independently computed four-liquid candidate, the proposed ingredient gate is complete coverage, mean log error at most 80% of its same-panel Onsager baseline, mean |Δf| ≤ 0.02, maximum relative ε error ≤ 25%, and no member's absolute log error worsening by more than 0.05. Numerical dipole/sampling validation is an additional requirement. These are prospectively fixed engineering criteria, not constants to optimize or estimates of a confidence level. The helper tests this arithmetic, but its Boolean validation arguments are not a physical certificate. No physical candidate is generated or accepted in R14.

P52: an experimental-ε oracle, with a narrow meaning

The oracle is worth running after P51 because it asks whether a more accurate input under the existing closure has useful pressure leverage. It is not zero computational cost: it uses up to 3,000 activity-model evaluations, but zero new quantum or MD calculations. It is experimental-input scoring against ThermoML and is therefore preregistered explicitly. It can never become the project's fit-free model through a favorable result.

The helper selects from an operator-designated, source-hashed historical Z0x VLE archive. It retains original test_one/test_both observations with valid temperatures, positive pressures ≤500 kPa and both reference permittivities. Strict interior compositions exclude the separate near-endpoint finite-difference strip. Up to 100 unordered systems are selected by a fixed SHA ordering, with up to ten observations per system. No observed error enters selection. Original file-row ordinals, bound to the full archive hash, are the query identities. A small or reference-biased eligible universe is reported rather than silently expanded.

The chosen scope is a bounded exposed diagnostic, not a recreation of all 9,432 main7 common observations. It also is not a general benchmark for every dielectric-table compound. Its fresh COSMO-SAC baseline is evaluated on the identical selected rows. Comparing its oracle AAD to the historical 8.62% from another subset would be invalid.

Each selected pair receives the current stored-ε Z0x baseline, experimental-ε Z0x, and COSMO-SAC 2010. All three use the same UD profiles and frozen pure-component saturation pressures. `zcosmo.scope.psat` takes an InChIKey and returns kPa, which matches the archive's P. The draft adapter was checked against that actual interface and its unit convention. The source compound table and installed property-provider versions are frozen with the plan. No vapor-pressure correlation is selected by its effect on the oracle.

Before either later arm starts, the current stored-ε baseline must reproduce the archived pressure to relative error below 1e-7 on every selected observation. This is a deliberately tight replay condition. A failure can indicate a historical source-version or property-provider change, including an older numerical branch; it is not a failed ε hypothesis. The code blocks subsequent scoring rather than weakening the gate or mixing baselines. An actual mismatch would need a separate reproduction decision before new scientific output.

The oracle updates `.eps` before any call and uses the existing analytic composition derivative. Profile overrides resolve both components explicitly in an isolated fresh process. There is no silent fallback for a missing overlay file, and a process-global profile cache cannot retain another arm. P28 is set identically, while selected rows remain outside its endpoint scope. Experimental ε298 stays constant with T, exactly isolating the current constant-table convention.

All jobs have recorded identities before execution. A permanent claim prevents rerunning a plan into another output directory. Each worker has a 120-second deadline; the driver has 7,200 seconds. Attempt receipts are written before model calls. A missing or nonfinite new result withholds complete aggregate errors, rather than producing a smaller favorable intersection. The check command replays saved arithmetic and verifies hashes without additional model calls. Private paths and row-level predictions are excluded from the public allowlist.

Report pressure AAD and signed bias, equal-system AAD, paired oracle change and residual comparator gap. For the selected sample only,

\[
 H=\mathrm{AAD}_{baseline}-\mathrm{AAD}_{experimental\ \epsilon},\qquad
 R=\mathrm{AAD}_{experimental\ \epsilon}-\mathrm{AAD}_{2010}.
\]

Their sum is the same-subset baseline-to-2010 gap. A recovery ratio H/(H+R) is reported only for a positive non-negligible denominator, without clipping. No positive result guarantees that a fit-free estimator reproduces it. A negative result does not prove that no better dielectric/contact theory exists; it questions this pure-ε substitution within this particular mixture rule and profile convention.

| Oracle outcome | Decision supported |
|---|---|
| Little pressure change despite sizeable ε errors | Bulk ε accuracy alone has limited practical leverage on this selected sample under the current closure. Do not launch a portfolio MD campaign to pursue that small lever. |
| Worse VLE with reference ε | The old approximation may compensate for another model error. Do not tune g or select a different experimental table to recover the previous score. |
| Substantial improvement | There is empirical-input headroom for the declared closure on these exposed rows. A physical estimator still needs independent ingredient validation and its own new-source evaluation. |
| Failed replay, insufficient coverage or incomplete output | No complete headroom result. Preserve the failure record; do not call it evidence for or against orientational correlation. |

No retrospective percentage threshold is used to select among physical recipes. Even a very large oracle improvement cannot authorize choosing g, a volume scale, temperature rule or training target from phase-equilibrium error. The initial scientific choice is frozen; the diagnostic only decides whether further investigation is worth proposing.

An honest next evaluation

Keep the original split and all reported results. Describe a new variant as motivated by exposed evidence and frozen before its own execution. A single additional look at the old split can be a transparent fixed-design comparison, but it cannot recover the sampling guarantees of a holdout used only once. System bootstrap intervals on that set describe variation within an exposed dataset; they do not erase adaptive model development.

A genuinely new validation needs a custodian. Before the candidate is finalized, the custodian records source files and checks overlap by DOI, publication, molecular identity, binary pair and numerical measurement series against both old archives and exposed analyses. The model developer receives only eligibility and state metadata. Any later measurement from the same study, duplicate republication or exposed abstract belongs in the exposure ledger. Old glycol observations remain excluded from a new acceptance decision, while water and branched-polyol controls remain compulsory physical checks rather than favorable subsets.

Freeze the candidate rule and its fallback, applicable elements/liquid states, experimental-source hashes and endpoint/temperature conventions before revealing new responses. Use the original primary VLE AAD definition and a paired system-level bootstrap, with coverage and independent chemical-system counts. A study of one binary is a useful external case study but cannot support a universal claim to close the VLE gap. No particular sample size is asserted to provide power without a prospective variance/power calculation.

The verified NIST bulk archive does not supply the requested new post-2019 holdout. The 2023 ACS record is a concrete acquisition lead, but its abstract is now exposed and its raw rows were not validated here. No genuinely unexposed multi-system VLE/HE dataset has been certified during this review. That is an exposure limitation to record, not a reason to invent a download URL or a new split label. P51's receipt explicitly marks incomplete private-history auditing, and P52 is restricted to exposed data.

Rank against association and direct simulation

The explicit COSMO HB switch has already been turned off in Z0w and its descendants. Proposing that switch as a new fix would repeat earlier work. The remaining architectural problem concerns the contact/reference partition, electrostatic overlap, site multiplicities and consistency between simulated densities and the mass-action inversion. The existing nitrogen-site mismatch and noisy temperature fit make a universal inversion particularly doubtful. Matching a simulated bonded fraction is not proof that TPT1 is a correct excess chemical-potential model. [S4, S11]

There is also a current-source implementation issue distinct from those scientific failures. The association subclasses implement their additional free energy through `_g`. The optimized base `Z0xBinary.lngamma` uses `_analytic` in the interior and `_endpoint` under P28, bypassing that subclass override. A source-level synthetic regression reproduces this bypass on the verified current base class. Fresh current-main association predictions must therefore be quarantined until dispatch is audited and repaired under a separate registration. This does not retroactively invalidate archived w/w2/w3 results produced with earlier code. P52 does not run those classes. [S6, S11]

An actual association redesign would need a new, physically justified reference Hamiltonian or contact partition, then independent dimer/cluster and liquid validation. Simply adding simulated bond strengths to a residual model and scoring a fourth TPT1 variant on the same data is not justified. Of the possible large projects, a properly defined replacement architecture could have more direct leverage than a small high-ε correction, but its physical closure is currently less complete. No free-compute performance claim is established for it.

Direct simulation avoids the local-contact closure only if the molecular potential and free-energy calculation are valid. For the usual number-density standard-state convention,

\[
 \ln\gamma_i^\infty=\beta\left[\mu_i^{ex}(j)-\mu_i^{ex}(i)\right]
                   +\ln(\rho_j/\rho_i).
\]

Both excess chemical potentials and the density term are required. A well-converged hydration free energy alone is not a complete activity coefficient. The existing soft-core/cavity TI path supplies a feasibility basis, but overlap, finite-step bias, independent equilibration and effective sample size remain requirements. [S9, S10]

The old 30 ps/window experiment, at 0.5 fs and 114–125 ms per batched step, corresponds to roughly 1.9–2.1 GPU-hours for a single such free-energy leg, excluding preparation. Its quoted statistical SE was about 0.23 kcal/mol. For an illustrative target SE of 0.1 in ln γ at 298.15 K, two equally uncertain independent legs each need about 0.0419 kcal/mol. Assuming unchanged variance and inverse-square-root scaling, the sampling multiplier is approximately (0.23/0.0419)^2 = 30.1. That suggests about 115–126 GPU-hours per independent two-leg result, before systematic errors. Reusing pure-component references can save later work, and better sampling can improve this scenario, but neither turns the present short probe into a validated all-pairs engine. [S10]

The first-principles claim also needs precise scope. A potential trained on electronic-structure data is fit-free with respect to the target experimental benchmark, but is still a learned approximate Hamiltonian. Its exact free energy need not equal a real liquid's free energy. Current MACE density and bonding checks are useful validations of a limited scope, not general dielectric or chemical-potential certificates. [S4, U3]

My recommendation is to execute P51 and one P52 run, and continue writing the existing paper now. There is a real, falsifiable possibility of improvement from correcting low-to-moderate ε inputs or from identifying an inadequate mixing/contact rule. There is not enough evidence to promise closure of the 5.53-point main7 gap using a fit-free g correction within the free budget. Association redesign and direct γ remain separately scoped research programs, not automatic fallbacks when the oracle is disappointing.

Code and reporting issues to retain

The dielectric generator silently clips the Clausius–Mossotti parameter at 0.95, implying an optical estimate of 58 at the cap. It ignores embedding/MMFF status and collapses calculation failures into NaN without per-molecule reasons. It also writes a new dielectric table without the prospective manifest machinery used in later review rounds. These are audit/provenance concerns; the supplied code does not remove the cap, change a geometry or reinterpret existing results. P51 exposes missing/invalid values rather than repairing them by an unregistered rule. [S7]

The current manuscript's statement that no experimental thermodynamic data are used anywhere in Z0 is broader than the defensible claim about its interaction constants. Its profile conventions and documented upstream conformation history have their own provenance, and VLE uses the same experimental/correlative vapor-pressure provider as its comparators. The later examined test sets should not be described as newly untouched for an R14 variant. P53 gives exact replacement-scope wording without altering any historical score. It also preserves the completed P35 explanation rather than restarting its geometry search. [S5, S12]

Execution and verification record

Executed here: repository source review and public reference-location checks; screening/KF and cost arithmetic; forty-five portable tests, including successful and failed mocked oracle runs, immutable output/tamper checks, and a real subprocess timeout test with no chemistry. The current base `z0x.py` was reconstructed byte-for-byte and verified against Git blob `c558d4e95db9b78f3b57d6a103a293e21feeb9af` before testing its dispatch with synthetic dependencies. The public reference schema was inspected, but its full joined benchmark was not calculated. Patch and command checks are recorded below after extraction.

Not executed here: the Mac-only CRC acquisition/ingredient census, any real ε benchmark, the VLE oracle, a new SCF, a liquid simulation, a model score or a remote repository modification. The full dielectric-table census and exact historical NPT-driver audit remain maintainer-side prerequisites where applicable. No private UD data was retrieved. PySCF, thermo and chemicals are unavailable in this runtime; no installation was attempted. Tests use synthetic chemical inputs and model adapters, not a substitute for native acceptance. The working source subset is a verified reconstruction, not a complete repository clone.

Exact application and execution commands

Save this report outside the repository. From the exact baseline checkout, extract and apply its five patches. The extraction checks the expected patch identifiers instead of blindly running every code fence. All real-data commands below are for the asset-bearing Mac and retain output outside Git.

```bash
set -euo pipefail
BASE=864aaac1e85eda31a43f24e856770c7f56ccb760
test "$(git rev-parse HEAD)" = "$BASE"
: "${R14_REPORT:?Set R14_REPORT to the downloaded ZCOSMO_ROUND14_REPORT.md}"
export R14_PATCHES="$(mktemp -d)"
python - <<'PY'
import os,re
from pathlib import Path
text=Path(os.environ['R14_REPORT']).read_text()
items=re.findall(r'<!-- BEGIN PATCH (\w+) -->\s*```diff\n(.*?)\n```\s*<!-- END PATCH \1 -->',text,re.S)
assert [x[0] for x in items]==['P51','P52','H14','P53','REG14']
root=Path(os.environ['R14_PATCHES'])
for name,body in items:(root/(name+'.patch')).write_text(body+'\n')
PY
for p in P51 P52 H14 P53 REG14; do
  git apply --check "$R14_PATCHES/$p.patch"
done
cat "$R14_PATCHES/P51.patch" "$R14_PATCHES/P52.patch" \
  "$R14_PATCHES/H14.patch" "$R14_PATCHES/P53.patch" \
  "$R14_PATCHES/REG14.patch" > "$R14_PATCHES/all.patch"
git apply --check "$R14_PATCHES/all.patch"
git apply "$R14_PATCHES/all.patch"
PYTHONPATH=src:scripts python scripts/r14_selftest.py
PYTHONPATH=scripts python scripts/r14_dielectric.py screening
python -m py_compile scripts/r14_dielectric.py scripts/r14_oracle.py scripts/r14_selftest.py
```

The next block records adoption. It does not execute an experiment merely by adding a proposed registration file. The three helper files are checked against this exact registration commit on each real operation.

```bash
set -euo pipefail
umask 077
printf '\nRound 14 adopted at %s\n\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> PREREGISTRATION.md
cat docs/astra/round14/REGISTRATION_PROPOSED.md >> PREREGISTRATION.md
git add scripts/r14_dielectric.py scripts/r14_oracle.py scripts/r14_selftest.py \
  docs/astra/round14/REGISTRATION_PROPOSED.md docs/astra/round14/STATUS_PROPOSED.md \
  PREREGISTRATION.md
git commit -m "Register R14 dielectric ingredient and exposed VLE oracle diagnostic"
export R14_REG="$(git rev-parse HEAD)"
export R14_PRIVATE="${R14_PRIVATE:-$HOME/zc-r14-20261008}"
mkdir -p "$R14_PRIVATE"
chmod 700 "$R14_PRIVATE"
export PYTHONPATH=src:scripts
python scripts/r14_dielectric.py catalog
python scripts/r14_dielectric.py acquire --registration "$R14_REG" \
  --out "$R14_PRIVATE/source" > "$R14_PRIVATE/acquire.log" 2>&1
/usr/bin/time -p python scripts/r14_dielectric.py ingredients \
  --registration "$R14_REG" --source "$R14_PRIVATE/source" \
  --out "$R14_PRIVATE/ingredients" > "$R14_PRIVATE/ingredients.log" 2>&1
python scripts/r14_dielectric.py check --out "$R14_PRIVATE/ingredients" \
  > "$R14_PRIVATE/ingredients-check.log" 2>&1
```

Inspect `ingredients.json` locally. It is the ingredient score and coverage record, not a production ε table. A real invalid-baseline or state/identity problem must be reported, not corrected by choosing a new source after examining errors. Preparation of P52 requires a completed ingredient result.

```bash
set -euo pipefail
umask 077
: "${R14_REG:?Run the registration block first}"
: "${R14_PRIVATE:?Run the registration block first}"
: "${R14_VLE_ARCHIVE:?Set to the original Z0x VLE CSV with c1,c2,T,x1,P,pred_P,split}"
: "${R14_PROFILE_ROOT:?Set to the main Mac checkout's data/pyscf_sigma}"
: "${R14_UD_PROFILES:?Set to the main Mac checkout's data/raw/nist/UD/sigma3}"
export PYTHONPATH=src:scripts
python scripts/r14_oracle.py freeze --registration "$R14_REG" \
  --ingredients "$R14_PRIVATE/ingredients" --archive "$R14_VLE_ARCHIVE" \
  --profile-root "$R14_PROFILE_ROOT" --ud-profiles "$R14_UD_PROFILES" \
  --out "$R14_PRIVATE/oracle-plan" > "$R14_PRIVATE/freeze.log" 2>&1
cp "$R14_PRIVATE/oracle-plan/PLAN_SHA256.txt" docs/astra/round14/ORACLE_PLAN_SHA256.txt
git add docs/astra/round14/ORACLE_PLAN_SHA256.txt
git commit -m "Freeze R14 private oracle plan digest"
export R14_PLAN_COMMIT="$(git rev-parse HEAD)"
set +e
/usr/bin/time -p python scripts/r14_oracle.py run \
  --plan "$R14_PRIVATE/oracle-plan/plan.json" --plan-commit "$R14_PLAN_COMMIT" \
  --out "$R14_PRIVATE/oracle" > "$R14_PRIVATE/oracle-run.log" 2>&1
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  printf 'R14 returned status %s. Preserve all receipts; do not retry.\n' "$rc"
  exit "$rc"
fi
python scripts/r14_oracle.py check \
  --plan "$R14_PRIVATE/oracle-plan/plan.json" --plan-commit "$R14_PLAN_COMMIT" \
  --run "$R14_PRIVATE/oracle" > "$R14_PRIVATE/oracle-check.log" 2>&1
# Only public-errors.json is eligible for separate human-reviewed publication.
# Do not commit the private plan, reference table, logs or worker outputs.
```

The checker may be rerun without model calls. An interrupted or failed claimed execution may not be restarted. A zero-model check after a failure can inspect receipts, but cannot turn incomplete coverage into a successful scientific result. The code intentionally includes no MD launch command or production ε override.

Sources

[S1] [Round-14 prompt](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/docs/astra/ROUND14_PROMPT.md) and [optimization brief](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/docs/OPTIMIZATION_BRIEF.md).

[S2] [Original and amended preregistrations](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/PREREGISTRATION.md), including the original split, metrics, Z0e/Z0s/Z0x and association protocols.

[S3] [main7 test scorecard](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/results/scorecard_test_main7.md), [temporal common scorecard](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/results/scorecard_temporal_ext.md), and [temporal-test scorecard](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/results/scorecard_temporal_test_ext.md). These are different subsets.

[S4] [Progress log](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/PROGRESS.md), particularly sessions 1 and 5 and the Z0w3 outcome.

[S5] [Round-13 closeout](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/docs/astra/round13/RESULTS.md).

[S6] [Z0x implementation](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/src/zcosmo/z0x.py) and [theoretical contact coefficient](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/src/zcosmo/zmodel.py).

[S7] [Dielectric generator](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/src/zcosmo/qc_dielectric.py) and [stored dielectric table](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/results/qc/dielectric.csv).

[S8] [COSMO-SAC parameters and evaluator](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/src/zcosmo/cosmosac.py), [pressure provider](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/src/zcosmo/scope.py), and [benchmark evaluator](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/src/zcosmo/evaluate.py).

[S9] [MultiMACE](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/cloud/s15/multi_mace.py) and [cavity TI implementation](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/cloud/s15/bench15_core.py). The historical NPT-driver provenance limitation is stated above.

[S10] The [original optimization brief's measured MLIP and TI timings](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/docs/OPTIMIZATION_BRIEF.md) and the direct-route definitions in [PREREGISTRATION.md](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/PREREGISTRATION.md). Cost extrapolations here are explicitly conditional arithmetic.

[S11] [Association implementation](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/src/zcosmo/z0w.py), together with S2/S4 for historical versions and outcomes.

[S12] [Current manuscript draft](https://github.com/Victor-Liang-ChE/zcosmo/blob/864aaac1e85eda31a43f24e856770c7f56ccb760/manuscript/draft.md).

[U1] Neumann, “Dipole moment fluctuation formulas in computer simulations of polar systems,” Molecular Physics 50 (1983), 841–858, [DOI 10.1080/00268978300102721](https://doi.org/10.1080/00268978300102721). The field-response derivation above states the model assumptions explicitly; it is not a claim of a new numerical dielectric result.

[U2] [Official chemicals permittivity documentation](https://chemicals.readthedocs.io/chemicals.permittivity.html) and the pinned data file in the source inventory. The source is a reference compilation, not newly verified measurement-level independence.

[U3] [Official MACE-OFF model repository](https://github.com/ACEsuit/mace-off). Current-project energy/force interfaces and their limitations are assessed from S9 rather than assumed to include an unverified dipole model.

The following independent new-file diffs target the pinned main. H14 depends on P51/P52 when its tests are executed. REG14 is proposed text, not an assertion that it has been adopted.

<!-- BEGIN PATCH P51 -->
```diff
diff --git a/scripts/r14_dielectric.py b/scripts/r14_dielectric.py
new file mode 100644
--- /dev/null
+++ b/scripts/r14_dielectric.py
@@ -0,0 +1,325 @@
+"""R14 ingredient audit and exposure receipt. No quantum or activity-model calls.
+
+Real data work is private and Mac-only. Unit tests use synthetic records.
+Experimental permittivities are references, never a production replacement.
+"""
+from __future__ import annotations
+import argparse
+import csv
+import hashlib
+import importlib.metadata
+import io
+import json
+import math
+import os
+from pathlib import Path
+import platform
+import re
+import subprocess
+import sys
+import time
+import urllib.request
+import numpy as np
+
+ROOT = Path(__file__).resolve().parents[1]
+BASE = '864aaac1e85eda31a43f24e856770c7f56ccb760'
+MARKER = 'R14-P51-P52-P53: exposure, dielectric ingredient, and oracle diagnostic'
+SOURCE_COMMIT = 'e79047588b30cfabc564c79fb26d760c746877d7'
+SOURCE_BLOB = 'bf12ffba51b478a021acc6ed58778c04deb9b988'
+SOURCE_URL = ('https://raw.githubusercontent.com/CalebBell/chemicals/' + SOURCE_COMMIT +
+    '/chemicals/Electrolytes/Permittivity%20%28Dielectric%20Constant%29%20of%20Liquids.tsv')
+TREF = 298.15
+DESIGN = dict(T_K=TREF, point_temperature_tolerance_K=0.10,
+    coefficient_policy='A and B required; absent C/D mean zero in documented polynomial',
+    no_extrapolation=True, identity='exact unique key to unique checksum-valid CAS',
+    baseline_gate='descriptive only; no baseline error threshold authorizes a model',
+    candidate_mean_abs_log_ratio_max=0.8, candidate_mean_abs_f_max=0.02,
+    candidate_max_relative_error=0.25, candidate_per_member_log_worsening_max=0.05,
+    candidate_scope='four predeclared pilot liquids only; not a 740-compound acceptance',
+    native_budget=0, activity_model_budget=0, adoption=False)
+PILOT = ('XLYOFNOQVPJJNP-UHFFFAOYSA-N','OKKJLVBELUTLKV-UHFFFAOYSA-N',
+         'WEVYAHXRMPXWCK-UHFFFAOYSA-N','UHOVQNZJYSORNB-UHFFFAOYSA-N')
+
+
+def require(ok, message):
+    if not ok:
+        raise ValueError(message)
+
+
+def sha(path):
+    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
+
+
+def blob(data):
+    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
+
+
+def read(path):
+    return json.loads(Path(path).read_text())
+
+
+def write(path, obj):
+    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
+    with p.open('x') as f:
+        json.dump(obj, f, indent=2, sort_keys=True, allow_nan=False)
+        f.write('\n')
+    p.chmod(0o600)
+
+
+def records(path, delimiter=','):
+    with Path(path).open(newline='') as f:
+        return list(csv.DictReader(f, delimiter=delimiter))
+
+
+def number(value):
+    try:
+        x=float(value)
+        return x if math.isfinite(x) else None
+    except (ValueError, TypeError):
+        return None
+
+
+def screening(eps):
+    x=np.asarray(eps, float)
+    require(np.isfinite(x).all() and (x>=1).all(), 'epsilon must be finite and >= 1')
+    return 1.0-1.5/(x+0.5)
+
+
+def sensitivity(old, new):
+    a=float(screening(old)); b=float(screening(new))
+    return dict(old_f=a,new_f=b,delta_f=b-a,
+        relative_coefficient_change=None if a==0 else (b-a)/a,
+        residual_to_conductor=1-a, d_f_d_epsilon=1.5/(old+0.5)**2)
+
+
+def kf_epsilon(mu_D, volume_A3, eps_inf, g, T=TREF):
+    """KF closure only. The input g must have the proper bulk/boundary convention."""
+    vals=np.asarray([mu_D,volume_A3,eps_inf,g,T],float)
+    require(np.isfinite(vals).all() and mu_D>=0 and volume_A3>0 and
+            eps_inf>=1 and g>=0 and T>0, 'invalid KF arguments')
+    y=1e30/volume_A3*(mu_D*3.33564e-30)**2/(9*8.8541878128e-12*1.380649e-23*T)
+    b=eps_inf+(eps_inf+2)**2*y*g
+    return float((b+math.sqrt(b*b+8*eps_inf*eps_inf))/4)
+
+
+def cas_valid(cas):
+    if not isinstance(cas,str) or not re.fullmatch(r'\d{2,7}-\d{2}-\d',cas):
+        return False
+    left, last=cas.rsplit('-',1)
+    digits=left.replace('-','')
+    return sum((i+1)*int(v) for i,v in enumerate(reversed(digits)))%10==int(last)
+
+
+def reference_at(row, T=TREF):
+    """Use the declared polynomial only inside its range, else a near-exact point."""
+    a,b,c,d=(number(row.get(k)) for k in ('A','B','C','D'))
+    lo,hi=number(row.get('Tmin')),number(row.get('Tmax'))
+    if a is not None and b is not None and lo is not None and hi is not None and lo<=T<=hi:
+        v=a+T*(b+T*((c or 0.)+T*(d or 0.)))
+        require(math.isfinite(v) and v>=1, 'invalid interpolated reference')
+        return v, 'CRC_polynomial_in_range'
+    t,v=number(row.get('T')),number(row.get('Permittivity'))
+    if t is not None and v is not None and abs(t-T)<=DESIGN['point_temperature_tolerance_K']:
+        require(v>=1, 'invalid reference point')
+        return v, 'CRC_point_within_0.10_K'
+    return None, 'no_reference_at_declared_temperature'
+
+
+def metrics(pred, ref):
+    p=np.asarray(pred,float); r=np.asarray(ref,float)
+    require(p.ndim==1 and p.shape==r.shape and len(p)>0, 'empty or misaligned ingredient comparison')
+    require(np.isfinite(p).all() and np.isfinite(r).all() and (p>=1).all() and (r>=1).all(),
+            'nonfinite ingredient value; do not shrink to a favorable intersection')
+    z=np.log(p/r); relative=np.abs(p-r)/r
+    return dict(n=len(p),mean_abs_log_epsilon=float(abs(z).mean()),
+        median_abs_log_epsilon=float(np.median(abs(z))),mean_log_bias=float(z.mean()),
+        mean_abs_relative_error=float(relative.mean()),max_relative_error=float(relative.max()),
+        mean_abs_f_error=float(abs(screening(p)-screening(r)).mean()))
+
+
+def ingredient_rows(stored, identities, reference):
+    keys=[r['inchikey'] for r in stored]
+    require(len(keys)==len(set(keys)), 'duplicate dielectric keys')
+    bykey={}; bycas={}; ref={}
+    for r in identities:
+        k,c=r['inchikey'],r['cas'].strip()
+        bykey.setdefault(k,set()).add(c); bycas.setdefault(c,set()).add(k)
+    for r in reference:
+        c=r['CAS'].strip()
+        require(cas_valid(c), 'invalid CAS in source')
+        require(c not in ref, 'duplicate CAS in dielectric reference')
+        ref[c]=r
+    out=[]
+    for r in stored:
+        k=r['inchikey']; z=dict(key=k,status='unmatched',stored_epsilon=number(r['eps']))
+        cs=bykey.get(k,set())
+        if len(cs)!=1:
+            z['status']='missing_or_ambiguous_key_to_CAS'
+        else:
+            c=next(iter(cs)); z['CAS']=c
+            if not cas_valid(c) or len(bycas.get(c,set()))!=1:
+                z['status']='invalid_or_stereochemically_ambiguous_CAS'
+            elif c not in ref:
+                z['status']='CAS_absent_from_reference'
+            else:
+                v,how=reference_at(ref[c]); z['reference_method']=how
+                if v is None:
+                    z['status']=how
+                else:
+                    z['reference_epsilon']=v
+                    z['status']='matched' if z['stored_epsilon'] is not None and z['stored_epsilon']>=1 else 'invalid_stored_epsilon'
+        out.append(z)
+    return out
+
+
+def candidate_gate(rows, candidates):
+    """Future physical-pilot gate. R14 provides no candidate-generating authorization."""
+    by={r['key']:r for r in rows}; cs={r['key']:r for r in candidates}
+    require(len(cs)==len(candidates) and set(cs)==set(PILOT), 'candidate must contain exactly the frozen four-liquid panel')
+    require(all(k in by and by[k]['status']=='matched' for k in PILOT), 'pilot reference coverage incomplete')
+    require(all(cs[k].get('sampling_gate_passed') is True and cs[k].get('dipole_gate_passed') is True
+                for k in PILOT), 'physical validation missing')
+    p=[cs[k]['eps'] for k in PILOT]; b=[by[k]['stored_epsilon'] for k in PILOT]
+    r=[by[k]['reference_epsilon'] for k in PILOT]
+    m0,m1=metrics(b,r),metrics(p,r)
+    worse=float(np.max(np.abs(np.log(np.array(p)/r))-np.abs(np.log(np.array(b)/r))))
+    checks=dict(log_improvement=m1['mean_abs_log_epsilon']<=0.8*m0['mean_abs_log_epsilon'],
+        f_accuracy=m1['mean_abs_f_error']<=0.02,individual_relative=m1['max_relative_error']<=0.25,
+        no_large_member_regression=worse<=0.05)
+    return dict(passed=all(checks.values()),checks=checks,baseline=m0,candidate=m1,
+                adopted=False,scope='ingredient pilot only, not phase-equilibrium acceptance')
+
+
+def environment():
+    ans={'python':platform.python_version(),'machine':platform.machine()}
+    for name in ('numpy','scipy','pandas','rdkit','thermo','chemicals'):
+        try: ans[name]=importlib.metadata.version(name)
+        except importlib.metadata.PackageNotFoundError: ans[name]=None
+    return ans
+
+
+def mac():
+    require(sys.platform=='darwin' and not os.environ.get('CI') and not os.environ.get('GITHUB_ACTIONS'),
+            'Real R14 data work is restricted to the private Mac, outside CI')
+
+
+def private(path, fresh=False):
+    p=Path(path).expanduser().resolve()
+    require(not p.is_relative_to(ROOT.resolve()), 'private output must be outside this checkout')
+    require(not any((v/'.git').exists() for v in (p,*p.parents)), 'private output cannot be inside a Git checkout')
+    if fresh:
+        p.mkdir(parents=True,exist_ok=False,mode=0o700)
+    return p
+
+
+def registration(commit):
+    require(re.fullmatch(r'[0-9a-f]{40}',commit) is not None,'use a full registration commit')
+    subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT,check=True,capture_output=True)
+    text=subprocess.check_output(['git','show',commit+':PREREGISTRATION.md'],cwd=ROOT,text=True)
+    require(MARKER in text,'registration marker missing')
+    subprocess.run(['git','merge-base','--is-ancestor',BASE,commit],cwd=ROOT,check=True,capture_output=True)
+    for rel in ('scripts/r14_dielectric.py','scripts/r14_oracle.py','scripts/r14_selftest.py'):
+        registered=subprocess.check_output(['git','show',commit+':'+rel],cwd=ROOT)
+        require(registered==(ROOT/rel).read_bytes(),'helper differs from registered bytes: '+rel)
+    return commit
+
+
+def fingerprint(paths):
+    return {str(Path(p).resolve()):sha(p) for p in paths}
+
+
+def check_inputs(saved):
+    for p,h in saved.items():
+        require(sha(p)==h,'input mutation: '+Path(p).name)
+
+
+def exposure_receipt(reg):
+    """An exposure declaration, not proof of what every collaborator has seen."""
+    return dict(registration=reg,base=BASE,
+        test_20pct='repeatedly inspected; historical partition retained, not a new holdout',
+        temporal_2017_2019='repeatedly inspected; no reset of holdout status',
+        glycol_R4_R12='inspected; P35 stays closed',
+        dielectric_reference='source schema and some values exposed during design; new property benchmark, not wholly blinded',
+        phase_oracle='retrospective explanatory scoring; experimental epsilon is not fit-free input',
+        new_post2019_source='not certified unexposed; custodian/document/duplicate audit required',
+        may_score_frozen_retrospective_oracle=True,may_claim_unexposed=False,
+        may_adopt=False,native_budget=0)
+
+
+def acquire(a):
+    mac(); reg=registration(a.registration); out=private(a.out,True)
+    exp=exposure_receipt(reg)
+    exp['reviewed_public_record_hashes']=fingerprint([ROOT/p for p in (
+        'PREREGISTRATION.md','PROGRESS.md','results/scorecard_test_main7.md',
+        'results/scorecard_temporal_ext.md','results/scorecard_temporal_test_ext.md',
+        'docs/astra/round12/RESULTS.md','docs/astra/round13/RESULTS.md','manuscript/draft.md')])
+    exp['private_queue_and_collaborator_exposure_complete']=False
+    write(out/'exposure.json',exp)
+    start=time.monotonic()
+    try:
+        with urllib.request.urlopen(SOURCE_URL,timeout=30) as response:
+            data=response.read(2_000_001)
+        require(len(data)<=2_000_000 and blob(data)==SOURCE_BLOB,'source size or pinned Git blob mismatch')
+        with (out/'reference.tsv').open('xb') as f: f.write(data)
+        (out/'reference.tsv').chmod(0o600)
+        write(out/'acquisition.json',dict(status='complete',url=SOURCE_URL,git_blob=SOURCE_BLOB,
+              sha256=sha(out/'reference.tsv'),registration=reg,wall_s=time.monotonic()-start))
+    except Exception as e:
+        write(out/'acquisition.json',dict(status='failed',error_type=type(e).__name__,
+              registration=reg,wall_s=time.monotonic()-start))
+        raise
+
+
+def ingredients(a):
+    mac(); reg=registration(a.registration); source=private(a.source); out=private(a.out,True)
+    exp=read(source/'exposure.json'); require(exp['registration']==reg,'exposure registration differs')
+    acq=read(source/'acquisition.json'); require(acq['status']=='complete','acquisition incomplete')
+    require(blob((source/'reference.tsv').read_bytes())==SOURCE_BLOB,'source blob changed')
+    paths=[source/'reference.tsv',source/'exposure.json',ROOT/'results/qc/dielectric.csv',
+           ROOT/'data/processed_ext/ud_complist.csv',Path(__file__)]
+    fp=fingerprint(paths); env=environment(); start=time.monotonic()
+    manifest=dict(design=DESIGN,registration=reg,exposure=exp,inputs=fp,environment=env)
+    write(out/'manifest.json',manifest)
+    rows=ingredient_rows(records(paths[2]),records(paths[3]),records(paths[0],'\t'))
+    matched=[r for r in rows if r['status']=='matched']
+    invalid=[r for r in rows if r['status']=='invalid_stored_epsilon']
+    status={k:sum(r['status']==k for r in rows) for k in sorted({r['status'] for r in rows})}
+    aggregate=metrics([r['stored_epsilon'] for r in matched],[r['reference_epsilon'] for r in matched]) if matched and not invalid else None
+    check_inputs(fp)
+    write(out/'ingredients.json',dict(manifest_sha256=sha(out/'manifest.json'),rows=rows,
+        population=len(rows),status_counts=status,baseline_metrics=aggregate,
+        reference_comparison_complete=bool(matched and not invalid),
+        invalid_stored_values_block_complete_comparison=bool(invalid),
+        missing_reference_is_not_zero_error=True,experimental_input_not_adopted=True,
+        source_independence='different measured property; common laboratories/compilations and unknown per-row lineage remain possible',
+        wall_s=time.monotonic()-start,activity_model_calls=0,SCF_calls=0))
+    print('Private ingredient audit complete. No activity model or quantum calculation ran.')
+
+
+def check(a):
+    mac(); out=private(a.out); m=read(out/'manifest.json'); registration(m['registration'])
+    check_inputs(m['inputs']); require(environment()==m['environment'],'package environment changed')
+    require(m['design']==DESIGN,'ingredient design changed')
+    d=read(out/'ingredients.json'); require(d['manifest_sha256']==sha(out/'manifest.json'),'manifest changed')
+    rows=ingredient_rows(records(ROOT/'results/qc/dielectric.csv'),
+        records(ROOT/'data/processed_ext/ud_complist.csv'),
+        records(next(p for p in m['inputs'] if Path(p).name=='reference.tsv'),'\t'))
+    require(rows==d['rows'],'ingredient rows do not reproduce')
+    matched=[r for r in rows if r['status']=='matched']
+    invalid=any(r['status']=='invalid_stored_epsilon' for r in rows)
+    aggregate=metrics([r['stored_epsilon'] for r in matched],[r['reference_epsilon'] for r in matched]) if matched and not invalid else None
+    require(aggregate==d['baseline_metrics'],'ingredient metrics do not reproduce')
+    print('Ingredient inputs and numerical summary verified; this is not production acceptance.')
+
+
+def main():
+    p=argparse.ArgumentParser(description=__doc__); s=p.add_subparsers(dest='command',required=True)
+    q=s.add_parser('catalog'); q.set_defaults(fn=lambda a:print(json.dumps(dict(url=SOURCE_URL,commit=SOURCE_COMMIT,blob=SOURCE_BLOB,design=DESIGN),indent=2)))
+    q=s.add_parser('screening'); q.set_defaults(fn=lambda a:print(json.dumps(dict(
+        water=sensitivity(52.93798366132173,78.),methanol=sensitivity(24.447223573823276,33.)),indent=2)))
+    q=s.add_parser('acquire');q.add_argument('--registration',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=acquire)
+    q=s.add_parser('ingredients');q.add_argument('--registration',required=True);q.add_argument('--source',required=True);q.add_argument('--out',required=True);q.set_defaults(fn=ingredients)
+    q=s.add_parser('check');q.add_argument('--out',required=True);q.set_defaults(fn=check)
+    a=p.parse_args();a.fn(a)
+
+if __name__=='__main__':main()
```
<!-- END PATCH P51 -->

<!-- BEGIN PATCH P52 -->
```diff
diff --git a/scripts/r14_oracle.py b/scripts/r14_oracle.py
new file mode 100644
--- /dev/null
+++ b/scripts/r14_oracle.py
@@ -0,0 +1,318 @@
+"""Private, retrospective R14 epsilon-298 oracle. No native calculations or adoption.
+
+The same frozen sigma profiles, parameters and pure vapor pressures are used in
+all arms. The experiment is deliberately not a new held-out scorecard.
+"""
+from __future__ import annotations
+import argparse
+import hashlib
+import importlib.metadata
+import json
+import math
+import os
+from pathlib import Path
+import signal
+import subprocess
+import sys
+import time
+import numpy as np
+import r14_dielectric as d
+
+ROOT=d.ROOT
+ARMS=('baseline','experimental_epsilon_298','cosmosac2010')
+DESIGN=dict(max_systems=100,max_rows_per_system=10,max_rows=1000,
+    selection_seed='R14-oracle-v1',split='already_exposed_test_one_and_test_both',
+    interior_strip=1e-4,baseline_relative_pressure_tolerance=1e-7,
+    max_model_calls=3000,worker_seconds=120,driver_seconds=7200,
+    epsilon_temperature_K=298.15,temperature_dependence_changed=False,
+    profile_source='frozen_UD',fallback='exclude missing reference from paired oracle, enumerate exclusions',
+    result='retrospective sensitivity, not an attainable upper bound or production model',
+    SCF_calls=0,adopted=False,pressure_unit='kPa')
+
+
+def stable_order(text):
+    return hashlib.sha256((DESIGN['selection_seed']+'|'+text).encode()).hexdigest()
+
+
+def select(rows, refs):
+    """Stable identities are input-file ordinals bound to the complete file hash."""
+    groups={}; counts={}
+    for i,r in enumerate(rows):
+        why=None
+        k1,k2=r['c1'],r['c2']
+        x,t,p,old=(d.number(r.get(k)) for k in ('x1','T','P','pred_P'))
+        if r.get('split') not in ('test_one','test_both'):why='other_historical_split'
+        elif k1==k2:why='self_pair'
+        elif k1 not in refs or k2 not in refs:why='missing_exact_reference_identity'
+        elif None in (x,t,p,old) or t<=0 or p<=0 or old<=0:why='invalid_archived_query_or_prediction'
+        elif not DESIGN['interior_strip']<x<1-DESIGN['interior_strip']:why='endpoint_or_numerical_strip'
+        if why:
+            counts[why]=counts.get(why,0)+1; continue
+        system='|'.join(sorted((k1,k2)))
+        z=dict(row_id=str(i),c1=k1,c2=k2,T=t,x1=x,P=p,archived_pred_P=old,system=system)
+        groups.setdefault(system,[]).append(z)
+    selected=[]
+    eligible_rows=sum(map(len,groups.values()))
+    chosen=sorted(groups,key=stable_order)[:DESIGN['max_systems']]
+    for system in chosen:
+        chosen_rows=sorted(groups[system],key=lambda r:stable_order(system+'|'+r['row_id']))[:DESIGN['max_rows_per_system']]
+        selected.extend(chosen_rows)
+    d.require(selected,'no eligible oracle rows; no substitute selection authorized')
+    return selected,dict(input_rows=len(rows),eligible_rows=eligible_rows,eligible_systems=len(groups),
+        selected_rows=len(selected),selected_systems=len(chosen),
+        eligible_not_sampled=eligible_rows-len(selected),excluded=counts)
+
+
+def protected_profiles(root):
+    root=Path(root).resolve(); files=[]; counts={}
+    for folder,expected in (('profiles_v2',630),('s1_stalled',1),('s2_stalled',5)):
+        ps=sorted((root/folder).glob('*.sigma'))
+        d.require(len(ps)==expected,'protected profile count differs in '+folder)
+        counts[folder]=len(ps); files.extend(ps)
+    d.require(len({p.stem for p in files})==636,'duplicate protected identities')
+    return d.fingerprint(files),counts
+
+
+def profile_path(key, folder):
+    folder=Path(folder).resolve(); exact=folder/(key+'.sigma')
+    if exact.is_file():return exact
+    matches=sorted(folder.glob(key[:14]+'-*.sigma'))
+    d.require(len(matches)==1,'missing or ambiguous historical UD profile: '+key)
+    return matches[0]
+
+
+def pressure(lg,x,psat):
+    """All pressures are kPa, as in zcosmo.scope.psat and the archive."""
+    lg=np.asarray(lg,float); psat=np.asarray(psat,float)
+    d.require(lg.shape==(2,) and psat.shape==(2,) and np.isfinite(lg).all() and
+              np.isfinite(psat).all() and (psat>0).all(),'invalid pressure ingredients')
+    with np.errstate(over='raise',invalid='raise'):
+        p=float(np.sum(np.array([x,1-x])*np.exp(lg)*psat))
+    d.require(math.isfinite(p) and p>0,'invalid predicted pressure')
+    return p
+
+
+def error_summary(rows, values):
+    a=np.asarray(values,float); n=len(rows)
+    d.require(n>0 and a.shape==(n,3),'oracle dimensions changed')
+    finite=np.isfinite(a)&(a>0)
+    receipt=dict(requested_rows=n,finite_counts=finite.sum(0).tolist(),complete=bool(finite.all()),
+        adopted=False,confirmatory=False,experimental_epsilon_is_fit_free=False)
+    if not finite.all():return dict(status=receipt,aggregate_errors=None)
+    truth=np.array([r['P'] for r in rows]); d.require(np.isfinite(truth).all() and (truth>0).all(),'invalid observed pressure')
+    err=100*np.abs(a/truth[:,None]-1)
+    signed=100*(a/truth[:,None]-1)
+    means=err.mean(0); gap=float(means[0]-means[2]);gain=float(means[0]-means[1])
+    groups=sorted({r['system'] for r in rows})
+    grouped=np.array([err[[r['system']==g for r in rows]].mean(0) for g in groups])
+    return dict(status=receipt,aggregate_errors=dict(arms=list(ARMS),rows=n,systems=len(groups),
+        AAD_percent=means.tolist(),bias_percent=signed.mean(0).tolist(),
+        equal_system_AAD_percent=grouped.mean(0).tolist(),
+        oracle_minus_baseline_pp=-gain,baseline_minus_cosmosac2010_pp=gap,
+        oracle_minus_cosmosac2010_pp=float(means[1]-means[2]),
+        signed_gap_recovery=None if gap<=1e-6 else gain/gap,
+        improved_rows=int((err[:,1]<err[:,0]).sum()),worsened_rows=int((err[:,1]>err[:,0]).sum()),
+        no_generalization_CI=True))
+
+
+def code_paths():
+    return list((ROOT/'src/zcosmo').glob('*.py'))+[ROOT/'scripts/r14_dielectric.py',
+        ROOT/'scripts/r14_oracle.py',ROOT/'scripts/r14_selftest.py']
+
+
+def freeze(a):
+    d.mac();reg=d.registration(a.registration);out=d.private(a.out,True)
+    ingredient=d.private(a.ingredients)
+    d.check(argparse.Namespace(out=str(ingredient)))
+    im=d.read(ingredient/'manifest.json'); ir=d.read(ingredient/'ingredients.json')
+    d.require(im['registration']==reg and im['exposure']['may_score_frozen_retrospective_oracle'] is True
+              and im['exposure']['may_claim_unexposed'] is False,'exposure or registration mismatch')
+    refs={r['key']:r['reference_epsilon'] for r in ir['rows'] if r['status']=='matched'}
+    rows,census=select(d.records(a.archive),refs)
+    ps,counts=protected_profiles(a.profile_root)
+    tables=[ROOT/'results/qc/dielectric.csv',ROOT/'results/qc/dispersion.csv',ROOT/'results/z_params/Z0.json']
+    files=code_paths()+tables+[ROOT/'data/benchmark/compounds.csv',Path(a.archive),ingredient/'manifest.json',ingredient/'ingredients.json']
+    filehash=d.fingerprint(files);filehash.update(ps)
+    profiles={k:str(profile_path(k,a.ud_profiles)) for k in {v for r in rows for v in (r['c1'],r['c2'])}}
+    filehash.update(d.fingerprint(profiles.values()))
+    # This is the existing vapor-pressure provider, used once to freeze common inputs.
+    # No activity coefficient is queried here and experimental mixture P is not used.
+    for key in list(os.environ):
+        if key.startswith('ZC_'):os.environ.pop(key)
+    from zcosmo.scope import psat
+    for r in rows:
+        r['psat']=[float(psat(k,r['T'])) for k in (r['c1'],r['c2'])]
+        d.require(all(math.isfinite(v) and v>0 for v in r['psat']),'invalid pure vapor pressure; preparation stops')
+    jobs=[]
+    pairs=sorted({(r['c1'],r['c2']) for r in rows})
+    for arm in ARMS:
+        for pair in pairs:
+            idx=[i for i,r in enumerate(rows) if (r['c1'],r['c2'])==pair]
+            jobs.append(dict(id=f'job-{len(jobs):04d}',arm=arm,keys=list(pair),indices=idx))
+    d.require(sum(len(j['indices']) for j in jobs)==3*len(rows)<=DESIGN['max_model_calls'],'request budget mismatch')
+    d.check_inputs(filehash)
+    m=dict(schema='r14-oracle-v1',base=d.BASE,registration=reg,design=DESIGN,environment=d.environment(),
+        inputs=filehash,ingredient_manifest=im,exposure=im['exposure'],rows=rows,census=census,
+        reference_epsilon={k:refs[k] for k in profiles},profiles=profiles,protected_counts=counts,jobs=jobs)
+    d.write(out/'plan.json',m)
+    with (out/'PLAN_SHA256.txt').open('x') as f:f.write(d.sha(out/'plan.json')+'\n')
+    print('Private oracle plan frozen. Commit only its digest before the one run.')
+
+
+def load(plan, plan_commit):
+    d.mac();p=d.private(plan);m=d.read(p);d.registration(m['registration'])
+    d.require(m['design']==DESIGN and m['schema']=='r14-oracle-v1','design changed')
+    d.require(m['environment']==d.environment(),'environment changed')
+    d.check_inputs(m['inputs']);d.check_inputs(m['ingredient_manifest']['inputs'])
+    d.require(m['exposure']['may_claim_unexposed'] is False,'oracle cannot be relabeled held out')
+    subprocess.run(['git','merge-base','--is-ancestor',plan_commit,'HEAD'],cwd=ROOT,check=True,capture_output=True)
+    text=subprocess.check_output(['git','show',plan_commit+':docs/astra/round14/ORACLE_PLAN_SHA256.txt'],cwd=ROOT,text=True).strip()
+    d.require(text==d.sha(p),'uncommitted or different oracle plan')
+    return p,m
+
+
+def worker(a):
+    p,m=load(a.plan,a.plan_commit); job=next(j for j in m['jobs'] if j['id']==a.job)
+    claim=d.read(p.parent/'execution_claim.json')
+    expected=Path(claim['output']).resolve()/job['id']
+    d.require(claim['plan_sha256']==d.sha(p) and d.private(a.out)==expected,'worker outside the one claimed run')
+    out=d.private(a.out,True)
+    for key in list(os.environ):
+        if key.startswith('ZC_'):os.environ.pop(key)
+    os.environ['ZC_R6_ENDPOINT']='1';os.environ['ZC_SIGMA_OVERRIDE_DIR']=str(out/'overlay')
+    ov=out/'overlay';ov.mkdir(mode=0o700)
+    for key in job['keys']:(ov/(key+'.sigma')).symlink_to(Path(m['profiles'][key]))
+    from zcosmo.z0x import Z0xBinary
+    from zcosmo.cosmosac import Mixture,Params,load_fluid
+    # Explicit overlay verification prevents silent fallback or cached profiles.
+    for key in job['keys']:
+        fl=load_fluid(key)
+        d.require(fl.psigA.shape==(3,51) and np.isfinite(fl.psigA).all(),'invalid frozen profile')
+    if job['arm']=='cosmosac2010':model=Mixture(job['keys'],Params(use_dsp=False))
+    else:
+        model=Z0xBinary(job['keys'])
+        if job['arm']=='experimental_epsilon_298':
+            model.eps=np.array([m['reference_epsilon'][k] for k in job['keys']],float)
+            model._mix.clear()
+    values=[]; start=time.monotonic()
+    for i in job['indices']:
+        r=m['rows'][i]; value=None; error=None
+        d.write(out/f'attempt-{len(values):04d}.json',dict(row_id=r['row_id'],attempted=True))
+        try:value=pressure(model.lngamma(r['T'],np.array([r['x1'],1-r['x1']])),r['x1'],r['psat'])
+        except Exception as e:error=type(e).__name__
+        values.append(dict(row_id=r['row_id'],value=value,error=error))
+    d.check_inputs(m['inputs'])
+    d.write(out/'result.json',dict(job=job['id'],arm=job['arm'],plan_sha256=d.sha(p),
+        requested=len(job['indices']),attempted=len(values),values=values,wall_s=time.monotonic()-start))
+
+
+def launch(cmd, log, seconds, env):
+    with Path(log).open('xb') as f:
+        proc=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,start_new_session=True)
+        try:return dict(state='returned',returncode=proc.wait(timeout=seconds))
+        except subprocess.TimeoutExpired:
+            os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=5)
+            return dict(state='timeout',returncode=proc.returncode)
+
+
+def arrays(m, run, plan_hash):
+    a=np.full((len(m['rows']),3),np.nan);hashes={};attempts=0
+    for job in m['jobs']:
+        tpath=run/(job['id']+'.terminal.json'); term=d.read(tpath);hashes[str(tpath)]=d.sha(tpath)
+        d.require(term['job']==job['id'] and term['plan_sha256']==plan_hash,'terminal identity changed')
+        folder=run/job['id'];started=sorted(folder.glob('attempt-*.json')) if folder.exists() else []
+        for j,ap in enumerate(started):
+            expected_row=m['rows'][job['indices'][j]]['row_id'] if j<len(job['indices']) else None
+            d.require(ap.name==f'attempt-{j:04d}.json' and d.read(ap)==dict(row_id=expected_row,attempted=True),'attempt receipt changed')
+        attempts+=len(started)
+        d.require(len(started)<=len(job['indices']),'per-job request ceiling exceeded')
+        hashes.update(d.fingerprint(started))
+        rp=folder/'result.json'
+        if term['state']!='returned' or term['returncode']!=0 or not rp.is_file():continue
+        z=d.read(rp);hashes[str(rp)]=d.sha(rp)
+        expected=[m['rows'][i]['row_id'] for i in job['indices']]
+        d.require(z['job']==job['id'] and z['arm']==job['arm'] and z['plan_sha256']==plan_hash
+            and z['requested']==len(expected) and z['attempted']==len(started)==len(expected)
+            and [v['row_id'] for v in z['values']]==expected,'result identities or counts changed')
+        for i,v in zip(job['indices'],z['values']):
+            if v['value'] is not None:a[i,ARMS.index(job['arm'])]=float(v['value'])
+    d.require(attempts<=3*len(m['rows'])<=DESIGN['max_model_calls'],'total request ceiling exceeded')
+    return a,attempts,hashes
+
+
+def anchor_pass(rows, baseline):
+    old=np.array([r['archived_pred_P'] for r in rows]); b=np.asarray(baseline,float)
+    finite=np.isfinite(b)&(b>0)
+    error=float(np.max(np.abs(b/old-1))) if finite.all() else None
+    return dict(passed=bool(finite.all() and error<DESIGN['baseline_relative_pressure_tolerance']),
+        max_relative_pressure_error=error,requested=len(rows),finite=int(finite.sum()))
+
+
+def run(a):
+    p,m=load(a.plan,a.plan_commit);out=d.private(a.out)
+    d.write(p.parent/'execution_claim.json',dict(plan_sha256=d.sha(p),output=str(out)))
+    out=d.private(out,True);start=time.monotonic(); env=dict(os.environ)
+    env.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
+    anchor=None
+    # All terminals exist first, so a killed driver cannot erase requested identities.
+    for job in m['jobs']:
+        d.write(out/(job['id']+'.terminal.json'),dict(job=job['id'],plan_sha256=d.sha(p),state='not_started',returncode=None))
+    for job in m['jobs']:
+        if job['arm']!='baseline' and anchor is None:
+            v,_,_=arrays(m,out,d.sha(p));anchor=anchor_pass(m['rows'],v[:,0])
+        rem=DESIGN['driver_seconds']-(time.monotonic()-start)
+        term=dict(job=job['id'],plan_sha256=d.sha(p),state='not_run_budget',returncode=None)
+        if job['arm']!='baseline' and not anchor['passed']:term['state']='blocked_anchor'
+        elif rem>1:
+            cmd=[sys.executable,str(Path(__file__).resolve()),'_worker','--plan',str(p),
+                '--plan-commit',a.plan_commit,'--job',job['id'],'--out',str(out/job['id'])]
+            try:term.update(launch(cmd,out/(job['id']+'.log'),min(rem,DESIGN['worker_seconds']),env))
+            except Exception:term.update(state='launch_failed')
+        # Only terminal receipts are updated, never a native/model result or input.
+        tp=out/(job['id']+'.terminal.json'); tmp=out/(job['id']+'.terminal.tmp')
+        d.write(tmp,term);os.replace(tmp,tp)
+    v,attempts,hashes=arrays(m,out,d.sha(p));anchor=anchor_pass(m['rows'],v[:,0])
+    load(a.plan,a.plan_commit)
+    result=error_summary(m['rows'],v)
+    if not anchor['passed']:result['aggregate_errors']=None;result['status']['complete']=False
+    summary=dict(plan_sha256=d.sha(p),anchor=anchor,**result,
+        attempted_model_calls=attempts,wall_s=time.monotonic()-start,output_hashes=hashes,
+        SCF_calls=0,source_profiles_unchanged=True)
+    d.write(out/'summary.json',summary)
+    d.write(out/'public-errors.json',dict(status=result['status'],anchor=anchor,
+        aggregate_errors=result['aggregate_errors'],census=m['census'],
+        interpretation=DESIGN['result'],adopted=False,SCF_calls=0))
+    print('Private oracle finished. Complete:',result['status']['complete'])
+    return 0 if result['status']['complete'] else 2
+
+
+def check(a):
+    p,m=load(a.plan,a.plan_commit);runpath=d.private(a.run);z=d.read(runpath/'summary.json')
+    claim=d.read(p.parent/'execution_claim.json')
+    d.require(claim==dict(plan_sha256=d.sha(p),output=str(runpath)),'run claim changed')
+    v,n,h=arrays(m,runpath,d.sha(p));fresh=error_summary(m['rows'],v);anchor=anchor_pass(m['rows'],v[:,0])
+    if not anchor['passed']:fresh['aggregate_errors']=None;fresh['status']['complete']=False
+    d.require(z['plan_sha256']==d.sha(p) and z['anchor']==anchor and
+        z['attempted_model_calls']==n and z['output_hashes']==h and
+        z['status']==fresh['status'] and z['aggregate_errors']==fresh['aggregate_errors'],'saved summary changed')
+    public=dict(status=fresh['status'],anchor=anchor,aggregate_errors=fresh['aggregate_errors'],
+        census=m['census'],interpretation=DESIGN['result'],adopted=False,SCF_calls=0)
+    d.require(public==d.read(runpath/'public-errors.json'),'public summary changed')
+    print('Saved oracle checked without model calls. Complete:',fresh['status']['complete'])
+    return 0 if fresh['status']['complete'] else 2
+
+
+def main():
+    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='cmd',required=True)
+    q=s.add_parser('freeze');q.add_argument('--registration',required=True);q.add_argument('--ingredients',required=True)
+    q.add_argument('--archive',required=True);q.add_argument('--profile-root',required=True);q.add_argument('--ud-profiles',required=True)
+    q.add_argument('--out',required=True);q.set_defaults(fn=freeze)
+    for name,fn in (('run',run),('check',check),('_worker',worker)):
+        q=s.add_parser(name);q.add_argument('--plan',required=True);q.add_argument('--plan-commit',required=True)
+        if name=='check':q.add_argument('--run',required=True)
+        else:q.add_argument('--out',required=True)
+        if name=='_worker':q.add_argument('--job',required=True)
+        q.set_defaults(fn=fn)
+    a=p.parse_args();return a.fn(a)
+
+if __name__=='__main__':raise SystemExit(main())
```
<!-- END PATCH P52 -->

<!-- BEGIN PATCH H14 -->
```diff
diff --git a/scripts/r14_selftest.py b/scripts/r14_selftest.py
new file mode 100644
--- /dev/null
+++ b/scripts/r14_selftest.py
@@ -0,0 +1,295 @@
+"""Portable R14 tests: synthetic arrays/files and mocked model orchestration only."""
+from __future__ import annotations
+import ast
+import argparse
+import hashlib
+import importlib.util
+import json
+import os
+from pathlib import Path
+import sys
+import tempfile
+import types
+import unittest
+from unittest.mock import patch
+import numpy as np
+import r14_dielectric as d
+import r14_oracle as o
+
+
+def query(i, c1='a', c2='b'):
+    return dict(c1=c1,c2=c2,T='298.15',x1=str(.02+.9*(i%19)/19),P='100000',
+                pred_P='110000',split='test_one',system_id='irrelevant-name')
+
+
+def reference(cas='7732-18-5',**kw):
+    r=dict(CAS=cas,Chemical='fixture',T='298.15',Permittivity='10',A='',B='',C='',D='',Tmin='',Tmax='')
+    r.update(kw);return r
+
+
+def load_base():
+    path=d.ROOT/'src/zcosmo/z0x.py'
+    if not path.is_file():raise unittest.SkipTest('verified current z0x source not available')
+    require_blob='c558d4e95db9b78f3b57d6a103a293e21feeb9af'
+    if d.blob(path.read_bytes())!=require_blob:raise AssertionError('test requires the reviewed z0x Git blob')
+    cosmos=types.ModuleType('zcosmo.cosmosac');models=types.ModuleType('zcosmo.models');zm=types.ModuleType('zcosmo.zmodel')
+    class P:
+        aeff=7.25
+        def __init__(self,c=1.):self.A_ES=c
+        def with_(self,**kw):return P(kw['A_ES'])
+    class Mix:
+        def __init__(self,keys,prm):
+            self.prm=prm;self.A=np.array([1.,2.]);self.fl=[]
+            for i in range(2):
+                p=np.zeros((3,51));p[0,5+30*i]=self.A[i]
+                self.fl.append(types.SimpleNamespace(key=keys[i],psigA=p))
+        def _E(self,T):return np.ones((153,153))
+        def lngamma_comb(self,x):return np.zeros(2)
+        def lngamma_disp(self,x,T):return np.zeros(2)
+        def lngamma(self,T,x):return np.array([self.prm.A_ES,-self.prm.A_ES])
+    cosmos.Mixture=Mix;cosmos.load_fluid=lambda k:types.SimpleNamespace(V=1.)
+    cosmos.solve_gamma=lambda e,p:np.ones(153);cosmos._pure_lnG=lambda *a:np.zeros(153)
+    cosmos.SIG=np.linspace(-.025,.025,51);cosmos.R_KCAL=.001987
+    models.load_z_params=lambda n:P();models.ROOT=d.ROOT
+    zm.c_es_theory=lambda fpol=1.:12000*fpol
+    spec=importlib.util.spec_from_file_location('r14_test_z0x',path);mod=importlib.util.module_from_spec(spec)
+    with patch.dict(sys.modules,{'zcosmo.cosmosac':cosmos,'zcosmo.models':models,'zcosmo.zmodel':zm}):
+        spec.loader.exec_module(mod)
+    return mod
+
+
+class Physics(unittest.TestCase):
+    def test_f_monotonic_and_saturation(self):
+        f=d.screening([1,2,10,100,1e12]);self.assertTrue(np.all(np.diff(f)>0));self.assertAlmostEqual(f[0],0)
+        self.assertLess(f[-1],1)
+    def test_f_derivative(self):
+        x=24.447;h=1e-3;fd=(d.screening(x+h)-d.screening(x-h))/(2*h)
+        self.assertAlmostEqual(fd,1.5/(x+.5)**2,places=10)
+    def test_water_coefficient_not_epsilon_fraction(self):
+        s=d.sensitivity(52.93798366132173,78.)
+        self.assertGreater(s['delta_f'],0);self.assertLess(s['relative_coefficient_change'],.01)
+    def test_bad_epsilon(self):
+        for e in (np.nan,np.inf,0.5):
+            with self.assertRaises(ValueError):d.screening(e)
+    def test_kf_zero_dipole(self):self.assertAlmostEqual(d.kf_epsilon(0,50,2.4,3),2.4)
+    def test_kf_g_monotonic(self):
+        self.assertLess(d.kf_epsilon(2,50,2,1),d.kf_epsilon(2,50,2,2))
+    def test_kf_temperature(self):
+        self.assertGreater(d.kf_epsilon(2,50,2,1,280),d.kf_epsilon(2,50,2,1,330))
+    def test_kf_input_rejected(self):
+        with self.assertRaises(ValueError):d.kf_epsilon(2,-1,2,1)
+    def test_pressure_units(self):self.assertAlmostEqual(o.pressure([0,0],.25,[1e5,2e5]),175000)
+    def test_pressure_nonfinite(self):
+        with self.assertRaises(ValueError):o.pressure([np.nan,0],.5,[1,1])
+
+
+class Ingredient(unittest.TestCase):
+    def test_CAS_checksum(self):
+        self.assertTrue(d.cas_valid('7732-18-5'));self.assertTrue(d.cas_valid('67-56-1'))
+        self.assertFalse(d.cas_valid('7732-18-4'));self.assertFalse(d.cas_valid('water'))
+    def test_polynomial_range(self):
+        r=reference(A='20',B='-0.01',Tmin='290',Tmax='310')
+        self.assertAlmostEqual(d.reference_at(r)[0],17.0185)
+    def test_no_extrapolation(self):
+        r=reference(A='20',B='-.01',Tmin='280',Tmax='290',T='293.15')
+        self.assertIsNone(d.reference_at(r)[0])
+    def test_exact_temperature_point(self):
+        self.assertEqual(d.reference_at(reference())[0],10.)
+        self.assertIsNone(d.reference_at(reference(T='293.15'))[0])
+    def test_invalid_polynomial(self):
+        with self.assertRaises(ValueError):d.reference_at(reference(A='-1',B='0',Tmin='290',Tmax='310'))
+    def test_exact_join(self):
+        rr=d.ingredient_rows([dict(inchikey='K',eps='8')],[dict(inchikey='K',cas='7732-18-5')],[reference()])
+        self.assertEqual(rr[0]['status'],'matched')
+    def test_stereo_ambiguity(self):
+        rr=d.ingredient_rows([dict(inchikey='K',eps='8')],
+           [dict(inchikey='K',cas='7732-18-5'),dict(inchikey='K2',cas='7732-18-5')],[reference()])
+        self.assertEqual(rr[0]['status'],'invalid_or_stereochemically_ambiguous_CAS')
+    def test_duplicates_refused(self):
+        with self.assertRaises(ValueError):d.ingredient_rows([dict(inchikey='K',eps='8')]*2,[],[])
+        with self.assertRaises(ValueError):d.ingredient_rows([],[],[reference(),reference()])
+    def test_nonfinite_explicit(self):
+        rr=d.ingredient_rows([dict(inchikey='K',eps='nan')],[dict(inchikey='K',cas='7732-18-5')],[reference()])
+        self.assertEqual(rr[0]['status'],'invalid_stored_epsilon')
+        with self.assertRaises(ValueError):d.metrics([1,np.nan],[1,2])
+    def test_metrics(self):
+        m=d.metrics([2,4],[2,4]);self.assertEqual(m['mean_abs_f_error'],0);self.assertEqual(m['mean_abs_log_epsilon'],0)
+    def test_future_pilot_gate(self):
+        rows=[dict(key=k,status='matched',stored_epsilon=10.,reference_epsilon=20.) for k in d.PILOT]
+        c=[dict(key=k,eps=20.,sampling_gate_passed=True,dipole_gate_passed=True) for k in d.PILOT]
+        self.assertTrue(d.candidate_gate(rows,c)['passed'])
+        c[0]['dipole_gate_passed']=False
+        with self.assertRaises(ValueError):d.candidate_gate(rows,c)
+    def test_missing_pilot_member(self):
+        with self.assertRaises(ValueError):d.candidate_gate([],[])
+
+
+class Oracle(unittest.TestCase):
+    def test_selection_counts_and_budget(self):
+        rows=[query(i,f'K{i//20}','b') for i in range(2200)]
+        ref={r['c1']:10 for r in rows};ref['b']=2
+        got,c=o.select(rows,ref)
+        self.assertEqual(len(got),1000);self.assertEqual(c['selected_systems'],100)
+        self.assertEqual(3*len(got),o.DESIGN['max_model_calls'])
+    def test_selection_ignores_observed_error(self):
+        rows=[query(i) for i in range(20)]
+        a,_=o.select(rows,{'a':10,'b':2})
+        rows[0]['P']='9e20';rows[0]['pred_P']='1e-3'
+        b,_=o.select(rows,{'a':10,'b':2})
+        self.assertEqual([r['row_id'] for r in a],[r['row_id'] for r in b])
+    def test_unknown_refs_are_exclusions(self):
+        rows=[query(0),query(1,'missing','b')];r,c=o.select(rows,{'a':10,'b':2})
+        self.assertEqual(len(r),1);self.assertEqual(c['excluded']['missing_exact_reference_identity'],1)
+    def test_pure_endpoints_excluded(self):
+        r=query(0);r['x1']='0';rows=[r,query(1)]
+        g,c=o.select(rows,{'a':10,'b':2});self.assertEqual(len(g),1)
+    def test_preserve_nonfinite(self):
+        rows,_=o.select([query(0)],{'a':10,'b':2})
+        s=o.error_summary(rows,[[1e5,np.nan,1e5]])
+        self.assertFalse(s['status']['complete']);self.assertIsNone(s['aggregate_errors'])
+        self.assertEqual(s['status']['requested_rows'],1)
+    def test_gain_and_residual(self):
+        rows,_=o.select([query(0)],{'a':10,'b':2})
+        s=o.error_summary(rows,[[120000,110000,100000]])['aggregate_errors']
+        self.assertAlmostEqual(s['signed_gap_recovery'],.5)
+        self.assertAlmostEqual(s['oracle_minus_baseline_pp']+s['baseline_minus_cosmosac2010_pp'],s['oracle_minus_cosmosac2010_pp'])
+    def test_recovery_not_clipped(self):
+        rows,_=o.select([query(0)],{'a':10,'b':2})
+        q=o.error_summary(rows,[[120000,140000,100000]])['aggregate_errors']
+        self.assertAlmostEqual(q['signed_gap_recovery'],-1)
+    def test_zero_gap_ratio_unavailable(self):
+        rows,_=o.select([query(0)],{'a':10,'b':2})
+        q=o.error_summary(rows,[[120000,100000,120000]])['aggregate_errors']
+        self.assertIsNone(q['signed_gap_recovery'])
+    def test_anchor_gate(self):
+        rows,_=o.select([query(0)],{'a':10,'b':2})
+        self.assertTrue(o.anchor_pass(rows,[110000])['passed'])
+        self.assertFalse(o.anchor_pass(rows,[110001])['passed'])
+    def test_source_mutation(self):
+        with tempfile.TemporaryDirectory() as t:
+            p=Path(t)/'source';p.write_text('one');fp=d.fingerprint([p]);d.check_inputs(fp)
+            p.write_text('two')
+            with self.assertRaises(ValueError):d.check_inputs(fp)
+    def test_exclusive_output(self):
+        with tempfile.TemporaryDirectory() as t:
+            p=Path(t)/'out.json';d.write(p,dict(ok=True))
+            with self.assertRaises(FileExistsError):d.write(p,dict(ok=False))
+    def test_private_git_path(self):
+        with tempfile.TemporaryDirectory() as t:
+            root=Path(t);(root/'.git').mkdir()
+            with self.assertRaises(ValueError):d.private(root/'out')
+    def test_exposure_never_claims_new_holdout(self):
+        e=d.exposure_receipt('fixture');self.assertFalse(e['may_claim_unexposed']);self.assertFalse(e['may_adopt'])
+
+
+class ActualSourceDispatch(unittest.TestCase):
+    def test_override_updates_composition_screening(self):
+        m=load_base();b=m.Z0xBinary.__new__(m.Z0xBinary);b.V=np.array([1.,2.]);b.eps=np.array([10.,2.])
+        c=b._c(.4);der=(b._c(.40001)-b._c(.39999))/.00002
+        b.eps=np.array([20.,3.]);self.assertNotEqual(c,b._c(.4))
+        self.assertNotEqual(der,(b._c(.40001)-b._c(.39999))/.00002)
+    def test_analytic_branch_reads_replaced_epsilon(self):
+        m=load_base();b=m.Z0xBinary.__new__(m.Z0xBinary)
+        b.V=np.array([1.,2.]);b.keys=['a','b'];b.z0=m.load_z_params('Z0');b.eps=np.array([10.,2.])
+        old=b._analytic(298.15,.4);b.eps=np.array([20.,3.]);new=b._analytic(298.15,.4)
+        self.assertGreater(np.max(abs(old-new)),0)
+    def test_observed_subclass_dispatch_limitation(self):
+        m=load_base()
+        class Extension(m.Z0xBinary):
+            def _g(self,T,x):return x*(1-x)
+        b=Extension.__new__(Extension);b._analytic=lambda T,x:np.zeros(2);b._endpoint=lambda T,x:np.zeros(2)
+        self.assertTrue(np.array_equal(b.lngamma(298.15,[.4,.6]),[0,0]))
+        with patch.dict(os.environ,{'ZC_R6_ENDPOINT':'1'}):self.assertEqual(b.lngamma_inf(298.15),0.)
+        with patch.dict(os.environ,{'ZC_R6_ENDPOINT':'0'}):self.assertGreater(b.lngamma_inf(298.15),.99)
+        # This documents a base-class extension hazard, not correct association physics.
+
+
+
+class Orchestration(unittest.TestCase):
+    """Exercise the real driver and archive checker with mocked model workers."""
+    def fixture(self, folder):
+        root=Path(folder);plan=root/'plan.json';run=root/'run'
+        d.write(plan,{'private_fixture':True})
+        rows=[dict(row_id='row-0',c1='A',c2='B',system='A|B',T=298.15,x1=.4,
+                   P=100.,archived_pred_P=120.,psat=[120.,80.])]
+        jobs=[dict(id=f'job-{i:04d}',arm=arm,keys=['A','B'],indices=[0]) for i,arm in enumerate(o.ARMS)]
+        manifest=dict(rows=rows,jobs=jobs,exposure=d.exposure_receipt('a'*40),
+                      census={'eligible_rows':1,'selected_rows':1})
+        return plan,run,manifest
+
+    def execute(self, folder, bad_anchor=False, missing=False):
+        p,out,m=self.fixture(folder);seen=[]
+        def fake_launch(command, log, seconds, env):
+            jid=command[command.index('--job')+1];job=next(j for j in m['jobs'] if j['id']==jid)
+            dest=Path(command[command.index('--out')+1]);dest.mkdir();seen.append(job['arm'])
+            d.write(dest/'attempt-0000.json',{'row_id':'row-0','attempted':True})
+            value={'baseline':121. if bad_anchor else 120.,'experimental_epsilon_298':105.,'cosmosac2010':110.}[job['arm']]
+            if not (missing and job['arm']=='experimental_epsilon_298'):
+                d.write(dest/'result.json',dict(job=jid,plan_sha256=d.sha(p),arm=job['arm'],requested=1,
+                    attempted=1,values=[dict(row_id='row-0',value=value,error=None)]))
+            return dict(state='returned',returncode=0,wall_s=.001)
+        args=argparse.Namespace(plan=str(p),plan_commit='synthetic',out=str(out))
+        with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=lambda v,fresh=False: self.private(v,fresh)),patch.object(o,'launch',side_effect=fake_launch):
+            rc=o.run(args)
+        return rc,p,out,m,seen
+
+    @staticmethod
+    def private(v,fresh=False):
+        p=Path(v).resolve()
+        if fresh:p.mkdir()
+        return p
+
+    def test_complete_run_and_repeated_readonly_check(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,p,out,m,seen=self.execute(t)
+            self.assertEqual(rc,0);self.assertEqual(seen,list(o.ARMS))
+            q=d.read(out/'summary.json');self.assertEqual(q['attempted_model_calls'],3)
+            self.assertTrue(q['status']['complete'])
+            with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=self.private):
+                for _ in range(2):o.check(argparse.Namespace(plan=str(p),plan_commit='synthetic',run=str(out)))
+            public=d.read(out/'public-errors.json')
+            self.assertNotIn('receipts',public);self.assertNotIn('rows',public)
+
+    def test_failed_anchor_blocks_all_new_arms(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,p,out,m,seen=self.execute(t,bad_anchor=True)
+            self.assertEqual(rc,2);self.assertEqual(seen,['baseline'])
+            q=d.read(out/'summary.json');self.assertFalse(q['status']['complete']);self.assertEqual(q['attempted_model_calls'],1)
+            self.assertEqual(d.read(out/'job-0001.terminal.json')['state'],'blocked_anchor')
+
+    def test_missing_result_keeps_requested_denominator(self):
+        with tempfile.TemporaryDirectory() as t:
+            rc,p,out,m,seen=self.execute(t,missing=True)
+            self.assertEqual(rc,2);q=d.read(out/'summary.json')
+            self.assertEqual(q['status']['requested_rows'],1);self.assertEqual(q['attempted_model_calls'],3)
+            self.assertIsNone(q['aggregate_errors'])
+
+    def test_permanent_claim_blocks_second_run(self):
+        with tempfile.TemporaryDirectory() as t:
+            _,p,out,m,_=self.execute(t)
+            with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=self.private):
+                with self.assertRaises(FileExistsError):
+                    o.run(argparse.Namespace(plan=str(p),plan_commit='synthetic',out=str(out.parent/'other')))
+
+    def test_changed_worker_result_is_detected(self):
+        with tempfile.TemporaryDirectory() as t:
+            _,p,out,m,_=self.execute(t)
+            result=out/'job-0001/result.json';q=d.read(result);q['values'][0]['value']=104.
+            result.write_text(__import__('json').dumps(q))
+            with patch.object(o,'load',return_value=(p,m)),patch.object(d,'private',side_effect=self.private):
+                with self.assertRaises(ValueError):o.check(argparse.Namespace(plan=str(p),plan_commit='synthetic',run=str(out)))
+
+    def test_real_process_timeout_without_chemistry(self):
+        with tempfile.TemporaryDirectory() as t:
+            got=o.launch([sys.executable,'-c','import time;time.sleep(10)'],Path(t)/'log',.05,dict(os.environ))
+            self.assertEqual(got['state'],'timeout');self.assertNotEqual(got['returncode'],0)
+
+    def test_existing_pressure_api_is_key_based_and_kpa(self):
+        self.assertEqual(o.DESIGN['pressure_unit'],'kPa')
+        self.assertAlmostEqual(o.pressure([0.,0.],.4,[120.,80.]),96.)
+        source=Path(o.__file__).read_text()
+        self.assertIn('from zcosmo.scope import psat',source)
+        self.assertIn("float(psat(k,r['T']))",source)
+        self.assertNotIn('vapor_pressure(',source)
+
+if __name__=='__main__':unittest.main(verbosity=2)
```
<!-- END PATCH H14 -->

<!-- BEGIN PATCH P53 -->
```diff
diff --git a/docs/astra/round14/STATUS_PROPOSED.md b/docs/astra/round14/STATUS_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round14/STATUS_PROPOSED.md
@@ -0,0 +1,57 @@
+Round 14: proposed dielectric investigation, not a new model result
+
+The P35 explanatory campaign remains closed with its R10-R12 findings and
+liquid-state qualifications. The 630 primary profiles and six S1/S2 profiles
+remain frozen. Round 14 concerns the dielectric ingredient and the remaining
+VLE deficit of the main UD-backed Z0x model, not another glycol geometry rule.
+
+On the historical main7 common test subset, Z0x has VLE AAD 14.15 percent,
+against 8.62 percent for COSMO-SAC 2010, on 9,432 observations. On the different
+2017-2019 temporal common subset, the corresponding values are 9.47 and 7.28
+percent on 7,722 observations. These are archived comparisons. Both datasets
+have subsequently informed development and are not newly untouched test sets.
+The original IDAC/LLE strengths and HE/VLE limitations should be reported with
+their original denominators, not merged across scorecards.
+
+The pure-liquid permittivity estimate combines a single-conformer xTB dipole,
+D4 polarizability and COSMO cavity volume in an Onsager closure without an
+independent orientational-correlation calculation. Its possible errors include
+dipole, molecular-volume and local-field approximations as well as correlations.
+Increasing epsilon increases f=(epsilon-1)/(epsilon+0.5), toward the conductor
+limit. Improved bulk epsilon therefore does not automatically improve VLE.
+The coefficient saturates at large epsilon, but this alone does not bound the
+activity-coefficient or pressure response.
+
+P51 proposes a private experimental static-permittivity ingredient benchmark.
+P52 proposes one explicitly retrospective experimental-epsilon substitution
+on a source-hashed, reference-covered subset of the historical VLE archive.
+Both require prospective registration. No R14 ingredient score or VLE oracle
+result is claimed in this status note. The experimental-epsilon arm is not a
+fit-free model and is never a production replacement. It holds the profiles,
+interaction constants and pure vapor pressures fixed.
+
+The current manuscript should say that Z0/Z0x interaction constants were not
+regressed to ThermoML, rather than that no experimental information enters any
+upstream input or the VLE calculation. The existing vapor-pressure provider is
+shared by all models; profile conventions and documented UD input history have
+their own provenance. A later model motivated by exposed scorecards is a
+prospectively specified development variant, not a new validation of the old
+holdout. Experimental-epsilon diagnostics should appear in a separately labelled
+explanatory section with identical-subset baselines and coverage accounting.
+
+The association implementation already sets the explicit COSMO hydrogen-bond
+coefficients to zero. A redesign must address the reference/contact partition,
+remaining electrostatic overlap and site assumptions rather than repeat that
+switch. There is also a current-source dispatch concern: the association
+subclasses implement their additional free energy in _g, while the optimized
+base class uses _analytic in the interior and _endpoint under P28. Those paths
+can bypass the subclass contribution. This calls for a separately scoped
+source-version regression audit before any fresh association benchmark. It
+does not retroactively invalidate simulations or scorecards generated with an
+earlier dispatch path, and R14 changes no association production code.
+
+No 740-compound MD rollout is justified by density or hydrogen-bond agreement
+alone. A field-response/dipole model, converged collective fluctuations and
+independent validation are required. The proposed R14 source and oracle checks
+are a bounded way to assess the value of that project. Preparation of the
+current paper can proceed regardless of their outcome.
```
<!-- END PATCH P53 -->

<!-- BEGIN PATCH REG14 -->
```diff
diff --git a/docs/astra/round14/REGISTRATION_PROPOSED.md b/docs/astra/round14/REGISTRATION_PROPOSED.md
new file mode 100644
--- /dev/null
+++ b/docs/astra/round14/REGISTRATION_PROPOSED.md
@@ -0,0 +1,182 @@
+R14-P51-P52-P53: exposure, dielectric ingredient, and oracle diagnostic
+
+Proposed text. Append this complete text to PREREGISTRATION.md and commit it
+with the three reviewed helpers before acquiring the reference, computing an
+ingredient score, or freezing the oracle plan. Record the actual adoption time.
+Base: 864aaac1e85eda31a43f24e856770c7f56ccb760. This is a new main-question
+investigation, not a reopening of P35 or the R8/R9 numerical-gradient campaign.
+All 630 primary and six S1/S2 profiles remain frozen. No production model or
+experimental reference value is adopted. The R13 closeout remains historical.
+
+P51 is E read-only source acquisition and ingredient analysis. P52 is an A,
+experimental-input, retrospective explanatory VLE diagnostic, with E integrity
+checks. P53 is E reporting. R14 authorizes zero new SCF attempts, zero quantum
+gradients, zero conformer searches, zero new molecular-dynamics steps and zero
+paid or cloud jobs. Real data operations occur only on the private Mac. No
+raw UD data, dense profiles, row-level predictions or private paths enter Git.
+The helpers upload nothing. Synthetic software tests may run elsewhere.
+
+Exposure precedes scoring. The original 20-percent compound split and the
+2017-2019 temporal collection have both been examined repeatedly. Retain their
+historical identities, but do not describe them as newly untouched. P35's
+142 observations and its structural follow-ups remain exposed. Excluding them
+cannot restore blindness to the previously examined aggregate scorecards.
+The public CRC-derived dielectric table is a different measured property,
+not a verified independent laboratory sample. Its schema and some values,
+including the approximate water/methanol discrepancies, informed this design.
+No systematic comparison of the complete stored epsilon table with it has yet
+been performed in this review. Record hashes of the public registrations,
+progress log, main7/temporal scorecards, manuscript and closeout records in the
+exposure receipt. Private queue histories and every collaborator's past
+exposure have not been exhaustively audited. This receipt does not certify a
+new holdout. Only the exposed retrospective oracle is authorized.
+
+Acquire exactly the liquid-permittivity TSV from CalebBell/chemicals commit
+e79047588b30cfabc564c79fb26d760c746877d7, path
+chemicals/Electrolytes/Permittivity (Dielectric Constant) of Liquids.tsv,
+Git blob bf12ffba51b478a021acc6ed58778c04deb9b988. Preserve its bytes and record
+SHA256. One request, 30-second socket timeout, maximum 2 MB, no automatic
+retry or alternative reference source. A failed request retains a receipt;
+rerunning into an existing directory is forbidden. Store the reference and
+all outputs privately outside any Git checkout.
+
+Use all entries of the current results/qc/dielectric.csv, including failed
+entries in the coverage accounting. Resolve an exact InChIKey through the
+existing data/processed_ext/ud_complist.csv to exactly one checksum-valid CAS.
+Require that CAS to map to exactly one project key and one reference row.
+No names, connectivity-only fallback, racemate substitutions, or selected
+synonyms resolve an ambiguous dielectric identity. Missing identity or
+reference values are explicit coverage outcomes, never zero error.
+
+The reference state is 298.15 K. Use A+B*T+C*T^2+D*T^3 only inside the source's
+stated Tmin/Tmax range and when A and B are present. Missing higher-order C/D
+coefficients are zero as in the documented polynomial representation. Otherwise
+accept only a tabulated point within 0.10 K. Do not extrapolate, rescale a
+293.2 K value to 298.15 K, infer a temperature from its chemical name, or use
+optical permittivity as static permittivity. Values must be finite and >=1.
+If any reference-matched entry has an invalid stored epsilon, withhold a
+complete aggregate rather than silently removing it. Report the entire
+population and the reason-specific coverage counts. The retained reference
+state is the liquid state described by the compilation, not proof of a
+stable ambient-pressure liquid for every compound in the portfolio.
+
+Freeze input and helper hashes, installed numerical package versions and the
+exposure receipt before computing P51 outputs. Metrics are equal-compound mean
+and median absolute log epsilon error, signed log bias, mean and maximum
+relative epsilon error, and mean absolute error in f=(epsilon-1)/(epsilon+0.5).
+These metrics assess an ingredient. They are not an estimate of VLE error or a
+gate accepting the existing Onsager approximation. Checks of saved inputs and
+arithmetic may be repeated without new scores from a changed recipe.
+
+For a possible future physical pilot, the fixed four liquids are water,
+methanol, acetonitrile and benzene, identified by r14_dielectric.PILOT. A new
+candidate must independently pass its separately registered dipole/sampling
+validation and have complete reference coverage on all four. Prespecified
+ingredient criteria are mean absolute log error <=80 percent of the same-panel
+Onsager error, mean absolute f error <=0.02, maximum relative epsilon error
+<=25 percent, and no individual absolute log-error deterioration >0.05.
+These are engineering pilot criteria, not a confidence interval or a license
+to fit g to measurements. The helper's Boolean validation inputs are not a
+substitute for the actual physical receipts. No candidate-generating protocol,
+MD run, dipole training or production rollout is authorized here. Those need a
+new registration with reproducible model files and numerical validation.
+
+P52 uses an operator-designated original Z0x VLE prediction archive containing
+c1,c2,T,x1,P,pred_P,split. Hash it in its entirety. Query identities are original
+file-row ordinals bound to that hash, not names. Restrict to its original
+test_one/test_both rows, 250-450 K, 0<P<=500 kPa, strict interior compositions
+1e-4<x1<1-1e-4, finite positive archived prediction, and P51 references for
+both components. Do not select by observed error, hydrogen-bond class, epsilon
+error, or hoped-for improvement. All exclusion reasons are counted. This is an
+explicitly reference-covered, exposed subset, not the original main7 common set.
+
+Select at most 100 unordered binary systems by SHA256('R14-oracle-v1|'+system).
+Within each, retain at most ten eligible observations under SHA256 of the
+original file-row identity. Preserve ordered component representation and the
+original temperatures and compositions. Freeze the resulting identities and
+actual counts. The maximum is 1,000 observations, with three arm requests per
+observation, hence 3,000 activity-model API calls. These counts do not denote
+internal segment iterations. A smaller eligible universe is reported as such.
+
+Use the original UD profiles, unchanged, for all three arms. Record the exact
+profile paths resolved by the existing exact-key/unique-connectivity rule and
+provide both profiles explicitly in a private per-worker overlay. Keep the
+explicit dielectric CAS policy stricter than that historical profile policy.
+Protect hashes of exactly 630 profiles_v2, one S1 and five S2 files. Freeze the
+Z0 parameter, dispersion and dielectric tables, the compound table used by the
+existing vapor-pressure provider, all current zcosmo Python sources, the new
+helpers and installed package versions. Source or input drift stops execution.
+
+Freeze pure-component vapor pressures through the existing zcosmo.scope.psat
+function using its InChIKey interface. Its output and the archived experimental
+pressures are kPa. These same positive finite values enter every arm. This
+preparation invokes the existing property provider, but no activity model.
+Changed pure vapor-pressure inputs are not part of the epsilon intervention.
+Archive the frozen values privately with the plan.
+
+The three arms are current Z0x with its stored epsilon, current Z0x with the
+P51 experimental epsilon at 298.15 K, and COSMO-SAC 2010. The experimental values
+remain constant with temperature, just like current Z0x's stored table; this
+is not an epsilon(T) experiment. Replace only the instance's two epsilon
+values before any query, leaving its volume-fraction mixing rule and its
+composition derivative intact. Clear its instance mixture cache. Do not
+replace only c_ES while accidentally retaining an old dc_ES/dx. Enable P28
+identically, though the selected rows are outside the endpoint strip. All
+Z0/HB/London constants and input profiles remain unchanged. This experiment
+does not change the meaning of a fit-free production model: its experimental-
+epsilon arm is expressly NOT fit-free and can never be adopted by this result.
+
+Before the experimental-epsilon or COSMO-SAC arm starts, reproduce every
+selected archived Z0x pressure with the current stored-epsilon baseline at
+relative difference <1e-7. Require finite coverage on every selected identity.
+A mismatch blocks both later arms. A historical source-version or property-
+provider discrepancy requires a separate reproduction decision, not a relaxed
+gate after seeing the oracle. A blocked run is not evidence against the
+permittivity hypothesis. No old scorecard or historical endpoint result is
+overwritten.
+
+Use one fresh subprocess for each ordered pair and arm; preserve selected
+row order within that process. Clear inherited ZC_* settings before creating
+the model. Each attempted query has a prewritten receipt. All requested jobs
+have terminal records, including blocked and unstarted ones. Each subprocess
+has 120 seconds; the serial Mac driver has 7,200 seconds including orchestration,
+with a five-second process-kill allowance rather than additional scientific
+compute. At most four OpenMP threads and one BLAS thread. No second claimed
+run, retry, resume, alternate outcome directory or automatic budget extension.
+Independent jobs continue after another fails within the remaining allocation.
+
+The private oracle plan is bound to a committed SHA256 in
+ docs/astra/round14/ORACLE_PLAN_SHA256.txt
+before the first activity call. The registration and plan commits must be
+ancestors of the execution checkout. The registration checker also verifies
+the exact three helper files against their committed registration versions.
+Do not change the helpers between an accepted registration and execution.
+
+Require every requested new prediction to be finite before issuing complete
+aggregate errors. Do not select a favorable finite intersection. On the fixed
+subset report row-weighted AAD and signed pressure bias, equal-system AAD,
+paired oracle-minus-baseline AAD, residual oracle-minus-COSMO-SAC AAD, and
+improved/worsened counts. A signed comparator-gap recovery is reported only
+for a positive baseline-minus-COSMO-SAC AAD gap above 1e-6 percentage points;
+it is not clipped. Report all outcomes, including worse scores. No inferential
+confidence interval or production-acceptance threshold is attached to this
+exposed explanatory sample. The old 14.15/8.62 main7 comparison is not used as
+the denominator for this newly selected sample.
+
+Only the allowlisted aggregate error summary, after separate operator review,
+is eligible for publication. Per-row predictions, parameter inputs, detailed
+receipts and logs stay on the Mac. The independent check recomputes the saved
+arithmetic and hashes without any model calls. No favorable oracle outcome
+selects a physical recipe, fits a constant, authorizes 740 liquid simulations,
+or grants a new confirmatory look at an old split. An unhelpful result supports
+writing up current limitations; a helpful result identifies limited headroom
+under this particular closure, not a rigorous upper bound.
+
+P53 records a dielectric-development status separate from P35. Retain all
+original benchmarks with their actual common subsets and their exposure.
+A new physical variant needs an independently verified field/dipole model,
+finite-size and sampling tests, and a genuinely unexposed custodian-frozen
+validation source or an explicitly exposed fixed-design confirmation. The
+current Z0w inheritance/dispatch concern is a source-version audit item; no
+association code or historical failure is changed under R14. No fourth
+association fit or simulation-based activity-coefficient campaign is authorized.
```
<!-- END PATCH REG14 -->

Delivered-artifact verification: all five patches were extracted from this Markdown file. Independent and combined `git apply --check` passed against the verified source reconstruction. The combined patch applied and reproduced all five intended new files byte-for-byte. Python compilation and all three Bash command-block syntax checks passed. All 45 tests passed again from the extracted/applied artifact, including the mocked driver/checker cases and the real non-chemistry timeout test. The `catalog`, `screening` and help commands were also exercised. Registration commits and all Mac-only real-data commands remain unexecuted.
