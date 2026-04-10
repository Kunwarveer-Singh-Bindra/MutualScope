import requests
import pandas as pd


def get_all_funds():
    amfi_url = "https://www.amfiindia.com/spages/NAVAll.txt"
    response = requests.get(amfi_url, timeout=10)

    if response.status_code == 200:
        data = response.text
        return data
    else:
        return None


def build_dataframe(raw_data: str):
    rows = []

    for line in raw_data.strip().split('\n'):
        parts = line.split(";")
        if len(parts) < 4 or parts[0] == "Scheme Code":
            continue

        scheme_code = parts[0].strip()
        if scheme_code.isdigit():
            scheme_code = int(scheme_code)
        scheme_name = parts[3].strip()
        rows.append({
            "scheme_code": scheme_code,
            "scheme_name": scheme_name
        })

    df = pd.DataFrame(rows)
    return df

def get_nav_history(scheme_code: int):
    mfapi_url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(mfapi_url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            return {
                "nav_history": data["data"],
                "fund_name": data["meta"]["scheme_name"]
            }
    print(f"Failed to fetch NAV history for {scheme_code}")
    return None

def build_nav_dataframe(nav_history: list):
    for data_dict in nav_history:
        data_dict['nav'] = float(data_dict.get('nav', 0))
    df = pd.DataFrame(nav_history)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df = df.set_index("date")
    df = df.sort_index(ascending=True)
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df = df.dropna(subset=["nav"])
    df = df[df["nav"] > 0]
    return df

def search_funds(query: str):
    raw = get_all_funds()
    if not raw:
        return []
    df = build_dataframe(raw)
    results = df[df["scheme_name"].str.contains(query, case=False, na=False)]
    return results.head(5).to_dict(orient="records")