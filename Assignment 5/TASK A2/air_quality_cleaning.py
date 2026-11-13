import csv
from pathlib import Path
from datetime import datetime
from statistics import mean, pstdev, median
# Input and output folders
DATA_FOLDER = Path("../station_data")
# Change to "F" if source temperature values are in Fahrenheit
TEMPERATURE_UNIT = "C"
# Maximum number of consecutive missing readings to forward-fill
MAX_GAP = 1
# Configure these limits using the biometric/environmental
# sensor manufacturer's documented valid ranges.
MAX_LIMITS = {
    "pm25": None,
    "pm10": None,
    "no2": None
}
clean_records = []
rejected_records = []
seen_records = {}
# Convert missing values
def clean_number(value):
    value = (value or "").strip()
    if value.upper() in ("", "NA", "N/A", "NULL", "NONE"):
        return None
    return float(value)
# Convert Fahrenheit to Celsius
def to_celsius(value):
    if value is None:
        return None
    if TEMPERATURE_UNIT == "F":
        return (value - 32) * 5 / 9
    return value
# Read all station CSV files
for file_path in sorted(DATA_FOLDER.glob("*.csv")):
    try:
        with open(file_path, "r", encoding="utf-8-sig",
                  newline="") as file:
            reader = csv.DictReader(file)
            required = {
                "station", "date", "hour",
                "pm25", "pm10", "no2", "temperature"
            }
            if not reader.fieldnames or not required.issubset(
                set(reader.fieldnames)
            ):
                rejected_records.append([
                    file_path.name, 1, "",
                    "Missing required columns"
                ])
                continue
            for line_no, row in enumerate(reader, start=2):
                try:
                    station = (row["station"] or "").strip().title()
                    date = (row["date"] or "").strip()
                    hour = (row["hour"] or "").strip()
                    if not station or not date or not hour:
                        raise ValueError("Missing station, date or hour")
                    datetime.strptime(date, "%Y-%m-%d")
                    datetime.strptime(hour, "%H:%M")
                    pm25 = clean_number(row["pm25"])
                    pm10 = clean_number(row["pm10"])
                    no2 = clean_number(row["no2"])
                    temperature = clean_number(row["temperature"])
                    values = {
                        "pm25": pm25,
                        "pm10": pm10,
                        "no2": no2
                    }
                    # Reject negative and impossible pollutant values
                    for name, value in values.items():
                        if value is not None:
                            if value < 0:
                                raise ValueError(
                                    f"Negative {name} value"
                                )
                            limit = MAX_LIMITS[name]
                            if limit is not None and value > limit:
                                raise ValueError(
                                    f"{name} exceeds sensor limit"
                                )
                    temperature_c = to_celsius(temperature)
                    # Create a unique reading key
                    key = (station, date, hour)
                    record = {
                        "station": station,
                        "date": date,
                        "hour": hour,
                        "pm25": pm25,
                        "pm10": pm10,
                        "no2": no2,
                        "temperature_c": temperature_c,
                        "imputed": "No"
                    }
                    # Duplicate handling
                    if key in seen_records:
                        old_record = seen_records[key]
                        if old_record == record:
                            continue
                        else:
                            rejected_records.append([
                                file_path.name, line_no,
                                str(row),
                                "Conflicting duplicate record"
                            ])
                            continue
                    seen_records[key] = record
                except (ValueError, TypeError) as error:
                    rejected_records.append([
                        file_path.name, line_no,
                        str(row), str(error)
                    ])
    except (FileNotFoundError, PermissionError,
            UnicodeDecodeError) as error:
        rejected_records.append([
            file_path.name, "File error", "", str(error)
        ])
# Sort readings by station, date and hour
records = sorted(
    seen_records.values(),
    key=lambda x: (x["station"], x["date"], x["hour"])
)
# Forward-fill only one short missing gap within a station
previous = {}
for record in records:
    station = record["station"]
    for field in ("pm25", "pm10", "no2"):
        key = (station, field)
        if record[field] is not None:
            previous[key] = (record[field], 0)
        elif key in previous:
            old_value, gap = previous[key]
            if gap < MAX_GAP:
                record[field] = old_value
                record["imputed"] = "Yes"
                previous[key] = (old_value, gap + 1)
            else:
                previous.pop(key, None)
# Calculate station-level medians for remaining missing values
for station in sorted(set(r["station"] for r in records)):
    station_records = [
        r for r in records if r["station"] == station
    ]
    for field in ("pm25", "pm10", "no2"):
        available = [
            r[field] for r in station_records
            if r[field] is not None
        ]
        if not available:
            continue
        middle_value = median(available)
        for record in station_records:
            if record[field] is None:
                record[field] = middle_value
                record["imputed"] = "Yes"
# Calculate min-max and z-score normalisation
for field in ("pm25", "pm10", "no2"):
    values = [r[field] for r in records if r[field] is not None]
    if not values:
        continue
    minimum = min(values)
    maximum = max(values)
    average = mean(values)
    deviation = pstdev(values)
    for record in records:
        value = record[field]
        if value is None:
            record[field + "_minmax"] = None
            record[field + "_zscore"] = None
            continue
        if maximum == minimum:
            minmax = 0
        else:
            minmax = (value - minimum) / (maximum - minimum)
        if deviation == 0:
            zscore = 0
        else:
            zscore = (value - average) / deviation
        record[field + "_minmax"] = round(minmax, 4)
        record[field + "_zscore"] = round(zscore, 4)
# Write cleaned and normalised records
output_fields = [
    "station", "date", "hour",
    "pm25", "pm10", "no2", "temperature_c", "imputed",
    "pm25_minmax", "pm25_zscore",
    "pm10_minmax", "pm10_zscore",
    "no2_minmax", "no2_zscore"
]
with open("cleaned_readings.csv", "w", newline="",
          encoding="utf-8",) as output:
    writer = csv.DictWriter(output, fieldnames=output_fields)
    writer.writeheader()
    writer.writerows(records)
# Write rejected records
with open("rejected_records.csv", "w", newline="",
          encoding="utf-8") as output:
    writer = csv.writer(output)
    writer.writerow([
        "File Name", "Line Number", "Record", "Reason"
    ])
    writer.writerows(rejected_records)
print("Cleaning and normalisation completed!")
print("Total clean records:", len(records))
print("Rejected records:", len(rejected_records))
print("Generated files:")
print("1. cleaned_readings.csv")
print("2. rejected_records.csv")
