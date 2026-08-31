import numpy as np
import pandas as pd

def build_forecast(sales: pd.DataFrame, products: pd.DataFrame, horizon_days: int = 30) -> pd.DataFrame:
    sales = sales.copy()
    sales["order_date"] = pd.to_datetime(sales["order_date"])
    cutoff = sales.order_date.max()
    weekly = (sales.assign(week=sales.order_date.dt.to_period("W").dt.start_time)
              .groupby(["product_id", "week"], as_index=False).quantity.sum())
    rows = []
    for product_id, group in weekly.groupby("product_id"):
        values = group.sort_values("week").quantity.tail(12).to_numpy(dtype=float)
        if len(values) < 2: continue
        weights = np.arange(1, len(values)+1)
        base = np.average(values, weights=weights)
        slope = np.polyfit(np.arange(len(values)), values, 1)[0]
        weekly_forecast = max(0, base + slope * 2)
        daily = weekly_forecast / 7
        product = products.loc[products.product_id == product_id].iloc[0]
        current_stock = max(0, int(product.reorder_point + product.safety_stock - sales.loc[(sales.product_id == product_id) & (sales.order_date > cutoff - pd.Timedelta(days=21)), "quantity"].sum() / 3))
        forecast_units = round(daily * horizon_days)
        stockout_days = round(current_stock / daily) if daily > 0 else 999
        rows.append((product_id, cutoff.date(), horizon_days, round(daily, 2), forecast_units, current_stock, stockout_days, stockout_days < horizon_days))
    return pd.DataFrame(rows, columns=["product_id", "forecast_as_of", "horizon_days", "forecast_daily_units", "forecast_units", "estimated_on_hand", "days_to_stockout", "stockout_risk"])
