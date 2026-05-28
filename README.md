# HD 189733 b Transit Lab — No Lightkurve

**Author:** Biswajit Jana  
**Main file:** `HD189733b_Transit_From_FITS_No_Lightkurve.ipynb`

## About

A transparent Google Colab pipeline that recovers the transit of **HD 189733 b** directly from public **TESS FITS light-curve files**, without using Lightkurve. The project downloads data from MAST, reads the FITS columns with Astropy, applies quality masking, uses NASA Exoplanet Archive ephemerides, locally normalises predicted transit windows, folds the light curve, estimates the transit depth, and overlays a simple physical transit model using `batman`.

**GitHub About text:**  
`No-Lightkurve Colab pipeline for recovering the HD 189733 b TESS transit directly from MAST FITS files, with local detrending, depth estimation and a physical batman model overlay.`

Suggested topics:

```text
exoplanets
transit-photometry
tess
mast
fits
astropy
astroquery
batman
hd189733b
citizen-science
astronomy-python
```

---

## Why this version exists

The first version used `lightkurve`, which is excellent for quick exploration, but it hides many steps. This version is more inspectable and closer to a real analysis workflow:

1. query MAST directly,
2. download real TESS `*_lc.fits` products,
3. read `TIME`, `PDCSAP_FLUX`, `SAP_FLUX`, and `QUALITY` columns manually,
4. use archive ephemerides rather than blindly trusting an automatic fold,
5. locally detrend each predicted transit window,
6. estimate depth from the folded light curve,
7. compare with the expected value from \( (R_p/R_\star)^2 \),
8. overlay a physical transit model.

---

## Open in Google Colab

Upload the notebook to Google Colab, or place it in this repository and open it from GitHub using Colab.

Notebook:

```text
HD189733b_Transit_From_FITS_No_Lightkurve.ipynb
```

---

## What the notebook produces

The notebook creates an `outputs/` folder containing:

```text
01_nasa_exoplanet_archive_pscomppars.csv
02_selected_target_parameters.csv
03_quality_masked_tess_lightcurve.csv
04_raw_quality_masked_tess_lightcurve.png
05_predicted_transits_on_raw_flux.png
06_locally_normalised_transit_points.csv
07_binned_folded_transit.csv
08_HD189733b_final_transit_model_plot.png
09_transit_model_residuals.png
10_narrow_bls_sanity_check.png
11_final_science_summary.csv
```

The main plot is:

```text
08_HD189733b_final_transit_model_plot.png
```

---

## Scientific idea

For a transiting exoplanet, the approximate transit depth is:

\[
\delta \approx \left(\frac{R_p}{R_\star}\right)^2
\]

HD 189733 b is a hot Jupiter, so its transit is deep enough to be a good public demonstration target. The notebook estimates the observed depth from locally normalised TESS data and compares it with the expected archive value.

---

## Method summary

### 1. Data access

The notebook uses `astroquery.mast.Observations` to search for public TESS light-curve products near HD 189733 and downloads selected `*_lc.fits` files.

### 2. FITS-level reading

The notebook reads the TESS FITS table directly using:

```python
from astropy.io import fits
```

The preferred flux column is:

```text
PDCSAP_FLUX
```

If that is unavailable, the notebook falls back to:

```text
SAP_FLUX
```

### 3. Quality masking

By default, the notebook uses:

```python
QUALITY == 0
```

This keeps the cleanest cadences. Users can switch to `QUALITY_MODE = "loose"` if the strict mask leaves too few points.

### 4. Local transit normalisation

Each predicted transit is extracted in a window around the expected transit centre. The code fits a baseline only to out-of-transit points and divides the window by that baseline. This reduces slow stellar/instrumental trends while keeping the transit shape visible.

### 5. Physical model

The notebook uses `batman-package` to overlay a simple limb-darkened transit model. Most orbital parameters are taken from archive values, while the radius ratio can be fitted to the binned folded transit.

---

## Requirements

The notebook installs its own dependencies in Colab:

```bash
pip install astroquery astropy batman-package scipy pandas numpy matplotlib
```

No Lightkurve is required.

---

## Limitations

This is a teaching and demonstration workflow, not a final publication-grade transit analysis.

Known simplifications:

- limb-darkening coefficients are approximate,
- the baseline model is a simple local polynomial,
- uncertainties are estimated with a simple bootstrap,
- the physical model is a compact fit, not a full MCMC posterior,
- HD 189733 is an active spotted star, so residuals may include real stellar activity.

---

## Good next upgrades

- Add a target selector for several hot Jupiters.
- Add automatic sector-by-sector comparison.
- Add real TESS-band limb-darkening lookup.
- Add MCMC fitting with `emcee` or `exoplanet`.
- Add support for uploaded ground-based Exoplanet Watch CSV files.
- Add a web-dashboard version for public users.

---

## Acknowledgements

This project uses public data and open-source astronomy tools from:

- MAST / STScI for TESS data access.
- NASA Exoplanet Archive for published exoplanet parameters.
- Astropy and Astroquery for scientific Python data access.
- Batman for analytic/numerical transit light-curve modelling.

---

## Citation notes

When using this repository, cite the relevant mission/archive/software papers for:

- TESS and MAST data products,
- NASA Exoplanet Archive,
- Astropy / Astroquery,
- Batman transit modelling.
