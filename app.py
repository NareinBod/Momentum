from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))
from momentum.simulator import simulate_reorder
from momentum.pipeline import run as run_pipeline

st.set_page_config(page_title="Momentum | Operations Intelligence", page_icon="◒", layout="wide")
DATA = Path(__file__).parent / "data" / "processed"

def ensure_data():
    """Make the dashboard usable on a fresh checkout without manual staging."""
    required = ["fact_sales.csv", "supplier_performance.csv", "demand_forecast.csv"]
    if not all((DATA / name).exists() for name in required):
        run_pipeline()

ensure_data()

@st.cache_data
def load(name):
    return pd.read_csv(DATA / f"{name}.csv")

sales, suppliers, products = load("fact_sales"), load("supplier_performance"), load("dim_products")
forecast, inventory = load("demand_forecast"), load("inventory_metrics")
st.title("Momentum")
st.caption("Operations intelligence for inventory and supplier decisions")
page = st.sidebar.radio("Workspace", ["Executive overview", "Supplier risk", "Reorder simulator"])

if page == "Executive overview":
    revenue, profit = sales.net_sales.sum(), sales.gross_profit.sum()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Net sales", f"${revenue:,.0f}")
    c2.metric("Gross margin", f"{profit / revenue:.1%}")
    c3.metric("Average inventory turns", f"{inventory.inventory_turnover.mean():.1f}x")
    c4.metric("Products at stockout risk", int(forecast.stockout_risk.sum()))
    monthly = sales.assign(month=pd.to_datetime(sales.order_date).dt.to_period("M").dt.to_timestamp()).groupby("month", as_index=False).agg(net_sales=("net_sales","sum"), gross_profit=("gross_profit","sum"))
    st.plotly_chart(px.line(monthly, x="month", y=["net_sales", "gross_profit"], title="Revenue and gross profit trend", labels={"value":"USD", "month":"Month"}), use_container_width=True)
    risks = forecast.merge(products[["product_id","sku","product_name"]], on="product_id").query("stockout_risk == True").sort_values("days_to_stockout")
    st.subheader("Inventory exceptions")
    st.dataframe(risks[["sku","product_name","forecast_units","estimated_on_hand","days_to_stockout"]], hide_index=True, use_container_width=True)
elif page == "Supplier risk":
    st.subheader("Supplier risk profile")
    st.plotly_chart(px.bar(suppliers.sort_values("supplier_risk_score"), x="supplier_risk_score", y="supplier_name", color="risk_band", orientation="h", title="Supplier Risk Score (higher = more exposure)", color_discrete_map={"Low":"#3A9D72","Moderate":"#E6A23C","High":"#C84B4B"}), use_container_width=True)
    st.dataframe(suppliers[["supplier_name","region","supplier_risk_score","risk_band","late_delivery_rate","defect_rate","price_variance"]].sort_values("supplier_risk_score", ascending=False), hide_index=True, use_container_width=True)
else:
    st.subheader("What-if reorder simulator")
    st.caption("Test a uniform reorder quantity and supplier lead time against the 30-day demand forecast.")
    a,b=st.columns(2)
    quantity=a.slider("Reorder quantity per SKU", 25, 400, 120, 5)
    lead_time=b.slider("Assumed lead time (days)", 5, 60, 21)
    scenario=simulate_reorder(forecast, products, quantity, lead_time)
    st.metric("Scenario inventory investment", f"${scenario.reorder_value.sum():,.0f}")
    st.dataframe(scenario[["sku","product_name","forecast_daily_units","estimated_on_hand","demand_during_lead_time","projected_stock_at_arrival","shortage_units","scenario_status","reorder_value"]], hide_index=True, use_container_width=True)
