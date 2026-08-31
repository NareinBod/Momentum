from pathlib import Path
import sys
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from momentum.pipeline import run
from momentum.simulator import simulate_reorder


class MomentumPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run()
        cls.processed = ROOT / "data" / "processed"
        cls.sales = pd.read_csv(cls.processed / "fact_sales.csv")
        cls.forecast = pd.read_csv(cls.processed / "demand_forecast.csv")
        cls.products = pd.read_csv(cls.processed / "dim_products.csv")
        cls.suppliers = pd.read_csv(cls.processed / "supplier_performance.csv")
        cls.inventory = pd.read_csv(cls.processed / "inventory_metrics.csv")

    def test_transaction_volume_and_financial_math(self):
        self.assertGreater(len(self.sales), 5_000)
        self.assertTrue((self.sales.quantity > 0).all())
        self.assertTrue((self.sales.net_sales > 0).all())
        expected = (self.sales.net_sales - self.sales.cogs).round(2)
        pd.testing.assert_series_equal(self.sales.gross_profit, expected, check_names=False)

    def test_forecast_covers_product_catalog(self):
        self.assertEqual(len(self.forecast), len(self.products))
        self.assertTrue((self.forecast.forecast_units >= 0).all())
        self.assertTrue((self.forecast.days_to_stockout >= 0).all())

    def test_reorder_scenario_has_required_outputs(self):
        result = simulate_reorder(self.forecast, self.products, reorder_quantity=120, lead_time_days=21)
        self.assertEqual(len(result), len(self.products))
        self.assertTrue((result.reorder_value > 0).all())
        self.assertTrue(set(result.scenario_status).issubset({"At risk", "Covered"}))

    def test_operational_metrics_are_in_expected_ranges(self):
        self.assertTrue(self.suppliers.supplier_risk_score.between(0, 100).all())
        self.assertTrue(self.suppliers.risk_band.notna().all())
        self.assertTrue((self.inventory.inventory_turnover > 0).all())
        self.assertTrue((self.sales.profit_margin < 1).all())


if __name__ == "__main__":
    unittest.main()
