num = int(input("Enter a number: "))
org = num
rev = 0

while num > 0:
    digit = num % 10
    rev = rev * 10 + digit
    num = num // 10

print("Reversed number:", rev)
print(type(rev))

if rev == org:
    print("Palindrome")
else:
    print("Not palindrome")


