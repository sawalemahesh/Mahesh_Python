# -------------------------------
# Bank Transaction Management System
# -------------------------------

customers = {}

# -------------------------------
# 1. Add New Customer
# -------------------------------
def add_customer(customer_id, name, mobile):
    if customer_id in customers:
        print("Customer ID already exists!")
        return

    customers[customer_id] = {
        "name": name,
        "mobile": mobile,
        "accounts": []
    }
    print("Customer added successfully!")


# -------------------------------
# 2. Add Account to Customer
# -------------------------------
def add_account(customer_id, account_no, account_type, balance):
    if customer_id not in customers:
        print("Customer not found!")
        return

    if balance < 1000:
        print("Initial balance must be at least ₹1000")
        return

    # Check for duplicate account number
    for acc in customers[customer_id]["accounts"]:
        if acc[0] == account_no:
            print("Account number already exists!")
            return

    account = (account_no, account_type, balance)
    customers[customer_id]["accounts"].append(account)
    print("Account added successfully!")


# -------------------------------
# 3. Deposit Money
# -------------------------------
def deposit(customer_id, account_no, amount):
    if amount <= 0:
        print("Deposit amount must be positive!")
        return

    for i, acc in enumerate(customers.get(customer_id, {}).get("accounts", [])):
        if acc[0] == account_no:
            new_balance = acc[2] + amount
            customers[customer_id]["accounts"][i] = (acc[0], acc[1], new_balance)
            print(f"₹{amount} deposited successfully!")
            return

    print("Account not found!")


# -------------------------------
# 4. Withdraw Money
# -------------------------------
def withdraw(customer_id, account_no, amount):
    if amount <= 0:
        print("Withdrawal amount must be positive!")
        return

    for i, acc in enumerate(customers.get(customer_id, {}).get("accounts", [])):
        if acc[0] == account_no:
            if acc[2] - amount < 1000:
                print("Insufficient balance! Minimum ₹1000 required.")
                return
            new_balance = acc[2] - amount
            customers[customer_id]["accounts"][i] = (acc[0], acc[1], new_balance)
            print(f"₹{amount} withdrawn successfully!")
            return

    print("Account not found!")


# -------------------------------
# 5. Display Customer Summary
# -------------------------------
def display_customer(customer_id):
    if customer_id not in customers:
        print("Customer not found!")
        return

    customer = customers[customer_id]
    print("\nCustomer ID:", customer_id)
    print("Name       :", customer["name"])
    print("Mobile     :", customer["mobile"])
    print("\nAccounts:")

    if not customer["accounts"]:
        print("No accounts available.")
        return

    for acc in customer["accounts"]:
        print(f"{acc[0]} | {acc[1]} | Balance: ₹{acc[2]:,}")


# -------------------------------
# 6. Monthly Report
# -------------------------------
def monthly_report(customer_id):
    if customer_id not in customers:
        print("Customer not found!")
        return

    accounts = customers[customer_id]["accounts"]
    if not accounts:
        print("No accounts to generate report.")
        return

    total_balance = sum(acc[2] for acc in accounts)
    highest_account = max(accounts, key=lambda x: x[2])

    print("\n--- Monthly Report ---")
    print("Total Accounts :", len(accounts))
    print("Total Balance  : ₹{:,.2f}".format(total_balance))
    print("Highest Balance Account:")
    print(f"{highest_account[0]} | {highest_account[1]} | ₹{highest_account[2]:,}")


# -------------------------------
# Demo Execution
# -------------------------------
add_customer("C101", "Rahul Sharma", "9876543210")
add_account("C101", "A1001", "Savings", 25000)
add_account("C101", "A1002", "Current", 50000)

deposit("C101", "A1001", 5000)
withdraw("C101", "A1002", 10000)

display_customer("C101")
monthly_report("C101")
