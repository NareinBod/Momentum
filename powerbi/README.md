# Power BI report build guide

Load every CSV from `data/processed/` using **Get Data > Text/CSV**, or invoke the reusable `LoadCsv` function in `power_query.m`. Set `order_date`, `forecast_as_of`, and `month` to Date; numeric values to Decimal Number; IDs to Whole Number; and `stockout_risk` to True/False.

Create these single-direction, many-to-one relationships:

| From | Column | To | Column |
| --- | --- | --- | --- |
| fact_sales | product_id | dim_products | product_id |
| fact_purchase_orders | product_id | dim_products | product_id |
| fact_purchase_orders | supplier_id | dim_suppliers | supplier_id |
| supplier_performance | supplier_id | dim_suppliers | supplier_id |
| demand_forecast | product_id | dim_products | product_id |
| inventory_metrics | product_id | dim_products | product_id |
| monthly_operations | product_id | dim_products | product_id |

Use the measures in `measures.dax`. The report layout is in `report_blueprint.md`; this produces the requested three-page business dashboard without committing an opaque proprietary `.pbix` binary.
