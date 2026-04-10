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

## 📂 Project Structure

```text
mutualscope/
├── analytics/           # Financial metric calculations (CAGR, Sharpe, Drawdown)
│   └── metrics.py
├── api/                 # API routes and data serving endpoints
│   └── main.py
├── data/                # Data ingestion pipelines
│   ├── fetcher.py       # Core fund data fetcher (mFdata API integration)
│   ├── holdings.py      # Extracts and processes fund portfolio holdings
│   └── news.py          # Fetches related financial news
├── llm/                 # AI Analyst integration
│   └── analyst.py
├── src/                 # Visualization generators
│   └── charts.py        # Generates NAV, Drawdown, and Sector graphs
├── web/                 # Web application (Flask)
│   ├── app.py           # Main web server
│   ├── static/          # Styles, scripts, and generated chart images
│   └── templates/       # HTML templates (index, fund, compare, base)
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- (Optional) Virtual environment recommended

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/mutualscope.git
   cd mutualscope
   ```

2. **Install dependencies:**
   *(Ensure you create and activate a virtual environment first)*
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have Flask, Pandas, Matplotlib, and other required libraries installed depending on your specific requirements file).*

3. **Run the Application:**
   ```bash
   python web/app.py
   ```

4. **Access the platform:**
   Open your browser and navigate to `http://localhost:5000` (or the port specified by your web runner).

## 🛠️ Usage
- **Search:** Enter a mutual fund scheme code (e.g., `120503`) on the landing page to load the dashboard.
- **Analyze:** Review the AI insights, historical risk metrics, and top asset holdings on the fund page.
- **Compare:** Navigate to the comparison tool (e.g., `/compare?scheme_codes=120503,122640`) to evaluate two funds head-to-head.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! 

## 📜 License
This project is licensed under the MIT License.

