import streamlit as st


st.set_page_config(
    page_title="Methodology | Momentum",
    page_icon="◒",
    layout="wide",
)

st.title("Methodology")
st.caption("Transparent definitions behind the operational signals")

st.subheader("Core business metrics")
metric_1, metric_2 = st.columns(2)

with metric_1:
    st.markdown("#### Profit margin")
    st.code("(Net sales − cost of goods sold) ÷ net sales", language=None)
    st.write(
        "Net sales reflects discounts, while cost of goods sold is based on the "
        "product unit cost and quantity sold."
    )

with metric_2:
    st.markdown("#### Inventory turnover")
    st.code("Annualized cost of goods sold ÷ average inventory value", language=None)
    st.write(
        "The metric indicates how efficiently inventory investment supports demand. "
        "Higher turnover is generally more efficient, but extremely high turnover "
        "can signal insufficient buffer stock."
    )

st.divider()

st.subheader("Supplier Risk Score")
st.write(
    "The score combines four normalized risk dimensions on a 0–100 scale. Higher "
    "values indicate greater operational exposure."
)

risk_components = {
    "Late-delivery rate": "35%",
    "Quality defect rate": "30%",
    "Purchase-price variance": "20%",
    "Supplier concentration": "15%",
}

for label, weight in risk_components.items():
    st.write(f"**{weight} — {label}**")

st.caption(
    "The weighting favors continuity and product quality because delays and defects "
    "have the most direct impact on manufacturing availability."
)

st.divider()

st.subheader("Demand and shortage logic")
st.markdown(
    """
Demand is aggregated by SKU and week. Recent periods receive greater weight, and
the recent direction of demand is incorporated into a 30-day estimate. The model
then compares expected daily demand with estimated on-hand inventory to calculate
days to stockout.

The reorder scenario applies two user-controlled assumptions:

- **Reorder quantity** — units expected to arrive in the replenishment order.
- **Lead time** — days before the replenishment becomes available.

Demand expected during lead time is deducted from available inventory. The
result shows projected stock at arrival, potential shortage units, scenario
status, and the associated inventory investment.
"""
)

st.warning(
    "Forecasts are planning estimates, not guarantees. A production deployment "
    "should add seasonality testing, forecast-error monitoring, service-level "
    "targets, and live inventory balances."
)

