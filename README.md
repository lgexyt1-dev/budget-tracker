VS Code içinde oluşturduğun **`README.md`** dosyasının içine hiçbir değişiklik yapmadan, direkt kopyalayıp yapıştırabileceğin tam ve eksiksiz metin aşağıdadır:

```markdown
# Personal Budget Tracker (CLI)

A feature-packed, interactive Command-Line Interface (CLI) application built in Python for tracking personal finances, managing expense categories, persisting transaction history, and generating visual data analytics using Matplotlib.

---

## Key Features

- **Income & Categorical Expense Logging:** Record incomes and categorize expenses (e.g., Food, Rent, Utilities) with automatic input normalization.
- **Dynamic Financial Reporting:** View a concise summary of total incomes, total expenses, and your current net balance.
- **Visual Analytics (Matplotlib):**
  - **Income vs. Expense Chart:** Interactive pie chart illustrating total balance distribution.
  - **Category Breakdown Chart:** Visual distribution of spending across custom categories.
- **Category Editing:** Batch update existing expense category names to correct typos or reorganize budgets without losing transaction values.
- **Persistent Local Storage:** Automatic JSON persistence (`data.json`) ensures all financial records remain safe across app restarts.
- **Robust Error Handling:** Integrated `try-except` validation prevents application crashes from invalid inputs.
- **System Reset Utility:** Administrative reset option featuring confirmation safety prompts for clearing system state.

---

## Tech Stack

- **Language:** Python 3.12+
- **Data Visualization:** Matplotlib
- **Data Persistence:** JSON
- **Environment:** Cross-platform CLI (Windows / macOS / Linux)

---

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/lgexyt1-dev/budget-tracker.git](https://github.com/lgexyt1-dev/budget-tracker.git)
   cd budget-tracker

```

2. **Install Dependencies**
```bash
pip install matplotlib

```


3. **Run the Application**
```bash
python budget-tracker.py

```



---

## How to Use

Launch the application and select options from the interactive terminal menu:

```text
--- PERSONAL BUDGET TRACKER ---
1. Add Income
2. Add Expense
3. View Financial Report
4. View Income vs Expense Chart
5. View Expense Breakdown by Category
6. Edit Expense Category
7. Exit
8. Reset System

```

* **Option 1 & 2:** Enter transaction amounts and specify categories.
* **Option 3:** Inspect total income, expenses, and net balance.
* **Option 4 & 5:** Generate real-time Matplotlib graphical distributions.
* **Option 6:** Rename an existing expense category across all matching historical entries.
* **Option 7:** Exit the application safely.
* **Option 8:** Permanently purge `data.json` and reset session variables.

---

## Data Structure

Transactions are preserved in `data.json` with the following schema:

```json
{
    "incomes": [1500.0, 300.0],
    "expenses": [
        {
            "amount": 45.5,
            "category": "Food"
        },
        {
            "amount": 120.0,
            "category": "Utilities"
        }
    ]
}

```

```

<ElicitationsGroup message="README kaydedildikten sonraki adım:">
  <Elicitation label="Depoyu oluşturdum ve Git komutlarını çalıştırıp projeyi gönderelim" query="README.md dosyasını kaydettim, şimdi projeyi GitHub'a pushlayalım."/>
</ElicitationsGroup>

```