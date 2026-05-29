# HD 189733 b Transit Photometry

**Author:** Biswajit Jana  
**Notebook:** `HD189733b_Transit_Photometry.ipynb`

## About

This is a short Google Colab notebook for exploring the transit method using public TESS light-curve data. The default target is **HD 189733 b**, a well-studied hot Jupiter with a deep transit, but the notebook is written so that users can try other known transiting planets by changing the target settings.

The notebook downloads TESS light curves, uses published planet parameters from the NASA Exoplanet Archive, aligns the observed data using the known transit ephemeris, stacks the individual transit windows, measures the transit depth, and estimates simple physical parameters such as \(R_p/R_\star\), planet radius, bulk density, transit probability, and approximate equilibrium temperature where archive inputs are available.


## Suggested topics

```text
exoplanets
transit-photometry
hd189733b
tess
lightkurve
nasa-exoplanet-archive
astronomy-python
google-colab
citizen-science
```

## What the notebook does

1. Lets users choose a target from presets or add a custom planet.
2. Gets planet and stellar parameters from the NASA Exoplanet Archive.
3. Downloads real public TESS light-curve data using Lightkurve.
4. Uses the published ephemeris to predict transit centres in the observed data.
5. Locally normalises and stacks individual transit windows.
6. Measures the transit depth.
7. Uses the depth to estimate \(R_p/R_\star\) and planet radius.
8. Saves plots and CSV summary tables.

## Why HD 189733 b?

HD 189733 b is a useful first target because it is a nearby, bright, well-studied hot Jupiter with a deep transit. That makes the transit signal easier to recover in a teaching notebook than many smaller or shallower planets.

## Is this real data?

Yes. The scatter points in the final plot come from real public TESS light-curve products downloaded through Lightkurve. The notebook uses the published orbital period and transit midpoint to align the observed data. No fake transit is injected.

The smooth curve in the final plot is a binned version of the observed folded data.

## What can be estimated from the dip?

The simplest transit relation is:

\[
\delta \approx \left(\frac{R_p}{R_\star}\right)^2
\]

where \(\delta\) is the fractional transit depth. Therefore:

\[
\frac{R_p}{R_\star} \approx \sqrt{\delta}
\]

If the stellar radius is known, the planet radius can be estimated as:

\[
R_p \approx R_\star \sqrt{\delta}
\]

The notebook uses this to estimate:

- measured transit depth,
- \(R_p/R_\star\),
- planet radius in Earth radii,
- planet radius in Jupiter radii,
- approximate bulk density if planet mass is available,
- approximate equilibrium temperature,
- approximate transit probability.

These are first-order estimates, not a replacement for a full transit model.

## Output files

After running the notebook, the `outputs/` folder contains:

```text
target_info.csv
01_tess_light_curve.png
stacked_transit_points.csv
binned_transit.csv
derived_physical_parameters.csv
final_transit_plot.png
transit_photometry_results.zip
```

## How to run

Open the notebook in Google Colab:

```text
HD189733b_Transit_Photometry.ipynb
```

Then run all cells from top to bottom.

The notebook installs its own dependencies:

```bash
pip install lightkurve pandas numpy matplotlib astropy
```

## Trying other targets

In the notebook, edit:

```python
TARGET_KEY = "HD 189733 b"
```

Available presets include:

```text
HD 189733 b
HD 209458 b
WASP-12 b
HAT-P-32 b
```

You can also set:

```python
CUSTOM_MODE = True
```

and edit the custom target block.

Good beginner targets usually have:

- bright host stars,
- deep transits,
- short orbital periods,
- published ephemerides,
- available TESS light curves.


## Notes and limitations

This notebook is designed for learning and experimentation. It does not perform a full physical transit fit with limb darkening, starspot modelling, correlated noise treatment, or posterior sampling. HD 189733 is an active star, so real residuals can include starspot and stellar-activity effects.

## Future ideas

- Add more preset planets.
- Add sector-by-sector comparison.
- Add an optional `batman` transit model overlay.
- Add a BLS search cell for unknown periods.
- Add user-uploaded CSV support for ground-based observations.
- Turn the notebook into a simple web tool for citizen-science users.

## References

Bakos, G. Á. et al. (2006) ‘Refined parameters of the planet orbiting HD 189733’, *The Astrophysical Journal*.

Bouchy, F. et al. (2005) ‘ELODIE metallicity-biased search for transiting Hot Jupiters II. A very hot Jupiter transiting the bright K star HD189733’, *Astronomy & Astrophysics*.

Lightkurve Collaboration et al. (2018) ‘Lightkurve: Kepler and TESS time series analysis in Python’, *Astrophysics Source Code Library*.

NASA Exoplanet Archive (n.d.) ‘Planetary Systems Composite Parameters and TAP service’, NASA Exoplanet Science Institute.

Pont, F. et al. (2007) ‘Hubble Space Telescope time-series photometry of the planetary transit of HD 189733: no moon, no rings, starspots’, *Astronomy & Astrophysics*.

Ricker, G. R. et al. (2015) ‘Transiting Exoplanet Survey Satellite’, *Journal of Astronomical Telescopes, Instruments, and Systems*.
