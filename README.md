# Momentum

Momentum is an operations and manufacturing analytics workspace for turning transactional activity into inventory and supplier decisions.

It includes a normalized MySQL schema, a reproducible Pandas ETL workflow over 5,000+ records, business metrics, demand forecasts, a reorder scenario simulator, and Power BI-ready reporting tables.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python -m momentum.pipeline
streamlit run app.py
```

The pipeline generates source files in `data/raw/` and analysis-ready tables in `data/processed/`. No external data is required.

To load the normalized source data into MySQL, first execute `sql/schema.sql`, set the values in `.env.example` as environment variables, then run `python -m momentum.mysql_loader`.

## Project map

- `sql/schema.sql` — normalized MySQL operational model
- `src/momentum/pipeline.py` — extraction, cleaning, transformations, and metrics
- `src/momentum/forecasting.py` — demand forecast and stockout flags
- `src/momentum/simulator.py` — what-if reorder analysis
- `app.py` — decision-facing interactive dashboard
- `pages/` — About, Methodology, and Data Guide pages for the deployed application
- `powerbi/` — model relationships, DAX measures, and 3-page report blueprint
- `tests/` — repeatable checks for ETL, metrics, forecast coverage, and reorder scenarios
- `DEPLOYMENT.md` — recommended public and production deployment paths

## Business definitions

Profit margin is `(net sales - COGS) / net sales`. Inventory turnover uses annualized COGS divided by average inventory value. Supplier Risk Score is a 0–100 composite of late delivery, quality defects, price variance, and concentration exposure; higher is riskier.

## Quality checks

```powershell
python -m unittest discover -s tests -v
```

The checks confirm the transaction volume, financial calculations, full catalog forecast coverage, and the scenario output contract.
