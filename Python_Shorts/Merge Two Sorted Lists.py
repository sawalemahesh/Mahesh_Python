list1 = [1, 3, 5]
b = [2, 4, 6]

i = 0
j = 0
merged = []

while i < len(list1) and j < len(b):
    if list1[i] < b[j]:
        merged.append(list1[i])
        i += 1
    else:
        merged.append(b[j])
        j += 1

# Add remaining elements
while i < len(list1):
    merged.append(list1[i])
    i += 1

while j < len(b):
    merged.append(b[j])
    j += 1

print(merged)