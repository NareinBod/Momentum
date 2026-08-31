# Generated data assets

This directory is created by `python -m momentum.pipeline` and is intentionally excluded from source control. The deterministic source generator creates 5,600 sales orders with 11,000+ order lines, 1,500 purchase orders, 60 products, and eight suppliers.

- `raw/` holds normalized source extracts mirroring the MySQL operational tables.
- `processed/` holds dashboard-ready fact, dimension, metric, and forecast tables.

Running the pipeline again regenerates the same dataset and outputs.
