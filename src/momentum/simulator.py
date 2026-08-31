import pandas as pd

def simulate_reorder(forecast: pd.DataFrame, products: pd.DataFrame, reorder_quantity: int, lead_time_days: int) -> pd.DataFrame:
    base = forecast.merge(products[["product_id", "sku", "product_name", "unit_cost", "safety_stock"]], on="product_id")
    base["reorder_quantity"] = reorder_quantity
    base["lead_time_days"] = lead_time_days
    base["demand_during_lead_time"] = (base.forecast_daily_units * lead_time_days).round().astype(int)
    base["projected_stock_at_arrival"] = base.estimated_on_hand + reorder_quantity - base.demand_during_lead_time
    base["shortage_units"] = (base.safety_stock - base.projected_stock_at_arrival).clip(lower=0)
    base["scenario_status"] = base.shortage_units.map(lambda x: "At risk" if x > 0 else "Covered")
    base["reorder_value"] = (base.reorder_quantity * base.unit_cost).round(2)
    return base.sort_values(["shortage_units", "reorder_value"], ascending=[False, False])
