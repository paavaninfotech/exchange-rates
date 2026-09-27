import requests
import json
import os

# Using Frankfurter (ECB rates) as the free upstream data source
response = requests.get("https://api.frankfurter.app/latest")
data = response.json()

base_currency = data["base"].upper() # EUR
rates = data["rates"]

# Add the base currency to the rates list with a 1:1 ratio
rates[base_currency] = 1.0

# Create a directory to hold the JSON files
os.makedirs("api/v1", exist_ok=True)

# Generate a JSON file for EVERY currency as the base
for from_curr in rates:
    from_curr_upper = from_curr.upper()
    converted_rates = {}
    
    # Calculate cross-rates based on EUR
    for to_curr, to_rate in rates.items():
        to_curr_upper = to_curr.upper()
        converted_rates[to_curr_upper] = to_rate / rates[from_curr]

    # The JSON structure ERPNext will read
    output_data = {
        from_curr_upper: converted_rates
    }

    # Save to api/v1/USD.json, api/v1/INR.json, etc.
    file_path = f"api/v1/{from_curr_upper}.json"
    with open(file_path, "w") as f:
        json.dump(output_data, f, separators=(',', ':'))

print("Successfully generated uppercase exchange rate files.")
