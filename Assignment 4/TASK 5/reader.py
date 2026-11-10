from datetime import date


def read_records(filename):
    records = []
    errors = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                fields = [x.strip() for x in line.strip().split(",")]

                if len(fields) != 2:
                    errors.append((line_no, "expected date,status"))
                    continue

                day, status = fields
                status = status.upper()

                try:
                    date.fromisoformat(day)
                except ValueError:
                    errors.append((line_no, "invalid date"))
                    continue

                if status not in {"P", "A"}:
                    errors.append((line_no, "status must be P or A"))
                    continue

                records.append((day, status))

    except OSError as error:
        errors.append((0, f"file error: {error}"))

    return records, errors
