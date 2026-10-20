"""Rate card of the village milk co-operative (used as a module)."""

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
STEP = 0.1


def rate_per_litre(fat, snf):
    """Returns the price per litre, rounded to 2 decimals."""
    fat_steps = round((fat - STANDARD_FAT) / STEP)
    snf_steps = round((snf - STANDARD_SNF) / STEP)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return round(rate, 2)


def payout(litres, fat, snf):
    """Returns the amount payable to the farmer, rounded to 2 decimals."""
    return round(litres * rate_per_litre(fat, snf), 2)


if __name__ == "__main__":
    for litres, fat, snf in [
        (10, 3.5, 8.5),
        (8.5, 4.2, 8.7),
        (12, 3.1, 8.3)
    ]:
        rate, pay = rate_per_litre(fat, snf), payout(litres, fat, snf)
        print(
            f"{litres:5} L fat {fat} snf {snf} "
            f"rate {rate:6.2f} pay {pay:8.2f}"
        )
