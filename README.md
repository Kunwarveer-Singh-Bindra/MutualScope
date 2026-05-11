# MutualScope

MutualScope is a modern, fintech-style mutual fund analytics platform. It provides deep performance tracking, risk assessment, holding breakdowns, and AI-driven insights to help users analyze mutual funds like a pro. 

Inspired by modern investing platforms, MutualScope delivers a clean, data-rich interface for actionable financial intelligence.

## ✨ Features

- **Comprehensive Analytics**: View detailed mutual fund metrics including 3Y CAGR, Sharpe Ratio, Standard Deviation (Volatility), and Max Drawdown.
- **AI Analyst Insights**: Get automated, machine-learning-driven evaluations on fund momentum and portfolio optimization.
- **Fund Comparison**: Side-by-side comparison of multiple mutual funds with metric matrixes and sector concentration analysis.
- **Visual Dashboards**: Interactive NAV charts, sector allocation donuts, and drawdown visualization.
- **Live Holdings & Market Intel**: Fetches real-time equity/debt holdings, credit ratings, and curated market news.
- **Modern Fintech UI**: A sleek, dark-themed responsive UI built with Tailwind CSS, featuring glassmorphism and bento-grid layouts.
- **Dockerized Deployment**: Separate Docker containers for the API and Web services for easy, reproducible deployments.

## 📂 Project Structure

```text
mutualscope/
├── analytics/           # Financial metric calculations (CAGR, Sharpe, Drawdown)
│   └── metrics.py
├── api/                 # FastAPI backend serving JSON endpoints
│   └── main.py
├── data/                # Data ingestion pipelines
│   ├── fetcher.py       # Core fund data fetcher (mFdata API integration)
│   ├── holdings.py      # Extracts and processes fund portfolio holdings
│   └── news.py          # Fetches related financial news
├── llm/                 # AI Analyst integration (Gemini)
│   └── analyst.py
├── src/                 # Visualization generators
│   └── charts.py        # Generates NAV, Drawdown, and Sector graphs
├── web/                 # Web application (Flask frontend)
│   ├── app.py           # Main web server
│   ├── static/          # Styles, scripts, and generated chart images
│   └── templates/       # HTML templates (index, fund, compare, base)
├── Dockerfile.api       # Docker config for the FastAPI backend
├── Dockerfile.web       # Docker config for the Flask web frontend
├── .dockerignore        # Files excluded from Docker builds
├── .env.example         # Template for required environment variables
├── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker (optional, for containerized deployment)

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kunwarveer-Singh-Bindra/MutualScope.git
   cd MutualScope
   ```

2. **Create your environment file:**
   ```bash
   cp .env.example .env
   ```
   Fill in your API keys in `.env`:
   - `GEMINI_KEY` — Google Gemini API key (for AI analyst)
   - `SERP_API_KEY` — SerpAPI key (for market news)
   - `SERP_API_ENDPOINT` — SerpAPI endpoint URL

3. **Install dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   # source .venv/bin/activate   # Linux/Mac
   pip install -r requirements.txt
   ```

### Running Locally

**API server (FastAPI):**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```
Access the API at `http://localhost:8000`

**Web frontend (Flask):**
```bash
python web/app.py
```
Access the UI at `http://localhost:5000`

### Running with Docker

**Build and run the API:**
```bash
docker build -f Dockerfile.api -t mutualscope-api .
docker run -p 8000:8000 --env-file .env mutualscope-api
```

**Build and run the Web frontend:**
```bash
docker build -f Dockerfile.web -t mutualscope-web .
docker run -p 5000:5000 --env-file .env mutualscope-web
```

## 🛠️ Usage
- **Search:** Enter a mutual fund scheme code (e.g., `120503`) on the landing page to load the dashboard.
- **Analyze:** Review the AI insights, historical risk metrics, and top asset holdings on the fund page.
- **Compare:** Navigate to the comparison tool (e.g., `/compare?scheme_codes=120503,122640`) to evaluate two funds head-to-head.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 

## 📜 License
This project is licensed under the MIT License.
