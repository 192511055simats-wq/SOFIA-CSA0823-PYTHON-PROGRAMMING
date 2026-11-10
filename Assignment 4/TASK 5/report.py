from stats import attendance_percentage, consecutive_absences


def print_report(records, errors):
    present = sum(1 for _, status in records if status == "P")
    total = len(records)

    print(f"Valid records: {total}")
    print(
        f"Attendance percentage: "
        f"{attendance_percentage(present, total):.2f}%"
    )
    print(
        "Longest consecutive absence:",
        consecutive_absences(records)
    )
    print("Rejected rows:", len(errors))

    for error in errors:
        print(error)
