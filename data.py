import json
import os
import time
import warnings
from datetime import datetime

import pandas as pd
import yfinance as yf
from curl_cffi import requests as curl_requests

warnings.filterwarnings("ignore")

CACHE_FILE = "/tmp/dados.json" if os.environ.get("VERCEL") else os.path.join(os.path.dirname(__file__), "cache", "dados.json")
CACHE_TTL = 3600  # 1 hora em segundos

ACOES = {
    "VALE3.SA": "Vale",
    "ITUB4.SA": "Itaú Unibanco",
    "BBAS3.SA": "Banco do Brasil",
}

START_2025 = "2025-01-01"


def _cache_valido():
    if not os.path.exists(CACHE_FILE):
        return False
    return time.time() - os.path.getmtime(CACHE_FILE) < CACHE_TTL


def _salvar_cache(dados: dict):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True) if os.path.dirname(CACHE_FILE) else None
    with open(CACHE_FILE, "w") as f:
        json.dump(dados, f)


def _carregar_cache() -> dict:
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def buscar_dados() -> dict[str, pd.DataFrame]:
    if _cache_valido():
        raw = _carregar_cache()
        return {ticker: pd.DataFrame(v) for ticker, v in raw.items()}

    resultado = {}
    hoje = datetime.today().strftime("%Y-%m-%d")
    session = curl_requests.Session(verify=False, impersonate="chrome")

    for ticker in ACOES:
        try:
            df = yf.download(
                ticker,
                start=START_2025,
                end=hoje,
                auto_adjust=True,
                progress=False,
                session=session,
            )
        except Exception:
            df = pd.DataFrame()

        if df.empty:
            continue

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
        df.index = df.index.strftime("%Y-%m-%d")
        resultado[ticker] = df

    _salvar_cache({ticker: df.to_dict() for ticker, df in resultado.items()})
    return resultado


def calcular_resumo(dados: dict[str, pd.DataFrame]) -> list[dict]:
    resumo = []
    for ticker, df in dados.items():
        if df.empty:
            continue
        preco_atual = float(df["Close"].iloc[-1])
        preco_ontem = float(df["Close"].iloc[-2]) if len(df) > 1 else preco_atual
        preco_inicio = float(df["Close"].iloc[0])

        var_dia = preco_atual - preco_ontem
        var_dia_pct = (var_dia / preco_ontem) * 100
        var_ano_pct = ((preco_atual - preco_inicio) / preco_inicio) * 100

        resumo.append({
            "ticker": ticker,
            "nome": ACOES[ticker],
            "preco_atual": preco_atual,
            "var_dia": var_dia,
            "var_dia_pct": var_dia_pct,
            "var_ano_pct": var_ano_pct,
            "maxima": float(df["High"].max()),
            "minima": float(df["Low"].min()),
        })
    return resumo
