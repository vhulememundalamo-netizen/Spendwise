# SpendWise – Personal Expense Tracker

A Python and Flet capstone project for recording and reviewing personal expenses.

## Features

- Dashboard with total spending, transaction count and recent expenses.
- Add expenses with description, amount, category and date.
- View and delete recorded transactions.
- Category spending report with percentage bars.
- JSON file storage so records remain available after restarting the app.
- Input validation and error handling.
- Route-based views for Dashboard, Add Expense, History and Reports.

## Requirements

- Python 3.10 or later (use a Python version supported by your installed Flet release).
- Flet.

## Setup on Windows

Open Command Prompt in this project folder and run:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run as a desktop app

```bat
flet run main.py
```

## Run in a web browser

```bat
flet run --web main.py
```

## Run tests

```bat
python -m unittest -v
```

## Project files

- `main.py`: Flet user interface and navigation.
- `expense.py`: Expense data model (class).
- `expense_manager.py`: JSON file handling and expense operations.
- `expenses.json`: saved expense records.
- `test_expense_manager.py`: automated tests.

## Notes

The starter version stores data in a local JSON file. This is suitable for demonstrating file handling in a learning project, but it is not a shared cloud database. For a deployed multi-user app, use a secure backend/database and user authentication.
