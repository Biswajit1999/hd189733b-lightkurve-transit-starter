#!/usr/bin/env python3
"""
HD 189733 b Lightkurve Transit Starter
Author: Biswajit Jana

A beginner-friendly template for downloading TESS light curves with Lightkurve,
folding the data on a known exoplanet period, estimating the transit depth, and
saving plots for sharing.

Run:
    python src/hd189733b_lightkurve_template.py

Optional:
    python src/hd189733b_lightkurve_template.py --target "HD 189733" --planet "HD 189733 b"
"""

from __future__ import annotations

import argparse
import warnings
from pathlib import Path
from urllib.parse import quote

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import astropy.units as u
import lightkurve as lk


# -----------------------------
# User settings
# -----------------------------
DEFAULT_TARGET = "HD 189733"
DEFAULT_PLANET = "HD 189733 b"
OUTDIR = Path("outputs")
OUTDIR.mkdir(exist_ok=True)


def query_nasa_exoplanet_archive(planet_name: str) -> pd.DataFrame:
    """
    Query the NASA Exoplanet Archive PSCompPars table through TAP.

    Returns one row for the planet if available.
    """
    base = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    sql = f"""
    SELECT
        pl_name, hostname,
        pl_orbper, pl_tranmid, pl_trandur,
        pl_rade, pl_radj, pl_bmassj,
        pl_orbsmax, pl_orbincl,
        st_teff, st_rad, st_mass,
        sy_dist
    FROM pscomppars
    WHERE pl_name = '{planet_name}'
    """
    url = f"{base}?query={quote(sql)}&format=csv"
    return pd.read_csv(url)


def fallback_hd189733b_properties() -> pd.DataFrame:
    """
    Safe fallback values. These are only used if the online archive query fails.
    Always prefer the live NASA Exoplanet Archive values when possible.
    """
    return pd.DataFrame([{
        "pl_name": "HD 189733 b",
        "hostname": "HD 189733",
        "pl_orbper": 2.21857567,     # days
        "pl_tranmid": np.nan,        # BJD, may be filled from archive
        "pl_trandur": 1.8,           # hours, approximate fallback
        "pl_rade": np.nan,
        "pl_radj": 1.13,
        "pl_bmassj": 1.13,
        "pl_orbsmax": 0.031,
        "pl_orbincl": 85.7,
        "st_teff": 5000,
        "st_rad": 0.76,
        "st_mass": 0.82,
        "sy_dist": 19.8,
    }])


def get_planet_properties(planet_name: str) -> pd.Series:
    """
    Fetch planet properties, with a local fallback for demo robustness.
    """
    try:
        props = query_nasa_exoplanet_archive(planet_name)
        if len(props) == 0:
            raise ValueError("No rows returned from NASA Exoplanet Archive.")
        print("✅ Planet properties loaded from NASA Exoplanet Archive.")
    except Exception as exc:
        warnings.warn(f"Archive query failed; using fallback values. Reason: {exc}")
        props = fallback_hd189733b_properties()

    props.to_csv(OUTDIR / "05_physical_properties.csv", index=False)
    return props.iloc[0]


def convert_archive_epoch_to_lightkurve_time(epoch_bjd: float, lc_time_values: np.ndarray) -> float:
    """
    Convert a full BJD transit midpoint to the time system used by many mission light curves.

    TESS Lightkurve times are usually BTJD = BJD - 2457000.
    Kepler/K2 Lightkurve times are often BKJD = BJD - 2454833.

    If the epoch is already small, return it unchanged.
    """
    if not np.isfinite(epoch_bjd):
        return float(np.nanmedian(lc_time_values))

    if epoch_bjd > 2_400_000:
        median_time = float(np.nanmedian(lc_time_values))

        candidates = {
            "BJD": epoch_bjd,
            "BTJD": epoch_bjd - 2457000.0,
            "BKJD": epoch_bjd - 2454833.0,
        }

        # Pick the candidate closest to the observed time range.
        best_name, best_value = min(
            candidates.items(),
            key=lambda item: abs(item[1] - median_time)
        )
        print(f"✅ Converted archive epoch using {best_name}: {best_value:.5f}")
        return float(best_value)

    return float(epoch_bjd)


def download_tess_lightcurve(target: str):
    """
    Search and download a TESS light curve from MAST using Lightkurve.
    """
    print(f"🔎 Searching TESS light curves for: {target}")
    search = lk.search_lightcurve(target, mission="TESS")

    if len(search) == 0:
        raise RuntimeError(f"No TESS light curves found for {target}.")

    print(search[:10])
    print(f"✅ Found {len(search)} light curve products.")

    # Prefer short-cadence / mission light curve products when available.
    collection = search.download_all(download_dir="data/downloads")
    if collection is None or len(collection) == 0:
        raise RuntimeError("Download failed or returned no light curves.")

    # Stitch multiple sectors/cadences into one light curve.
    lc = collection.stitch().remove_nans().normalize()
    return lc


def make_transit_mask(time_values: np.ndarray, period: float, epoch_time: float, duration_hours: float) -> np.ndarray:
    """
    Build a mask around expected transit times.
    The mask is True during transit, so Lightkurve flattening can avoid fitting through transits.
    """
    duration_days = duration_hours / 24.0 if np.isfinite(duration_hours) else 2.0 / 24.0

    phase_days = ((time_values - epoch_time + 0.5 * period) % period) - 0.5 * period

    # Mask a bit wider than the expected transit to protect the transit shape.
    return np.abs(phase_days) < 1.5 * duration_days


def estimate_depth(folded_lc, duration_hours: float) -> dict:
    """
    Simple transit-depth estimate using median in-transit and out-of-transit flux.

    This is intentionally simple for a beginner notebook.
    """
    phase_days = np.asarray(folded_lc.time.value, dtype=float)
    flux = np.asarray(folded_lc.flux.value, dtype=float)

    duration_days = duration_hours / 24.0 if np.isfinite(duration_hours) else 2.0 / 24.0

    in_transit = np.abs(phase_days) < 0.5 * duration_days
    out_transit = (np.abs(phase_days) > 1.5 * duration_days) & (np.abs(phase_days) < 3.0 * duration_days)

    if in_transit.sum() < 5 or out_transit.sum() < 5:
        return {"depth_fraction": np.nan, "depth_percent": np.nan, "depth_ppm": np.nan}

    f_in = np.nanmedian(flux[in_transit])
    f_out = np.nanmedian(flux[out_transit])
    depth_fraction = 1.0 - (f_in / f_out)

    return {
        "depth_fraction": float(depth_fraction),
        "depth_percent": float(depth_fraction * 100.0),
        "depth_ppm": float(depth_fraction * 1e6),
    }


def expected_depth_from_radii(props: pd.Series) -> dict:
    """
    Estimate expected transit depth from planet radius and stellar radius.

    depth ≈ (Rp/Rs)^2

    Uses Earth radius and Solar radius if pl_rade and st_rad are available.
    """
    rearth_to_rsun = 0.0091577

    rp_earth = props.get("pl_rade", np.nan)
    st_rad_sun = props.get("st_rad", np.nan)

    if np.isfinite(rp_earth) and np.isfinite(st_rad_sun) and st_rad_sun > 0:
        rp_rs = (rp_earth * rearth_to_rsun) / st_rad_sun
        depth = rp_rs ** 2
        return {
            "expected_rp_rs": float(rp_rs),
            "expected_depth_percent": float(depth * 100.0),
            "expected_depth_ppm": float(depth * 1e6),
        }

    return {"expected_rp_rs": np.nan, "expected_depth_percent": np.nan, "expected_depth_ppm": np.nan}


def plot_lightcurves(lc, clean_lc, folded_lc, binned_lc, target: str, planet: str, depth_metrics: dict):
    """
    Create and save the main project plots.
    """
    # 1. Raw light curve
    ax = lc.plot(label="Raw / stitched light curve", normalize=False)
    ax.set_title(f"{target}: raw stitched TESS light curve")
    ax.figure.tight_layout()
    ax.figure.savefig(OUTDIR / "01_raw_lightcurve.png", dpi=200)
    plt.close(ax.figure)

    # 2. Cleaned light curve
    ax = clean_lc.plot(label="Cleaned + normalized")
    ax.set_title(f"{target}: cleaned normalized light curve")
    ax.figure.tight_layout()
    ax.figure.savefig(OUTDIR / "02_cleaned_lightcurve.png", dpi=200)
    plt.close(ax.figure)

    # 3. Folded transit
    ax = folded_lc.scatter(label="Folded data", s=4, alpha=0.45)
    ax.set_title(f"{planet}: folded transit")
    ax.set_xlabel("Time from mid-transit [days]")
    ax.figure.tight_layout()
    ax.figure.savefig(OUTDIR / "03_folded_transit.png", dpi=200)
    plt.close(ax.figure)

    # 4. Binned folded transit
    ax = folded_lc.scatter(label="Folded data", s=3, alpha=0.25)
    binned_lc.errorbar(ax=ax, label="Binned light curve")

    depth_text = "Measured depth ≈ "
    if np.isfinite(depth_metrics["depth_percent"]):
        depth_text += f"{depth_metrics['depth_percent']:.3f}% ({depth_metrics['depth_ppm']:.0f} ppm)"
    else:
        depth_text += "not available"

    ax.set_title(f"{planet}: binned transit depth\n{depth_text}")
    ax.set_xlabel("Time from mid-transit [days]")
    ax.figure.tight_layout()
    ax.figure.savefig(OUTDIR / "04_binned_transit_depth.png", dpi=220)
    plt.close(ax.figure)


def optional_tpf_plot(target: str):
    """
    Optional: try to download and plot the TESS target pixel file / cutout.
    This may not be available for every target, so it is allowed to fail gracefully.
    """
    try:
        tpf_search = lk.search_targetpixelfile(target, mission="TESS")
        if len(tpf_search) == 0:
            print("No TESS target pixel files found.")
            return

        tpf = tpf_search[0].download(download_dir="data/downloads")
        ax = tpf.plot(aperture_mask=tpf.pipeline_mask)
        ax.set_title(f"{target}: TESS pixel stamp / aperture")
        ax.figure.tight_layout()
        ax.figure.savefig(OUTDIR / "07_tpf_aperture.png", dpi=200)
        plt.close(ax.figure)
        print("✅ Saved optional TPF aperture plot.")
    except Exception as exc:
        print(f"Optional TPF plot skipped: {exc}")


def main(target: str = DEFAULT_TARGET, planet: str = DEFAULT_PLANET, make_tpf: bool = True):
    print("=" * 70)
    print("HD 189733 b Lightkurve Transit Starter")
    print("=" * 70)

    props = get_planet_properties(planet)
    period = float(props.get("pl_orbper", np.nan))
    duration_hours = float(props.get("pl_trandur", np.nan))
    epoch_bjd = float(props.get("pl_tranmid", np.nan))

    if not np.isfinite(period):
        raise RuntimeError("Orbital period is missing. Cannot fold light curve.")

    lc = download_tess_lightcurve(target)
    lc_time_values = np.asarray(lc.time.value, dtype=float)

    epoch_time = convert_archive_epoch_to_lightkurve_time(epoch_bjd, lc_time_values)

    transit_mask = make_transit_mask(
        time_values=lc_time_values,
        period=period,
        epoch_time=epoch_time,
        duration_hours=duration_hours,
    )

    print("🧼 Cleaning light curve...")
    clean_lc = (
        lc.flatten(window_length=401, mask=transit_mask)
          .remove_outliers(sigma=5)
          .remove_nans()
          .normalize()
    )

    print("🌀 Folding light curve...")
    folded_lc = clean_lc.fold(period=period, epoch_time=epoch_time)

    print("📉 Binning folded light curve...")
    binned_lc = folded_lc.bin(time_bin_size=5 * u.minute)

    depth_metrics = estimate_depth(folded_lc, duration_hours)
    expected_metrics = expected_depth_from_radii(props)

    summary = {
        "target": target,
        "planet": planet,
        "period_days": period,
        "epoch_time_used": epoch_time,
        "duration_hours": duration_hours,
        **depth_metrics,
        **expected_metrics,
    }

    pd.DataFrame([summary]).to_csv(OUTDIR / "06_summary_metrics.csv", index=False)

    print("📊 Saving plots...")
    plot_lightcurves(lc, clean_lc, folded_lc, binned_lc, target, planet, depth_metrics)

    if make_tpf:
        optional_tpf_plot(target)

    print("\n✅ Done. Files saved in:", OUTDIR.resolve())
    print(pd.DataFrame([summary]).T.rename(columns={0: "value"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lightkurve starter workflow for HD 189733 b.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="Host star / target name")
    parser.add_argument("--planet", default=DEFAULT_PLANET, help="Planet name in NASA Exoplanet Archive")
    parser.add_argument("--no-tpf", action="store_true", help="Skip optional TPF aperture plot")
    args = parser.parse_args()

    main(target=args.target, planet=args.planet, make_tpf=not args.no_tpf)
