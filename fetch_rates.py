import requests
import json
import os
from datetime import datetime

# Get today's date in YYYY-MM-DD format
today_date = datetime.now().strftime('%Y-%m-%d')

# Fetch the raw lowercase data from fawazahmed0's Cloudflare fallback
response = requests.get("https://latest.currency-api.pages.dev/v1/currencies/usd.json")
data = response.json()
rates = data["usd"]

# Create directories for both today's date and a "latest" fallback
date_path = f"api/{today_date}"
latest_path = "api/latest"
os.makedirs(date_path, exist_ok=True)
os.makedirs(latest_path, exist_ok=True)

for from_curr in rates:
    from_curr_upper = from_curr.upper()
    converted_rates = {}
    
    if rates[from_curr] == 0:
        continue
        
    for to_curr, to_rate in rates.items():
        to_curr_upper = to_curr.upper()
        converted_rates[to_curr_upper] = to_rate / rates[from_curr]

    output_data = {
        from_curr_upper: converted_rates
    }

    # Save to the dated folder (e.g., api/2026-09-27/USD.json)
    with open(f"{date_path}/{from_curr_upper}.json", "w") as f:
        json.dump(output_data, f, separators=(',', ':'))
        
    # Save to the latest folder (e.g., api/latest/USD.json)
    with open(f"{latest_path}/{from_curr_upper}.json", "w") as f:
        json.dump(output_data, f, separators=(',', ':'))

print(f"Successfully generated historical files for {today_date}.")
