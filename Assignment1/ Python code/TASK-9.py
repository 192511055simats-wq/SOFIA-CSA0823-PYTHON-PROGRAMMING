from decimal import Decimal
BASE_RATE = Decimal("30.00")
def rate_per_litre(fat, snf):
    rate = BASE_RATE

    # Add money for fat above 3.5
    rate = rate + (Decimal(str(fat)) - Decimal("3.5")) * Decimal("4.00")

    # Add money for SNF above 8.5
    rate = rate + (Decimal(str(snf)) - Decimal("8.5")) * Decimal("3.00")

    return rate
def payout(litres, fat, snf):
    rate = rate_per_litre(fat, snf)
    amount = Decimal(str(litres)) * rate
    return amount.quantize(Decimal("0.01"))
def validate(litres, fat, snf):
    if litres < 0:
        return False

    if fat < 2.0 or fat > 7.0:
        return False

    if snf < 0:
        return False

    return True


def run_tests():

    print("Standard:", payout(10, 3.5, 8.5))
    print("Above standard:", payout(8.5, 4.2, 8.7))
    print("Below standard:", payout(12, 3.1, 8.3))

    print("Fat low:", payout(10, 2.0, 8.5))
    print("Fat high:", payout(10, 7.0, 8.5))

    print("Negative litres:", validate(-1, 3.5, 8.5))
    print("Fat too low:", validate(10, 1.9, 8.5))
    print("Fat too high:", validate(10, 7.1, 8.5))

    payments = [
        payout(10, 3.5, 8.5),
        payout(8.5, 4.2, 8.7),
        payout(12, 3.1, 8.3),
        payout(5, 4.0, 8.5),
        payout(7, 3.5, 8.2)
    ]

    total = sum(payments)

    print("Total:", total)


if __name__ == "__main__":
    run_tests()