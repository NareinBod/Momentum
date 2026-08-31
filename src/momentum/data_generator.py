from pathlib import Path
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

def generate_raw_data(output_dir: Path) -> None:
    """Create a deterministic, business-plausible transactional source set."""
    output_dir.mkdir(parents=True, exist_ok=True)
    suppliers = pd.DataFrame([
        (1, "Apex Components", "North America", 12, 30), (2, "Nordic Precision", "Europe", 20, 45),
        (3, "Pacific Materials", "Asia Pacific", 34, 60), (4, "ForgeWorks", "North America", 16, 30),
        (5, "Meridian Industrial", "Europe", 25, 45), (6, "Vertex Supply", "Asia Pacific", 40, 60),
        (7, "Cobalt Manufacturing", "North America", 18, 30), (8, "Kestrel Parts", "Europe", 22, 45),
    ], columns=["supplier_id", "supplier_name", "region", "lead_time_days", "payment_terms_days"])
    categories = ["Motion", "Controls", "Power Systems", "Hydraulics", "Safety"]
    product_rows = []
    for i in range(1, 61):
        cost = round(float(RNG.uniform(18, 260)), 2)
        product_rows.append((i, f"MOM-{i:03d}", f"{categories[(i-1)%5]} Component {i:02d}", categories[(i-1)%5], cost, round(cost * RNG.uniform(1.38, 1.9), 2), int(RNG.integers(35, 120)), int(RNG.integers(15, 55))))
    products = pd.DataFrame(product_rows, columns=["product_id", "sku", "product_name", "category", "unit_cost", "unit_price", "reorder_point", "safety_stock"])
    primary = ((products.product_id - 1) % len(suppliers) + 1).astype(int)
    product_suppliers = pd.DataFrame({"product_id": products.product_id, "supplier_id": primary, "is_primary": 1})
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    order_rows, line_rows, line_id = [], [], 1
    for order_id in range(100001, 105601):
        date = dates[int(RNG.integers(0, len(dates)))]
        order_rows.append((order_id, date.date(), RNG.choice(["Enterprise", "Mid-Market", "SMB"], p=[.35,.4,.25]), RNG.choice(["Direct", "Distributor", "E-commerce"], p=[.5,.35,.15])))
        for product_id in RNG.choice(products.product_id, size=int(RNG.integers(1, 4)), replace=False):
            price = float(products.loc[products.product_id == product_id, "unit_price"].iloc[0])
            line_rows.append((line_id, order_id, product_id, int(RNG.integers(2, 24)), round(price * RNG.uniform(.96, 1.04), 2), round(float(RNG.choice([0,.03,.05,.08], p=[.62,.18,.13,.07])), 2)))
            line_id += 1
    orders = pd.DataFrame(order_rows, columns=["order_id", "order_date", "customer_segment", "channel"])
    lines = pd.DataFrame(line_rows, columns=["order_line_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"])
    po_rows, po_id = [], 700001
    for month in pd.date_range("2023-12-01", "2025-12-01", freq="MS"):
        for product_id in products.product_id:
            supplier_id = int(product_suppliers.loc[product_suppliers.product_id == product_id, "supplier_id"].iloc[0])
            lead = int(suppliers.loc[suppliers.supplier_id == supplier_id, "lead_time_days"].iloc[0])
            ordered = month + pd.Timedelta(days=int(RNG.integers(0, 15)))
            promised = ordered + pd.Timedelta(days=lead)
            late = max(0, int(RNG.normal(2 if supplier_id in [3,6] else 0, 4)))
            received = promised + pd.Timedelta(days=late)
            cost = float(products.loc[products.product_id == product_id, "unit_cost"].iloc[0])
            qty = int(RNG.integers(70, 240))
            po_rows.append((po_id, supplier_id, product_id, ordered.date(), promised.date(), received.date(), qty, round(cost * RNG.uniform(.94, 1.12), 2), int(RNG.binomial(qty, .025 if supplier_id in [3,6] else .009))))
            po_id += 1
    pos = pd.DataFrame(po_rows, columns=["po_id", "supplier_id", "product_id", "ordered_date", "promised_date", "received_date", "quantity", "unit_cost", "defect_units"])
    for name, frame in {"suppliers":suppliers, "products":products, "product_suppliers":product_suppliers, "sales_orders":orders, "sales_order_lines":lines, "purchase_orders":pos}.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)
