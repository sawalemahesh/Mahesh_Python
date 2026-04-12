def abc(text):
    k = ""
    for i in range(len(text)):
        k += text[:i + 1]
    return k

print(abc("ACL"))