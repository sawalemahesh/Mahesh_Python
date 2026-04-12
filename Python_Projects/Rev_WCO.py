s = "Mahesh Sawale"

words = s.split()
result = []

for word in words:
    result.append(word[::-1])

output = " ".join(result)
print(output)


s = "Mahesh Sawale"
words = s.split()

words = s.split()
result = []

for word in words:
    rev = ""
    for ch in word:
        rev = ch + rev
    result.append(rev)

print(" ".join(result))