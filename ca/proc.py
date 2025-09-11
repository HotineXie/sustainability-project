import pandas as pd, glob, os
from pathlib import Path


CO2_DIR = "co2_per_resource"
SUP_DIR = "supply_trend"


norm = {
    "biogas":"biogas","biomass":"biomass","natural gas":"natural gas","coal":"coal",
    "imports":"imports","geothermal":"geothermal","solar":"solar","wind":"wind",
    "small hydro":"small hydro","large hydro":"large hydro","batteries":"batteries",
    "nuclear":"nuclear","other":"other"
}

def read_daily_energy():
    rows=[]
    for fp in glob.glob(os.path.join("data", SUP_DIR, "*.csv")):
        date = Path(fp).stem  # YYYYMMDD
        df = pd.read_csv(fp)
        df = df.fillna(0)
        num = df.select_dtypes("number").clip(lower=0)
        df[num.columns] = num
        factor = 1/12
        cols = [c for c in df.columns if c.lower() in [*norm.keys()]]
        daily = (df[cols]*factor).sum()
        for col,val in daily.items():
            rows.append({"date": pd.to_datetime(date), "resource": col.lower(), "energy_mwh": float(val)})
    return pd.DataFrame(rows)

def read_daily_co2():
    rows=[]
    for fp in glob.glob(os.path.join("data", CO2_DIR, "*.csv")):
        date = Path(fp).stem  # YYYYMMDD
        df = pd.read_csv(fp)
        df = df.fillna(0)
        co2_cols = [c for c in df.columns if c.lower().endswith(" co2")]
        df[co2_cols] = df[co2_cols].clip(lower=0)
        factor = (1/12) * 1_000_000
        daily = (df[co2_cols].sum() * factor)
        for col,val in daily.items():
            res = col[:-4].lower()
            rows.append({"date": pd.to_datetime(date), "resource": res, "co2_g": float(val)})
    return pd.DataFrame(rows)

daily_energy = read_daily_energy()
daily_co2 = read_daily_co2()

def unify(r):
    r = r.strip().lower()
    return norm.get(r, r)

daily_energy["resource"] = daily_energy["resource"].apply(unify)
daily_co2["resource"]   = daily_co2["resource"].apply(unify)

daily_all = pd.merge(daily_energy, daily_co2, on=["date","resource"], how="outer").fillna(0)

sys_daily = daily_all.groupby("date", as_index=False).agg(
    total_energy_mwh=("energy_mwh","sum"),
    total_co2_g=("co2_g","sum")
)
sys_daily["gco2_per_kwh"] = sys_daily["total_co2_g"] / (sys_daily["total_energy_mwh"]*1000)  # g / kWh

by_res_daily = daily_all.copy()
mask = by_res_daily["energy_mwh"] > 0
by_res_daily.loc[mask, "gco2_per_kwh"] = by_res_daily.loc[mask, "co2_g"] / (by_res_daily.loc[mask, "energy_mwh"]*1000)
by_res_daily.loc[~mask, "gco2_per_kwh"] = pd.NA


sys_daily["year"] = sys_daily["date"].dt.year
annual = sys_daily.groupby("year", as_index=False).agg(
    total_energy_mwh=("total_energy_mwh","sum"),
    total_co2_g=("total_co2_g","sum")
)
annual["gco2_per_kwh"] = annual["total_co2_g"] / (annual["total_energy_mwh"]*1000)

sys_daily.to_csv("daily_system_intensity.csv", index=False)
by_res_daily.to_csv("daily_by_resource_intensity.csv", index=False)
annual.to_csv("annual_system_intensity.csv", index=False)
