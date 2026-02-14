print("Welcome to the ATM Simulation Program")

PIN = 1234
MAX_ATTEMPTS = 3

def PIN_Verification():
    attempts = 0
    print("You have only 3 attempts to enter your PIN\n")

    while attempts < MAX_ATTEMPTS:
        user_input = input("Enter your ATM PIN: ")

        # Input validation
        if not user_input.isdigit():
            print("Invalid input! Please enter numbers only.\n")
            continue

        ATM_PIN = int(user_input)

        if ATM_PIN == PIN:
            print("\nPIN Verified ✅")
            print("Proceed for Transaction")
            return  # Exit function successfully
        else:
            attempts += 1
            remaining = MAX_ATTEMPTS - attempts
            if remaining > 0:
                print(f"Incorrect PIN ❌. Remaining attempts: {remaining}\n")
            else:
                print("\nYour limit is exceeded 🚫")
                print("Card blocked. Please contact the bank.")


def Transaction():
    pass

if __name__ == "__main__":
    PIN_Verification()
    Transaction()
