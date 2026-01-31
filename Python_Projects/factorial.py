# def factorial(n):
#     if n == 0:
#         return 1
#     else:
#         return n * factorial(n-1)
# fac = factorial(5)
# print(fac)


# --------------------------------*
# num = int(input("Enter a number: "))
#
# if num <= 1:
#     print("Not Prime")
# else:
#     for i in range(2, num):
#         if num % i == 0:
#             print("Not Prime")
#             break
#     else:
#         print("Prime")


# n = int(input("Enter number of terms: "))
#
# a, b = 0, 1
#
# for i in range(n):
#     print(a, end=" ")
#     a, b = b, a + b

#
# a = str(input("Enter a str: ")).lower()
# vowels = 'aeiou'
# n = 0
#
# for char in a:
#     if char in vowels:
#         n = n + 1
# print(n)

#
# num = int(input("Enter a number: "))
# total = 0
#
# while num > 0:
#     digit = num % 10
#     total += digit
#     num = num // 10
#
# print("Sum of digits:", total)
