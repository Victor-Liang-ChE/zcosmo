P54 bias clarification, proposed for the round-16 record

The round-15 corner table and factor table report different statistics. From
corner 000 to corner 001, the displayed pressure bias changes from +1.44% to
-2.79%, a one-at-a-time change of -4.23 percentage points. The factor table's
-4.47 percentage points is the Shapley-allocated dispersion contribution to
bias, averaged over all other ingredient contexts. The rounded corner table
reproduces that allocation as approximately -4.4733 percentage points.

The R15 prose and R16 prompt should not describe -4.47 as the one-at-a-time
bias shift. This clarification preserves both original tables and every
registered result; it does not rerun predictions or revise their denominators.
The dispersion error-reduction attribution remains 2.24 percentage points
(67%) and its one-at-a-time AAD reduction remains 2.02 percentage points.

Source: ../round15/RESULTS.md at ca5c7e94627fcdebbf787afb688f8cab10e42a03.
The updated manuscript distinguishes these quantities explicitly.
