from flask import Flask, jsonify, render_template

from charts import grafico_cotacoes, grafico_performance, grafico_volume
from data import buscar_dados, calcular_resumo

app = Flask(__name__)


@app.route("/")
def index():
    dados = buscar_dados()
    resumo = calcular_resumo(dados)
    return render_template(
        "index.html",
        resumo=resumo,
        chart_cotacoes=grafico_cotacoes(dados),
        chart_performance=grafico_performance(dados),
        chart_volume=grafico_volume(dados),
    )


@app.route("/api/dados")
def api_dados():
    dados = buscar_dados()
    return jsonify({
        ticker: df.to_dict() for ticker, df in dados.items()
    })


@app.route("/atualizar")
def atualizar():
    import os
    cache = os.path.join(os.path.dirname(__file__), "cache", "dados.json")
    if os.path.exists(cache):
        os.remove(cache)
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)
