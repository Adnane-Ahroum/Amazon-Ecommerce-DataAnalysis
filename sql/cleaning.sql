-- Amazon E-commerce Cleaning & Metrics (SQLite)
--make them .csv files for compatibility with other tools if needed
-- Orders cleaned view

CREATE VIEW IF NOT EXISTS v_orders AS
SELECT
  UPPER(COALESCE(sku, passport_sku)) AS sku,
  amazon_order_id,
  quantity,
  item_price,
  (COALESCE(item_price,0) * CASE WHEN quantity = 0 THEN 1 ELSE quantity END) AS item_price_total,
  DATE(purchase_d) AS purchase_date,
  strftime('%Y-W%W', DATE(purchase_d)) AS week
FROM orders;

-- Sponsored Products aggregation
CREATE VIEW IF NOT EXISTS v_sp AS
SELECT
  UPPER(COALESCE(advertised_sku, passport_sku__)) AS sku,
  campaign_name,
  SUM(COALESCE(spend,0)) AS ad_spend_sp,
  SUM(COALESCE([7_day_total_sales],0)) AS ad_sales_sp,
  SUM(COALESCE([7_day_total_orders__],0)) AS ad_orders_sp,
  SUM(COALESCE([7_day_total_units__],0)) AS ad_units_sp
FROM sponsored_products
GROUP BY 1,2;

-- Returns aggregation
CREATE VIEW IF NOT EXISTS v_returns AS
SELECT
  UPPER(sku) AS sku,
  SUM(COALESCE(quantity,1)) AS units_returned
FROM returns
GROUP BY 1;

-- Costs/fees lookup
CREATE VIEW IF NOT EXISTS v_costs AS
SELECT
  UPPER(sku) AS sku,
  unit_cost,
  referral_fee,
  fba_cost,
  storage_oct_dec,
  storage_cos_jan_sep
FROM xref;

-- Fee per unit lookup
CREATE VIEW IF NOT EXISTS v_fee AS
SELECT UPPER(sku) AS sku, estimated_fee_total FROM fee_preview;

-- SKU metrics
CREATE VIEW IF NOT EXISTS v_sku_metrics AS
WITH ord AS (
  SELECT sku,
         COUNT(DISTINCT amazon_order_id) AS orders_cnt,
         SUM(quantity) AS units_sold,
         SUM(item_price_total) AS gross_sales
  FROM v_orders GROUP BY 1
), ret AS (
  SELECT sku, units_returned FROM v_returns
), sp AS (
  SELECT sku,
         SUM(ad_spend_sp) AS ad_spend_total,
         SUM(ad_sales_sp) AS ad_sales_total
  FROM v_sp GROUP BY 1
), costs AS (
  SELECT sku, unit_cost, referral_fee, fba_cost, storage_oct_dec, storage_cos_jan_sep FROM v_costs
), fees AS (
  SELECT sku, estimated_fee_total FROM v_fee
)
SELECT
  ord.sku,
  ord.orders_cnt,
  ord.units_sold,
  COALESCE(ret.units_returned,0) AS units_returned,
  ord.gross_sales,
  (ord.gross_sales) AS net_sales, -- returns value requires price; simplifying if missing
  COALESCE(sp.ad_spend_total,0) AS ad_spend_total,
  COALESCE(sp.ad_sales_total,0) AS ad_sales_sp,
  COALESCE(costs.unit_cost,0) AS unit_cost,
  COALESCE(costs.referral_fee,0) AS referral_fee,
  COALESCE(costs.fba_cost,0) AS fba_cost,
  COALESCE(fees.estimated_fee_total,0) AS estimated_fee_total
FROM ord
LEFT JOIN ret ON ret.sku = ord.sku
LEFT JOIN sp ON sp.sku = ord.sku
LEFT JOIN costs ON costs.sku = ord.sku
LEFT JOIN fees ON fees.sku = ord.sku;

-- Summary checks
SELECT COUNT(*) AS skus FROM v_sku_metrics;
SELECT sku, net_sales, ad_spend_total, ad_sales_sp FROM v_sku_metrics ORDER BY net_sales DESC LIMIT 10;
