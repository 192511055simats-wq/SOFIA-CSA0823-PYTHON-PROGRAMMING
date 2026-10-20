from decimal import Decimal
import time
# Rate card
BASE_RATE = Decimal("30.00")
FAT_RATE = Decimal("0.40")
SNF_RATE = Decimal("0.30")
def rate(fat, snf):
    """Calculate rate per litre."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    return BASE_RATE + Decimal(str(fat_steps)) * FAT_RATE + Decimal(str(snf_steps)) * SNF_RATE
def payment(litres, fat, snf):
    """Calculate farmer payment."""
    return (Decimal(str(litres)) * rate(fat, snf)).quantize(Decimal("0.01"))
# Test cases
print("Standard:", payment(10, 3.5, 8.5))
print("High fat:", payment(10, 4.2, 8.7))
print("Low fat:", payment(10, 3.1, 8.3))
# Measure time
start = time.perf_counter()
for i in range(10000):
    payment(10, 4.2, 8.7)
end = time.perf_counter()
print("Time for 10,000 payments:", end - start, "seconds")
# Rate revision example
print("\nOld base rate:", BASE_RATE)
BASE_RATE = Decimal("32.00")

print("New base rate:", BASE_RATE)
print("New payment:", payment(10, 4.2, 8.7))