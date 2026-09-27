# Methods and inference boundary

## Data lineage

The notebook queries the NASA Exoplanet Archive `pscomppars` table for the
published ephemeris and system parameters. It then uses Lightkurve to request
public TESS light-curve products, preferring SPOC short-cadence products and
PDCSAP flux when available. The notebook records the selected mission/sector,
MAST product filename and data URI, flux column, epoch source, and target
parameters in its output tables.

## Product selection

Candidate products are ranked only by usable coverage: the product with the
largest number of finite, quality-filtered cadences is selected, with the
lowest search-result index as a deterministic tie-break. Neither measured nor
published transit depth participates in this choice. This prevents a
best-looking-sector or closest-to-reference selection from manufacturing the
subsequent depth agreement.

## Epoch and depth estimands

The orbital period and initial midpoint are externally supplied by the archive
or the declared target preset. Within a prespecified ±0.25-day window, the
epoch offset is fitted as a nuisance parameter by maximizing a robust
box-depth contrast. This makes the analysis an ephemeris-conditioned transit
measurement, not an independent period discovery.

For the selected product, each transit is normalized by the median of its own
out-of-transit points. The primary depth estimand is the median of these
per-event depths. At least five in-transit and five local baseline points are
required per event, and at least three measurable transits are required.

## Uncertainty

A fixed-seed event bootstrap resamples complete transit depths 5,000 times and
reports the 16th and 84th percentiles. Resampling whole events preserves
within-event cadence structure better than treating every photometric point as
independent. The interval remains conditional on the selected pipeline
product, fixed ephemeris family, baseline windows, and unmodelled PDCSAP
systematics; it is not a full posterior credible interval.

## Interpretation limits

- The depth-to-radius conversion uses the small-planet geometric
  approximation and an externally supplied stellar radius.
- No limb-darkened physical transit model, spot-crossing model, dilution
  inference, Gaussian process, or sector hierarchy is fitted.
- HD 189733 is active; transit-to-transit scatter can contain real stellar
  variability as well as instrumental residuals.
- Equilibrium temperature assumes zero Bond albedo and complete heat
  redistribution through the usual simplified expression.
- Bulk density combines the depth-derived radius with an archive mass and is
  therefore not an independent dynamical measurement.

## Primary references

- Lightkurve Collaboration et al. 2018, *Astrophysics Source Code Library*,
  ascl:1812.013.
- NASA Exoplanet Archive, Planetary Systems Composite Parameters and TAP
  service.
- Ricker et al. 2015, *Journal of Astronomical Telescopes, Instruments, and
  Systems*, 1, 014003. DOI: 10.1117/1.JATIS.1.1.014003.
- Pont et al. 2007, *Astronomy & Astrophysics*, 476, 1347–1355. DOI:
  10.1051/0004-6361:20078269.
