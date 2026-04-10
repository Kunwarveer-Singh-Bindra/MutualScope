from fastapi import FastAPI, Query

from analytics.metrics import get_all_metrics
from llm.analyst import get_analyst_note
from data.fetcher import search_funds
from data.holdings import extract_family_id, extract_stock_list, fetch_compare_data
app = FastAPI()

@app.get('/metrics/{scheme_code}')
def metrics(scheme_code: int):
    metric_data = get_all_metrics(scheme_code)
    if not metric_data:
        return {"error": "Invalid scheme code or data unavailable"}
    note = get_analyst_note(metric_data)
    family_id = extract_family_id(scheme_code)
    holdings = extract_stock_list(family_id) if family_id else []
    return {
        'metrics'   : metric_data,
        'analyst_note': note,
        'holdings': holdings
    }


@app.get("/search")
def search(query: str = Query(..., description="Search query for mutual funds")):
    return search_funds(query)


@app.get("/compare")
def compare(scheme_code_1: int, scheme_code_2: int):
    if not scheme_code_1 or not scheme_code_2:
        return {"error": "Both scheme codes are required"}

    raw = fetch_compare_data(scheme_code_1, scheme_code_2)

    m1 = get_all_metrics(scheme_code_1)
    m2 = get_all_metrics(scheme_code_2)

    fund_1 = {}
    fund_2 = {}

    data = raw.get("data")
    if isinstance(data, list) and len(data) >= 2:
        fund_1 = data[0]
        fund_2 = data[1]

    fund_1.update(m1)
    fund_2.update(m2)

    return {
        "fund_1": fund_1,
        "fund_2": fund_2
    }

