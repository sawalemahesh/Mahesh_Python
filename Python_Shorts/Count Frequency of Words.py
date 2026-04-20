input ='this is test this is'
# output = {'this': 2, 'is': 2, 'test': 1}
list1 = input.split()
freq = {}
for char in list1:
    freq[char] = freq.get(char,0)+1
print(freq)