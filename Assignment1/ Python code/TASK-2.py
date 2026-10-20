from decimal import Decimal

# User input
n = int(input("Enter number of payments: "))
payments = []

for i in range(n):
    amount = input(f"Enter payment {i + 1} in rupees: ")
    payments.append(amount)

def total_float(items):
    total = 0.0
    for amount in items:
        total += float(amount)
    return total

def total_decimal(items):
    total = Decimal("0.00")
    for amount in items:
        total += Decimal(amount)
    return total

print("Float total:", total_float(payments))
print("Decimal total:", total_decimal(payments))

print(0.1 + 0.2 == 0.3)
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))