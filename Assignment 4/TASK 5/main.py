from attendance_utils import (
    attendance_percentage,
    consecutive_absences
)

records = [
    ("2026-01-01", "A"),
    ("2026-01-02", "A"),
    ("2026-01-04", "A"),
    ("2026-01-05", "P")
]

print(f"Attendance: {attendance_percentage(8, 10):.2f}%")
print("Longest consecutive absence:",
      consecutive_absences(records))
