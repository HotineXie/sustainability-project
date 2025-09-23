import json
import pandas as pd
from pathlib import Path


THIS_DIR = Path(__file__).parent
ENERGY_JSON = THIS_DIR / "data" / "data.summary.json"          # annual energy by resource (GWh)
FACTORS_JSON = THIS_DIR / "data" / "gco2_per_kwh.json"         # gCO2/kWh by resource
OUTPUT_CSV = THIS_DIR / "annual_system_intensity.csv" # year, weighted_gco2_per_kwh


def load_energy_by_year() -> pd.DataFrame:
    with open(ENERGY_JSON, "r") as f:
        data = json.load(f)
    rows = []
    for year, res_map in data.items():
        for resource, gwh in res_map.items():
            rows.append({"year": int(year), "resource": resource, "energy_gwh": float(gwh)})
    return pd.DataFrame(rows)


def load_factors() -> pd.DataFrame:
    with open(FACTORS_JSON, "r") as f:
        data = json.load(f)
    rows = [{"resource": k, "gco2_per_kwh": float(v)} for k, v in data.items()]
    return pd.DataFrame(rows)


def compute_annual_intensity(energy_df: pd.DataFrame, factors_df: pd.DataFrame) -> pd.DataFrame:
    df = energy_df.merge(factors_df, on="resource", how="inner")
    # Convert GWh to kWh for weighting
    df["energy_kwh"] = df["energy_gwh"] * 1_000_000
    # Ignore negative energy (e.g., WSL or corrections)
    df = df[df["energy_kwh"] > 0]

    grouped = df.groupby("year", as_index=False).apply(
        lambda g: pd.Series({
            "weighted_gco2_per_kwh": (g["energy_kwh"] * g["gco2_per_kwh"]).sum() / g["energy_kwh"].sum()
        })
    )
    return grouped[["year", "weighted_gco2_per_kwh"]]


def main() -> None:
    energy_df = load_energy_by_year()
    factors_df = load_factors()
    annual = compute_annual_intensity(energy_df, factors_df)
    annual.sort_values("year").to_csv(OUTPUT_CSV, index=False)


if __name__ == "__main__":
    main()
