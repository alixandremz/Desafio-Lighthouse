import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

CSV = "/home/alixandremz/lighthouse/1-lh_nautical_csv"
OUT = "/home/alixandremz/lighthouse/respostas/dashboard"
plt.rcParams.update({
    "figure.dpi": 110, "font.family": "DejaVu Sans", "axes.grid": True,
    "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False,
})
CMAP = plt.get_cmap("Set2")

BR_REV = {"Domingo": "Domingo", "Segunda-feira": "Segunda-feira", "Terça-feira": "Terça-feira",
          "Quarta-feira": "Quarta-feira", "Quinta-feira": "Quinta-feira",
          "Sexta-feira": "Sexta-feira", "Sábado": "Sábado"}

orders = pd.read_csv(f"{CSV}/orders.csv", parse_dates=["placed_at"])
oi = pd.read_csv(f"{CSV}/order_items.csv")
pv = pd.read_csv(f"{CSV}/product_variants.csv")
prod = pd.read_csv(f"{CSV}/products.csv")

# ------------------------------------------------------------------ 1
# Vendas médias por dia da semana (lojas físicas, com dias sem venda)
# ------------------------------------------------------------------
pos = orders[orders["channel"] == "pos"].copy()
pos["d"] = pos["placed_at"].dt.normalize()
cal = pd.date_range(pos["d"].min(), pos["d"].max(), freq="D")
weekday = {0:"Domingo",1:"Segunda-feira",2:"Terça-feira",3:"Quarta-feira",4:"Quinta-feira",5:"Sexta-feira",6:"Sábado"}
daily = pos.groupby("d")["total"].sum()
wd_media = {}
for d in cal:
    w = weekday[d.weekday()]
    wd_media[w] = wd_media.get(w, [0, 0])
    wd_media[w][0] += 1                  # dias abertos
    wd_media[w][1] += float(daily.get(d, 0.0))  # faturamento (0 p/ dia sem venda)
rows = sorted(((nome, d[0], d[1] / d[0]) for nome, d in wd_media.items()), key=lambda r: r[2])
df_wd = pd.DataFrame(rows, columns=["dia_semana", "dias_abertos", "media"])
fig, ax = plt.subplots(figsize=(9, 4.6))
bar = ax.barh(df_wd["dia_semana"], df_wd["media"] / 1e3, color=CMAP(0.4))
ax.set_xlabel("Média de vendas (R$ mil/dia)")
ax.set_title("Média de vendas por dia da semana — lojas físicas (2020-2026)\nconsiderando TODOS os dias do calendário (dias sem venda = 0)")
for i, v in enumerate(df_wd["media"] / 1e3):
    ax.text(v + 2, i, f"R${v/1000:.1f} mil" if v > 1000 else f"{v:.1f}k", va="center")
pior = df_wd.iloc[0]
bar[0].set_color("crimson")
ax.text(0.98, 0.02, f"Pior dia: {pior['dia_semana']} (R${pior['media']/1000:.1f} mil)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=9, color="crimson")
plt.tight_layout(); plt.savefig(f"{OUT}/1_dia_semana.png"); plt.close()

# ------------------------------------------------------------------ 2
# Ranking de prejuízo por produto (devoluções completas)
# ------------------------------------------------------------------
prej = pd.read_csv("/home/alixandremz/lighthouse/respostas/q_prejuizo_produto.csv").head(10)
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.barh(np.arange(10)[::-1], prej["refund_total"] / 1e3, color=CMAP(0.2))
ax.set_yticks(np.arange(10)[::-1]); ax.set_yticklabels(prej["name"])
ax.set_xlabel("Prejuízo (R$ mil)")
ax.set_title("Top 10 produtos por prejuízo em devoluções (R$ estornados)\nmotivos principais: desistência, compra duplicada, avaria no transporte")
for i, v in enumerate(np.arange(10)[::-1]):
    ax.text(prej["refund_total"].iloc[v] / 1e3 + 0.5, i, f"{prej['refund_total'].iloc[v]/1e3:.1f}k",
            va="center")
plt.tight_layout(); plt.savefig(f"{OUT}/2_prejuizo_produto.png"); plt.close()

# ------------------------------------------------------------------ 3
# Clientes com maior lucro acumulado
# ------------------------------------------------------------------
lucro = pd.read_csv("/home/alixandremz/lighthouse/respostas/q_lucro_clientes.csv").head(10)
labels = [f"#{r['customer_id']}" if False else (str(r["legal_name"])[:24]) for _, r in lucro.iterrows()]
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.barh(np.arange(10)[::-1], lucro["profit"] / 1e3, color=CMAP(0.6))
ax.set_yticks(np.arange(10)[::-1]); ax.set_yticklabels(lucro["legal_name"].str[:28])
ax.set_xlabel("Lucro acumulado (R$ mil)")
ax.set_title("Top 10 clientes por lucro acumulado (receita − custo dos produtos)")
for v, i in zip(lucro["profit"].values[::-1], range(10)):
    ax.text(v / 1e3 + 3, i, f"{v/1e3:.0f}k", va="center")
plt.tight_layout(); plt.savefig(f"{OUT}/3_lucro_clientes.png"); plt.close()

# ------------------------------------------------------------------ 4
# Receita mensal (2020-2026) e categoria
# ------------------------------------------------------------------
ser = pd.read_csv("/home/alixandremz/lighthouse/respostas/q_serie_receita.csv")
ser["mes"] = pd.to_datetime(ser["mes"].astype(str) + "-01")
fig, ax = plt.subplots(figsize=(9.5, 4.2))
ax.plot(ser["mes"], ser["line_total"] / 1e6, lw=1.6, color=CMAP(0.0))
m7 = ser.set_index("mes")["line_total"].rolling(7, center=True).mean() / 1e6
ax.plot(ser["mes"], m7, lw=2.2, color="crimson", label="Média móvel 7 meses")
ax.set_ylabel("Receita (R$ milhões/mês)"); ax.set_title("Receita mensal — vendas efetivas (paid/confirmed)")
ax.legend()
plt.tight_layout(); plt.savefig(f"{OUT}/4_receita_mensal.png"); plt.close()

cat = pd.read_csv("/home/alixandremz/lighthouse/respostas/q_receita_categoria.csv").head(10)
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.barh(np.arange(10)[::-1], cat["line_total"] / 1e6, color=CMAP(np.linspace(0, 1, 10)))
ax.set_yticks(np.arange(10)[::-1]); ax.set_yticklabels(cat["name"])
ax.set_xlabel("Receita (R$ milhões)"); ax.set_title("Receita por categoria de produto (top 10)")
plt.tight_layout(); plt.savefig(f"{OUT}/5_receita_categoria.png"); plt.close()

# ------------------------------------------------------------------ 5
# Q7 - recomendação: top 5 similares
# ------------------------------------------------------------------
import importlib.util
spec = importlib.util.spec_from_file_location("q7", "/home/alixandremz/lighthouse/respostas/questao7_recomendacao.py")
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    rank = mod.rank
    nomes = mod.nomes
    fig, ax = plt.subplots(figsize=(9, 4))
    y = np.arange(len(rank))[::-1]
    ax.barh(y, rank.values, color=CMAP(0.5))
    ax.set_yticks(y); ax.set_yticklabels([str(nomes[i]) for i in rank.index])
    ax.set_xlabel("Similaridade de cosseno"); ax.set_ylabel("Produto")
    ax.set_title("Quem comprou 'Motor de Popa 1949' também levou...\nTop 5 produtos por similaridade de cosseno (coocorrência de clientes)")
    for i, v in zip(y, rank.values):
        ax.text(v + 0.005, i, f"{v:.3f}", va="center")
    ax.set_xlim(0, rank.max() + 0.08)
    plt.tight_layout(); plt.savefig(f"{OUT}/8_recomendacao_q7.png"); plt.close()
except Exception as e:
    rank = None
    print("skip q7 chart:", e)

# ------------------------------------------------------------------ 6
# Q6 - previsão vs real Q1 2026
# ------------------------------------------------------------------
esp = importlib.util.spec_from_file_location("q6", "/home/alixandremz/lighthouse/respostas/questao6_previsao_demanda.py")
m6 = importlib.util.module_from_spec(esp)
try:
    esp.loader.exec_module(m6)
    res = m6.result
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(res)); w = 0.35
    ax.bar(x - w/2, res["real"], w, label="Real", color=CMAP(1.0))
    ax.bar(x + w/2, res["previsao"], w, label="Previsão (MMA 3)", color=CMAP(0.7))
    ax.set_xticks(x); ax.set_xticklabels(res.index)
    ax.set_ylabel("Unidades/mês"); ax.set_title("Bússola de Bordo 702 — previsão vs real (1º tri 2026)\nMAE = "
                                                f"{res['erro_abs'].mean():.2f} unidades")
    ax.legend()
    plt.tight_layout(); plt.savefig(f"{OUT}/6_previsao_q6.png"); plt.close()
except Exception as e:
    print("skip q6 chart:", e)

# ------------------------------------------------------------------ 7
# Canal e forma de pagamento
# ------------------------------------------------------------------
pay = pd.read_csv(f"{CSV}/payments.csv")
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ch = orders["channel"].value_counts()
ax[0].pie(ch.values, labels=ch.index, autopct="%.0f%%", startangle=90, colors=[CMAP(0.2), CMAP(0.5)])
ax[0].set_title("Pedidos por canal")
pm = pay["method"].value_counts()
ax[1].pie(pm.values, labels=pm.index, autopct="%.0f%%", startangle=90, colors=[CMAP(i) for i in np.linspace(0, 1, len(pm))])
ax[1].set_title("Pagamentos por método")
plt.tight_layout(); plt.savefig(f"{OUT}/7_canal_pagamento.png"); plt.close()

print("charts gerados em", OUT)
for f in sorted(__import__("os").listdir(OUT)):
    print(" ", f)