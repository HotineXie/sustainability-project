# Energy generated in GWh
energy_data = { 
    "2018": {"Biomass": 563, "Coal": 93249, "Gas": 23487, "Gas-CC": 143719, "Hydro": 811, "Nuclear": 41125, "Other": 29, "Solar": 3240, "Wind": 69796},
    "2019": {"Biomass": 421, "Coal": 77857, "Gas": 27379, "Gas-CC": 154391, "Hydro": 956, "Nuclear": 41314, "Other": 24, "Solar": 4398, "Wind": 76708},
    "2020": {"Biomass": 353, "Coal": 68514, "Gas": 22433, "Gas-CC": 151364, "Hydro": 639, "Nuclear": 41459, "Other": 2, "Solar": 8749, "Wind": 87090},
    "2021": {"Biomass": 434, "Coal": 74825, "Gas": 26106, "Gas-CC": 138314, "Hydro": 504, "Nuclear": 40270, "Other": 10, "Solar": 15712, "Wind": 95403},
    "2022": {"Biomass": 625, "Coal": 71501, "Gas": 29627, "Gas-CC": 153358, "Hydro": 344, "Nuclear": 41658, "Other": 570, "Solar": 24193, "WSL": -665, "Wind": 107264},
    "2023": {"Biomass": 378, "Coal": 61734, "Gas": 36418, "Gas-CC": 164008, "Hydro": 345, "Nuclear": 40746, "Other": 839, "Solar": 32402, "WSL": -1037, "Wind": 107995},
    "2024": {"Biomass": 291, "Coal": 58317, "Gas": 39821, "Gas-CC": 164568, "Hydro": 461, "Nuclear": 38733, "Other": 2331, "Solar": 48222, "WSL": -2, "Wind": 111744}
}

# gCO2/kWh factors
gco2_factors = {
    "Biomass": 230,
    "Coal": 820,
    "Gas": 490,
    "Gas-CC": 490,
    "Hydro": 12,
    "Nuclear": 8,
    "Solar": 34,
    "Wind": 10
}

average_gco2_per_year = {}

for year, resources in energy_data.items():
    total_energy_kwh = 0
    total_emissions_g = 0
    for resource, gwh in resources.items():
        if resource in gco2_factors:
            kwh = gwh * 1e6  # convert GWh -> kWh
            total_energy_kwh += kwh
            total_emissions_g += kwh * gco2_factors[resource]
    average_gco2 = total_emissions_g / total_energy_kwh if total_energy_kwh > 0 else 0
    average_gco2_per_year[year] = average_gco2

# Print result
for year, avg in average_gco2_per_year.items():
    print(f"{year}: {avg:.2f} gCO2/kWh")
