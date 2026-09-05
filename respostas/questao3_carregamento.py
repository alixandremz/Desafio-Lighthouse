"""
Questão 3 — Carregamento
LH Nautical | Análise de Dados com Python

Carga de todos os 24 arquivos CSV no banco de dados bruto, respeitando o
schema definido na Questão 2 (respostas/schema.sql).

Premissas obedecidas:
- Python 3 + bibliotecas nativas (csv, sqlite3, re, decimal) — zero dependências externas;
- Carrega TODOS os CSVs, um por tabela, SEM qualquer tratamento de dados
  (não remove nulos, não corrige caracteres, não ajusta formatos);
- Usa os tipos definidos no schema.sql (INTEGER, NUMERIC, VARCHAR, TIMESTAMP, BOOLEAN, ...).

Guardas de engenharia (preservação + integridade de carga):
- o nfe_access_key da NF-e tem 44 dígitos e NÃO cabe em BIGINT/INTEGER de 64 bits.
  Tal valor é gravado como texto para não perder dígitos (a chave de acesso é
  gravada/consultada como string na vida real). Nenhum conteúdo é alterado.
- valores vazios em colunas numéricas são gravados como NULL (ausência de dado,
  não é remoção); valores vazios em colunas de texto são gravados como ''.

Uso:
    python3 questao3_carregamento.py
Gera o banco bruto em: respostas/lh_nautical_raw.db
"""

import csv
import os
import re
import sqlite3
from decimal import Decimal, InvalidOperation, localcontext

CSV_DIR = "/home/alixandremz/lighthouse/1-lh_nautical_csv"
SCHEMA_SQL = "/home/alixandremz/lighthouse/respostas/schema.sql"
DB_PATH = "/home/alixandremz/lighthouse/respostas/lh_nautical_raw.db"

INT64_MIN = -(2**63)
INT64_MAX = (2**63) - 1


# ---------------------------------------------------------------------------
# 1. Leitura do schema.sql (Questão 2) -> dicionário: tabela -> [(coluna, tipo)]
# ---------------------------------------------------------------------------
def parse_schema(path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    tables = {}
    pattern = re.compile(r'CREATE TABLE IF NOT EXISTS "(\w+)" \((.*?)\);', re.S)
    for m in pattern.finditer(sql):
        table, body = m.group(1), m.group(2)
        cols = []
        for line in body.splitlines():
            line = line.strip()
            mcol = re.match(r'^"(\w+)"\s+([A-Z]+)(?:\(\d+,\d+\))?', line)
            if mcol:
                cols.append((mcol.group(1), mcol.group(2)))
        tables[table] = cols
    return tables


def classify(base_type):
    """Mapeia o tipo do schema para a categoria de conversão de dados."""
    if base_type in ("INT", "INTEGER", "BIGINT", "SMALLINT"):
        return "int"
    if base_type in ("NUMERIC", "DECIMAL", "REAL", "FLOAT", "DOUBLE"):
        return "num"
    if base_type in ("BOOLEAN", "BOOL"):
        return "bool"
    return "text"  # VARCHAR, CHAR, TEXT, TIMESTAMP, DATE, TIME, ...


def to_int(value):
    """Inteiro com guarda de overflow: fora do range int64 vira texto (ex.: nfe_access_key)."""
    s = value.strip()
    if s == "":
        return None
    if not re.fullmatch(r"[-+]?\d+", s):
        return s
    i = int(s)
    return i if INT64_MIN <= i <= INT64_MAX else s


def to_num(value):
    """NUMERIC/DECIMAL do schema. Vazio -> NULL; não-numérico fica como texto."""
    s = value.strip()
    if s == "":
        return None
    try:
        with localcontext() as ctx:
            ctx.prec = 18
            return float(Decimal(s))
    except (InvalidOperation, ValueError):
        return s


def to_bool(value):
    s = value.strip().lower()
    if s in ("true", "1", "t", "yes"):
        return 1
    if s in ("false", "0", "f", "no"):
        return 0
    if s == "":
        return None
    return s


# ---------------------------------------------------------------------------
# 3. Carga em si
# ---------------------------------------------------------------------------
def main():
    tables = parse_schema(SCHEMA_SQL)
    handlers = {
        "int": to_int,
        "num": to_num,
        "bool": to_bool,
        "text": lambda v: v,  # sem nenhuma transformação (dado bruto)
    }

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # carga limpa, do zero

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    ddl = open(SCHEMA_SQL, encoding="utf-8").read()
    # Ajuste fiel à realidade dos dados: a chave de acesso da NF-e (44 dígitos)
    # não é representável em nenhum inteiro 64-bit (BIGINT do schema). Gravamos a
    # coluna como VARCHAR para preservar a chave integral; demais colunas intactas.
    ddl = ddl.replace('"nfe_access_key" BIGINT NOT NULL', '"nfe_access_key" VARCHAR(44) NOT NULL')
    cur.executescript(ddl)  # DDL da Questão 2 (com o ajuste acima)

    print(f"{'tabela':<24} {'linhas':>8} {'colunas':>8} {'atípicos/overflow':>18}")
    print("-" * 64)

    total_rows = 0
    for table, cols in tables.items():
        csv_path = os.path.join(CSV_DIR, f"{table}.csv")
        if not os.path.exists(csv_path):
            print(f"{table:<24} ARQUIVO NÃO ENCONTRADO: {csv_path}")
            continue

        col_names = [name for name, _ in cols]
        ddl_types = {name: base for name, base in cols}
        atyp = 0
        rows = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # header
            for row in reader:
                coerced = []
                for idx, name in enumerate(col_names):
                    raw = row[idx] if idx < len(row) else ""
                    cat = classify(ddl_types[name])
                    value = handlers[cat](raw)
                    if cat in ("int", "num") and raw.strip() != "" and isinstance(value, str):
                        atyp += 1  # valor mantido como texto (atípico/overflow)
                    coerced.append(value)
                rows.append(coerced)

        placeholders = ",".join("?" for _ in col_names)
        col_list = ",".join(f'"{n}"' for n in col_names)
        cur.executemany(f'INSERT INTO "{table}" ({col_list}) VALUES ({placeholders})', rows)
        total_rows += len(rows)
        print(f"{table:<24} {len(rows):>8} {len(col_names):>8} {atyp:>18}")

    con.commit()
    con.close()
    print("-" * 64)
    print(f"TOTAL CARREGADO: {total_rows} linhas em {len(tables)} tabelas -> {DB_PATH}")


if __name__ == "__main__":
    main()