from decimal import Decimal
import time
def float_total(n):
    total = 0.0
    for _ in range(n):
        total += 33.40
    return total
def decimal_total(n):
    total = Decimal("0.00")
    amount = Decimal("33.40")
    for _ in range(n):
        total += amount
    return total
for n in (300, 6000, 150000):
    start = time.perf_counter()
    f = float_total(n)
    float_time = time.perf_counter() - start

    start = time.perf_counter()
    d = decimal_total(n)
    decimal_time = time.perf_counter() - start

    difference = Decimal(str(f)) - d

    print(f"n={n}")
    print(f"  float   = {f!r}")
    print(f"  Decimal = {d}")
    print(f"  diff    = {difference}")
    print(f"  float time   = {float_time:.8f} s")
    print(f"  Decimal time = {decimal_time:.8f} s")

# Demonstrate payment-level vs total-level rounding.
payments = [10.005, 10.005, 10.005]
payment_level = sum(round(x, 2) for x in payments)
total_level = round(sum(payments), 2)
print("payment-level rounding:", payment_level)
print("total-level rounding:", total_level)
