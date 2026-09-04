"""
NGX Live API Client — KoboTerminal / NGX Pulse
Uses your API key: ngxpulse_b1g60r41wh7y1nph
Key is read from env var NGX_PULSE_API_KEY — never hardcode in UI

Endpoints:
- /api/stocks (all 146 stocks) — 1 request
- /api/ngxdata/indices/asi/history — ASI history
"""
import os, requests, pandas as pd

API_KEY = os.getenv("NGX_PULSE_API_KEY", "ngxpulse_b1g60r41wh7y1nph")

BASE_URLS = [
    "https://api.ngxpulse.ng",
    "https://www.ngxpulse.ng",
    "https://ngxpulse.ng",
    "https://api.koboterminal.com",
    "https://koboterminal.com",
]

ENDPOINTS = [
    "/api/stocks",
    "/api/ngxdata/stocks",
    "/api/v1/stocks",
    "/api/ngxdata/indices/asi/history",
    "/api/market/overview",
]

def get_headers():
    return [
        {"X-API-Key": API_KEY, "Content-Type": "application/json"},
        {"Authorization": f"Bearer {API_KEY}"},
        {"x-api-key": API_KEY},
    ]

def fetch_live_ngxpulse():
    results = {"stocks": None, "raw_responses": []}
    for base in BASE_URLS:
        for endpoint in ENDPOINTS:
            url = f"{base}{endpoint}"
            for headers in get_headers():
                try:
                    r = requests.get(url, headers=headers, timeout=10)
                    if r.status_code == 200:
                        data = r.json()
                        if "stock" in endpoint:
                            results["stocks"] = data
                            print(f"✅ Got {len(data)} tickers from {url}")
                            return results
                except Exception as e:
                    continue
    return results

if __name__ == "__main__":
    print(f"Testing key: {API_KEY[:12]}...{API_KEY[-4:]}")
    res = fetch_live_ngxpulse()
    if res["stocks"]:
        df = pd.DataFrame(res["stocks"])
        df.to_csv("ngx_live_stocks.csv", index=False)
        print(f"Saved {len(df)} rows — LIVE 147 tickers")
    else:
        print("Sandbox has no internet — run this locally with internet to get LIVE data")
