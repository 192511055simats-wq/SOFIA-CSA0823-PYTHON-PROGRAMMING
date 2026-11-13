import csv
import io
import sqlite3
import statistics
import random
import time
import cProfile
import pstats
from datetime import date, timedelta
import pandas as pd
# =====================================================
# B3.1 - CORRECTNESS ON SMALL DATA
# =====================================================
print("\n========== B3.1 CORRECTNESS TEST ==========")
CSV_TEXT = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-01,52
Guindy,2026-10-01,95
Guindy,2026-10-02,121
"""
# Method 1: Python loops
groups = {}
for row in csv.DictReader(io.StringIO(CSV_TEXT)):
    key = (row["station"], row["date"])
    groups.setdefault(key, []).append(float(row["pm25"]))
loop_result = {
    key: statistics.mean(values)
    for key, values in groups.items()
}
# Method 2: Pandas
frame = pd.read_csv(io.StringIO(CSV_TEXT))
pandas_result = (
    frame.groupby(["station", "date"])["pm25"]
    .mean()
    .to_dict()
)
# Method 3: SQL
con = sqlite3.connect(":memory:")
con.execute("""
CREATE TABLE aq(
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")
small_rows = [
    (row["station"], row["date"], float(row["pm25"]))
    for row in csv.DictReader(io.StringIO(CSV_TEXT))
]
con.executemany(
    "INSERT INTO aq VALUES(?,?,?)",
    small_rows
)
sql_result = {
    (station, day): mean
    for station, day, mean in con.execute("""
        SELECT station, day, AVG(pm25)
        FROM aq
        GROUP BY station, day
    """)
}
con.close()
# Verify all three methods
for key in loop_result:
    assert abs(loop_result[key] - pandas_result[key]) < 1e-9
    assert abs(loop_result[key] - sql_result[key]) < 1e-9
print("Python loops:", loop_result)
print("Pandas:", pandas_result)
print("SQL:", sql_result)
print("All three methods agree.")
# =====================================================
# B3.2 - GENERATE AND BENCHMARK LARGER DATASETS
# =====================================================
print("\n========== B3.2 PERFORMANCE BENCHMARK ==========")
random.seed(42)
def generate_data(station_count):
    rows = []
    start_date = date(2026, 1, 1)
    for station_id in range(station_count):
        station_name = f"Station_{station_id + 1:03d}"
        for day_number in range(365):
            current_date = (
                start_date + timedelta(days=day_number)
            ).isoformat()
            for hour in range(24):
                pm25 = round(random.uniform(5, 180), 2)
                rows.append(
                    (station_name, current_date, hour, pm25)
                )
    return rows
# Method 1: Plain Python loops
def loop_method(rows):
    accumulator = {}
    for station, day, hour, value in rows:
        key = (station, day)
        total, count = accumulator.get(key, (0.0, 0))
        accumulator[key] = (total + value, count + 1)
    return {
        key: total / count
        for key, (total, count) in accumulator.items()
    }
# Method 2: Pandas groupby
def pandas_method(rows):
    df = pd.DataFrame(
        rows,
        columns=["station", "day", "hour", "pm25"]
    )
    return df.groupby(
        ["station", "day"]
    )["pm25"].mean()
# Method 3: SQLite GROUP BY
def sql_method(rows):
    connection = sqlite3.connect(":memory:")
    connection.execute("""
        CREATE TABLE aq(
            station TEXT,
            day TEXT,
            hour INTEGER,
            pm25 REAL
        )
    """)
    connection.executemany(
        "INSERT INTO aq VALUES(?,?,?,?)",
        rows
    )
    result = connection.execute("""
        SELECT station, day, AVG(pm25)
        FROM aq
        GROUP BY station, day
    """).fetchall()
    connection.close()
    return result
benchmark_results = []
for station_count in (1, 12, 120):
    print(f"\nTesting {station_count} station(s)...")
    data = generate_data(station_count)
    row_count = len(data)
    print("Total rows:", f"{row_count:,}")
    methods = [
        ("Loops", loop_method),
        ("Pandas", pandas_method),
        ("SQL", sql_method)
    ]
    method_times = {}
    for method_name, function in methods:
        samples = []
        for trial in range(3):
            start_time = time.perf_counter()
            function(data)
            elapsed = time.perf_counter() - start_time
            samples.append(elapsed)
        median_time = statistics.median(samples)
        method_times[method_name] = median_time
    fastest_method = min(
        method_times,
        key=method_times.get
    )
    print("Loops:", round(method_times["Loops"], 4), "seconds")
    print("Pandas:", round(method_times["Pandas"], 4), "seconds")
    print("SQL:", round(method_times["SQL"], 4), "seconds")
    print("Fastest:", fastest_method)
    benchmark_results.append({
        "Stations": station_count,
        "Approx Rows": row_count,
        "Loops (s)": round(method_times["Loops"], 4),
        "Pandas (s)": round(method_times["Pandas"], 4),
        "SQL (s)": round(method_times["SQL"], 4),
        "Fastest": fastest_method
    })
# Display benchmark table
print("\n========== BENCHMARK SUMMARY ==========")
results_frame = pd.DataFrame(benchmark_results)
print(results_frame.to_string(index=False))
results_frame.to_csv(
    "B3_benchmark_results.csv",
    index=False
)
print("\nBenchmark saved to B3_benchmark_results.csv")
# =====================================================
# B3.3 - PROFILE PLAIN PYTHON VERSION
# =====================================================
print("\n========== B3.3 CPROFILE REPORT ==========")
# Use the largest generated dataset (120 stations)
profiler = cProfile.Profile()
profiler.enable()
profile_result = loop_method(data)
profiler.disable()
stats = pstats.Stats(profiler)
stats.strip_dirs()
stats.sort_stats("cumulative")
stats.print_stats(15)
stats.dump_stats("B3_profile.prof")
print("Profile saved to B3_profile.prof")
# =====================================================
# B3.4 - ENGINEERING TRADE-OFF
# =====================================================
print("\n========== B3.4 ENGINEERING TRADE-OFF ==========")
print("""
1. Python loops:
   Suitable for streaming and low-dependency processing.
   A running-sum dictionary uses O(n) time and O(g) memory.
2. Pandas:
   Provides concise and convenient groupby operations.
   Suitable for one-time analysis when sufficient memory is available.
3. SQL:
   GROUP BY performs aggregation inside the database.
   Suitable for daily reports when readings are already stored in SQLite.
Selection:
   Use Python loops for streaming, Pandas for exploratory analysis,
   and SQL for recurring database reports.
The final choice should consider measured runtime, memory,
maintainability and operational requirements.
""")
print("\n========== B3 TESTING COMPLETED ==========")
