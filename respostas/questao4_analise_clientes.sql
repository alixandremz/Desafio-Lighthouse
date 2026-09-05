-- =============================================================
-- Questão 4 - Análise de clientes (LH Nautical)
-- Clientes fiéis: Ticket Médio e Diversidade de Categorias
-- =============================================================

-- Passo 1: ticket médio (faturamento total / frequência) e diversidade por cliente
WITH totals AS (
    SELECT
        customer_id,
        SUM(total) AS faturamento_total,
        COUNT(*)    AS frequencia
    FROM orders
    GROUP BY customer_id
),
diversity AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi       ON oi.order_id = o.id
    JOIN product_variants pv  ON pv.id = oi.product_variant_id
    JOIN products p           ON p.id = pv.product_id
    GROUP BY o.customer_id
),
-- Passo 2: métricas por cliente + filtro de elite (13+ categorias distintas)
elite AS (
    SELECT
        t.customer_id,
        t.faturamento_total,
        t.frequencia,
        t.faturamento_total * 1.0 / t.frequencia AS ticket_medio,
        d.diversidade_categorias
    FROM totals t
    JOIN diversity d ON d.customer_id = t.customer_id
    WHERE d.diversidade_categorias >= 13
),
-- Passo 3: desempate por customer_id (crescente) e top 10
top10 AS (
    SELECT customer_id
    FROM elite
    ORDER BY ticket_medio DESC, customer_id ASC
    LIMIT 10
)

-- Passo 4: categoria com maior quantidade total de itens comprados pelo grupo
SELECT
    p.category_id,
    SUM(oi.quantity) AS total_itens
FROM orders o
JOIN top10 t            ON t.customer_id = o.customer_id
JOIN order_items oi     ON oi.order_id = o.id
JOIN product_variants pv ON pv.id = oi.product_variant_id
JOIN products p         ON p.id = pv.product_id
GROUP BY p.category_id
ORDER BY total_itens DESC
LIMIT 1;