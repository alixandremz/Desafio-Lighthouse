-- =============================================================
-- Questão 5 - Dimensão de calendário (LH Nautical)
-- Corrige a média de vendas por dia da semana das lojas físicas,
-- incluindo dias em que a loja abriu e vendeu zero.
-- =============================================================

-- ---------------------------------------------------------------------------
-- 1) DIMENSÃO DE DATAS (dimensão de calendário)
--    Período: da data mais antiga até a data mais recente de venda nas
--    lojas físicas (channel = 'pos'). A loja fica aberta todos os dias.
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS dim_dates;

CREATE TABLE dim_dates AS
WITH RECURSIVE calendar AS (
    SELECT
        MIN(DATE(o.placed_at)) AS dt,
        MAX(DATE(o.placed_at)) AS last_dt
    FROM orders o
    WHERE o.channel = 'pos'
    UNION ALL
    SELECT
        DATE(dt, '+1 day'),
        last_dt
    FROM calendar
    WHERE DATE(dt, '+1 day') <= last_dt
)
SELECT
    dt                                                                  AS data,
    STRFTIME('%Y', dt)                                                  AS ano,
    STRFTIME('%m', dt)                                                  AS mes,
    STRFTIME('%d', dt)                                                  AS dia,
    CASE STRFTIME('%w', dt)
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Segunda-feira'
        WHEN '2' THEN 'Terça-feira'
        WHEN '3' THEN 'Quarta-feira'
        WHEN '4' THEN 'Quinta-feira'
        WHEN '5' THEN 'Sexta-feira'
        ELSE 'Sábado'
    END                                                                 AS dia_semana
FROM calendar;

-- ---------------------------------------------------------------------------
-- 2) VENDAS DIÁRIAS nas lojas físicas (soma do valor da venda por dia)
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS vendas_diarias;

CREATE TABLE vendas_diarias AS
SELECT
    DATE(placed_at) AS data,
    SUM(total)      AS valor_venda
FROM orders
WHERE channel = 'pos'
GROUP BY DATE(placed_at);

-- ---------------------------------------------------------------------------
-- 3) CRUZAMENTO: calendário x vendas (LEFT JOIN + COALESCE p/ dias sem venda)
--    Dias sem registro viram 0 — o estagiário os ignorou, inflando a média.
-- ---------------------------------------------------------------------------
SELECT
    d.data,
    d.dia_semana,
    COALESCE(v.valor_venda, 0) AS valor_venda
FROM dim_dates d
LEFT JOIN vendas_diarias v ON v.data = d.data
ORDER BY d.data;

-- ---------------------------------------------------------------------------
-- 4) RESPOSTA (Sr. Almir): MÉDIA DE VENDAS POR DIA DA SEMANA
--    Denominador = TOTAL de dias do calendário em cada dia da semana
--    (inclusive os dias sem venda), não apenas os dias com venda.
-- ---------------------------------------------------------------------------
SELECT
    d.dia_semana,
    COUNT(*)                                                AS dias_abertos,
    SUM(COALESCE(v.valor_venda, 0))                         AS faturamento,
    ROUND(SUM(COALESCE(v.valor_venda, 0)) / COUNT(*), 2)    AS media_vendas
FROM dim_dates d
LEFT JOIN vendas_diarias v ON v.data = d.data
GROUP BY d.dia_semana
ORDER BY media_vendas ASC;