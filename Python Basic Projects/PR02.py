class Loan:
    def __init__(self, principal, interest_rate, tenure):
        self._principal = principal
        self._interest_rate = interest_rate / 100  # yearly
        self._tenure = tenure  # months
        self.remaining_balance = principal
        self.emi = 0

    def calculate_emi(self):
        r = self._interest_rate / 12
        n = self._tenure

        self.emi = (self._principal * r * (1 + r)**n) / ((1 + r)**n - 1)
        return self.emi

    def make_payment(self):
        self.remaining_balance -= self.emi

    def prepay(self, amount):
        self.remaining_balance -= amount
        print(f"Prepaid {amount}, Remaining Balance: {self.remaining_balance}")

    def summary(self):
        print("\n--- Loan Summary ---")
        print(f"Principal: {self._principal}")
        print(f"Interest Rate: {self._interest_rate * 100}%")
        print(f"Tenure: {self._tenure} months")
        print(f"EMI: {round(self.emi, 2)}")
        print(f"Remaining Balance: {round(self.remaining_balance, 2)}")


# 🔥 Child Classes (Polymorphism)
class PersonalLoan(Loan):
    def __init__(self, principal, tenure):
        super().__init__(principal, 10, tenure)  # 10%

class CarLoan(Loan):
    def __init__(self, principal, tenure):
        super().__init__(principal, 12, tenure)  # 12%

class HomeLoan(Loan):
    def __init__(self, principal, tenure):
        super().__init__(principal, 8, tenure)  # 8%


# 🚀 Usage
loan1 = PersonalLoan(100000, 12)
loan1.calculate_emi()
loan1.summary()

loan1.make_payment()
loan1.prepay(5000)
loan1.summary()