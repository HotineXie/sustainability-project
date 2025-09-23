# Sustainability Project: Energy Intensity Analysis

This project analyzes greenhouse gas emissions intensity (gCO₂/kWh) for electricity generation in California (CA) and Texas (TX).

## Data Sources

### Texas (TX)
- **Energy Data**: Annual generation by fuel type from `data/IntGenByFuel*.xlsx` files
- **Emission Factors**: Life-cycle greenhouse gas emissions from [Wikipedia](https://en.wikipedia.org/wiki/Life-cycle_greenhouse_gas_emissions_of_energy_sources)
- **Data Format**: JSON files (`data.summary.json`, `gco2_per_kwh.json`)

### California (CA)
- **Energy Data**: Daily supply trends from `data/supply_trend/*.csv` files
- **Emission Data**: Daily CO₂ emissions from `data/co2_per_resource/*.csv` files
- **Data Format**: CSV files with 5-minute interval data

## Methodology

### Daily System Intensity (CA only)
$$
gCO₂/kWh_{daily} = \frac{\text{Total CO₂ (g)}}{\text{Total Energy (MWh)} \times 1000}
$$

### Daily Resource-Specific Intensity (CA only)
$$
gCO₂/kWh_{res, daily} = \frac{\text{CO₂ (g)}_{res}}{\text{Energy (MWh)}_{res} \times 1000}
$$

### Annual Weighted Intensity (Both CA and TX)
$$
gCO₂/kWh_{annual} = \frac{\sum \text{CO₂ (g)}_{daily}}{\sum \text{Energy (MWh)}_{daily} \times 1000}
$$

The annual value is **generation-weighted**, not a simple average of daily intensities.

## Environment Setup

### Using uv (recommended)
```bash
# Install dependencies and create virtual environment
uv sync

# Run scripts
uv run python ca/data_proc.py
uv run python tx/data_proc.py
```

### Using pip
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pandas openpyxl

# Run scripts
python ca/data_proc.py
python tx/data_proc.py

# Deactivate when done
deactivate
```

## Usage

### Texas
```bash
cd tx
python data_proc.py
```
Output: `annual_system_intensity.csv` with columns `year, weighted_gco2_per_kwh`

### California
```bash
cd ca
python data_proc.py
```
Output: `annual_system_intensity.csv` with columns `year, weighted_gco2_per_kwh`

## Output Format

Both scripts generate `annual_system_intensity.csv` containing:
- `year`: Calendar year
- `weighted_gco2_per_kwh`: Generation-weighted greenhouse gas intensity in grams CO₂ per kWh