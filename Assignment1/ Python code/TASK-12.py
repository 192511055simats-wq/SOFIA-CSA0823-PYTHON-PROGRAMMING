from decimal import Decimal, ROUND_HALF_UP
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
STEP = Decimal("0.1")
RATE_CARDS = {
    "original": {
        "base": Decimal("30.00"),
        "fat_step": Decimal("0.40"),
        "snf_step": Decimal("0.30"),
    },
    "seasonal_apr_jun": {
        "base": Decimal("32.00"),
        "fat_step": Decimal("0.45"),
        "snf_step": Decimal("0.30"),
    },
}
def money(value):
    """Round a monetary Decimal to two decimal places."""
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
def rate_per_litre(fat, snf, season="original"):
    """Return the rate using the selected rate card."""
    card = RATE_CARDS[season]
    fat_steps = (
        (Decimal(str(fat)) - STANDARD_FAT) / STEP
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    snf_steps = (
        (Decimal(str(snf)) - STANDARD_SNF) / STEP
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    rate = (
        card["base"]
        + fat_steps * card["fat_step"]
        + snf_steps * card["snf_step"]
    )
    return money(rate)
def bonus_per_litre(ten_day_litres):
    """Return the seasonal volume bonus rate."""
    return Decimal("0.50") if ten_day_litres > 500 else Decimal("0.00")
def payout(litres, fat, snf, season="original"):
    """Return payment before the ten-day volume bonus."""
    return money(Decimal(str(litres)) * rate_per_litre(fat, snf, season))
def ten_day_payment(entries, season="original"):
    """Return total payment including the >500 litre bonus."""
    total_litres = sum(Decimal(str(e[0])) for e in entries)
    total = sum(
        (payout(e[0], e[1], e[2], season) for e in entries),
        Decimal("0.00")
    )
    bonus_rate = bonus_per_litre(total_litres)
    total += money(total_litres * bonus_rate)
    return money(total), total_litres, bonus_rate
if __name__ == "__main__":
    tests = [
        (10, 3.5, 8.5),
        (8.5, 4.23, 8.74),
        (12, 3.1, 8.3),
    ]

    for season in RATE_CARDS:
        print("\nSeason:", season)
        for litres, fat, snf in tests:
            r = rate_per_litre(fat, snf, season)
            print(f"{litres:5.1f} L fat {fat:5.2f} snf {snf:5.2f} rate {r:6.2f}")

    no_bonus = [(100, 3.5, 8.5)] * 5
    with_bonus = [(101, 3.5, 8.5)] * 5

    print("\nBonus tests")
    print("500 litres:", ten_day_payment(no_bonus, "seasonal_apr_jun"))
    print("505 litres:", ten_day_payment(with_bonus, "seasonal_apr_jun"))