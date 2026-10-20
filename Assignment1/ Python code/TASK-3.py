# Constants
BASE_RATE = 30.00
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
# User input
litres = float(input("Enter litres of milk: "))
fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))
# Display values
print("\nMilk Details")
print("Base rate:", BASE_RATE)
print("Standard fat:", STANDARD_FAT)
print("Standard SNF:", STANDARD_SNF)
print("Fat step value:", FAT_STEP_VALUE)
print("SNF step value:", SNF_STEP_VALUE)
print("Litres:", litres)
print("Fat:", fat)
print("SNF:", snf)
# Demonstrate different data types
value = int(input("\nEnter an integer: "))
print("Value:", value)
print("Type:", type(value))
name = input("Enter a word: ")
print("Value:", name)
print("Type:", type(name))
# Swap two numbers
a = int(input("Enter first number to swap: "))
b = int(input("Enter second number to swap: "))
a, b = b, a
print("After swapping:", a, b)
# Rate card dictionary
RATE_CARD = {
    "base": BASE_RATE,
    "fat": FAT_STEP_VALUE,
    "snf": SNF_STEP_VALUE
}

print("Rate card:", RATE_CARD)