a = 'aabbcdeff'
feq = {}
for char in a:
    feq[char] = feq.get(char, 0)+1

for char in feq:
    if feq[char] == 1:
        print(f"first Non-Repeating Charactor: {char}")
        break