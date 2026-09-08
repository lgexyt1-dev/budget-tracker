import matplotlib.pyplot as plt
import json
import os

# Save data to JSON file
def save_data(incomes, expenses):
    data = {
        "incomes": incomes,
        "expenses": expenses
    }
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Load data from JSON file
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("incomes", []), data.get("expenses", [])
    else:
        return [], []

# User interface functions
def greet_user():
    user = input("Please enter your name: ").strip().capitalize()
    print(f"Hello, {user}!\n")
    return user

def display_menu():
    print("--- PERSONAL BUDGET TRACKER ---")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Financial Report")
    print("4. View Income vs Expense Chart")
    print("5. View Expense Breakdown by Category")
    print("6. Edit Expense Category")
    print("7. Exit")
    print("8. Reset System")

# Initialize application
user_name = greet_user()
incomes, expenses = load_data()

while True:
    display_menu()
    choice = input("Select an option (1-8): ").strip()
    
    if choice == "1":
        try:
            amount = float(input("Enter income amount: "))
            incomes.append(amount)
            print(f"Successfully added income: ${amount:.2f}\n")
            save_data(incomes, expenses)
        except ValueError:
            print("Error: Invalid input. Please enter a valid numerical value.\n")

    elif choice == "2":
        try:
            amount = float(input("Enter expense amount: "))
            category = input("Enter category (e.g., Food, Rent, Utilities): ").strip().capitalize()

            expenses.append({"amount": amount, "category": category})
            print(f"Successfully added expense of ${amount:.2f} under '{category}'!\n")
            save_data(incomes, expenses)
        except ValueError:
            print("Error: Invalid input. Please enter a valid numerical value.\n")

    elif choice == "3":
        total_income = sum(incomes)
        total_expense = sum(expense['amount'] if isinstance(expense, dict) else expense for expense in expenses)
        net_balance = total_income - total_expense
        
        print("\n--- FINANCIAL REPORT ---")
        print(f"Total Income:  ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Balance:   ${net_balance:.2f}\n")

    elif choice == "4":
        total_income = sum(incomes)
        total_expense = sum(expense['amount'] if isinstance(expense, dict) else expense for expense in expenses)
        
        if total_income == 0 and total_expense == 0:
            print("No transactions recorded yet. Add income or expense first.\n")
        else:
            labels = ['Incomes', 'Expenses']
            values = [total_income, total_expense]
            plt.figure(figsize=(6, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("Overall Income vs Expense Distribution")
            plt.show()

    elif choice == "5":
        category_totals = {}
        for expense in expenses:
            if isinstance(expense, dict):
                cat = expense["category"]
                amt = expense["amount"]
                category_totals[cat] = category_totals.get(cat, 0) + amt

        if not category_totals:
            print("No categorical expenses recorded yet. Add expenses via Option 2 first.\n")
        else:
            labels = list(category_totals.keys())
            values = list(category_totals.values())

            plt.figure(figsize=(6, 6))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("Expense Breakdown by Category")
            plt.show()

    elif choice =="6":
        # Finding available Category
        existing_categories = set(expense["category"] for expense in expenses if isinstance(expense, dict))
        
        if not existing_categories:
            print("No expense categories found to edit.\n")
        else:
            print("\nAvailable Categories:", ", ".join(existing_categories))
            old_category = input("Enter the category name you want to rename: ").strip().capitalize()
            
            if old_category in existing_categories:
                new_category = input(f"Enter the new name for '{old_category}': ").strip().capitalize()

                # Update all expenses that use the old category name.
                updated_count = 0
                for expense in expenses:
                    if (isinstance(expense, dict)
                            and expense.get("category") == old_category):
                        expense["category"] = new_category
                        updated_count += 1

                save_data(incomes, expenses)
                print(
                    f"Updated {updated_count} expense(s) from "
                    f"'{old_category}' to '{new_category}'.\n"
                )
            else:
                print(f"Category '{old_category}' was not found.\n")

    elif choice == "7":
        print("Exiting application... Goodbye!")
        break

    elif choice == "8":
        print("Are you sure you want to reset all data?")
        print("Warning: This action will permanently delete all records.")
        confirm = input("Type 'yes' to confirm (Press Enter to cancel): ").strip().lower()
        
        if confirm == "yes":
            incomes.clear()
            expenses.clear()
            if os.path.exists("data.json"):
                os.remove("data.json")
            print("All system data has been successfully reset!\n")
        else:
            print("Reset operation canceled.\n")

    else:
        print("Invalid choice. Please select a valid option between 1 and 8.\n")