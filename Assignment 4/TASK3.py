from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
import os
# 3.1 Custom exception and record parser
class InvalidRecord(Exception):
    """Raised when an attendance record has invalid content."""
def parse_attendance_line(line):
    fields = [field.strip() for field in line.strip().split(",")]
    if len(fields) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(fields)}"
        )
    reg, date_text, status = fields
    if not reg:
        raise InvalidRecord("register number is empty")
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError as error:
        raise InvalidRecord(
            "date must use YYYY-MM-DD"
        ) from error
    status = status.upper()
    if status not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {status!r}")
    return reg, date_text, status
# 3.2 File summary with row-level and file-level handling
def summarise_file(filename):
    present = 0
    absent = 0
    errors = []
    valid_or_invalid_records = 0
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                valid_or_invalid_records += 1
                try:
                    reg, date_text, status = parse_attendance_line(line)
                except InvalidRecord as error:
                    errors.append((line_no, str(error)))
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
        if valid_or_invalid_records == 0:
            errors.append((0, "empty file"))
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"attendance file not found: {filename}"
        ) from error
    except PermissionError as error:
        raise PermissionError(
            f"cannot read attendance file: {filename}"
        ) from error
    except UnicodeDecodeError as error:
        raise UnicodeDecodeError(
            error.encoding,
            error.object,
            error.start,
            error.end,
            "attendance file is not valid UTF-8"
        ) from error
    except OSError as error:
        raise OSError(
            f"could not read {filename}: {error}"
        ) from error
    return present, absent, errors
# 3.3 Demonstration of try, except, else and finally
sample = (
    "101,2026-01-01,P\n"
    "102,2026-01-02,A\n"
    "bad,row\n"
    "103,2026-01-03,L\n"
)
temp_path = None
try:
    with NamedTemporaryFile(
        "w",
        delete=False,
        encoding="utf-8",
        suffix=".csv"
    ) as temp:
        temp.write(sample)
        temp_path = temp.name
    try:
        result = summarise_file(temp_path)
    except (
        FileNotFoundError,
        PermissionError,
        UnicodeDecodeError,
        OSError
    ) as error:
        print("File-level problem:", error)
    else:
        print(result)
finally:
    if temp_path and Path(temp_path).exists():
        os.remove(temp_path)
# 3.5 Demonstrating why bare except/pass is dangerous
total = 5
try:
    print(total)
except Exception:
    pass
print("Program continues, but the mistake was concealed.")
