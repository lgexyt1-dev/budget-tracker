import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "budget-tracker.py"
SPEC = importlib.util.spec_from_file_location("budget_tracker_app", SCRIPT_PATH)
app_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(app_module)


class BudgetTrackerTests(unittest.TestCase):
    def test_bom_prefixed_data_file_loads(self):
        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory) / "data.json"
            payload = json.dumps({
                "incomes": [{"amount": "10.25", "category": "Salary"}],
                "expenses": [],
            }).encode("utf-8")
            data_path.write_bytes(b"\xef\xbb\xbf" + payload)
            with patch.object(app_module, "DATA_FILE", str(data_path)):
                incomes, expenses, recurring = app_module.load_data("USD")

        self.assertEqual(incomes[0]["amount"], "10.25")
        self.assertEqual(expenses, [])
        self.assertEqual(recurring, [])

    def test_bom_prefixed_settings_file_loads(self):
        with tempfile.TemporaryDirectory() as directory:
            settings_path = Path(directory) / "settings.json"
            payload = json.dumps({"theme": "dark"}).encode("utf-8")
            settings_path.write_bytes(b"\xef\xbb\xbf" + payload)
            with patch.object(app_module, "SETTINGS_FILE", str(settings_path)):
                settings = app_module.load_settings()

        self.assertEqual(settings["theme"], "dark")

    def test_legacy_records_keep_amount_and_get_currency_and_id(self):
        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory) / "data.json"
            data_path.write_text(json.dumps({
                "incomes": [{"amount": 125.5, "category": "Salary"}],
                "expenses": [],
            }), encoding="utf-8")
            with patch.object(app_module, "DATA_FILE", str(data_path)):
                incomes, expenses, recurring = app_module.load_data("EUR")

        self.assertEqual(incomes[0]["amount"], 125.5)
        self.assertEqual(incomes[0]["currency"], "EUR")
        self.assertTrue(incomes[0]["id"])
        self.assertEqual(expenses, [])
        self.assertEqual(recurring, [])

    def test_saves_previous_data_as_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory) / "data.json"
            with patch.object(app_module, "DATA_FILE", str(data_path)):
                app_module.save_data([{"amount": "10.00"}], [], [])
                app_module.save_data([{"amount": "20.00"}], [], [{"id": "monthly"}])
                backup = json.loads(Path(str(data_path) + ".bak").read_text(encoding="utf-8"))
                current = json.loads(data_path.read_text(encoding="utf-8"))

        self.assertEqual(backup["incomes"][0]["amount"], "10.00")
        self.assertEqual(current["incomes"][0]["amount"], "20.00")
        self.assertEqual(current["recurring"][0]["id"], "monthly")

    def test_corrupt_data_recovers_from_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory) / "data.json"
            backup_path = Path(str(data_path) + ".bak")
            data_path.write_text("not valid JSON", encoding="utf-8")
            backup_path.write_text(json.dumps({
                "incomes": [{"amount": "42.10", "category": "Salary"}],
                "expenses": [],
            }), encoding="utf-8")
            with patch.object(app_module, "DATA_FILE", str(data_path)):
                incomes, expenses, recurring = app_module.load_data("USD")
            restored = json.loads(data_path.read_text(encoding="utf-8"))

        self.assertEqual(incomes[0]["amount"], "42.10")
        self.assertEqual(expenses, [])
        self.assertEqual(recurring, [])
        self.assertEqual(restored["incomes"][0]["amount"], "42.10")

    def test_decimal_totals_do_not_accumulate_binary_float_error(self):
        total = app_module.get_total_amount([
            {"amount": "0.10"}, {"amount": "0.20"}
        ])

        self.assertEqual(total, app_module.Decimal("0.30"))

    def test_currency_display_does_not_mutate_record(self):
        app = app_module.BudgetTrackerApp.__new__(app_module.BudgetTrackerApp)
        app.currency = "USD"
        app.preferences = {"exchange_rates": {"USD": 1.0, "EUR": 0.9}}
        record = {"amount": "90", "currency": "EUR"}

        self.assertAlmostEqual(app.display_amount(record), 100.0)
        self.assertEqual(record["amount"], "90")

    def test_monthly_schedule_handles_short_months(self):
        self.assertEqual(
            app_module.BudgetTrackerApp.next_month_date(date(2024, 1, 31)),
            date(2024, 2, 29),
        )
        self.assertEqual(
            app_module.BudgetTrackerApp.next_month_date(date(2025, 11, 30)),
            date(2025, 12, 30),
        )

    def test_due_recurring_transaction_is_generated_once(self):
        app = app_module.BudgetTrackerApp.__new__(app_module.BudgetTrackerApp)
        app.currency = "USD"
        app.incomes = []
        app.expenses = []
        app.recurring = [{
            "id": "template-1", "type": "Expense", "amount": 25,
            "currency": "USD", "category": "Streaming",
            "next_date": date.today().replace(day=1).isoformat(),
        }]
        app.persist_data = lambda: None

        app.process_recurring_transactions()
        first_run_count = len(app.expenses)
        app.process_recurring_transactions()

        self.assertEqual(first_run_count, 1)
        self.assertEqual(len(app.expenses), 1)
        self.assertEqual(app.expenses[0]["recurring_id"], "template-1")


if __name__ == "__main__":
    unittest.main()