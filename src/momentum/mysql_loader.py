"""Optional MySQL loader for generated Momentum source data."""
import os
from pathlib import Path
import mysql.connector
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

def load_mysql():
    connection = mysql.connector.connect(
        host=os.getenv("MOMENTUM_DB_HOST", "localhost"),
        port=int(os.getenv("MOMENTUM_DB_PORT", "3306")),
        user=os.getenv("MOMENTUM_DB_USER", "root"),
        password=os.getenv("MOMENTUM_DB_PASSWORD", ""),
        database=os.getenv("MOMENTUM_DB_NAME", "momentum"),
    )
    cursor = connection.cursor()
    tables = ["suppliers", "products", "product_suppliers", "sales_orders", "sales_order_lines", "purchase_orders"]
    for table in tables:
        frame = pd.read_csv(RAW / f"{table}.csv").where(pd.notna, None)
        columns = list(frame.columns)
        statement = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['%s'] * len(columns))})"
        cursor.executemany(statement, list(frame.itertuples(index=False, name=None)))
    connection.commit()
    cursor.close()
    connection.close()
    print("Momentum source data loaded into MySQL.")

if __name__ == "__main__":
    load_mysql()
