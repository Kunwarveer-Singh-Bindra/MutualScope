import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


def get_analyst_note(metrics: dict) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        prompt = f"""You are a CFA analyst.

Given these mutual fund metrics:
CAGR: {metrics.get('cagr', 0):.2%}
Volatility: {metrics.get('volatility', 0):.2%}
Sharpe Ratio: {metrics.get('sharpe', 0):.2f}
Max Drawdown: {metrics.get('max_drawdown', 0):.2%}
Health Score: {metrics.get('health_score', 0):.2f}/100

Instructions:
- Explain risk level (low/medium/high)
- Say if returns justify risk
- Keep it simple (retail investor)
- Max 3 sentences

Answer:"""

        time.sleep(2)

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        print("LLM Error:", e)
        return "Analysis unavailable right now."
