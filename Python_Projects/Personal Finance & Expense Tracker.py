import os
from datetime import datetime

INCOME_FILE = "income.txt"
EXPENSE_FILE = "expenses.txt"


# ------------------ Utility Functions ------------------ #
def read_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return file.readlines()


def write_file(filename, data):
    with open(filename, "w") as file:
        file.writelines(data)


def validate_amount(amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date format should be YYYY-MM-DD")


# ------------------ Income Functions ------------------ #
def add_income():
    try:
        source = input("Enter income source: ")
        amount = float(input("Enter income amount: "))
        validate_amount(amount)

        with open(INCOME_FILE, "a") as file:
            file.write(f"{source},{amount}\n")

        print("✅ Income added successfully")

    except Exception as e:
        print("❌ Error:", e)


def calculate_total_income():
    incomes = read_file(INCOME_FILE)
    total = 0
    for line in incomes:
        total += float(line.strip().split(",")[1])
    return total


# ------------------ Expense Functions ------------------ #
def add_expense():
    try:
        category = input("Enter expense category: ")
        amount = float(input("Enter expense amount: "))
        validate_amount(amount)

        date = input("Enter date (YYYY-MM-DD): ")
        validate_date(date)

        note = input("Enter note (optional): ")

        with open(EXPENSE_FILE, "a") as file:
            file.write(f"{category},{amount},{date},{note}\n")

        print("✅ Expense added successfully")

    except Exception as e:
        print("❌ Error:", e)


def view_expenses():
    expenses = read_file(EXPENSE_FILE)
    if not expenses:
        print("No expenses found")
        return

    print("\n--- Expenses ---")
    for index, line in enumerate(expenses):
        category, amount, date, note = line.strip().split(",")
        print(f"{index}. {category} | ₹{amount} | {date} | {note}")


def delete_expense():
    view_expenses()
    try:
        expenses = read_file(EXPENSE_FILE)
        index = int(input("Enter expense index to delete: "))
        expenses.pop(index)
        write_file(EXPENSE_FILE, expenses)
        print("✅ Expense deleted")
    except Exception:
        print("❌ Invalid index")


def update_expense():
    view_expenses()
    try:
        expenses = read_file(EXPENSE_FILE)
        index = int(input("Enter expense index to update: "))

        category = input("New category: ")
        amount = float(input("New amount: "))
        validate_amount(amount)

        date = input("New date (YYYY-MM-DD): ")
        validate_date(date)

        note = input("New note: ")

        expenses[index] = f"{category},{amount},{date},{note}\n"
        write_file(EXPENSE_FILE, expenses)

        print("✅ Expense updated")

    except Exception as e:
        print("❌ Error:", e)


def category_summary():
    expenses = read_file(EXPENSE_FILE)
    summary = {}

    for line in expenses:
        category, amount, _, _ = line.strip().split(",")
        summary[category] = summary.get(category, 0) + float(amount)

    print("\n--- Category-wise Expenses ---")
    for cat, amt in summary.items():
        print(f"{cat}: ₹{amt}")


def calculate_total_expense():
    expenses = read_file(EXPENSE_FILE)
    total = 0
    for line in expenses:
        total += float(line.strip().split(",")[1])
    return total


# ------------------ Main Menu ------------------ #
def main_menu():
    while True:
        print("\n==== Personal Finance Tracker ====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Expenses")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Category-wise Expense Summary")
        print("7. Financial Summary")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_expenses()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            category_summary()
        elif choice == "7":
            income = calculate_total_income()
            expense = calculate_total_expense()
            savings = income - expense

            print("\n--- Financial Summary ---")
            print(f"Total Income: ₹{income}")
            print(f"Total Expense: ₹{expense}")
            print(f"Savings: ₹{savings}")

        elif choice == "8":
            print("👋 Exiting... Thank you!")
            break
        else:
            print("❌ Invalid choice")


# ------------------ Program Start ------------------ #
main_menu()
