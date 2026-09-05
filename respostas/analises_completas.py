import pandas as pd
import numpy as np

CSV = "/home/alixandremz/lighthouse/1-lh_nautical_csv"
OUT = "/home/alixandremz/lighthouse/respostas"

orders = pd.read_csv(f"{CSV}/orders.csv", parse_dates=["placed_at"])
oi = pd.read_csv(f"{CSV}/order_items.csv")
pv = pd.read_csv(f"{CSV}/product_variants.csv")
prod = pd.read_csv(f"{CSV}/products.csv")
customers = pd.read_csv(f"{CSV}/customers.csv")
returns = pd.read_csv(f"{CSV}/returns.csv")
rit = pd.read_csv(f"{CSV}/return_items.csv")

STATUS_V = ["paid", "confirmed"]

# ---------- dataset unificado de itens com produto e pedido ----------
it = oi.merge(pv[["id", "product_id", "cost_price"]], left_on="product_variant_id", right_on="id", how="left", suffixes=("", "_pv")).drop(columns=["id_pv"])
it = it.merge(orders[["id", "customer_id", "status", "channel", "placed_at"]], left_on="order_id", right_on="id", how="left", suffixes=("", "_o")).drop(columns=["id_o"])
it = it.merge(prod[["id", "category_id", "name", "brand_id"]], left_on="product_id", right_on="id", how="left", suffixes=("", "_p")).drop(columns=["id_p"])

# Proteção contra linhas sem pedido/produto (dados consistentes neste caso)
assert it["customer_id"].notna().all() and it["category_id"].notna().all()

it["cost_total"] = it["quantity"] * it["cost_price"].fillna(0)
it["profit"] = it["line_total"] - it["cost_total"]

eff = it[it["status"].isin(STATUS_V)]  # vendas efetivas

# =====================================================================
# Q4 - Análise de clientes (fiel/elite)
# =====================================================================
tot = orders.groupby("customer_id")["total"].sum().rename("faturamento")
freq = orders.groupby("customer_id")["id"].count().rename("frequencia")
div = eff.groupby("customer_id")["category_id"].nunique().rename("diversidade")
if tot.shape[0] == freq.shape[0]:
    metricas = pd.concat([tot, freq, div], axis=1).rename_axis("customer_id")
else:
    metricas = pd.DataFrame({"customer_id": tot.index}).merge(tot.rename("faturamento"), on="customer_id", how="left") \
        .merge(freq.rename("frequencia"), on="customer_id", how="left") \
        .merge(div.rename("diversidade"), on="customer_id", how="left").set_index("customer_id")
metricas["ticket"] = metricas["faturamento"] / metricas["frequencia"]
print("nulos em metricas:", metricas.isna().sum().sum(), "| freq vs tot idx equal:", metricas.index.equals(tot.index.sort_values()) if False else "n/a")

elite = metricas[metricas["diversidade"] >= 13].sort_values(["ticket", "customer_id"], ascending=[False, True])
top10 = elite.head(10)
print("Elite (>=13 categorias):", len(elite), "clientes")
print("TOP 10 clientes elite:")
top10_export = top10.reset_index()
print(top10_export.to_string())

# categoria com maior soma de itens no grupo top10
cat_qty = eff[eff["customer_id"].isin(top10.index)].groupby("category_id")["quantity"].sum()
cat_id = cat_qty.idxmax()
cat_name = prod.loc[prod["id"] == cat_id, "name"].iloc[0]
print(f"\nCategoria com maior quantidade de itens no Top10: category_id={cat_id} -> {int(cat_qty.max())} itens")
top10_export.to_csv(f"{OUT}/q4_top10_clientes.csv", index=False)

# =====================================================================
# Prejuízo por produto (devoluções completas) - alvo dashboard Q4
# =====================================================================
ri = rit.rename(columns={"order_item_id": "order_item_id"})
ri = ri.merge(oi[["id", "product_variant_id"]].rename(columns={"id": "oi_id"}), left_on="order_item_id", right_on="oi_id", how="left")
ri = ri.merge(returns[["id", "status", "reason"]].rename(columns={"id": "return_ref", "status": "status_r", "reason": "reason_r"}),
              left_on="return_id", right_on="return_ref", how="left")
ri = ri[ri["status_r"] == "completed"]
ri = ri.merge(pv[["id", "product_id"]].rename(columns={"id": "pv2_id"}), left_on="product_variant_id", right_on="pv2_id", how="left")
ri = ri.merge(prod[["id", "name"]].rename(columns={"id": "p2_id"}), left_on="product_id", right_on="p2_id", how="left")
ri["refund"] = ri["quantity"] * ri["unit_refund_amount"]

prej = ri.groupby(["product_id", "name"]).agg(refund_total=("refund", "sum"), n_devolucoes=("return_id", "size"),
                                              motivo_principal=("reason_r", lambda s: s.mode().iloc[0] if s.mode().shape[0] else "")).reset_index()
prej = prej.sort_values("refund_total", ascending=False)
print("\n=== Ranking PREJUÍZO por produto (top 10) ===")
print(prej.head(10).to_string(index=False))
prej.to_csv(f"{OUT}/q_prejuizo_produto.csv", index=False)

# =====================================================================
# Lucro acumulado por cliente (dashboard Q5)
# =====================================================================
cust = eff.groupby("customer_id")[["line_total", "cost_total", "profit"]].sum().reset_index()
cust = cust.merge(customers[["id", "legal_name", "person_type"]], left_on="customer_id", right_on="id", how="left").drop(columns=["id"])
cust = cust.sort_values("profit", ascending=False)
print("\n=== TOP 10 CLIENTES por LUCRO acumulado ===")
print(cust.head(10).to_string(index=False))
cust.head(20).to_csv(f"{OUT}/q_lucro_clientes.csv", index=False)

# =====================================================================
# Recorrência / vendas por mês e categoria (dashboard)
# =====================================================================
eff["mes"] = eff["placed_at"].dt.to_period("M").astype(str)
serie_mensal = eff.groupby("mes")["line_total"].sum().reset_index()
serie_mensal.to_csv(f"{OUT}/q_serie_receita.csv", index=False)

cat_rev = eff.groupby("category_id")["line_total"].sum().reset_index()
cats = pd.read_csv(f"{CSV}/categories.csv")[["id", "name"]]
cat_rev = cat_rev.merge(cats, left_on="category_id", right_on="id", how="left").drop(columns=["id"])
cat_rev["name"] = cat_rev["name"].astype(str)
cat_rev = cat_rev.sort_values("line_total", ascending=False)
print("\n=== Receita por categoria (top 10) ===")
print(cat_rev.head(10).to_string(index=False))
cat_rev.to_csv(f"{OUT}/q_receita_categoria.csv", index=False)

print("\nfeito")