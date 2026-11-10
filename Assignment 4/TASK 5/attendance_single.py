from datetime import date
def attendance_percentage(present, total):
    if total <= 0:
        return 0.0
    return present / total * 100
def consecutive_absences(records):
    dates = sorted(
        (date.fromisoformat(day), status.upper())
        for day, status in records
    )

    longest = current = 0
    previous = None

    for day, status in dates:
        if status == "A":
            if previous is not None and (day - previous).days == 1:
                current += 1
            else:
                current = 1
            previous = day
            longest = max(longest, current)
        else:
            current = 0
            previous = None

    return longest


if __name__ == "__main__":
    sample = [
        ("2026-01-01", "A"),
        ("2026-01-02", "A"),
        ("2026-01-04", "A"),
        ("2026-01-05", "P")
    ]

    print(f"Attendance: {attendance_percentage(8, 10):.2f}%")
    print("Longest consecutive absence:",
          consecutive_absences(sample))
