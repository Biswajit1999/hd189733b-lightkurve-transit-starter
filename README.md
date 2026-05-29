# HD 189733 b Transit Photometry

**Author:** Biswajit Jana  
**Notebook:** `HD189733b_Transit_Photometry.ipynb`

## About

This is a short Google Colab notebook I made to explore the transit of **HD 189733 b** using public TESS data.

The notebook downloads the light curve, uses the published planet values from the NASA Exoplanet Archive, folds the data around the expected transit time, estimates the transit depth, and saves the final plot.

## GitHub About text

```text
A short Google Colab notebook exploring the TESS transit of HD 189733 b, from light curve download to a simple transit-depth estimate.
```

## Suggested topics

```text
exoplanets
transit-photometry
hd189733b
tess
lightkurve
astronomy-python
google-colab
citizen-science
```

## What it does

1. Downloads public TESS data for HD 189733.
2. Gets the published planet values from the NASA Exoplanet Archive.
3. Plots the raw light curve.
4. Removes slow trends while protecting the expected transit.
5. Folds the data using the known period.
6. Estimates the transit depth.
7. Saves the final plot and a small summary table.

## Output files

After running the notebook, the `outputs/` folder will contain:

```text
target_info.csv
01_tess_light_curve.png
02_detrended_light_curve.png
03_hd189733b_transit.png
transit_depth_summary.csv
```

## Why this target?

HD 189733 b is a well-known hot Jupiter with a deep transit, so it is a good target for a first exoplanet light-curve demonstration.

## Notes

This is not meant to be a full publication-level transit fit. It is a simple, readable starting point for learning how transit photometry works.

Possible future upgrades:

- add more planets,
- compare different TESS sectors,
- add a simple transit model,
- add uploaded CSV support for ground-based observations,
- turn the notebook into a small interactive web tool.
