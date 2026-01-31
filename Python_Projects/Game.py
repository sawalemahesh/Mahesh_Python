import random   # used to generate random numbers

# generate a random number between 1 and 100
secret_number = random.randint(1, 100)

attempts = 0        # to count number of guesses
max_attempts = 7    # limit attempts

print("🎯 Welcome to Number Guessing Game!")
print("Guess a number between 1 and 100")
print("You have", max_attempts, "attempts\n")

while attempts < max_attempts:
    guess = int(input("Enter your guess: "))
    attempts += 1

    if guess > secret_number:
        print("Too high! Try again.\n")
    elif guess < secret_number:
        print("Too low! Try again.\n")
    else:
        print("🎉 Congratulations!")
        print("You guessed the number in", attempts, "attempts.")
        break

# if attempts finished and number not guessed
if attempts == max_attempts and guess != secret_number:
    print("❌ Game Over!")
    print("The correct number was:", secret_number)
