from .reader import read_department_file


def process_files(paths):
    master = []
    event_groups = {}
    errors = []
    seen_register_numbers = set()

    for path in paths:
        rows, file_errors = read_department_file(path)
        errors.extend(file_errors)

        for line_no, record in rows:
            reg = record["register_no"]
            if reg in seen_register_numbers:
                errors.append((str(path), line_no, reg,
                               "duplicate register number"))
                continue

            seen_register_numbers.add(reg)
            master.append(record)

            for event in record["events"]:
                event_groups.setdefault(event, []).append(record)

    return master, event_groups, errors
