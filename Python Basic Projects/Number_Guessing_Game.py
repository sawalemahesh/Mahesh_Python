import random

random_num = random.randint(1, 100)

print("Welcome to Number Guessing Game")
print("You have to number between 1 to 100")
attempts = 0

while True:

    number  = int(input("Enter your lucy number: "))

    if number > 100:
        print("The number is higher than 100, please try again")
    elif number < 1:
        print("The number is lower than 1, please try again")
    elif number > random_num:
        print("Number is higher ")
    elif number < random_num:
        print("Number is lower")
    elif number == random_num:
        print(f"Wow , you guessed the number 🏆 in {attempts} attempts")
        break
    attempts += 1

