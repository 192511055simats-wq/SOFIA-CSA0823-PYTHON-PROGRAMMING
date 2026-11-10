from pathlib import Path
import csv


def write_outputs(master, event_groups, errors, output_folder):
    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)
    fields = ["register_no", "name", "department", "email", "events"]

    def write_records(path, records):
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for record in records:
                row = dict(record)
                row["events"] = ";".join(record["events"])
                writer.writerow(row)

    write_records(output / "master_registrations.csv", master)

    for event, records in sorted(event_groups.items()):
        safe_name = "".join(ch.lower() if ch.isalnum() else "_"
                            for ch in event)
        write_records(output / f"event_{safe_name}.csv", records)

    with (output / "registration_errors.csv").open(
            "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Line", "Record", "Reason"])
        writer.writerows(errors)

    with (output / "summary.txt").open("w", encoding="utf-8") as file:
        file.write(f"Accepted unique registrations: {len(master)}\n")
        file.write(f"Event groups: {len(event_groups)}\n")
        file.write(f"Errors / rejected records / file errors: {len(errors)}\n")
        for event, records in sorted(event_groups.items()):
            file.write(f"{event}: {len(records)}\n")
