from decimal import Decimal
BASE_RATE = Decimal("30.00")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STEP = Decimal("0.1")
def rate_per_litre(fat, snf):
    """Calculate rate per litre."""
    fat_steps = round((fat - STANDARD_FAT) / STEP)
    snf_steps = round((snf - STANDARD_SNF) / STEP)
    return BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
def payout(litres, fat, snf):
    """Calculate one farmer payment."""
    return Decimal(str(litres)) * rate_per_litre(
        Decimal(str(fat)), Decimal(str(snf))
    )
entries = [
    ("F001", 10, 3.5, 8.5),
    ("F002", 8.5, 4.2, 8.7),
    ("F003", 12, 3.1, 8.3),
]

running_total = Decimal("0.00")

for farmer_id, litres, fat, snf in entries:
    if litres < 0 or not (2.0 <= fat <= 7.0) or snf < 0:
        print("Invalid:", farmer_id)
        continue

    amount = payout(litres, fat, snf)
    running_total += amount
    print(f"{farmer_id}: {amount:.2f}")

print(f"Ten-day total: {running_total:.2f}")
