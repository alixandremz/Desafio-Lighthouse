"""
Gera o relatório final em PDF único: respostas de todas as questões +
dashboard (material complementar obrigatório) + anexos de código.
Saída: respostas/Relatorio_LH_Nautical.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, Preformatted, HRFlowable)
import pandas as pd

OUT = "/home/alixandremz/lighthouse/respostas"
DASH = f"{OUT}/dashboard"

# ---------------------------------------------------------------- estilos
NAVY = colors.HexColor("#0b3d66")
GOLD = colors.HexColor("#c8a24a")
LIGHT = colors.HexColor("#f2f6fa")

S = {
    "titulo": ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=26, textColor=NAVY,
                             leading=30, alignment=TA_CENTER, spaceAfter=6),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=13, textColor=colors.HexColor("#55616e"),
                          alignment=TA_CENTER, leading=18),
    "secao": ParagraphStyle("secao", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
                            spaceBefore=10, spaceAfter=8),
    "subsecao": ParagraphStyle("subsecao", fontName="Helvetica-Bold", fontSize=12,
                               textColor=colors.HexColor("#8c6f26"), spaceBefore=6, spaceAfter=4),
    "corpo": ParagraphStyle("corpo", fontName="Helvetica", fontSize=10, leading=14.5,
                            alignment=TA_JUSTIFY, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10, leading=14,
                             leftIndent=14, bulletIndent=4, spaceAfter=3),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=7.5, leading=9.2,
                           backColor=LIGHT, borderPadding=6, borderColor=colors.HexColor("#d5dee6"),
                           borderWidth=0.5, textColor=colors.HexColor("#203040")),
    "legenda": ParagraphStyle("legenda", fontName="Helvetica-Oblique", fontSize=8.5,
                              textColor=colors.HexColor("#6a7683"), leading=11, spaceAfter=10),
}

def br(x):
    return f"R${x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def mil(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

story = []

# ------------------------------------------------------------------ CAPA
story.append(Spacer(1, 30 * mm))
story.append(Paragraph("LH NAUTICAL", styles := S["titulo"]))
story.append(Paragraph("Desafio de Dados — Jornada de Dados & IA", S["sub"]))
story.append(Spacer(1, 8 * mm))
story.append(Paragraph("Do dado bruto à inteligência aplicada: 7 questões resolvidas + dashboard executivo", S["sub"]))
story.append(Spacer(1, 12 * mm))
story.append(Image(DASH + "/4_receita_mensal.png", width=150 * mm, height=66 * mm))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph("Stakeholders: Gabriel Santos · Marina Costa · Sr. Almir", S["legenda"]))
story.append(Paragraph("Ambiente: Python 3.12 + pandas/numpy/sklearn · SQL (SQLite) · visualizações Matplotlib", S["legenda"]))
story.append(PageBreak())

# ------------------------------------------------------------------ SUMÁRIO
story.append(Paragraph("Sumário Executivo", S["secao"]))
story.append(Paragraph(
    "Este trabalho percorre as 7 frentes do desafio a partir dos 24 arquivos CSV (433.424 registros): "
    "diagnóstico do dado bruto, modelagem SQL, carregamento com schema, análise de clientes fiéis, "
    "dimensão de calendário (correção da média por dia da semana), previsão de demanda e motor de "
    "recomendação. Os principais achados:", S["corpo"]))
for t in [
    "Receita efetiva (paid+confirmed) em crescimento contínuo: R$ 1,05 bi no período 2020–2026, com picos sazonais de verão e dezembro.",
    "Quinta-feira é o pior dia de vendas nas lojas físicas (R$ 157,1 mil/dia); o Domingo é o 2º pior — contrariando o estagiário, que ignorava dias sem venda (Q5).",
    "Clientes elite (13+ categorias): 1.919 clientes; os Top 10 por ticket médio concentram 399 itens em Hélices (Q4).",
    "Verde (lucratividade): os 1.000+ pares produto-variante não possuem nenhum caso estrutural de preço ≤ custo; as perdas vêm de devoluções/estornos.",
    "Previsão (Bússola de Bordo 702): baseline de média móvel de 3 meses entrega MAE de 16,56 un./mês (~27% da demanda) — inadequado para decisão de compra (Q6).",
    "Recomendação: 'Motor de Popa 1949' → Vela Mestra 1913 é o item com maior coocorrência de clientes (cosseno 0,245) (Q7).",
]:
    story.append(Paragraph(t, S["bullet"], bulletText="•"))
story.append(PageBreak())

# ------------------------------------------------------------------ Q1
story.append(Paragraph("Questão 1 — Análise Exploratória (EDA)", S["secao"]))
story.append(Paragraph("Panorama dos dados brutos", S["subsecao"]))
for t in [
    "<b>24 tabelas</b> e 433.424 linhas carregadas; sem linhas duplicadas em nenhuma tabela.",
    "Pedidos cobrem <b>2020-01-01 a 2026-12-31</b>: 48.998 pedidos (paid 34.365 · confirmed 7.335 · cancelled 4.847 · draft 2.451).",
    "Canais: <b>ecommerce 34.342</b> × <b>loja física (pos) 14.656</b>.",
    "Integridade financeira 100% consistente: total do pedido = subtotal − desconto = soma dos itens = soma dos pagamentos = NF-e.",
    "Nenhum par variante com preço de venda ≤ custo (prejuízo estrutural ausente); os impactos estão nas devoluções.",
    "Oportunidades de governança: <b>reorder_point 100% nulo</b> em stock_levels; motivos de devolução não padronizados (maiúsculas, typos, acentos); fiscal_invoices: chave de 44 dígitos (não-int64).",
]:
    story.append(Paragraph(t, S["bullet"], bulletText="•"))

story.append(Image(DASH + "/7_canal_pagamento.png", width=150 * mm, height=60 * mm))
story.append(Paragraph("Composição de canais e métodos de pagamento — base para segmentação.", S["legenda"]))
story.append(PageBreak())

# ------------------------------------------------------------------ Q2 / Q3
story.append(Paragraph("Questões 2 e 3 — Schema & Carregamento", S["secao"]))
story.append(Paragraph("Schema (Q2)", S["subsecao"]))
story.append(Paragraph(
    "A partir da inspeção dos 24 CSVs, foi gerado o arquivo <b>schema.sql</b> com 24 tabelas: tipos "
    "VARCHAR(n)/BIGINT/NUMERIC(18,4)/TIMESTAMP/BOOLEAN derivados do conteúdo observado, PKs nas tabelas "
    "de negócio e chave composta em tabelas de associação (product_variants, goods_receipt_items, etc.).", S["corpo"]))
story.append(Paragraph("Carregamento (Q3)", S["subsecao"]))
story.append(Paragraph(
    "O script <b>questao3_carregamento.py</b> executa o schema.sql e carrega todos os CSVs com Python 3 "
    "nativo (csv+sqlite3+decimal), sem tratamento de dados (nulos preservados, caracteres intactos). "
    "Guarda documentada: nfe_access_key (44 dígitos) excede qualquer int64 — a coluna é criada como "
    "VARCHAR para preservar a chave integral; as 24 tabelas foram validadas linha a linha contra a fonte.", S["corpo"]))
trows = [[Paragraph("<b>Tabela</b>", S["corpo"]), Paragraph("<b>Linhas</b>", S["corpo"]),
          Paragraph("<b>Tabela</b>", S["corpo"]), Paragraph("<b>Linhas</b>", S["corpo"])]]
order = ["addresses","orders","order_items","payments","customers","fiscal_invoices","products","product_variants",
         "stock_movements","stock_levels","purchase_orders","purchase_order_items","goods_receipts","goods_receipt_items",
         "returns","return_items","product_suppliers","variant_attribute_values","suppliers","employees","locations",
         "brands","categories","attributes"]
counts = {"addresses":3998,"orders":48998,"order_items":147320,"payments":53546,"customers":2000,"fiscal_invoices":34365,
          "products":500,"product_variants":1009,"stock_movements":115312,"stock_levels":6054,"purchase_orders":2000,
          "purchase_order_items":6059,"goods_receipts":1548,"goods_receipt_items":4733,"returns":980,"return_items":1384,
          "product_suppliers":1520,"variant_attribute_values":2018,"suppliers":25,"employees":15,"locations":6,
          "brands":12,"categories":14,"attributes":8}
for i in range(0, len(order), 2):
    a, b = order[i], order[i + 1]
    trows.append([a, counts[a], b, counts[b]])
tt = Table(trows, colWidths=[34 * mm, 25 * mm, 34 * mm, 25 * mm])
tt.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b6c2cd")),
    ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(tt)
story.append(Paragraph("Total carregado: 433.424 linhas.", S["legenda"]))
story.append(PageBreak())

# ------------------------------------------------------------------ Q4
story.append(Paragraph("Questão 4 — Análise de clientes (clientes fiéis)", S["secao"]))
story.append(Paragraph("Métricas e ranking de elite (SQL — questao4_analise_clientes.sql)", S["subsecao"]))
story.append(Paragraph(
    "Faturamento = SUM(total); Frequência = COUNT de pedidos; Ticket Médio = faturamento/frequência; "
    "Diversidade = COUNT DISTINCT category_id (cadeia orders→order_items→product_variants→products). "
    "Filtro elite: diversidade ≥ 13, ordenado por ticket DESC com desempate customer_id ASC, LIMIT 10.", S["corpo"]))
top10 = pd.read_csv(f"{OUT}/q4_top10_clientes.csv")
tr = [[Paragraph("<b>Cliente</b>", S["corpo"]), Paragraph("<b>Faturamento</b>", S["corpo"]),
       Paragraph("<b>Freq.</b>", S["corpo"]), Paragraph("<b>Ticket médio</b>", S["corpo"]),
       Paragraph("<b>Divers.</b>", S["corpo"])]]
for _, r in top10.head(10).iterrows():
    tr.append([str(r["customer_id"]), br(r["faturamento"]), int(r["frequencia"]), br(r["ticket"]), int(r["diversidade"])])
tt = Table(tr, colWidths=[22 * mm, 34 * mm, 18 * mm, 40 * mm, 22 * mm])
tt.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b6c2cd")),
    ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (2, 1), (2, -1), "CENTER"),
]))
story.append(tt)
story.append(Paragraph(
    "O filtro de elite deu 1.919 clientes (≥13 categorias). Para o grupo Top-10, a categoria que concentra "
    "a maior quantidade total de itens comprados (SUM(quantity)) é a categoria 8 = <b>Hélices</b> "
    "(399 itens).", S["corpo"]))
story.append(Image(DASH + "/3_lucro_clientes.png", width=145 * mm, height=77 * mm))
story.append(Paragraph("Lucro acumulado por cliente (receita − custo). Freitas Ltda lidera com ~R$ 530 mil.", S["legenda"]))
story.append(Image(DASH + "/2_prejuizo_produto.png", width=145 * mm, height=74 * mm))
story.append(Paragraph(
    "Prejuízo por produto em devoluções concluídas (estornos reembolsados ao cliente) — insumo direto para "
    "revisão de garantias, transporte e descrição de anúncio.", S["legenda"]))
story.append(PageBreak())

# ------------------------------------------------------------------ Q5
story.append(Paragraph("Questão 5 — Dimensão de calendário", S["secao"]))
story.append(Paragraph("Correção da média por dia da semana (lojas físicas)", S["subsecao"]))
story.append(Paragraph(
    "O estagiário agrupou direto a tabela de vendas e ignorou os dias em que a loja abriu e vendeu zero — "
    "esses dias não existem em orders, inflando a média (sobretudo do Domingo). A solução (questao5_dimensao_datas.sql): "
    "gerar a dimensão de datas com CTE recursiva (1 dia a 1 dia entre a menor e a maior venda), LEFT JOIN com "
    "as vendas diárias (channel=pos) e COALESCE(valor,0). A média passa a dividir pelo TOTAL de dias do "
    "calendário, dias sem venda incluídos.", S["corpo"]))
wd = [
    ("Quinta-feira", 366, br(57518480.61), br(157154.32)),
    ("Domingo", 365, br(57529887.95), br(157616.13)),
    ("Segunda-feira", 365, br(57758021.43), br(158241.15)),
    ("Sábado", 365, br(60173268.58), br(164858.27)),
    ("Terça-feira", 365, br(60633373.26), br(166118.83)),
    ("Sexta-feira", 365, br(62120694.25), br(170193.68)),
    ("Quarta-feira", 366, br(63539589.22), br(173605.44)),
]
wt = [[Paragraph("<b>Dia da semana</b>", S["corpo"]), Paragraph("<b>Dias abertos</b>", S["corpo"]),
       Paragraph("<b>Faturamento</b>", S["corpo"]), Paragraph("<b>Média/dia</b>", S["corpo"])]] + wd
tt = Table(wt, colWidths=[38 * mm, 30 * mm, 40 * mm, 36 * mm])
tt.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b6c2cd")),
    ("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("TEXTCOLOR", (0, 1), (0, 1), colors.HexColor("#a01010")),
    ("FONTNAME", (0, 1), (0, 1), "Helvetica-Bold"),
]))
story.append(tt)
story.append(Paragraph("<b>Resposta ao Sr. Almir:</b> o pior dia é <b>Quinta-feira</b> (R$ 157.154/dia). O Domingo "
                       "é o 2º pior — o estagiário estava errado: ele ignorou os domingos com venda zero.", S["corpo"]))
story.append(Image(DASH + "/1_dia_semana.png", width=150 * mm, height=77 * mm))
story.append(PageBreak())

# ------------------------------------------------------------------ Q6
story.append(Paragraph("Questão 6 — Previsão de demanda", S["secao"]))
story.append(Paragraph("Baseline: média móvel dos 3 meses anteriores (Bússola de Bordo 702)", S["subsecao"]))
story.append(Paragraph(
    "Dataset unificado (orders→order_items→product_variants→products), vendas efetivas paid/confirmed, "
    "série mensal. Treino até 31/12/2025; teste = 1º trimestre 2026. Para cada mês de teste, a previsão é a "
    "média dos 3 meses anteriores (sem lookahead — sem data leakage).", S["corpo"]))
ft = [[Paragraph("<b>Mês</b>", S["corpo"]), Paragraph("<b>Real (un.)</b>", S["corpo"]),
       Paragraph("<b>Previsão (un.)</b>", S["corpo"]), Paragraph("<b>Erro abs.</b>", S["corpo"])],
      ["Jan/2026", "76", "32,67", "43,33"],
      ["Fev/2026", "55", "49,67", "5,33"],
      ["Mar/2026", "51", "50,00", "1,00"]]
tt = Table(ft, colWidths=[30 * mm, 32 * mm, 34 * mm, 32 * mm])
tt.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b6c2cd")),
    ("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("ALIGN", (1, 1), (-1, -1), "CENTER"),
]))
story.append(tt)
story.append(Paragraph("<b>MAE = 16,56 unidades/mês</b> (~27,3% da demanda real média do trimestre, 60,67).", S["corpo"]))
story.append(Paragraph(
    "<b>a)</b> O baseline <b>não é adequado</b> para esse produto: subestima fortemente o pico de janeiro "
    "(76 vs 32,67) — a média móvel não capta a sazonalidade de verão essencial para a compra com fornecedor. "
    "<b>b)</b> Limitação: ignora tendência e sazonalidade (lag estrutural); um mês atípico desloca toda a previsão.", S["corpo"]))
story.append(Image(DASH + "/6_previsao_q6.png", width=120 * mm, height=60 * mm))
story.append(PageBreak())

# ------------------------------------------------------------------ Q7
story.append(Paragraph("Questão 7 — Sistema de recomendação", S["secao"]))
story.append(Paragraph("Similaridade de cosseno produto × produto (questao7_recomendacao.py)", S["subsecao"]))
story.append(Paragraph(
    "Matriz Usuário×Produto (linhas=cliente, colunas=produto, célula=1 se comprou ≥1 vez, 0 senão; quantidade "
    "ignorada; apenas vendas paid/confirmed). Similaridade: cosine_similarity(matriz.T) — vetor de cada produto = "
    "clientes que o compraram. Ranking de similaridade com 'Motor de Popa 1949', excluindo ele mesmo.", S["corpo"]))
rec = [("Vela Mestra 1913", "0,2452"), ("Cabo Náutico 2105", "0,2300"), ("GPS Plotter 2249", "0,2148"),
       ("Motor de Popa 1540", "0,2121"), ("Vela Mestra 3870", "0,2088")]
rt = [[Paragraph("<b>#</b>", S["corpo"]), Paragraph("<b>Produto</b>", S["corpo"]),
       Paragraph("<b>Similaridade (cos)</b>", S["corpo"])]] + \
     [[i + 1, nome, c] for i, (nome, c) in enumerate(rec)]
tt = Table(rt, colWidths=[14 * mm, 78 * mm, 46 * mm])
tt.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b6c2cd")),
    ("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("ALIGN", (0, 1), (0, -1), "CENTER"),
]))
story.append(tt)
story.append(Image(DASH + "/8_recomendacao_q7.png", width=150 * mm, height=67 * mm))
story.append(PageBreak())

# ------------------------------------------------------------------ DASHBOARD
story.append(Paragraph("Material Complementar — Dashboard", S["secao"]))
story.append(Paragraph(
    "Painel analítico dos principais resultados do desafio, comunicados em formato de dashboard executivo. "
    "Cada visual reflete uma decisão de análise documentada ao longo do relatório.", S["corpo"]))
for img, leg in [
    ("1_dia_semana.png", "G1 · Média de vendas por dia da semana (lojas físicas) com dias sem venda = 0 — pior dia: quinta."),
    ("2_prejuizo_produto.png", "G2 · Ranking de prejuízo por produto em devoluções (estornos reembolsados)."),
    ("3_lucro_clientes.png", "G3 · Top clientes por lucro acumulado (receita − custo dos produtos)."),
    ("4_receita_mensal.png", "G4 · Receita mensal com picos de verão/dezembro e crescimento contínuo."),
    ("5_receita_categoria.png", "G5 · Receita por categoria — Hélices gera a maior receita."),
    ("8_recomendacao_q7.png", "G6 · Vitrine 'quem comprou também levou' — Motor de Popa 1949."),
    ("6_previsao_q6.png", "G7 · Previsão vs real (Q6) — limite do baseline de média móvel."),
    ("7_canal_pagamento.png", "G8 · Composição de canais e métodos de pagamento."),
]:
    story.append(Image(DASH + "/" + img, width=148 * mm, height=76 * mm))
    story.append(Paragraph("&nbsp;&nbsp;" + leg, S["legenda"]))
    story.append(Spacer(1, 2 * mm))
story.append(PageBreak())

# ------------------------------------------------------------------ ANEXOS
story.append(Paragraph("Anexo — Código Fonte", S["secao"]))
def code_block(path, title):
    story.append(Paragraph(title, S["subsecao"]))
    with open(path, encoding="utf-8") as f:
        content = f.read()
    story.append(Preformatted(content, S["code"]))

code_block(f"{OUT}/questao5_dimensao_datas.sql", "A.1 · Questão 5 — Dimensão de datas (SQL)")
code_block(f"{OUT}/questao6_previsao_demanda.py", "A.2 · Questão 6 — Previsão de demanda (Python)")
code_block(f"{OUT}/questao7_recomendacao.py", "A.3 · Questão 7 — Sistema de recomendação (Python)")
code_block(f"{OUT}/questao3_carregamento.py", "A.4 · Questão 3 — Carregamento (Python)")

doc = SimpleDocTemplate(f"{OUT}/Relatorio_LH_Nautical.pdf", pagesize=A4,
                        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
                        title="LH Nautical — Desafio de Dados", author="Analista de Dados LH Nautical")
doc.build(story)
print("PDF gerado:", f"{OUT}/Relatorio_LH_Nautical.pdf")