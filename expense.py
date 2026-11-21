from dataclasses import dataclass, asdict
from uuid import uuid4


@dataclass
class Expense:
    description: str
    amount: float
    category: str
    date: str
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())

        self.description = self.description.strip()
        self.category = self.category.strip()

        if not self.description:
            raise ValueError("Expense description cannot be empty.")
        if not self.category:
            raise ValueError("Expense category cannot be empty.")
        if self.amount <= 0:
            raise ValueError("Expense amount must be greater than zero.")

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data["description"],
            amount=float(data["amount"]),
            category=data["category"],
            date=data["date"],
            id=data.get("id", ""),
        )
