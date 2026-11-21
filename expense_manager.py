import json
from pathlib import Path
from expense import Expense


class ExpenseManager:
    """Handles adding, reading, deleting and saving expenses as JSON."""

    def __init__(self, file_name="expenses.json"):
        self.file_path = Path(__file__).resolve().parent / file_name
        self.expenses = []
        self.load()

    def load(self):
        """Read saved expenses. Start with an empty list if no file exists."""
        if not self.file_path.exists():
            self.expenses = []
            return

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("The expense file must contain a JSON list.")

            self.expenses = [Expense.from_dict(item) for item in data]
        except json.JSONDecodeError as error:
            raise ValueError(
                "expenses.json is not valid JSON. Restore or correct the file."
            ) from error

    def save(self):
        """Write all current expenses to the JSON file."""
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                [expense.to_dict() for expense in self.expenses],
                file,
                indent=4,
            )

    def add(self, expense):
        if not isinstance(expense, Expense):
            raise TypeError("Only Expense objects can be added.")
        self.expenses.append(expense)
        self.save()

    def get_all(self):
        return list(self.expenses)

    def delete(self, expense_id):
        original_count = len(self.expenses)
        self.expenses = [
            expense for expense in self.expenses if expense.id != expense_id
        ]

        if len(self.expenses) == original_count:
            return False

        self.save()
        return True

    def total_spending(self):
        return sum(expense.amount for expense in self.expenses)

    def totals_by_category(self):
        totals = {}
        for expense in self.expenses:
            totals[expense.category] = (
                totals.get(expense.category, 0) + expense.amount
            )
        return totals
