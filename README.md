# Painel de Ações 2025

Site em Python para acompanhar e analisar a cotação e performance de três ações brasileiras ao longo de 2025.

**Ações monitoradas:** VALE3 · ITUB4 · BBAS3

## Funcionalidades

- Cotação histórica com preço de fechamento em R$
- Performance acumulada comparativa entre as 3 ações (%)
- Volume negociado diário
- Cards com preço atual, variação do dia e variação no ano
- Cache automático de 1 hora (botão para atualizar manualmente)

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python + Flask |
| Dados | yfinance (Yahoo Finance) |
| Gráficos | Plotly |
| Frontend | Bootstrap 5 + Jinja2 |

## Como rodar

**1. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**2. Inicie o servidor:**
```bash
python app.py
```

**3. Acesse no navegador:**
```
http://localhost:5000
```

## Estrutura

```
acoes-2025/
├── app.py          # Rotas Flask
├── data.py         # Busca e cache de dados via yfinance
├── charts.py       # Geração dos gráficos Plotly
├── templates/      # HTML (Jinja2)
├── static/         # CSS
├── cache/          # Cache local dos dados (gerado automaticamente)
└── requirements.txt
```
