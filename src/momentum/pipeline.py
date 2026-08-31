from pathlib import Path
import pandas as pd
from .data_generator import generate_raw_data
from .forecasting import build_forecast

ROOT = Path(__file__).resolve().parents[2]
RAW, PROCESSED = ROOT / "data" / "raw", ROOT / "data" / "processed"

def read(name): return pd.read_csv(RAW / f"{name}.csv")

def run():
    if not (RAW / "sales_orders.csv").exists(): generate_raw_data(RAW)
    suppliers, products = read("suppliers"), read("products")
    orders, lines, pos = read("sales_orders"), read("sales_order_lines"), read("purchase_orders")
    orders["order_date"] = pd.to_datetime(orders.order_date, errors="coerce")
    pos[["ordered_date", "promised_date", "received_date"]] = pos[["ordered_date", "promised_date", "received_date"]].apply(pd.to_datetime, errors="coerce")
    lines = lines.drop_duplicates("order_line_id").query("quantity > 0 and unit_price > 0")
    pos = pos.drop_duplicates("po_id").query("quantity > 0 and unit_cost > 0")
    sales = lines.merge(orders, on="order_id", validate="many_to_one").merge(products[["product_id", "sku", "product_name", "category", "unit_cost"]], on="product_id", validate="many_to_one")
    sales["gross_sales"] = (sales.quantity * sales.unit_price).round(2)
    sales["net_sales"] = (sales.gross_sales * (1 - sales.discount_pct)).round(2)
    sales["cogs"] = (sales.quantity * sales.unit_cost).round(2)
    sales["gross_profit"] = (sales.net_sales - sales.cogs).round(2)
    sales["profit_margin"] = (sales.gross_profit / sales.net_sales).round(4)
    pos["delivery_days_late"] = (pos.received_date - pos.promised_date).dt.days.clip(lower=0)
    pos["defect_rate"] = (pos.defect_units / pos.quantity).round(4)
    perf = pos.merge(suppliers[["supplier_id", "supplier_name", "region"]], on="supplier_id").groupby(["supplier_id", "supplier_name", "region"], as_index=False).agg(purchase_orders=("po_id", "count"), late_delivery_rate=("delivery_days_late", lambda x: (x > 0).mean()), avg_days_late=("delivery_days_late", "mean"), defect_rate=("defect_rate", "mean"))
    product_cost = pos.groupby("product_id").unit_cost.mean().rename("mean_product_cost")
    pos = pos.join(product_cost, on="product_id")
    variance = pos.assign(price_variance=(pos.unit_cost - pos.mean_product_cost).abs() / pos.mean_product_cost).groupby("supplier_id").price_variance.mean().rename("price_variance")
    concentration = pos.groupby("supplier_id").quantity.sum().div(pos.quantity.sum()).rename("concentration_exposure")
    perf = perf.join(variance, on="supplier_id").join(concentration, on="supplier_id")
    perf["supplier_risk_score"] = (100 * (.35 * perf.late_delivery_rate + .30 * (perf.defect_rate / max(perf.defect_rate.max(), .001)) + .20 * (perf.price_variance / perf.price_variance.max()) + .15 * (perf.concentration_exposure / perf.concentration_exposure.max()))).round(1)
    perf["risk_band"] = pd.cut(perf.supplier_risk_score, [-1, 35, 60, 100], labels=["Low", "Moderate", "High"])
    monthly = sales.assign(month=sales.order_date.dt.to_period("M").dt.to_timestamp()).groupby(["month", "product_id", "category"], as_index=False).agg(units_sold=("quantity", "sum"), net_sales=("net_sales", "sum"), gross_profit=("gross_profit", "sum"), cogs=("cogs", "sum"))
    inventory = monthly.groupby("product_id", as_index=False).agg(annualized_cogs=("cogs", "sum"), avg_monthly_units=("units_sold", "mean")).merge(products[["product_id", "unit_cost"]], on="product_id")
    inventory["avg_inventory_value"] = (inventory.avg_monthly_units * inventory.unit_cost * 1.5).round(2)
    inventory["inventory_turnover"] = (inventory.annualized_cogs / inventory.avg_inventory_value).round(2)
    forecast = build_forecast(sales, products)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for name, table in {"fact_sales":sales, "fact_purchase_orders":pos, "dim_products":products, "dim_suppliers":suppliers, "supplier_performance":perf, "monthly_operations":monthly, "inventory_metrics":inventory, "demand_forecast":forecast}.items(): table.to_csv(PROCESSED / f"{name}.csv", index=False)
    print(f"Momentum pipeline complete: {len(sales):,} sales lines and {len(pos):,} purchase orders processed.")

if __name__ == "__main__": run()
