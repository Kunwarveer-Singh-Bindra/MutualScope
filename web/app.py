from flask import Flask, render_template, request, redirect, url_for
import requests
from src.charts import generate_nav_chart, generate_drawdown_chart, generate_sector_chart
from data.news import get_global_market_news, get_fund_news, get_indian_market_news
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('scheme_code')

        if query and query.isdigit():
            return redirect(url_for('fund', scheme_code=query))

        if query:
            # call FastAPI search
            url = f"http://127.0.0.1:8000/search?query={query}"
            response = requests.get(url)

            results = response.json() if response.status_code == 200 else []

            return render_template("index.html", results=results)

    return render_template("index.html")

@app.route('/fund/<int:scheme_code>')
def fund(scheme_code):
    url = f"http://127.0.0.1:8000/metrics/{scheme_code}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error fetching data from API"

    data = response.json()
    if "metrics" not in data:
        return "Invalid API response"

    nav_chart = generate_nav_chart(scheme_code)
    drawdown_chart = generate_drawdown_chart(scheme_code)
    sector_chart = generate_sector_chart(scheme_code)
    data = response.json()

    fund_name = data['metrics']['fund_name']
    global_news = get_global_market_news()
    fund_news = get_fund_news(fund_name)
    indian_news = get_indian_market_news()
    holdings = data.get("holdings", [])
    return render_template(
        "fund.html",
        metrics=data['metrics'],
        analyst_note=data['analyst_note'],
        scheme_code=scheme_code,
        nav_chart=nav_chart,
        drawdown_chart=drawdown_chart,
        global_news=global_news,
        fund_news=fund_news,
        indian_news = indian_news,
        holdings = holdings,
        sector_chart=sector_chart
    )

@app.route('/compare', methods=['GET', 'POST'])
def compare_funds():
    if request.method == 'POST':
        code1 = request.form.get("scheme_code_1", "").strip()
        code2 = request.form.get("scheme_code_2", "").strip()
        scheme_code_1 = int(code1)
        scheme_code_2 = int(code2)

        charts_a = {
            "nav": generate_nav_chart(scheme_code_1),
            "drawdown": generate_drawdown_chart(scheme_code_1),
            "sector": generate_sector_chart(scheme_code_1),
        }
        charts_b = {
            "nav": generate_nav_chart(scheme_code_2),
            "drawdown": generate_drawdown_chart(scheme_code_2),
            "sector": generate_sector_chart(scheme_code_2),
        }

        if not (code1.isdigit() and code2.isdigit()):
            return render_template("compare.html", error="Enter valid numeric scheme codes.")

        url = f"http://127.0.0.1:8000/compare?scheme_code_1={code1}&scheme_code_2={code2}"
        response = requests.get(url)
        payload = response.json() if response.status_code == 200 else {}

        if "error" in payload:
            return render_template("compare.html", error=payload["error"])

        return render_template("compare.html", compare_data=payload, code1=code1, code2=code2,
                               charts_a=charts_a, charts_b=charts_b)


    return render_template("compare.html")


if __name__ == '__main__':
    app.run(debug=True)