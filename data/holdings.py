import requests

url = "https://mfdata.in"

def extract_family_id(scheme_code: int):
    try:
        response = requests.get(f"{url}/api/v1/schemes/{scheme_code}")
        if response.status_code == 200:
            data = response.json()
            return data['data'].get("family_id")
    except Exception as e:
        print(f"Error fetching family ID for {scheme_code}: {e}")
    return None

def extract_stock_list(family_id: int):
    try:
        response = requests.get(f"{url}/api/v1/families/{family_id}/holdings")
        if response.status_code == 200:
            data = response.json()
            holdings_data = data.get("data", {})

            equity_holdings = holdings_data.get("equity_holdings", [])
            if equity_holdings:
                return equity_holdings

            debt_holdings = holdings_data.get("debt_holdings", [])
            if debt_holdings:
                return debt_holdings

            return holdings_data.get("other_holdings", [])
    except Exception as e:
        print(f"Error fetching stock list for family ID {family_id}: {e}")
    return []

def sector_allocation(family_id: int):
    try:
        response = requests.get(f"{url}/api/v1/families/{family_id}/sectors")
        if response.status_code == 200:
            data = response.json()
            return data["data"]
    except Exception as e:
        print(f"Error fetching sector allocation for family ID {family_id}: {e}")
    return []


def fetch_compare_data(scheme_code_1: int, scheme_code_2: int):
    try:
        response = requests.get(
            f"{url}/api/v1/compare",
            params={"scheme_codes": f"{scheme_code_1},{scheme_code_2}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching compare data for {scheme_code_1}, {scheme_code_2}: {e}")
    return {}