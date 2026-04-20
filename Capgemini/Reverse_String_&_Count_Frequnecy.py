str1= input("Enter a String : ").lower()
freq= {}
rev=''
vowel = 'aeiou'
vowel_count = 0
conso_count = 0

for char in str1:
    if char.isalpha():
        rev = char + rev
        freq[char] = freq.get(char,0)+1
        if char in vowel:
            vowel_count += 1
        else:
            conso_count += 1

print(f"Reversed String, {rev}")
print(f"Frequency of String, {freq}")
print(f"Vowel Count,{vowel_count}")
print(f"Comnsosnent Count, {conso_count}")