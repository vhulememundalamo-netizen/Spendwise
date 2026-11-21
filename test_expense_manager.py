import tempfile
import unittest
from pathlib import Path

from expense import Expense
from expense_manager import ExpenseManager


class ExpenseManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_name = str(Path(self.temp_dir.name) / "test_expenses.json")
        self.manager = ExpenseManager(self.file_name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_reload_expense(self):
        expense = Expense("Lunch", 65.50, "Food", "2026-11-21")
        self.manager.add(expense)

        new_manager = ExpenseManager(self.file_name)
        self.assertEqual(len(new_manager.get_all()), 1)
        self.assertEqual(new_manager.get_all()[0].description, "Lunch")

    def test_total_spending(self):
        self.manager.add(Expense("Lunch", 50, "Food", "2026-11-21"))
        self.manager.add(Expense("Taxi", 30, "Transport", "2026-11-21"))
        self.assertEqual(self.manager.total_spending(), 80)

    def test_delete_expense(self):
        expense = Expense("Book", 120, "Education", "2026-11-21")
        self.manager.add(expense)
        self.assertTrue(self.manager.delete(expense.id))
        self.assertEqual(len(self.manager.get_all()), 0)


if __name__ == "__main__":
    unittest.main()
