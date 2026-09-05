# Desafio Lighthouse — LH Nautical

Repositório criado para resolver o **desafio final do processo seletivo da Indicium** para a vaga de estágio em dados.

O desafio consiste em um estudo de caso sobre a **LH Nautical**, uma loja fictícia do setor náutico, cobrindo todo o pipeline de dados: modelagem, carregamento, análises SQL/Python, previsão de demanda e sistema de recomendação.

---

## Contexto

- **Empresa:** LH Nautical (varejo náutico, canais físico `pos` e online)
- **Base de dados:** 24 arquivos CSV com dados de clientes, produtos, variantes, pedidos, estoque, fornecedores, devoluções e movimentações
- **Período dos dados:** 2020–2026
- **Ferramentas:** Python 3, SQLite/PostgreSQL, pandas, numpy, scikit-learn, matplotlib

---

## Estrutura do repositório

```
.
├── 1-lh_nautical_csv/          # Dados brutos (24 CSV)
│   └── 1-lh_nautical_csv.zip   # Mesmos dados, em arquivo único
└── respostas/                  # Soluções das 7 questões
    ├── schema.sql               # Q2 – Modelagem / schema derivado dos CSVs
    ├── generate_schema.py       # Q2 – Gerador automático do schema
    ├── questao2_1_codigo.pdf    # Q2 – Código + explicação (PDF)
    ├── questao3_carregamento.py # Q3 – Carga dos CSVs no banco bruto
    ├── lh_nautical_raw.db       # Q3 – Banco SQLite bruto gerado
    ├── questao4_analise_clientes.sql  # Q4 – Análise de clientes (SQL)
    ├── q4_top10_clientes.csv          # Q4 – Top 10 clientes elite
    ├── questao5_dimensao_datas.sql    # Q5 – Dimensão de calendário (SQL)
    ├── questao6_previsao_demanda.py   # Q6 – Previsão de demanda
    ├── q_serie_receita.csv            # Q6 – Série mensal de vendas
    ├── questao7_recomendacao.py       # Q7 – Sistema de recomendação
    ├── gerar_dashboard.py              # Gera os 8 gráficos do dashboard
    ├── dashboard/                      # Gráficos (receita, lucro, categorias…)
    ├── analises_completas.py           # Análises complementares (lucro/prejuízo)
    ├── build_relatorio.py              # Gera os PDFs de relatório
    ├── q_lucro_clientes.csv            # Lucro por cliente
    ├── q_prejuizo_produto.csv          # Prejuízo por produto
    ├── q_receita_categoria.csv         # Receita por categoria
    ├── LH_Nautical_Completo.pdf        # Relatório completo
    ├── Relatorio_LH_Nautical.pdf       # Relatório executivo
    └── lh_nautical_report_1.1.pdf      # Relatório versão 1.1
```

---

## Questões do desafio

| # | Tema | Entregável | Arquivo |
|---|------|-----------|---------|
| 1 | Exploração dos dados | Compreensão e estruturação dos dados | `1-lh_nautical_csv/` |
| 2 | Modelagem (schema) | Script gerador + DDL do banco | `generate_schema.py`, `schema.sql`, `questao2_1_codigo.pdf` |
| 3 | Carregamento | Carga dos 24 CSVs no banco bruto | `questao3_carregamento.py` → `lh_nautical_raw.db` |
| 4 | Análise de clientes | Top 10 clientes fiéis + categoria favorita | `questao4_analise_clientes.sql`, `q4_top10_clientes.csv` |
| 5 | Dimensão de datas | Média correta de vendas por dia da semana | `questao5_dimensao_datas.sql` |
| 6 | Previsão de demanda | Previsão mensal do produto "Bússola de Bordo 702" | `questao6_previsao_demanda.py`, `q_serie_receita.csv` |
| 7 | Recomendação | "Quem comprou isso, também levou…" | `questao7_recomendacao.py` |

### Destaques das respostas

- **Q2 (Schema):** 24 tabelas geradas automaticamente a partir dos CSVs, com tipos (INTEGER, NUMERIC, VARCHAR, TIMESTAMP, BOOLEAN) e inferência de `PRIMARY KEY`.
- **Q3 (Carregamento):** carga sem tratamento de dados (dado bruto), com guarda de engenharia para a chave de acesso da NF-e (44 dígitos → `VARCHAR` para não perder dígitos em inteiro 64-bit).
- **Q4 (Clientes):** clientes **elite** (13+ categorias distintas) ranqueados por ticket médio; identifica a categoria mais comprada pelo grupo.
- **Q5 (Datas):** cria uma **dimensão de calendário** recursiva que inclui dias sem venda (zero) no denominador — corrige a média que o estagiário inflou ao ignorar dias fechados.
- **Q6 (Previsão):** baseline de **média móvel dos 3 meses anteriores** (sem lookahead), treino até 12/2025 e teste no 1º trimestre de 2026, métrica **MAE**.
- **Q7 (Recomendação):** matriz usuário×produto com **similaridade de cosseno** e vitrine para o item "Motor de Popa 1949".

---

## Dashboard

8 gráficos gerados pelo script `gerar_dashboard.py`:

| Arquivo | Conteúdo |
|---------|----------|
| `1_dia_semana.png` | Média de vendas por dia da semana (lojas físicas) |
| `2_prejuizo_produto.png` | Top 10 produtos por prejuízo em devoluções |
| `3_lucro_clientes.png` | Lucro por cliente |
| `4_receita_mensal.png` | Receita mensal ao longo do tempo |
| `5_receita_categoria.png` | Receita por categoria |
| `6_previsao_q6.png` | Previsão de demanda (Q6) |
| `7_canal_pagamento.png` | Distribuição por canal de pagamento |
| `8_recomendacao_q7.png` | Recomendação de produtos (Q7) |

---

## Como executar

### Pré-requisitos

- Python 3.10+
- Dependências: `pip install pandas numpy scikit-learn matplotlib`

### Passo a passo

```bash
# 1. Gerar o schema (Q2)
python respostas/generate_schema.py

# 2. Carregar o banco bruto (Q3)
python respostas/questao3_carregamento.py

# 3. Análises SQL (Q4 e Q5) — executar contra o banco:
sqlite3 respostas/lh_nautical_raw.db < respostas/questao4_analise_clientes.sql
sqlite3 respostas/lh_nautical_raw.db < respostas/questao5_dimensao_datas.sql

# 4. Previsão de demanda (Q6)
python respostas/questao6_previsao_demanda.py

# 5. Sistema de recomendação (Q7)
python respostas/questao7_recomendacao.py

# 6. (Opcional) Gerar o dashboard e os relatórios
python respostas/gerar_dashboard.py
python respostas/build_relatorio.py
```

> **Nota:** os scripts usam caminhos absolutos (`/home/alixandremz/lighthouse/...`). Ajuste as variáveis `CSV_DIR`/`CSV`/`OUT` no topo de cada arquivo antes de rodar em outra máquina.

---
