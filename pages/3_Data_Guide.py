import streamlit as st


st.set_page_config(
    page_title="Data Guide | Momentum",
    page_icon="◒",
    layout="wide",
)

st.title("Data Guide")
st.caption("What sits behind each part of the application")

st.subheader("Operational source model")
st.dataframe(
    {
        "Table": [
            "Products",
            "Suppliers",
            "Product suppliers",
            "Sales orders",
            "Sales order lines",
            "Purchase orders",
        ],
        "Business purpose": [
            "Product catalog, commercial values, and inventory policy",
            "Supplier profile, region, lead time, and payment terms",
            "Product-to-supplier sourcing relationship",
            "Order date, customer segment, and sales channel",
            "SKU, quantity, selling price, and discount detail",
            "Receipt timing, purchased quantity, cost, and defects",
        ],
    },
    hide_index=True,
    use_container_width=True,
)

st.divider()

st.subheader("Analytics outputs")
st.dataframe(
    {
        "Output": [
            "Sales fact",
            "Purchase-order fact",
            "Monthly operations",
            "Inventory metrics",
            "Supplier performance",
            "Demand forecast",
        ],
        "Used for": [
            "Revenue, margin, category, channel, and customer analysis",
            "Delivery, quality, pricing, and procurement analysis",
            "Time-series and product trend reporting",
            "Inventory value and turnover analysis",
            "Supplier comparison and composite risk scoring",
            "30-day demand, on-hand estimates, and stockout flags",
        ],
    },
    hide_index=True,
    use_container_width=True,
)

st.divider()

st.subheader("Demonstration scope")
volume_1, volume_2, volume_3, volume_4 = st.columns(4)
volume_1.metric("Sales lines", "11,158")
volume_2.metric("Purchase orders", "1,500")
volume_3.metric("Products", "60")
volume_4.metric("Suppliers", "8")

st.write(
    "The source generator uses a fixed random seed. Each clean run produces the "
    "same records and reporting outputs, making results repeatable for testing, "
    "review, and portfolio demonstrations."
)

st.subheader("Production evolution")
st.markdown(
    """
For a live manufacturing environment, the generated source files would be
replaced with scheduled extracts from an ERP, purchasing platform, warehouse
management system, or operational MySQL database. The same transformation and
reporting layers can then be adapted to validated production feeds.
"""
)

