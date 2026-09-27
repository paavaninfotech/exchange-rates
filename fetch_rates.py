import requests
import json
import os

# 1. Fetch the raw lowercase data from fawazahmed0's Cloudflare fallback
# We use USD as the base to calculate all other cross-rates
response = requests.get("https://latest.currency-api.pages.dev/v1/currencies/usd.json")
data = response.json()

# The rates are nested under the 'usd' key
rates = data["usd"]

# 2. Create a directory to hold your new uppercase JSON files
os.makedirs("api/v1", exist_ok=True)

# 3. Generate an UPPERCASE JSON file for EVERY currency as the base
for from_curr in rates:
    from_curr_upper = from_curr.upper()
    converted_rates = {}
    
    # Prevent division by zero if a crypto asset has temporarily flatlined
    if rates[from_curr] == 0:
        continue
        
    # Calculate cross-rates based on the USD baseline
    for to_curr, to_rate in rates.items():
        to_curr_upper = to_curr.upper()
        # Formula: (1 / from_currency_usd_rate) * to_currency_usd_rate
        converted_rates[to_curr_upper] = to_rate / rates[from_curr]

    # Format exactly how ERPNext expects it
    output_data = {
        from_curr_upper: converted_rates
    }

    # Save to api/v1/USD.json, api/v1/INR.json, api/v1/CDF.json, etc.
    file_path = f"api/v1/{from_curr_upper}.json"
    with open(file_path, "w") as f:
        # separators=(',', ':') minifies the JSON to save bandwidth
        json.dump(output_data, f, separators=(',', ':'))

print(f"Successfully generated uppercase exchange rate files for {len(rates)} currencies.")
