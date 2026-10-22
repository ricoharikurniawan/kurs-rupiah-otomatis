import requests

url = "https://api.frankfurter.dev/v1/2026-07-01..2026-07-10"
parameter = {"base": "USD", "symbols": "IDR,EUR"}

respons = requests.get(url, params=parameter, timeout=30)
print(respons.status_code)

data = respons.json()
print(data["base"], data["start_date"], data["end_date"])
print(data["rates"]["2026-07-01"])
print(len(data["rates"]))