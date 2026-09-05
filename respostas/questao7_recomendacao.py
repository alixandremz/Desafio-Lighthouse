"""
Questão 7 - Sistema de recomendação (LH Nautical)

Motor de recomendação baseado em similaridade de cosseno produto x produto,
usando a presença/ausência de compra dos clientes (matriz Usuário x Produto).

Vitrine: "Quem comprou isso, também levou..." para o item Motor de Popa 1949.

Premissa: considera compras efetivas (pedidos paid/confirmed); cancelled/draft
não representam posse do produto.
Bibliotecas: pandas, numpy, sklearn (cosine_similarity).
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

CSV = "/home/alixandremz/lighthouse/1-lh_nautical_csv"
STATUS_VENDA = ["paid", "confirmed"]
REFERENCIA = "Motor de Popa 1949"
TOP_N = 5

# ---------------------------------------------------------------------------
# 1) Dataset unificado de compras efetivas
# ---------------------------------------------------------------------------
orders = pd.read_csv(f"{CSV}/orders.csv")
items = pd.read_csv(f"{CSV}/order_items.csv")

compras = items.merge(
    orders[["id", "customer_id", "status"]], left_on="order_id", right_on="id"
)
compras = compras[compras["status"].isin(STATUS_VENDA)]

# variante -> produto
variants = pd.read_csv(f"{CSV}/product_variants.csv")
pv_map = variants[["id", "product_id"]].drop_duplicates()
compras = compras.merge(pv_map, left_on="product_variant_id", right_on="id",
                        suffixes=("", "_pv"))
compras = compras[["customer_id", "product_id"]].drop_duplicates()
compras["interacao"] = 1  # presença/ausência (ignora quantidade)

# ---------------------------------------------------------------------------
# 2) Matriz de interação Usuário x Produto (1=comprou, 0=não comprou)
# ---------------------------------------------------------------------------
matriz = compras.pivot_table(
    index="customer_id", columns="product_id", values="interacao", fill_value=0
)

# ---------------------------------------------------------------------------
# 3) Similaridade de cosseno produto x produto
#    (vetor de cada produto = clientes que o compraram)
# ---------------------------------------------------------------------------
sim = cosine_similarity(matriz.T)  # linhas = produtos, colunas = clientes
sim_df = pd.DataFrame(sim, index=matriz.columns, columns=matriz.columns)

products = pd.read_csv(f"{CSV}/products.csv")
ref = int(products[products["name"] == REFERENCIA]["id"].iloc[0])
rank = sim_df[ref].drop(labels=[ref]).sort_values(ascending=False).head(TOP_N)

nomes = products.set_index("id")["name"]

print(f"=== TOP {TOP_N} mais similares a '{REFERENCIA}' ===")
for pid, score in rank.items():
    print(f"{nomes[pid]:<40} cos={score:.4f}")