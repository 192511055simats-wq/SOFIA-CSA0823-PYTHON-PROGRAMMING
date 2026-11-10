from pathlib import Path
from datetime import datetime
import csv
 
def process_attendance(input_folder, output_folder):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
 
    counts = {}       # register_no -> [present_count, absent_count]
    errors = []
 
    for path in sorted(input_folder.glob("*.csv")):
        try:
            with path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for line_no, row in enumerate(reader, start=1):
                    try:
                        if len(row) != 3:
                            raise ValueError("expected 3 fields")
                        reg, date_text, status = [x.strip() for x in row]
                        if not reg:
                            raise ValueError("empty register number")
                        datetime.strptime(date_text, "%Y-%m-%d")
                        status = status.upper()
                        if status not in {"P", "A"}:
                            raise ValueError("status must be P or A")
 
                        if reg not in counts:
                            counts[reg] = [0, 0]
                        counts[reg][0 if status == "P" else 1] += 1
 
                    except ValueError as error:
                        errors.append((path.name, line_no, ",".join(row), str(error)))
 
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
            errors.append((path.name, "-", "", f"file error: {error}"))
 
    report_path = output_folder / "attendance_report.csv"
    below_path = output_folder / "below_75.csv"
    error_path = output_folder / "attendance_errors.csv"
 
    with report_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Register Number", "Present", "Absent", "Total", "Percentage"])
        for reg, (present, absent) in sorted(counts.items()):
            total = present + absent
            percentage = (present / total * 100) if total else None
            writer.writerow([reg, present, absent, total,
                             f"{percentage:.2f}" if percentage is not None else "N/A"])
 
    with below_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Register Number", "Percentage"])
        for reg, (present, absent) in sorted(counts.items()):
            total = present + absent
            if total and present / total * 100 < 75:
                writer.writerow([reg, f"{present / total * 100:.2f}"])
 
    with error_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Line", "Raw Record", "Reason"])
        writer.writerows(errors)
 
    print(f"Students processed: {len(counts)}")
    print(f"Invalid records / file errors: {len(errors)}")
    print(f"Reports saved in: {output_folder}")
 
if __name__ == "__main__":
    process_attendance("attendance_input", "attendance_output")
