# HD 189733 b Lightkurve Transit Starter

**Author:** Biswajit Jana  
**Project type:** beginner-friendly exoplanet transit photometry notebook  
**Target used:** HD 189733 b, a well-studied hot Jupiter system

This repository is a small, reproducible starter project for the Exoplanet Watch / citizen-science community.  
It shows how to:

- search and download public TESS light curves using `lightkurve`
- fetch basic physical properties from the NASA Exoplanet Archive
- clean and normalize a light curve
- fold the light curve using the published orbital period
- estimate the transit depth
- save plots and CSV outputs for sharing

The aim is not to replace full scientific modelling. It is a clean first workflow that beginners can fork, run, and extend.

---

## Repository structure

```text
hd189733b-lightkurve-transit-starter/
├── notebooks/
│   └── HD189733b_Lightkurve_Starter.ipynb
├── src/
│   └── hd189733b_lightkurve_template.py
├── outputs/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quick start in Google Colab

1. Upload or clone this repository into Colab.
2. Open:

```text
notebooks/HD189733b_Lightkurve_Starter.ipynb
```

3. Run the notebook from top to bottom.

The notebook will create plots in the `outputs/` folder.

---

## Quick start locally

```bash
git clone <your-repo-url>
cd hd189733b-lightkurve-transit-starter
pip install -r requirements.txt
python src/hd189733b_lightkurve_template.py
```

Optional custom target:

```bash
python src/hd189733b_lightkurve_template.py --target "HD 189733" --planet "HD 189733 b"
```

---

## Outputs

The script/notebook saves:

```text
outputs/01_raw_lightcurve.png
outputs/02_cleaned_lightcurve.png
outputs/03_folded_transit.png
outputs/04_binned_transit_depth.png
outputs/05_physical_properties.csv
outputs/06_summary_metrics.csv
```

---

## What beginners should try next

- Try another target, e.g. `WASP-12`, `HAT-P-32`, `TOI-700`, or `HD 209458`.
- Compare SAP and PDCSAP flux where available.
- Change the flattening window length and see how the transit shape changes.
- Try different bin sizes for the folded light curve.
- Download Target Pixel Files and experiment with custom apertures.
- Add a simple transit model using `batman-package`.

---

## Notes and limitations

- This is a teaching and exploration notebook, not a final publication-grade transit fit.
- Transit parameters are pulled from the NASA Exoplanet Archive when available.
- TESS availability depends on whether the target was observed and whether products are available in MAST.
- The measured depth is a simple median-based estimate, so it should be treated as approximate.

---

## Data and software acknowledgement

This project uses public mission data and community tools:

- Lightkurve for working with Kepler, K2, and TESS light curves.
- MAST/STScI for public TESS data access.
- NASA Exoplanet Archive for confirmed exoplanet parameters.
- Astropy, NumPy, Pandas, and Matplotlib for scientific Python analysis.

---

## Feedback welcome

This project is intended to be public-friendly.  
Suggestions are welcome on how to make the workflow clearer, more accessible, and more useful for citizen scientists learning transit photometry.
