# Sort a List in Ascending Order

lst= [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
print(lst)
even = []
odd = []
for i in lst:
    if i % 2 == 0:
        even.append(i)
    if i % 2 !=0:
        odd.append(i)

print(even)
print(odd)

print("---------------------------------------------------------")

nums = [5, 1, 4, 2, 8]

n = len(nums)

for i in range(n):
    for j in range(0, n - i - 1):
        if nums[j] > nums[j + 1]:
            nums[j], nums[j + 1] = nums[j + 1], nums[j]

print(nums)
