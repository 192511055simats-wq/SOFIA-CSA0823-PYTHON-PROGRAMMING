import csv
import io
import sqlite3
import statistics
import time
import tracemalloc
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
# ==========================================
# TASK B1: IMPLEMENT AND VALIDATE CLEANING
# ==========================================
DB_FILE = Path("TASK A1/air_quality.db")
INPUT_FILE = Path("TASK A2/cleaned_readings.csv")
# ==========================================
# B1.1: VALIDATE CLEANING IMPLEMENTATION
# ==========================================
RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,1200
 adyar ,2026-10-01,48
"""
def load_clean(text):
    rows = []
    rejected = []
    reader = csv.DictReader(io.StringIO(text))

    for row in reader:
        try:
            raw = (row.get("pm25") or "").strip()

            if raw == "" or raw.upper() == "NA":
                rejected.append((row, "Missing PM2.5"))
                continue

            value = float(raw)

            if value < 0 or value > 999:
                rejected.append((row, "Value outside valid range"))
                continue

            station = row["station"].strip().title()
            reading_date = row["date"].strip()

            cleaned_row = (
                station,
                reading_date,
                value
            )

            rows.append(cleaned_row)

        except (ValueError, KeyError) as error:
            rejected.append((row, str(error)))

    # Remove exact duplicate records
    rows = list(dict.fromkeys(rows))

    return rows, rejected


def min_max(values):
    if not values:
        return []

    low = min(values)
    high = max(values)

    if high == low:
        return [0.0 for value in values]

    return [
        round((value - low) / (high - low), 3)
        for value in values
    ]


print("\n========== B1.1 CLEANING VALIDATION ==========")

print("\nBEFORE CLEANING:")
print(RAW)

clean, rejected = load_clean(RAW)

print("\nAFTER CLEANING:")
for row in clean:
    print(row)

print("\nREJECTED RECORDS:")
for row, reason in rejected:
    print(row, "->", reason)

values = [pm25 for station, day, pm25 in clean]

print("\nMIN-MAX NORMALISATION:")
print(min_max(values))

assert all(0 <= value <= 999 for value in values)
assert len(clean) == len(set(clean))

print("\nValidation assertions passed.")

# ==========================================
# B1.2: COMPARE WITH ORIGINAL DESIGN
# ==========================================

print("\n========== B1.2 DESIGN COMPARISON ==========")

print("""
1. Numeric conversion is performed using float().
2. Missing values are rejected in this sample test.
3. Negative and above-limit readings are rejected.
4. Station names are trimmed and standardised.
5. Exact duplicate records are removed.
6. Min-max normalisation scales values between 0 and 1.

The full Task A2 pipeline additionally performs
imputation and z-score normalisation.
""")

# ==========================================
# B1.3: STORE CLEANED DATA IN SQLITE
# ==========================================

print("\n========== B1.3 DATABASE OPERATIONS ==========")

if not DB_FILE.exists():
    raise FileNotFoundError(
        "Task A1 database not found: " + str(DB_FILE)
    )

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "Task A2 cleaned CSV not found: " + str(INPUT_FILE)
    )

df_input = pd.read_csv(INPUT_FILE)

required_columns = {
    "station", "date", "hour",
    "pm25", "pm10", "no2", "temperature_c"
}

if not required_columns.issubset(df_input.columns):
    raise ValueError("Required columns are missing from cleaned CSV.")

# Convert numeric columns
for column in ["pm25", "pm10", "no2", "temperature_c"]:
    df_input[column] = pd.to_numeric(
        df_input[column], errors="coerce"
    )

# Validate dates and hours
df_input["date"] = pd.to_datetime(
    df_input["date"], errors="coerce"
).dt.strftime("%Y-%m-%d")

df_input["hour"] = df_input["hour"].astype(str).str.strip()

df_input = df_input.dropna(
    subset=["station", "date", "hour"]
)

df_input["station"] = (
    df_input["station"].astype(str).str.strip().str.title()
)

# Keep valid PM2.5 readings
df_input = df_input[
    df_input["pm25"].isna()
    | ((df_input["pm25"] >= 0) & (df_input["pm25"] <= 999))
]

# Remove duplicate station/date/hour combinations
df_input = df_input.drop_duplicates(
    subset=["station", "date", "hour"],
    keep="first"
)

with sqlite3.connect(DB_FILE) as con:

    con.execute("PRAGMA foreign_keys=ON")

    # Read existing database schema
    station_columns = {
        row[1] for row in
        con.execute("PRAGMA table_info(stations)").fetchall()
    }

    reading_columns = {
        row[1] for row in
        con.execute("PRAGMA table_info(readings)").fetchall()
    }

    if not station_columns or not reading_columns:
        raise ValueError(
            "Expected stations and readings tables were not found."
        )

    # Insert stations
    station_names = [
        (name,) for name in df_input["station"].unique()
    ]

    if "temperature_unit" in station_columns:
        con.executemany("""
            INSERT OR IGNORE INTO stations
            (station_name, temperature_unit)
            VALUES (?, 'C')
        """, station_names)
    else:
        con.executemany("""
            INSERT OR IGNORE INTO stations (station_name)
            VALUES (?)
        """, station_names)

    station_map = dict(
        con.execute("""
            SELECT station_name, station_id
            FROM stations
        """).fetchall()
    )

    # Prepare database insertion
    payload = []

    for _, row in df_input.iterrows():

        payload.append((
            station_map[row["station"]],
            row["date"],
            row["hour"],
            None if pd.isna(row["pm25"]) else float(row["pm25"]),
            None if pd.isna(row["pm10"]) else float(row["pm10"]),
            None if pd.isna(row["no2"]) else float(row["no2"]),
            None if pd.isna(row["temperature_c"])
            else float(row["temperature_c"])
        ))

    insert_columns = [
        "station_id",
        "reading_date",
        "reading_hour",
        "pm25",
        "pm10",
        "no2",
        "temperature_c"
    ]

    # Include source_file if present in the existing schema
    if "source_file" in reading_columns:
        insert_columns.append("source_file")
        payload = [record + ("Task A2 cleaned data",) for record in payload]

    placeholders = ", ".join(["?"] * len(insert_columns))
    columns_sql = ", ".join(insert_columns)

    sql = f"""
        INSERT OR REPLACE INTO readings
        ({columns_sql})
        VALUES ({placeholders})
    """

    con.executemany(sql, payload)

    con.commit()

    print("Records inserted:", len(payload))

    # Query 1: October average PM2.5 at Adyar
    q1 = con.execute("""
        SELECT AVG(r.pm25)
        FROM readings r
        JOIN stations s USING(station_id)
        WHERE s.station_name = ?
        AND r.reading_date >= ?
        AND r.reading_date < ?
    """, ("Adyar", "2026-10-01", "2026-11-01")).fetchone()[0]

    print("\n1. October Average PM2.5 at Adyar:")
    print(q1)

    # Query 2: Daily average PM2.5 by station
    q2 = con.execute("""
        SELECT
            s.station_name,
            r.reading_date,
            AVG(r.pm25)
        FROM readings r
        JOIN stations s USING(station_id)
        WHERE r.pm25 IS NOT NULL
        GROUP BY s.station_name, r.reading_date
        ORDER BY AVG(r.pm25) DESC
    """).fetchall()

    print("\n2. Daily Average PM2.5 by Station:")
    for record in q2:
        print(record)

    # Query 3: Worst hours by average PM2.5
    q3 = con.execute("""
        SELECT reading_hour, AVG(pm25)
        FROM readings
        WHERE pm25 IS NOT NULL
        GROUP BY reading_hour
        ORDER BY AVG(pm25) DESC
    """).fetchall()

    print("\n3. Worst Hours by Average PM2.5:")
    for record in q3:
        print(record)

# ==========================================
# B1.4: DATA VISUALISATION
# ==========================================

print("\n========== B1.4 DATA VISUALISATION ==========")

with sqlite3.connect(DB_FILE) as con:

    df = pd.read_sql_query("""
        SELECT
            s.station_name AS station,
            r.reading_date AS day,
            r.reading_hour AS hour,
            r.pm25,
            r.temperature_c
        FROM readings r
        JOIN stations s USING(station_id)
        WHERE r.pm25 IS NOT NULL
    """, con)

if df.empty:
    print("No valid PM2.5 readings available for charts.")
else:

    # Convert date
    df["day"] = pd.to_datetime(df["day"], errors="coerce")
    df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")
    df["temperature_c"] = pd.to_numeric(
        df["temperature_c"], errors="coerce"
    )

    df = df.dropna(subset=["day", "pm25"])

    # --------------------------------------
    # CHART 1: DAILY PM2.5 TREND
    # --------------------------------------

    daily = (
        df.groupby(["day", "station"])["pm25"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(9, 5))

    for name, group in daily.groupby("station"):
        plt.plot(
            group["day"],
            group["pm25"],
            marker="o",
            label=name
        )

    plt.title("Daily Mean PM2.5 by Station")
    plt.xlabel("Date")
    plt.ylabel("Mean PM2.5 (µg/m³)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("B1_daily_pm25.png")
    plt.show()
    plt.close()

    # --------------------------------------
    # CHART 2: STATION COMPARISON
    # --------------------------------------

    df.groupby("station")["pm25"].mean().sort_values().plot(
        kind="bar", figsize=(8, 5)
    )

    plt.title("Mean PM2.5 by Station")
    plt.xlabel("Station")
    plt.ylabel("Mean PM2.5 (µg/m³)")
    plt.tight_layout()
    plt.savefig("B1_station_comparison.png")
    plt.show()
    plt.close()

    # --------------------------------------
    # CHART 3: TEMPERATURE VS PM2.5
    # --------------------------------------

    scatter_data = df.dropna(
        subset=["temperature_c", "pm25"]
    )

    plt.figure(figsize=(8, 5))

    plt.scatter(
        scatter_data["temperature_c"],
        scatter_data["pm25"],
        alpha=0.6
    )

    plt.title("Temperature vs PM2.5")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("PM2.5 (µg/m³)")
    plt.tight_layout()
    plt.savefig("B1_temperature_scatter.png")
    plt.show()
    plt.close()

    # --------------------------------------
    # CHART 4: HOURLY PM2.5
    # --------------------------------------

    df["hour_number"] = pd.to_datetime(
        df["hour"], format="%H:%M", errors="coerce"
    ).dt.hour

    hourly = (
        df.dropna(subset=["hour_number"])
        .groupby("hour_number")["pm25"]
        .mean()
        .sort_index()
    )

    hourly.plot(kind="bar", figsize=(8, 5))

    plt.title("Mean PM2.5 by Hour")
    plt.xlabel("Hour")
    plt.ylabel("Mean PM2.5 (µg/m³)")
    plt.tight_layout()
    plt.savefig("B1_hourly_pm25.png")
    plt.show()
    plt.close()

    print("All four charts generated successfully.")

# ==========================================
# ALTERNATIVE: CSV VS PANDAS BENCHMARK
# ==========================================

print("\n========== CSV VS PANDAS BENCHMARK ==========")

def csv_process(records):
    result = []

    for row in records:
        try:
            value = float(row["pm25"])

            if 0 <= value <= 999:
                result.append(value)

        except (ValueError, TypeError, KeyError):
            continue

    return result


def pandas_process(records):
    frame = pd.DataFrame(records)

    values = pd.to_numeric(
        frame["pm25"], errors="coerce"
    )

    return values[
        values.between(0, 999)
    ].tolist()


benchmark_results = []

for size in [1000, 100000, 1000000]:

    print(f"\nTesting {size:,} rows...")

    records = [
        {"pm25": str((i % 150) + 1)}
        for i in range(size)
    ]

    csv_times = []
    pandas_times = []

    csv_memory = []
    pandas_memory = []

    for trial in range(5):

        tracemalloc.start()
        start = time.perf_counter()
        csv_process(records)
        csv_times.append(time.perf_counter() - start)
        _, peak = tracemalloc.get_traced_memory()
        csv_memory.append(peak / (1024 * 1024))
        tracemalloc.stop()

        tracemalloc.start()
        start = time.perf_counter()
        pandas_process(records)
        pandas_times.append(time.perf_counter() - start)
        _, peak = tracemalloc.get_traced_memory()
        pandas_memory.append(peak / (1024 * 1024))
        tracemalloc.stop()

    csv_median = statistics.median(csv_times)
    pandas_median = statistics.median(pandas_times)

    csv_mem_median = statistics.median(csv_memory)
    pandas_mem_median = statistics.median(pandas_memory)

    benchmark_results.append({
        "Rows": size,
        "CSV time (s)": round(csv_median, 6),
        "Pandas time (s)": round(pandas_median, 6),
        "CSV peak memory (MB)": round(csv_mem_median, 3),
        "Pandas peak memory (MB)": round(pandas_mem_median, 3)
    })

benchmark_df = pd.DataFrame(benchmark_results)

print("\nBENCHMARK RESULTS:")
print(benchmark_df.to_string(index=False))

benchmark_df.to_csv(
    "B1_benchmark_results.csv",
    index=False
)

# ==========================================
# COMPLETION
# ==========================================

print("\n==========================================")
print("TASK B1 COMPLETED SUCCESSFULLY!")
print("==========================================")

print("\nGenerated files:")
print("1. B1_daily_pm25.png")
print("2. B1_station_comparison.png")
print("3. B1_temperature_scatter.png")
print("4. B1_hourly_pm25.png")
print("5. B1_benchmark_results.csv")
