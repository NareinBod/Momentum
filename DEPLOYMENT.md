# Deploying Momentum

## Recommended public deployment: Streamlit Community Cloud

This is the best first deployment for the portfolio version because the application is already built with Streamlit, uses a small reproducible dataset, and does not require a persistent production database.

1. Push the repository to GitHub. Keep `.env`, database credentials, `.venv`, generated CSV files, and local cache files out of version control.
2. Sign in at `share.streamlit.io` with GitHub and choose **Create app**.
3. Select the repository and branch, then set the entry point to `app.py`.
4. Choose Python 3.12 in Advanced settings.
5. Select a short custom subdomain, such as `momentum-operations` if it is available.
6. Deploy and review the build logs. The application will generate its demonstration data during its first start.

No database credentials are required for the public demonstration. The included MySQL schema and loader are architectural deliverables and can be demonstrated separately.

## When to choose a managed web service instead

Use Render, Azure App Service, AWS, or another container/web-service platform when Momentum needs persistent storage, private networking, scheduled ETL, authentication beyond repository-based access, a live MySQL connection, service-level monitoring, or guaranteed availability without Community Cloud hibernation.

For that production-style deployment, separate the ETL from the web process, run it on a schedule, store processed data in durable storage, and give the dashboard read-only database credentials through the platform's secret manager.

## Pre-deployment checklist

- All tests pass with `python -m unittest discover -s tests -v`.
- `requirements.txt` remains at the repository root beside `app.py`.
- Generated CSVs are not committed; the first-run pipeline recreates them.
- No credentials or local `.env` files are committed.
- The app is tested from a clean checkout using Python 3.12.
- The deployed About and Methodology pages clearly identify the data as a reproducible demonstration.

