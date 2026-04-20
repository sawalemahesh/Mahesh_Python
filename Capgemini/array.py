# Take array size
n = int(input("Enter number of elements: "))

arr = []

# Take array values
for i in range(n):
    val = int(input("Enter element: "))
    arr.append(val)

# Assume first element is smallest & largest
smallest = arr[0]
largest = arr[0]

# Find smallest and largest
for num in arr:
    if num < smallest:
        smallest = num
    if num > largest:
        largest = num

print("Array:", arr)
print("Smallest number:", smallest)
print("Largest number:", largest)