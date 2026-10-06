VS Code içinde oluşturduğun **`README.md`** dosyasının içine hiçbir değişiklik yapmadan, direkt kopyalayıp yapıştırabileceğin tam ve eksiksiz metin aşağıdadır:

```markdown
# Personal Budget Tracker

A desktop budget tracker built with Python, Tkinter, and Matplotlib. It stores data locally as JSON.

## Features

- Record income and expenses with a category, date, and currency.
- Review transaction history, search it, and filter by type, category, or date range.
- Edit or delete transactions, rename expense categories, and export transactions to CSV.
- Set monthly spending limits for categories and see spent and remaining amounts.
- Create monthly recurring transactions. Due entries are added when the app starts; deleting a generated entry also stops its recurring schedule.
- Review totals, charts, and month-to-date spending guidance.
- Choose a theme, language, and display currency.
- Keep a previous-data backup at `data.json.bak` whenever transaction data is saved; recover from it if the main JSON file is missing or invalid.

## Money Guidance

The planning tab uses the 50/30/20 guideline as a flexible starting point: up to 50% for needs, 30% for wants (including dining out), and 20% for savings or debt repayment. Groceries and dining out are different categories. It also reports the current month's expense-to-income ratio and gives a basic prompt based on that ratio.

These are general budgeting ideas, not individualized financial advice. The app does not recommend a fixed percentage of money for stocks; investing depends on goals, timeline, emergency savings, debts, and risk tolerance.

## Install And Run

Python 3.12 or later and Matplotlib are required.

```powershell
python -m pip install matplotlib
python .\budget-tracker.py
```

## Build A Windows Executable

Install PyInstaller in the same Python environment as the app, then build a single-file GUI executable:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --icon .\budget-tracker.ico --add-data ".\budget-tracker.ico;." --name BudgetTracker .\budget-tracker.py
```

The executable will be written to `dist\BudgetTracker.exe`. Keep it in a folder where the app can write `data.json` and `settings.json`.

## Run Tests

```powershell
python -m unittest discover -s tests
```

## Data And Currency

`data.json` stores transactions and recurring schedules. `settings.json` stores preferences and category budgets. Existing records without currency metadata are treated as using the currency selected in settings when they are first loaded.

Changing the display currency does not rewrite the original transaction amounts. Converted totals use the most recently available exchange rates, so displayed conversions can change when rates refresh; the stored amount and its currency remain unchanged. Keep a separate copy of your data files for an off-device backup.