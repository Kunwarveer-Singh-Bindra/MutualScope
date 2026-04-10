from data.fetcher import get_nav_history, build_nav_dataframe
import pandas as pd
import numpy as np


def get_daily_returns(df):
    df["Daily_Return"] = df["nav"].pct_change()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna().copy()
    return df


def get_volatility(daily_returns):
    volatility = daily_returns.std() * np.sqrt(252)
    return volatility


def get_sharpe(daily_returns):
    RISK_FREE_RATE = 0.065
    daily_rf = RISK_FREE_RATE / 252
    excess = daily_returns - daily_rf
    return (excess.mean() / excess.std()) * np.sqrt(252)


def get_max_drawdown(daily_returns):
    return float(get_drawdown_series(daily_returns).min())


def get_cagr(df):
    start_nav = df["nav"].iloc[0]
    end_nav = df["nav"].iloc[-1]
    years = (df.index[-1] - df.index[0]).days / 365.25
    return (end_nav / start_nav) ** (1 / years) - 1


def get_drawdown_series(daily_returns):
    cumulative = (1 + daily_returns).cumprod()
    rolling_max = cumulative.cummax()
    return (cumulative / rolling_max - 1)


def get_health_score(cagr, sharpe, max_drawdown) -> float:
    score = (0.4 * sharpe) + (0.3 * (1 + max_drawdown)) + (0.3 * cagr)
    return round(min(max(score * 100, 0), 100), 2)


def get_all_metrics(scheme_code: int) -> dict:
    raw = get_nav_history(scheme_code)
    if not raw or "nav_history" not in raw:
        return {}

    df = build_nav_dataframe(raw["nav_history"])
    daily_returns = df["nav"].pct_change().dropna()

    cagr = get_cagr(df)
    sharpe = get_sharpe(daily_returns)
    max_dd = get_max_drawdown(daily_returns)
    volatility = get_volatility(daily_returns)

    return {
        "scheme_code": scheme_code,
        "fund_name": raw["fund_name"],
        "latest_nav": float(df["nav"].iloc[-1]),
        "cagr": float(cagr),
        "volatility": float(volatility),
        "sharpe": float(sharpe),
        "max_drawdown": float(max_dd),
        "health_score": get_health_score(
            cagr,
            sharpe,
            max_dd
        )
    }
