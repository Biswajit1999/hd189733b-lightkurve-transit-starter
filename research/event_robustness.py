"""Event-level sensitivity diagnostics for a pinned HD 189733 b TESS product.

These are conditional descriptive checks, not a physical limb-darkened fit.
No cadence-level uncertainties or spot/systematic covariance are supplied.
"""
from __future__ import annotations

import csv
import math
import random
from statistics import median


def read_events(path):
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    events = [(int(r["event"]), float(r["depth_fraction"]),
               int(r["n_in"]), int(r["n_out"])) for r in rows]
    validate(events)
    return events


def validate(events):
    if len(events) < 3 or len({e[0] for e in events}) != len(events):
        raise ValueError("At least three distinct transit events required")
    if any(not 0 < d < 1 or not math.isfinite(d) or ni < 5 or no < 5
           for _, d, ni, no in events):
        raise ValueError("Invalid event depth or coverage")


def quantile(values, q):
    s = sorted(values)
    pos = (len(s)-1)*q
    i = int(pos)
    return s[i] + (s[min(i+1, len(s)-1)]-s[i])*(pos-i)


def bootstrap_depths(events, draws=5000, seed=189733):
    """Event bootstrap, leave-one-event-out median and coverage sensitivity."""
    validate(events)
    if draws < 1:
        raise ValueError("Positive number of bootstrap draws required")
    depths = [e[1] for e in events]
    n = len(depths)
    rng = random.Random(seed)
    replicates = [median(rng.choices(depths, k=n)) for _ in range(draws)]
    full = median(depths)
    loo = [median(depths[:i]+depths[i+1:]) for i in range(n)]
    # Predeclared diagnostic, not a quality-based post-hoc exclusion.
    coverage = [e[1] for e in events if e[3] >= 100]
    return {
        "events": n, "median_depth": full,
        "bootstrap_16_50_84": [quantile(replicates, q) for q in (0.16, 0.5, 0.84)],
        "max_abs_leave_one_event_out_shift": max(abs(v-full) for v in loo),
        "baseline_100plus_events": len(coverage),
        "baseline_100plus_median": median(coverage) if len(coverage) >= 3 else None,
        "bootstrap_draws": draws,
    }


def theil_sen_slope(events):
    """Median pairwise depth slope per orbital cycle (not per day)."""
    validate(events)
    ordered = sorted(events)
    return median((b[1]-a[1])/(b[0]-a[0])
                  for i, a in enumerate(ordered) for b in ordered[i+1:])


def trend_permutation(events, permutations=4000, seed=20261028):
    """Two-sided label permutation; conditional exchangeability is assumed."""
    validate(events)
    if permutations < 1:
        raise ValueError("At least one permutation required")
    ordered = sorted(events)
    depths = [e[1] for e in ordered]
    observed = theil_sen_slope(ordered)
    rng = random.Random(seed)
    exceed = 0
    for _ in range(permutations):
        shuffled = depths[:]
        rng.shuffle(shuffled)
        synthetic = [(e[0], d, e[2], e[3]) for e, d in zip(ordered, shuffled)]
        exceed += abs(theil_sen_slope(synthetic)) >= abs(observed)-1e-15
    return {"slope_depth_fraction_per_cycle": observed,
            "permutations": permutations,
            "two_sided_permutation_p": (exceed+1)/(permutations+1),
            "null_assumption": "exchangeable event depths; no temporal correlations"}


def radius_ratio_sensitivity(events, contaminant_flux_ratios=(0.0, 0.01, 0.05),
                             draws=5000, seed=189733):
    """Propagate event-depth bootstrap through sqrt(delta*(1+Fcont/Fstar)).

    This is an *illustrative* uniform-source, non-limb-darkened approximation;
    contaminant flux ratios are hypothetical and not measured for HD 189733.
    """
    validate(events)
    if draws < 1 or any(not math.isfinite(f) or f < 0 for f in contaminant_flux_ratios):
        raise ValueError("Invalid draws or contamination")
    rng = random.Random(seed)
    d = [e[1] for e in events]
    sampled = [median(rng.choices(d, k=len(d))) for _ in range(draws)]
    rows = []
    for f in contaminant_flux_ratios:
        if max(sampled)*(1+f) >= 1:
            raise ValueError("Unphysical corrected depth")
        rr = [math.sqrt(x*(1+f)) for x in sampled]
        rows.append({"Fcont_over_Fstar": f,
                     "radius_ratio_at_median_depth": math.sqrt(median(d)*(1+f)),
                     "bootstrap_16_50_84": [quantile(rr, q) for q in (0.16, 0.5, 0.84)]})
    return rows


def audit(events):
    return {"depth": bootstrap_depths(events),
            "trend": trend_permutation(events),
            "radius_ratio": radius_ratio_sensitivity(events),
            "assumptions": "One frozen TESS Sector 41 SPOC product; event-level resampling; fixed ephemeris and stellar radius; hypothetical third light; no stellar activity model"}
