# Read farmer details
farmer_id = input("Enter farmer ID: ")
while True:
    try:
        litres = float(input("Enter litres: "))
        if litres >= 0:
            break
        print("Litres cannot be negative.")
    except ValueError:
        print("Please enter a valid number.")
# Read fat
while True:
    try:
        fat = float(input("Enter fat percentage: "))
        if 2.0 <= fat <= 7.0:
            break
        print("Fat must be between 2.0 and 7.0.")
    except ValueError:
        print("Please enter a valid number.")
# Read SNF
while True:
    try:
        snf = float(input("Enter SNF percentage: "))
        if snf >= 0:
            break
        print("SNF cannot be negative.")
    except ValueError:
        print("Please enter a valid number.")
# Read shift
shift = input("Enter shift (Morning/Evening): ").title()
# Simple payment calculation
amount = 30.00 * litres
# Display result
print("\n--- Payment Result ---")
print(f"{'Farmer ID':<12}{'Shift':<10}{'Litres':>8}{'Fat':>8}{'SNF':>8}{'Amount':>12}")
print(f"{farmer_id:<12}{shift:<10}{litres:8.2f}{fat:8.2f}{snf:8.2f}{amount:12.2f}")