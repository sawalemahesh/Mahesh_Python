a = 'MaheshSawale'
vowels = 'aeiou'
vowel = 0
vowel_c = ''


for char in a:
    if char in vowels:
        vowel_c = vowel_c + char
        vowel = vowel + 1

print(vowel_c, vowel)
print(vowel_c)