from data.fetcher import build_nav_dataframe, get_nav_history
import plotly.graph_objs as go
from data.holdings import extract_family_id, sector_allocation


def generate_nav_chart(scheme_code: int):
    raw = get_nav_history(scheme_code)
    if not raw or "nav_history" not in raw:
        return "<p>Data unavailable</p>"

    df = build_nav_dataframe(raw["nav_history"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["nav"],
        mode='lines',
        line=dict(color='#22c55e', width=3),
        fill='tozeroy',
        fillcolor='rgba(34,197,94,0.1)',
        name='NAV'
    ))

    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        paper_bgcolor='#0f172a',
        plot_bgcolor='#0f172a',
        margin=dict(l=20, r=20, t=40, b=20),
        title=f"NAV Trend - {scheme_code}",
        xaxis=dict(
            showgrid=False,
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )

    return fig.to_html(full_html=False)


def generate_drawdown_chart(scheme_code: int):
    from analytics.metrics import get_drawdown_series

    raw = get_nav_history(scheme_code)
    if not raw or "nav_history" not in raw:
        return "<p>Data unavailable</p>"

    df = build_nav_dataframe(raw["nav_history"])
    daily_returns = df["nav"].pct_change().dropna()
    drawdown = get_drawdown_series(daily_returns)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=drawdown.index,
        y=drawdown,
        mode='lines',
        line=dict(color='#ef4444', width=2),
        fill='tozeroy',
        fillcolor='rgba(239,68,68,0.15)',
        name='Drawdown',
    ))

    fig.update_layout(
        template='plotly_dark',
        xaxis=dict(
            showgrid=False,
            rangeslider=dict(visible=True)
        ),
        hovermode='x unified',
        paper_bgcolor='#0f172a',
        plot_bgcolor='#0f172a',
        margin=dict(l=20, r=20, t=40, b=20),
        title=f"Drawdown - {scheme_code}",
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )

    return fig.to_html(full_html=False)

def generate_sector_chart(scheme_code: int):
    family_id = extract_family_id(scheme_code)
    if not family_id:
        return "<p>Sector data unavailable</p>"

    sector_data = sector_allocation(family_id)
    if not sector_data:
        return "<p>Sector data unavailable</p>"

    # Sort sectors (best UX)
    sector_data = sorted(sector_data, key=lambda x: x["total_weight"], reverse=True)

    # Top 6 + Others (clean UI)
    top = sector_data[:6]
    others_weight = sum(s["total_weight"] for s in sector_data[6:])

    if others_weight > 0:
        top.append({
            "sector": "Others",
            "total_weight": others_weight
        })

    labels = [s["sector"] for s in top]
    values = [s["total_weight"] for s in top]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,  # donut chart
        textinfo='label+percent',
        hoverinfo='label+percent',
        marker=dict(colors=[
            "#22c55e", "#3b82f6", "#f59e0b",
            "#ef4444", "#a855f7", "#14b8a6", "#64748b"
        ])
    ))

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0f172a',
        plot_bgcolor='#0f172a',
        margin=dict(l=20, r=20, t=40, b=20),
        title=f"Sector Allocation - {scheme_code}"
    )

    return fig.to_html(full_html=False)