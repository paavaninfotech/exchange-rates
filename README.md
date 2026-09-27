# 💱 ERPNext Custom Exchange Rates API

A fully free, zero-maintenance, static JSON API for daily and historical currency exchange rates. 

This repository automatically fetches exchange rates for over 200 global currencies (including cryptocurrencies) every day, calculates all cross-rates, and formats the output with **UPPERCASE ISO currency codes** to provide out-of-the-box compatibility with **ERPNext's Custom Currency Exchange Provider**.

## ✨ Features
* **100% Free:** No API keys, no subscriptions, no rate limits.
* **ERPNext Ready:** Currencies are formatted in UPPERCASE (e.g., `USD`, `INR`, `EUR`) allowing ERPNext to match them natively without server scripts.
* **200+ Currencies:** Covers fiat currencies, major cryptocurrencies, and precious metals.
* **Historical Data:** Supports ERPNext's `{transaction_date}` variable to pull accurate past rates for backdated invoices.
* **Blazing Fast:** Served globally via GitHub Pages / jsDelivr CDN.
* **Automated:** Updates automatically every day at Midnight UTC via GitHub Actions.

---

## 🔗 Endpoints & URL Structure

The endpoints support `HTTP GET` and return minified JSON.

### 1. Latest Exchange Rates
Get the most recent exchange rates for a base currency.

**URL Format:**  
`https://paavaninfotech.github.io/exchange-rates/api/latest/{CURRENCY}.json`

**Example (USD Base):**  
`https://paavaninfotech.github.io/exchange-rates/api/latest/USD.json`

### 2. Historical Exchange Rates
Get exchange rates for a specific past date (Format: `YYYY-MM-DD`). 
*(Note: Only dates from the time you started backfilling/running the action will be available).*

**URL Format:**  
`https://paavaninfotech.github.io/exchange-rates/api/{YYYY-MM-DD}/{CURRENCY}.json`

**Example (USD Base on Jan 15, 2026):**  
`https://paavaninfotech.github.io/exchange-rates/api/2026-01-15/USD.json`

---

## ⚙️ How to Configure in ERPNext

Because this API uses uppercase keys and date folders, you can set it up in ERPNext entirely from the user interface—no custom apps or server scripts required.

1. Log into ERPNext and search for **Currency Exchange Settings**.
2. Uncheck **Disabled** (if checked).
3. Set **Service Provider** to `Custom`.
4. Fill in the fields exactly as follows:

| Field | Value to Enter |
| :--- | :--- |
| **API Endpoint** | `https://paavaninfotech.github.io/exchange-rates/api/{transaction_date}/{from_currency}.json` |
| **Result Key** | `{from_currency}.{to_currency}` |
| **Access Key** | *(Leave completely blank)* |
| **Parameters** | *(Leave completely blank)* |

5. **Save** the settings.

### How ERPNext uses this:
If you create a Sales Invoice on `2026-05-12` requiring a conversion from `USD` to `INR`, ERPNext will automatically make a GET request to:
`https://.../api/2026-05-12/USD.json`
It will then parse the response using the Result Key `USD.INR` to extract the correct rate (e.g., `83.50`).

---

## 💻 Generic Developer Usage

You can easily use this API outside of ERPNext in any application. 

### JSON Response Format
```json
{
  "USD": {
    "EUR": 0.9234,
    "INR": 83.5120,
    "GBP": 0.7891,
    "BTC": 0.000015
  }
}
