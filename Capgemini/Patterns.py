n = 5
for i in range(n, 0 ,-1):
    for j in range(1,i+1):
        print(j, end = " ")
    print(" ")

print("__________________________________")

for i in range(1, n+1):
    for j in range(1,i+1):
        print(j, end= " ")
    print(" ")

print("__________________________________")

for i in range(1, n + 1):
    # spaces
    for j in range(n - i):
        print(" ", end="")

    # stars
    for k in range(i):
        print("* ", end="")

    print("")