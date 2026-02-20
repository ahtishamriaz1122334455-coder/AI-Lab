#LAB TASK 4 AI 
# Luhn Algorithm (Credit Card Validation) – Simplified
def luhn(card):
    digits = [int(d) for d in str(card)]
    for i in range(len(digits)-2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

# Test
card = 4532015112830366
print("Valid Card" if luhn(card) else "Invalid Card")

#2

#Remove Punctuations _ Simplified
import string

text = "Hello, world! This is AI Lab 4."
clean_text = "".join(c for c in text if c not in string.punctuation)
print(clean_text)

#3
#Sort Words in a Sentence Alphabetically – Simplified
sentence = "Python programming is fun and easy"
words = sentence.split()      
words.sort()                  
print(" ".join(words))