import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERP_API_KEY")
api_url = os.getenv("SERP_API_ENDPOINT", "https://serpapi.com/search")


def format_news(raw_news):
    formatted = []

    for item in raw_news[:5]:
        formatted.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "source": item.get("source"),
            "published_at": item.get("date")
        })

    return formatted


def fetch_news(query: str):
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key
    }

    try:
        response = requests.get(api_url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()
        return data.get("news_results", [])

    except Exception as e:
        print("News fetch error:", e)
        return []


def get_global_market_news():
    raw = fetch_news("global stock market")
    return format_news(raw)


def get_indian_market_news():
    raw = fetch_news("indian stock market")
    return format_news(raw)


def get_fund_news(scheme_name: str):
    query = f"{scheme_name} mutual fund"
    raw = fetch_news(query)
    return format_news(raw)