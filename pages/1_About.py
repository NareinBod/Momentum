import streamlit as st


st.set_page_config(
    page_title="About | Momentum",
    page_icon="◒",
    layout="wide",
)

st.title("About Momentum")
st.caption("From operational transactions to confident inventory decisions")

st.markdown(
    """
Momentum is a manufacturing operations analytics project built to connect the
parts of the business that are often reviewed separately: commercial
performance, supplier reliability, and inventory availability.

The application converts sales and purchasing activity into a focused set of
decision signals. Leaders can see where margin is being generated, which
suppliers introduce the most operational exposure, and which products may
require intervention before demand exceeds available stock.
"""
)

st.divider()

st.subheader("What the platform helps answer")
left, middle, right = st.columns(3)

with left:
    st.markdown("#### Protect margin")
    st.write(
        "Track net sales, gross profit, and product-level margin after discounts "
        "and cost of goods sold."
    )

with middle:
    st.markdown("#### Manage supplier exposure")
    st.write(
        "Compare delivery, quality, pricing, and concentration risk through one "
        "explainable supplier score."
    )

with right:
    st.markdown("#### Anticipate shortages")
    st.write(
        "Use recent demand behavior, stock estimates, and scenario assumptions "
        "to identify potential inventory gaps."
    )

st.divider()

st.subheader("How Momentum works")
st.markdown(
    """
1. **Organize** — Products, suppliers, sales orders, order lines, and purchase
   orders are maintained in a normalized relational structure.
2. **Prepare** — A repeatable data pipeline validates, cleans, joins, and enriches
   the transactional records.
3. **Measure** — Business metrics translate activity into profitability,
   inventory efficiency, and supplier risk indicators.
4. **Predict** — SKU-level demand estimates highlight products that may run out
   within the planning horizon.
5. **Decide** — The reorder simulator lets users test quantity and lead-time
   assumptions before committing working capital.
"""
)

st.info(
    "Momentum uses a deterministic demonstration dataset so the project remains "
    "reproducible and safe to share. It is designed as a portfolio and decision-"
    "support demonstration, not as a live production purchasing system."
)

