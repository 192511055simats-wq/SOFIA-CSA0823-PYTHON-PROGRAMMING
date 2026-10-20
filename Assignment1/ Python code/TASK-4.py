import math
# Constants
BASE_RATE = 30.00
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
FAT_STEP = 0.40
SNF_STEP = 0.30
# User input
litres = float(input("Enter litres: "))
fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))
# Calculate steps, rate and amount
fat_steps = round((fat - STANDARD_FAT) / 0.1)
snf_steps = round((snf - STANDARD_SNF) / 0.1)
rate = BASE_RATE + fat_steps * FAT_STEP + snf_steps * SNF_STEP
amount = rate * litres
print("Fat steps:", fat_steps)
print("SNF steps:", snf_steps)
print("Rate per litre:", round(rate, 2))
print("Total amount:", round(amount, 2))
# Unexpected expressions
print("\n--- Unexpected Results ---")
print("(4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)
print("0.1 + 0.2 =", 0.1 + 0.2)
print("-7 // 2 =", -7 // 2)
# Compare round(), int() and floor()
print("\n--- Step Comparison ---")
for f in [4.2, 3.1]:
    steps = (f - STANDARD_FAT) / 0.1
    print("\nFat:", f)
    print("Rate using round():", BASE_RATE + round(steps) * FAT_STEP)
    print("Rate using int():", BASE_RATE + int(steps) * FAT_STEP)
    print("Rate using floor():", BASE_RATE + math.floor(steps) * FAT_STEP)
# Comparison and Boolean operators
print("\nFat valid:", 2.0 <= fat <= 7.0)
print("Fat and SNF positive:", fat > 0 and snf > 0)
# Operator precedence and associativity
print("\n2 ** 3 ** 2 =", 2 ** 3 ** 2)
print("-2 ** 2 =", -2 ** 2)
print("(-2) ** 2 =", (-2) ** 2)