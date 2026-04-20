str1 = 'well done is better than well said'
lst = str1.split()

smallest = lst[0]
biggest = lst[0]

for word in lst:
    if len(word) < len(smallest):
        smallest = word
    if len(word) > len(biggest):
        biggest = word

print("The biggest word:", biggest)
print("The smallest word:", smallest)