''' Sum of Even number form give list
'''

list1 = [20,3,60,3,5,3,6,13,88]
even = []
for char in list1:
    if char % 2 == 0:
        even.append(char)
print(even)
print(sum(even))

print("Filter Method")
list1 = [20,3,60,3,5,3,6,13,88]
even = list(filter(lambda x:x%2==0,list1))
print(even)


# '------------------------------------------------------------------------------'

# Find second highest Temperature

cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"]
temps = [35, 40, 38, 42, 37]

# Combine both lists
data = list(zip(cities, temps))
print(data)

# Sort by temperature (highest first)
data_sorted = sorted(data, key=lambda x: x[1], reverse=True)

# Get second largest
second_largest = data_sorted[1]

print("Second highest temperature city:", second_largest[0])
print("Temperature:", second_largest[1])


# '------------------------------------------------------------------------------'

