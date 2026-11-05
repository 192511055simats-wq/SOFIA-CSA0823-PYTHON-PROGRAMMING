units = int(input("Enter electricity units consumed: "))
ration = input("Do you have a ration card? (yes/no): ").lower()
age = int(input("Enter age of the oldest household member: "))
# Method 1: Separate if statements
print("\n--- Using Separate If Statements ---")
if units <= 100:
    result1 = "Full Subsidy"
if 101 <= units <= 200 and ration == "yes":
    result1 = "Partial Subsidy"
if 101 <= units <= 200 and ration == "no":
    result1 = "No Subsidy"
if units > 200 and age > 80:
    result1 = "Senior Citizen Subsidy"
if units > 200 and age <= 80:
    result1 = "No Subsidy"
print("Result:", result1)
# Method 2: if-elif-else
print("\n--- Using If-Elif-Else ---")
if units <= 100:
    result2 = "Full Subsidy"
elif units <= 200:
    if ration == "yes":
        result2 = "Partial Subsidy"
    else:
        result2 = "No Subsidy"
elif age > 80:
    result2 = "Senior Citizen Subsidy"
else:
    result2 = "No Subsidy"
print("Result:", result2)
# Compare results
print("\n--- Comparison ---")
if result1 == result2:
    print("Both methods give the same result.")
else:
    print("Results are different.")