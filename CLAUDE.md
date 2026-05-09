# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

Python is installed at a non-standard path. Always use the full executable:

```powershell
$python = "C:\Users\Marcel\AppData\Local\Programs\Python\Python312\python.exe"
cd "C:\Users\Marcel\Desktop\Projetos Claude\acoes-2025"
& $python app.py
```

Install dependencies:
```powershell
& $python -m pip install -r requirements.txt
```

The app runs at `http://localhost:5000`.

To force a data refresh without restarting the server, delete the cache file:
```powershell
Remove-Item "cache\dados.json" -ErrorAction SilentlyContinue
```

## Architecture

Three modules form the pipeline: `data.py` → `charts.py` → `app.py` → templates.

**`data.py`** — single source of truth for market data. `buscar_dados()` returns `dict[ticker, DataFrame]` with columns `Open, High, Low, Close, Volume` and date strings as the index. Data is fetched from Yahoo Finance via `yfinance` and cached to `cache/dados.json` for 1 hour. `calcular_resumo()` computes per-ticker metrics (current price, day change, YTD change, high/low) from that same dict.

**`charts.py`** — receives the dict from `buscar_dados()` and returns embeddable HTML strings (`fig.to_html(full_html=False, include_plotlyjs=False)`). Plotly JS is loaded once in `base.html` via CDN. `LAYOUT_BASE` holds the shared dark-theme config applied to all figures.

**`app.py`** — thin Flask layer. The `/` route calls both modules and passes everything to `index.html`. `/atualizar` deletes the cache file so the next page load re-fetches live data. `/api/dados` exposes raw JSON for debugging.

## GitHub

Repositório: https://github.com/marcel-magalhaes/acoes-2025

Git está configurado com `http.sslVerify=false` globalmente (necessário nesta máquina por problema de certificado SSL).

**Auto-sync:** toda vez que Claude edita um arquivo, o hook em `.claude/settings.json` commita e faz push automático para `origin master` com a mensagem `auto: update <timestamp>`. O hook usa PowerShell e roda após cada `Edit` ou `Write`.

Para push manual:
```powershell
cd "C:\Users\Marcel\Desktop\Projetos Claude\acoes-2025"
git add -A
git commit -m "mensagem"
git push origin master
```

## Key constraints

- **SSL**: Yahoo Finance fails certificate verification on this machine. `data.py` uses a `curl_cffi.requests.Session(verify=False, impersonate="chrome")` passed to `yf.download()`. Do not replace this with a plain `requests.Session` — yfinance 1.x requires curl_cffi.
- **MultiIndex columns**: yfinance 1.x returns MultiIndex columns for single-ticker downloads. `data.py` flattens them with `df.columns.get_level_values(0)` before selecting columns.
- **Tickers**: Brazilian B3 tickers require the `.SA` suffix (e.g. `VALE3.SA`). The `ACOES` dict in `data.py` maps ticker → display name and is the single place to add/remove stocks.
