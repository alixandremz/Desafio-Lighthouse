-- =============================================================
-- LH Nautical - Schema PostgreSQL gerado automaticamente
-- Gerado em: 2026-08-12 14:25:38
-- Total de tabelas: 24
-- Script: generate_schema.py (Python 3 puro, sem libs externas)
-- =============================================================

-- Fonte: addresses.csv (3998 linhas, 12 colunas)
CREATE TABLE IF NOT EXISTS "addresses" (
    "id" INTEGER PRIMARY KEY,
    "customer_id" INTEGER NOT NULL,
    "address_type" VARCHAR(18) NOT NULL,
    "postal_code" VARCHAR(18) NOT NULL,
    "street" VARCHAR(70) NOT NULL,
    "number" INTEGER NOT NULL,
    "complement" VARCHAR(16),
    "district" VARCHAR(66) NOT NULL,
    "city" VARCHAR(54) NOT NULL,
    "state" VARCHAR(4) NOT NULL,
    "country" VARCHAR(4) NOT NULL,
    "is_primary" BOOLEAN NOT NULL
);

-- Fonte: attributes.csv (8 linhas, 3 colunas)
CREATE TABLE IF NOT EXISTS "attributes" (
    "id" INTEGER PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL,
    "data_type" VARCHAR(14) NOT NULL
);

-- Fonte: brands.csv (12 linhas, 6 colunas)
CREATE TABLE IF NOT EXISTS "brands" (
    "id" INTEGER PRIMARY KEY,
    "name" VARCHAR(28) NOT NULL,
    "country" VARCHAR(4),
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: categories.csv (14 linhas, 7 colunas)
CREATE TABLE IF NOT EXISTS "categories" (
    "id" INTEGER PRIMARY KEY,
    "name" VARCHAR(40) NOT NULL,
    "slug" VARCHAR(40) NOT NULL,
    "parent_category_id" INTEGER,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: customers.csv (2000 linhas, 11 colunas)
CREATE TABLE IF NOT EXISTS "customers" (
    "id" INTEGER PRIMARY KEY,
    "person_type" VARCHAR(4) NOT NULL,
    "legal_name" VARCHAR(64) NOT NULL,
    "trade_name" VARCHAR(54),
    "tax_id" BIGINT NOT NULL,
    "state_registration" VARCHAR(20),
    "email" VARCHAR(98),
    "phone" VARCHAR(28),
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: employees.csv (15 linhas, 11 colunas)
CREATE TABLE IF NOT EXISTS "employees" (
    "id" INTEGER PRIMARY KEY,
    "full_name" VARCHAR(50) NOT NULL,
    "cpf" BIGINT NOT NULL,
    "email" VARCHAR(92) NOT NULL,
    "role" VARCHAR(22) NOT NULL,
    "primary_location_id" INTEGER NOT NULL,
    "hire_date" DATE NOT NULL,
    "termination_date" DATE,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: fiscal_invoices.csv (34365 linhas, 11 colunas)
CREATE TABLE IF NOT EXISTS "fiscal_invoices" (
    "id" INTEGER PRIMARY KEY,
    "order_id" INTEGER NOT NULL,
    "nfe_number" VARCHAR(24) NOT NULL,
    "nfe_access_key" BIGINT NOT NULL,
    "series" INTEGER NOT NULL,
    "issued_at" TIMESTAMP NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "total_amount" NUMERIC(18,4) NOT NULL,
    "xml_storage_uri" VARCHAR(138) NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: goods_receipt_items.csv (4733 linhas, 4 colunas)
CREATE TABLE IF NOT EXISTS "goods_receipt_items" (
    "id" INTEGER PRIMARY KEY,
    "goods_receipt_id" INTEGER NOT NULL,
    "purchase_order_item_id" INTEGER NOT NULL,
    "quantity_received" NUMERIC(18,4) NOT NULL
);

-- Fonte: goods_receipts.csv (1548 linhas, 6 colunas)
CREATE TABLE IF NOT EXISTS "goods_receipts" (
    "id" INTEGER PRIMARY KEY,
    "purchase_order_id" INTEGER NOT NULL,
    "received_by_employee_id" INTEGER NOT NULL,
    "received_at" TIMESTAMP NOT NULL,
    "notes" VARCHAR(30),
    "created_at" TIMESTAMP NOT NULL
);

-- Fonte: locations.csv (6 linhas, 14 colunas)
CREATE TABLE IF NOT EXISTS "locations" (
    "id" INTEGER PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL,
    "location_type" VARCHAR(18) NOT NULL,
    "postal_code" VARCHAR(18) NOT NULL,
    "street" VARCHAR(48) NOT NULL,
    "number" INTEGER NOT NULL,
    "complement" VARCHAR(14),
    "district" VARCHAR(54) NOT NULL,
    "city" VARCHAR(36) NOT NULL,
    "state" VARCHAR(4) NOT NULL,
    "country" VARCHAR(4) NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: order_items.csv (147320 linhas, 8 colunas)
CREATE TABLE IF NOT EXISTS "order_items" (
    "id" INTEGER PRIMARY KEY,
    "order_id" INTEGER NOT NULL,
    "product_variant_id" INTEGER NOT NULL,
    "quantity" INTEGER NOT NULL,
    "unit_price" NUMERIC(18,4) NOT NULL,
    "icms_rate" NUMERIC(18,4) NOT NULL,
    "ipi_rate" NUMERIC(18,4) NOT NULL,
    "line_total" NUMERIC(18,4) NOT NULL
);

-- Fonte: orders.csv (48998 linhas, 13 colunas)
CREATE TABLE IF NOT EXISTS "orders" (
    "id" INTEGER PRIMARY KEY,
    "order_number" VARCHAR(18) NOT NULL,
    "channel" VARCHAR(18) NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "salesperson_id" INTEGER,
    "location_id" INTEGER NOT NULL,
    "status" VARCHAR(18) NOT NULL,
    "subtotal" NUMERIC(18,4) NOT NULL,
    "discount_amount" NUMERIC(18,4) NOT NULL,
    "total" NUMERIC(18,4) NOT NULL,
    "placed_at" TIMESTAMP NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: payments.csv (53546 linhas, 9 colunas)
CREATE TABLE IF NOT EXISTS "payments" (
    "id" INTEGER PRIMARY KEY,
    "order_id" INTEGER NOT NULL,
    "method" VARCHAR(26) NOT NULL,
    "installments" INTEGER NOT NULL,
    "amount" NUMERIC(18,4) NOT NULL,
    "status" VARCHAR(16) NOT NULL,
    "paid_at" TIMESTAMP,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: product_suppliers.csv (1520 linhas, 8 colunas)
CREATE TABLE IF NOT EXISTS "product_suppliers" (
    "product_variant_id" INTEGER NOT NULL,
    "supplier_id" INTEGER NOT NULL,
    "supplier_sku" VARCHAR(26),
    "last_quoted_cost" NUMERIC(18,4) NOT NULL,
    "lead_time_days" INTEGER NOT NULL,
    "is_preferred" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: product_variants.csv (1009 linhas, 12 colunas)
CREATE TABLE IF NOT EXISTS "product_variants" (
    "id" INTEGER PRIMARY KEY,
    "product_id" INTEGER NOT NULL,
    "sku" VARCHAR(20) NOT NULL,
    "barcode_ean" BIGINT,
    "sale_price" NUMERIC(18,4) NOT NULL,
    "cost_price" NUMERIC(18,4) NOT NULL,
    "weight_kg" NUMERIC(18,4) NOT NULL,
    "icms_rate" NUMERIC(18,4) NOT NULL,
    "ipi_rate" NUMERIC(18,4) NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: products.csv (500 linhas, 10 colunas)
CREATE TABLE IF NOT EXISTS "products" (
    "id" INTEGER PRIMARY KEY,
    "name" VARCHAR(46) NOT NULL,
    "description" VARCHAR(96),
    "brand_id" INTEGER NOT NULL,
    "category_id" INTEGER NOT NULL,
    "ncm_code" INTEGER NOT NULL,
    "unit_of_measure" VARCHAR(4) NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: purchase_order_items.csv (6059 linhas, 6 colunas)
CREATE TABLE IF NOT EXISTS "purchase_order_items" (
    "id" INTEGER PRIMARY KEY,
    "purchase_order_id" INTEGER NOT NULL,
    "product_variant_id" INTEGER NOT NULL,
    "quantity_ordered" INTEGER NOT NULL,
    "unit_cost" NUMERIC(18,4) NOT NULL,
    "line_total" NUMERIC(18,4) NOT NULL
);

-- Fonte: purchase_orders.csv (2000 linhas, 13 colunas)
CREATE TABLE IF NOT EXISTS "purchase_orders" (
    "id" INTEGER PRIMARY KEY,
    "po_number" VARCHAR(18) NOT NULL,
    "supplier_id" INTEGER NOT NULL,
    "buyer_id" INTEGER NOT NULL,
    "destination_location_id" INTEGER NOT NULL,
    "status" VARCHAR(36) NOT NULL,
    "currency" VARCHAR(6) NOT NULL,
    "subtotal" NUMERIC(18,4) NOT NULL,
    "total" NUMERIC(18,4) NOT NULL,
    "placed_at" TIMESTAMP NOT NULL,
    "expected_delivery_at" DATE,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: return_items.csv (1384 linhas, 7 colunas)
CREATE TABLE IF NOT EXISTS "return_items" (
    "id" INTEGER PRIMARY KEY,
    "return_id" INTEGER NOT NULL,
    "order_item_id" INTEGER NOT NULL,
    "quantity" NUMERIC(18,4) NOT NULL,
    "action" VARCHAR(16) NOT NULL,
    "exchange_variant_id" INTEGER,
    "unit_refund_amount" NUMERIC(18,4) NOT NULL
);

-- Fonte: returns.csv (980 linhas, 10 colunas)
CREATE TABLE IF NOT EXISTS "returns" (
    "id" INTEGER PRIMARY KEY,
    "return_number" VARCHAR(18) NOT NULL,
    "order_id" INTEGER NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "received_at_location_id" INTEGER NOT NULL,
    "status" VARCHAR(18) NOT NULL,
    "reason" VARCHAR(66),
    "total_refund_amount" NUMERIC(18,4) NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: stock_levels.csv (6054 linhas, 5 colunas)
CREATE TABLE IF NOT EXISTS "stock_levels" (
    "product_variant_id" INTEGER NOT NULL,
    "location_id" INTEGER NOT NULL,
    "quantity_on_hand" NUMERIC(18,4) NOT NULL,
    "reorder_point" TEXT,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: stock_movements.csv (115312 linhas, 11 colunas)
CREATE TABLE IF NOT EXISTS "stock_movements" (
    "id" INTEGER PRIMARY KEY,
    "product_variant_id" INTEGER NOT NULL,
    "location_id" INTEGER NOT NULL,
    "movement_type" VARCHAR(22) NOT NULL,
    "quantity" NUMERIC(18,4) NOT NULL,
    "reference_table" VARCHAR(28),
    "reference_id" INTEGER,
    "employee_id" INTEGER,
    "notes" VARCHAR(68),
    "occurred_at" TIMESTAMP NOT NULL,
    "created_at" TIMESTAMP NOT NULL
);

-- Fonte: suppliers.csv (25 linhas, 12 colunas)
CREATE TABLE IF NOT EXISTS "suppliers" (
    "id" INTEGER PRIMARY KEY,
    "legal_name" VARCHAR(60) NOT NULL,
    "trade_name" VARCHAR(22),
    "country" VARCHAR(4) NOT NULL,
    "tax_id" VARCHAR(28) NOT NULL,
    "tax_id_type" VARCHAR(8) NOT NULL,
    "email" VARCHAR(60) NOT NULL,
    "phone" BIGINT NOT NULL,
    "contact_name" VARCHAR(54) NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- Fonte: variant_attribute_values.csv (2018 linhas, 3 colunas)
CREATE TABLE IF NOT EXISTS "variant_attribute_values" (
    "product_variant_id" INTEGER NOT NULL,
    "attribute_id" INTEGER NOT NULL,
    "value" VARCHAR(28) NOT NULL
);
