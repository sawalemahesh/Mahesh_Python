import string
import random

a = string.ascii_lowercase
b= string.ascii_uppercase

all = a + b

c= ''.join(random.choice(all) for _ in range(6))
print(c)

