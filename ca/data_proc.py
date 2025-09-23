import glob
import os
from pathlib import Path
import pandas as pd


THIS_DIR = Path(__file__).parent
CO2_DIR = THIS_DIR / "data" / "co2_per_resource"
SUP_DIR = THIS_DIR / "data" / "supply_trend"
OUTPUT_CSV = THIS_DIR / "annual_system_intensity.csv"  # year, weighted_gco2_per_kwh


def read_daily_energy() -> pd.DataFrame:
    rows = []
    for fp in glob.glob(os.path.join(SUP_DIR.as_posix(), "*.csv")):
        date = Path(fp).stem  # YYYYMMDD
        df = pd.read_csv(fp).fillna(0)
        numeric = df.select_dtypes("number").clip(lower=0)
        df[numeric.columns] = numeric
        # files are monthly, each row is 5-min; 12 intervals per hour → 1/12 MWh scaling used previously
        factor = 1/12
        cols = list(numeric.columns)
        daily = (df[cols] * factor).sum()
        for col, val in daily.items():
            rows.append({"date": pd.to_datetime(date), "resource": col.lower(), "energy_mwh": float(val)})
    return pd.DataFrame(rows)


def read_daily_co2() -> pd.DataFrame:
    rows = []
    for fp in glob.glob(os.path.join(CO2_DIR.as_posix(), "*.csv")):
        date = Path(fp).stem  # YYYYMMDD
        df = pd.read_csv(fp).fillna(0)
        co2_cols = [c for c in df.columns if c.lower().endswith(" co2")]
        df[co2_cols] = df[co2_cols].clip(lower=0)
        # Convert from metric tons to grams (1e6), keeping the same 1/12 scaling as energy side
        factor = (1/12) * 1_000_000
        daily = (df[co2_cols].sum() * factor)
        for col, val in daily.items():
            res = col[:-4].lower()
            rows.append({"date": pd.to_datetime(date), "resource": res, "co2_g": float(val)})
    return pd.DataFrame(rows)


def compute_annual_intensity() -> pd.DataFrame:
    daily_energy = read_daily_energy()
    daily_co2 = read_daily_co2()

    daily_all = pd.merge(daily_energy, daily_co2, on=["date", "resource"], how="outer").fillna(0)
    sys_daily = daily_all.groupby("date", as_index=False).agg(
        total_energy_mwh=("energy_mwh", "sum"),
        total_co2_g=("co2_g", "sum")
    )

    sys_daily["year"] = sys_daily["date"].dt.year
    annual = sys_daily.groupby("year", as_index=False).agg(
        total_energy_mwh=("total_energy_mwh", "sum"),
        total_co2_g=("total_co2_g", "sum")
    )
    annual["weighted_gco2_per_kwh"] = annual["total_co2_g"] / (annual["total_energy_mwh"] * 1000)
    return annual[["year", "weighted_gco2_per_kwh"]]


def main() -> None:
    annual = compute_annual_intensity()
    annual.sort_values("year").to_csv(OUTPUT_CSV, index=False)


if __name__ == "__main__":
    main()
