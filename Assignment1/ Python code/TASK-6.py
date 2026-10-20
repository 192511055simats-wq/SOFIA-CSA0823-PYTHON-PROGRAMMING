from decimal import Decimal
# Constants
BASE_RATE = Decimal("30.00")
FAT_STEP = Decimal("0.40")
SNF_STEP = Decimal("0.30")
def rate_per_litre(fat, snf):
    """Calculate the milk rate per litre."""
 
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    rate = BASE_RATE + Decimal(str(fat_steps)) * FAT_STEP
    rate = rate + Decimal(str(snf_steps)) * SNF_STEP

    return rate
def payout(litres, fat, snf):
    """Calculate the payment for the milk supplied."""
    
    rate = rate_per_litre(fat, snf)
    amount = Decimal(str(litres)) * rate

    return amount


def ten_day_total(payments):
    """Calculate the total payment for ten days."""
    
    total = Decimal("0.00")

    for payment in payments:
        total = total + payment

    return total
# Main program
entries = [
    (10, 3.5, 8.5),
    (8.5, 4.2, 8.7),
    (12, 3.1, 8.3)
]
payments = []
for litres, fat, snf in entries:

    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)

    payments.append(amount)

    print("Rate per litre:", rate)
    print("Amount:", amount)
    print()

print("Ten-day total:", ten_day_total(payments))