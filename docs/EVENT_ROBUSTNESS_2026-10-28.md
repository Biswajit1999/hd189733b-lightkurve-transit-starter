# HD 189733 b TESS Sector 41 event-level robustness (2026-10-28)

Three **conditional, independent** diagnostics using the existing
`outputs/per_transit_depths.csv` (11 SPOC PDCSAP events). No network
retrieval, new transit fit, new product selection, or frozen-data edits.

1. **Event bootstrap and deletion/coverage sensitivity.** Resample whole
   event depths (5,000 seeded draws), compute the median, 16/50/84% interval,
   maximum leave-one-event-out median shift, and the fixed `n_out >= 100`
   local-baseline coverage subset. The coverage cut is a diagnostic only.
2. **Depth-versus-orbit-index sensitivity.** Theil-Sen median pairwise slope
   in fractional depth per orbit, with a 4,000-shuffle, two-sided permutation
   test. The null assumes exchangeable event depths; correlated starspot
   evolution or TESS systematics violate that assumption.
3. **Nonlinear radius-ratio propagation and hypothetical dilution.** Apply
   `Rp/Rs = sqrt(depth * (1 + Fcont/Fstar))` to the same event-bootstrap
   samples at illustrative contaminant-to-target flux ratios 0%, 1%, 5%.
   These are **not measured** contamination estimates. Limb darkening,
   occulted spots, stellar-radius uncertainty, and ingress geometry are not
   included.

## Reproduce

```sh
python -m unittest discover -s tests -p 'test_event_robustness.py' -v
python scripts/run_event_robustness.py
# optional: python -m pip install matplotlib
python scripts/plot_event_robustness.py event_robustness.png
```

Local read-only run on the 11 committed event depths: median **2.265954%**;
bootstrap 16/84% **2.24736/2.30679%** (matching the existing notebook's
seeded event bootstrap); maximum leave-one-event-out median shift **64.16 ppm**;
`n_out >= 100` retains 10 events with median **2.26683%**.
Theil-Sen slope **-27.06 ppm per orbital cycle**, two-sided permutation
**p=0.3572** under the declared exchangeability null. No significant trend
is established. Zero-dilution radius ratio **0.150531**; illustrative 5%
contamination increases it to **0.154248**.

The reference planet parameters, notebook, plots and original outputs are
unchanged. These are descriptive sensitivities, not a spot-corrected planet
radius, atmospheric inference, or independent TESS discovery.
