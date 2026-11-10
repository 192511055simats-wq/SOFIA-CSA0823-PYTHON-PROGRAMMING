from pathlib import Path
from fest_registration import process_files, write_outputs


base = Path(__file__).parent
input_folder = base / "input"
output_folder = base / "output"

department_files = [
    input_folder / f"department{i}.csv" for i in range(1, 6)
]

master, event_groups, errors = process_files(department_files)
write_outputs(master, event_groups, errors, output_folder)

print("Accepted unique registrations:", len(master))
print("Event groups:", len(event_groups))
print("Errors / rejected records / file errors:", len(errors))

for event, records in sorted(event_groups.items()):
    print(f"{event}: {len(records)}")

print("Output folder:", output_folder)
