"""
Questão 6 - Previsão de demanda (LH Nautical)

Produto: 'Bússola de Bordo 702'
Baseline: média móvel dos 3 meses anteriores (sem lookahead - usa apenas
dados anteriores à data prevista).
Treino: até 31/12/2025 | Teste: 1º trimestre de 2026 | Base: mensal
Métrica: MAE (Mean Absolute Error)

Premissas:
- considera como venda efetiva os pedidos com status paid/confirmed
  (cancelled/draft não geraram receita);
- o produto possui duas variantes ativas (147 e 148), unificadas no dataset;
- unidades = SUM(quantity).
"""

import pandas as pd
import numpy as np

CSV = "/home/alixandremz/lighthouse/1-lh_nautical_csv"
PROD_NAME = "Bússola de Bordo 702"
STATUS_VENDA = ["paid", "confirmed"]  # vendas efetivas

# ---------------------------------------------------------------------------
# 1) Dataset unificado: products + product_variants + order_items + orders
# ---------------------------------------------------------------------------
products = pd.read_csv(f"{CSV}/products.csv")
variants = pd.read_csv(f"{CSV}/product_variants.csv")
items = pd.read_csv(f"{CSV}/order_items.csv")
orders = pd.read_csv(f"{CSV}/orders.csv", parse_dates=["placed_at"])

prod = products[products["name"] == PROD_NAME]
prod_ids = set(prod["id"])
var_ids = set(variants[variants["product_id"].isin(prod_ids)]["id"])

it = items[items["product_variant_id"].isin(var_ids)].merge(
    orders[["id", "placed_at", "status"]], left_on="order_id", right_on="id"
)

# une variante -> produto (para cruzar pelo product_id) e confirmar o produto-alvo
unified = it.merge(
    variants[["id", "product_id"]], left_on="product_variant_id", right_on="id",
    suffixes=("", "_var"),
)
unified = unified[["product_variant_id", "product_id", "placed_at", "status", "quantity"]]
unified = unified[unified["product_id"].isin(prod_ids)]

# ---------------------------------------------------------------------------
# 2) Série mensal de vendas (unidades) - vendas efetivas
# ---------------------------------------------------------------------------
unified = unified[unified["status"].isin(STATUS_VENDA)]
unified["month"] = unified["placed_at"].dt.to_period("M")

monthly = (
    unified.groupby("month")["quantity"]
    .sum()
    .rename("unidades")
    .sort_index()
)

# ---------------------------------------------------------------------------
# 3) Baseline: média móvel dos 3 meses anteriores
# ---------------------------------------------------------------------------
def forecast_ma3(series, month):
    """Média móvel dos 3 meses anteriores a `month` (somente dados já conhecidos)."""
    prior = series[series.index < month]
    return float(prior.tail(3).mean())

months = monthly.index
test_months = pd.period_range("2026-01", "2026-03", freq="M")
actual = {m: float(monthly.get(m, 0.0)) for m in test_months}
pred = {m: forecast_ma3(monthly, m) for m in test_months}

result = pd.DataFrame(
    {
        "real": [float(actual[m]) for m in test_months],
        "previsao": [float(pred[m]) for m in test_months],
        "erro_abs": [abs(actual[m] - pred[m]) for m in test_months],
    },
    index=[str(m) for m in test_months],
)

mae = result["erro_abs"].mean()

# ---------------------------------------------------------------------------
# 4) Saídas
# ---------------------------------------------------------------------------
print("=== Série mensal (últimos 15 meses de treino) ===")
print((monthly[monthly.index < "2026-01"].tail(15)).astype(int).to_string())
print("\n=== Previsão mensal 1º trimestre 2026 (unidades) ===")
print(result.astype(float).round(2).to_string())
print(f"\nMAE = {mae:.2f} unidades/mês")
print(f"Vendas reais médias no trimestre: {result['real'].mean():.2f} | MAE = {100*mae/result['real'].mean():.2f}% da média real")
print(f"Volatilidade histórica (desvio-padrão mensal, 2020-2025): {monthly[monthly.index<'2026-01'].std():.2f}")