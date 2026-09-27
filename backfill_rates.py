import requests
import json
import os
import time
from datetime import datetime, timedelta

# Define start date and end date
start_date = datetime(2025, 1, 1)
end_date = datetime.now()
delta = timedelta(days=1)

current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    date_path = f"api/{date_str}"
    
    # Skip if we already downloaded this date
    if os.path.exists(date_path):
        print(f"Skipping {date_str}, already exists.")
        current_date += delta
        continue
        
    url = f"https://{date_str}.currency-api.pages.dev/v1/currencies/usd.json"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {date_str} (Status: {response.status_code})")
            current_date += delta
            continue
            
        data = response.json()
        rates = data.get("usd", {})
        
        if not rates:
            current_date += delta
            continue
            
        os.makedirs(date_path, exist_ok=True)
        
        # Calculate cross rates for every currency
        for from_curr in rates:
            from_curr_upper = from_curr.upper()
            converted_rates = {}
            
            if rates[from_curr] == 0:
                continue
                
            for to_curr, to_rate in rates.items():
                converted_rates[to_curr.upper()] = to_rate / rates[from_curr]

            # Save uppercase JSON
            with open(f"{date_path}/{from_curr_upper}.json", "w") as f:
                json.dump({from_curr_upper: converted_rates}, f, separators=(',', ':'))
                
        print(f"Successfully backfilled {date_str}")
        
    except Exception as e:
        print(f"Error on {date_str}: {str(e)}")
        
    # Be polite to the API server and avoid rate limits
    time.sleep(0.5)
    
    current_date += delta

print("Backfill complete!")
