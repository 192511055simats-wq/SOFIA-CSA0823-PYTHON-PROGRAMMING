from .reader import read_records
from .stats import attendance_percentage, consecutive_absences
from .report import print_report

__all__ = [
    "read_records",
    "attendance_percentage",
    "consecutive_absences",
    "print_report"
]
