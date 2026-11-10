import csv
from .validation import parse_registration, InvalidRegistration


def read_department_file(path):
    accepted, errors = [], []

    try:
        with open(path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                line_no = reader.line_num
                try:
                    accepted.append((line_no, parse_registration(row)))
                except InvalidRegistration as error:
                    errors.append((str(path), line_no, ",".join(row), str(error)))

    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError,
            csv.Error) as error:
        errors.append((str(path), "-", "", f"file error: {error}"))

    return accepted, errors
