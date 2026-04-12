s = "Alexa"
result = ""
temp = ""

for ch in s:
    temp = temp + ch
    result = result + temp

print(result)


s = "Alexa"
result = ""

for i in range(len(s)):
    result = result + s[:i+1]

print(result)