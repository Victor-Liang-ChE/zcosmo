Round 14: proposed dielectric investigation, not a new model result

The P35 explanatory campaign remains closed with its R10-R12 findings and
liquid-state qualifications. The 630 primary profiles and six S1/S2 profiles
remain frozen. Round 14 concerns the dielectric ingredient and the remaining
VLE deficit of the main UD-backed Z0x model, not another glycol geometry rule.

On the historical main7 common test subset, Z0x has VLE AAD 14.15 percent,
against 8.62 percent for COSMO-SAC 2010, on 9,432 observations. On the different
2017-2019 temporal common subset, the corresponding values are 9.47 and 7.28
percent on 7,722 observations. These are archived comparisons. Both datasets
have subsequently informed development and are not newly untouched test sets.
The original IDAC/LLE strengths and HE/VLE limitations should be reported with
their original denominators, not merged across scorecards.

The pure-liquid permittivity estimate combines a single-conformer xTB dipole,
D4 polarizability and COSMO cavity volume in an Onsager closure without an
independent orientational-correlation calculation. Its possible errors include
dipole, molecular-volume and local-field approximations as well as correlations.
Increasing epsilon increases f=(epsilon-1)/(epsilon+0.5), toward the conductor
limit. Improved bulk epsilon therefore does not automatically improve VLE.
The coefficient saturates at large epsilon, but this alone does not bound the
activity-coefficient or pressure response.

P51 proposes a private experimental static-permittivity ingredient benchmark.
P52 proposes one explicitly retrospective experimental-epsilon substitution
on a source-hashed, reference-covered subset of the historical VLE archive.
Both require prospective registration. No R14 ingredient score or VLE oracle
result is claimed in this status note. The experimental-epsilon arm is not a
fit-free model and is never a production replacement. It holds the profiles,
interaction constants and pure vapor pressures fixed.

The current manuscript should say that Z0/Z0x interaction constants were not
regressed to ThermoML, rather than that no experimental information enters any
upstream input or the VLE calculation. The existing vapor-pressure provider is
shared by all models; profile conventions and documented UD input history have
their own provenance. A later model motivated by exposed scorecards is a
prospectively specified development variant, not a new validation of the old
holdout. Experimental-epsilon diagnostics should appear in a separately labelled
explanatory section with identical-subset baselines and coverage accounting.

The association implementation already sets the explicit COSMO hydrogen-bond
coefficients to zero. A redesign must address the reference/contact partition,
remaining electrostatic overlap and site assumptions rather than repeat that
switch. There is also a current-source dispatch concern: the association
subclasses implement their additional free energy in _g, while the optimized
base class uses _analytic in the interior and _endpoint under P28. Those paths
can bypass the subclass contribution. This calls for a separately scoped
source-version regression audit before any fresh association benchmark. It
does not retroactively invalidate simulations or scorecards generated with an
earlier dispatch path, and R14 changes no association production code.

No 740-compound MD rollout is justified by density or hydrogen-bond agreement
alone. A field-response/dipole model, converged collective fluctuations and
independent validation are required. The proposed R14 source and oracle checks
are a bounded way to assess the value of that project. Preparation of the
current paper can proceed regardless of their outcome.
