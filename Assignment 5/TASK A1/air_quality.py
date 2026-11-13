import csv
import sqlite3
from pathlib import Path
from datetime import datetime

# Folder containing station CSV files
DATA_FOLDER = Path("station_data")

# Database connection
conn = sqlite3.connect("air_quality.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# Create stations table
cursor.execute("""
CREATE TABLE IF NOT EXISTS stations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT NOT NULL UNIQUE,
    temperature_unit TEXT NOT NULL
        CHECK(temperature_unit IN ('C', 'F'))
)
""")

# Create readings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    station_id INTEGER NOT NULL,
    reading_date TEXT NOT NULL,
    reading_hour TEXT NOT NULL,
    pm25 REAL,
    pm10 REAL,
    no2 REAL,
    temperature_c REAL,
    source_file TEXT,
    PRIMARY KEY (station_id, reading_date, reading_hour),
    FOREIGN KEY (station_id) REFERENCES stations(station_id),
    CHECK(pm25 IS NULL OR pm25 >= 0),
    CHECK(pm10 IS NULL OR pm10 >= 0),
    CHECK(no2 IS NULL OR no2 >= 0)
)
""")

# Index for faster station and date searches
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_readings_date
ON readings(station_id, reading_date)
""")

# Data-quality error log
errors = []

# Process all station CSV files
for file_path in sorted(DATA_FOLDER.glob("*.csv")):

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "station", "date", "hour",
                "pm25", "pm10", "no2", "temperature"
            }

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                errors.append([
                    file_path.name, 1, "",
                    "Missing required CSV columns"
                ])
                continue

            for line_number, row in enumerate(reader, start=2):
                try:
                    station = (row["station"] or "").strip().title()
                    date = (row["date"] or "").strip()
                    hour = (row["hour"] or "").strip()

                    if not station or not date or not hour:
                        raise ValueError("Missing required field")

                    # Validate date and hour
                    datetime.strptime(date, "%Y-%m-%d")
                    datetime.strptime(hour, "%H:%M")

                    # Convert numeric values
                    def get_number(value):
                        value = (value or "").strip()
                        if value.upper() in ("", "NA", "N/A", "NULL"):
                            return None
                        number = float(value)
                        if number < 0:
                            raise ValueError("Negative sensor value")
                        return number

                    pm25 = get_number(row["pm25"])
                    pm10 = get_number(row["pm10"])
                    no2 = get_number(row["no2"])
                    temperature = get_number(row["temperature"])

                    # Assume source temperature is Celsius
                    temperature_c = temperature

                    # Insert station if it does not exist
                    cursor.execute("""
                        INSERT OR IGNORE INTO stations
                        (station_name, temperature_unit)
                        VALUES (?, 'C')
                    """, (station,))

                    cursor.execute("""
                        SELECT station_id FROM stations
                        WHERE station_name = ?
                    """, (station,))

                    station_id = cursor.fetchone()[0]

                    # Insert reading
                    cursor.execute("""
                        INSERT INTO readings
                        (station_id, reading_date, reading_hour,
                         pm25, pm10, no2, temperature_c, source_file)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        station_id, date, hour,
                        pm25, pm10, no2,
                        temperature_c, file_path.name
                    ))

                except (ValueError, TypeError, sqlite3.IntegrityError) as e:
                    errors.append([
                        file_path.name, line_number,
                        str(row), str(e)
                    ])

        conn.commit()

    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        errors.append([
            file_path.name, "File error", "", str(e)
        ])

# Save data-quality errors
with open("data_errors.csv", "w", newline="", encoding="utf-8") as error_file:
    writer = csv.writer(error_file)
    writer.writerow(["File Name", "Line Number", "Damaged Record", "Reason"])
    writer.writerows(errors)

print("CSV data acquisition completed.")
print("Database: air_quality.db")
print("Error report: data_errors.csv")

# -------------------------------------------------
# QUERY 1: Average PM2.5 at Adyar during October
# -------------------------------------------------

print("\n1. Average PM2.5 at Adyar in October")

cursor.execute("""
SELECT s.station_name, ROUND(AVG(r.pm25), 2)
FROM readings r
JOIN stations s ON r.station_id = s.station_id
WHERE s.station_name = 'Adyar'
AND r.reading_date >= '2026-10-01'
AND r.reading_date < '2026-11-01'
GROUP BY s.station_name
""")

print(cursor.fetchall())

# -------------------------------------------------
# QUERY 2: Highest daily average PM2.5 by station
# -------------------------------------------------

print("\n2. Highest daily average PM2.5")

cursor.execute("""
SELECT s.station_name, r.reading_date,
       ROUND(AVG(r.pm25), 2) AS daily_average
FROM readings r
JOIN stations s ON r.station_id = s.station_id
WHERE r.pm25 IS NOT NULL
GROUP BY s.station_name, r.reading_date
ORDER BY daily_average DESC
LIMIT 10
""")

for result in cursor.fetchall():
    print(result)

# -------------------------------------------------
# QUERY 3: Worst hours based on average PM2.5
# -------------------------------------------------

print("\n3. Hours with highest average PM2.5")

cursor.execute("""
SELECT reading_hour, ROUND(AVG(pm25), 2) AS average_pm25
FROM readings
WHERE pm25 IS NOT NULL
GROUP BY reading_hour
ORDER BY average_pm25 DESC
""")

for result in cursor.fetchall():
    print(result)

conn.close()
print("\nDatabase connection closed.")