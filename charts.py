import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data import ACOES

CORES = {
    "VALE3.SA": "#1565C0",
    "ITUB4.SA": "#E65100",
    "BBAS3.SA": "#2E7D32",
}

LAYOUT_BASE = dict(
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font=dict(color="#cdd6f4", family="Inter, sans-serif"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
    margin=dict(l=50, r=20, t=50, b=50),
    xaxis=dict(gridcolor="#313244", showgrid=True),
    yaxis=dict(gridcolor="#313244", showgrid=True),
)


def grafico_cotacoes(dados: dict[str, pd.DataFrame]) -> str:
    fig = go.Figure()
    for ticker, df in dados.items():
        dates = list(df.index)
        closes = [float(v) for v in df["Close"].values]
        fig.add_trace(go.Scatter(
            x=dates,
            y=closes,
            name=ACOES[ticker],
            line=dict(color=CORES[ticker], width=2),
            hovertemplate="%{x}<br>R$ %{y:.2f}<extra>" + ACOES[ticker] + "</extra>",
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        title="Cotação — Preço de Fechamento (R$)",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def grafico_performance(dados: dict[str, pd.DataFrame]) -> str:
    fig = go.Figure()
    for ticker, df in dados.items():
        closes = [float(v) for v in df["Close"].values]
        base = closes[0]
        perf = [(p / base - 1) * 100 for p in closes]
        fig.add_trace(go.Scatter(
            x=list(df.index),
            y=perf,
            name=ACOES[ticker],
            line=dict(color=CORES[ticker], width=2),
            hovertemplate="%{x}<br>%{y:.2f}%<extra>" + ACOES[ticker] + "</extra>",
        ))
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.3)")
    fig.update_layout(
        **LAYOUT_BASE,
        title="Performance Acumulada em 2025 (%)",
        yaxis_title="Variação (%)",
        hovermode="x unified",
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def grafico_volume(dados: dict[str, pd.DataFrame]) -> str:
    fig = go.Figure()
    for ticker, df in dados.items():
        volumes = [float(v) for v in df["Volume"].values]
        fig.add_trace(go.Bar(
            x=list(df.index),
            y=volumes,
            name=ACOES[ticker],
            marker_color=CORES[ticker],
            opacity=0.8,
            hovertemplate="%{x}<br>%{y:,.0f}<extra>" + ACOES[ticker] + "</extra>",
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        title="Volume Negociado Diário",
        yaxis_title="Volume",
        barmode="group",
        hovermode="x unified",
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)
