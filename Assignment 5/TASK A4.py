import csv
import logging
import time
import timeit
import cProfile
import pstats
from pathlib import Path
from collections import defaultdict
from pdb import set_trace
# ---------------------------------------
# TASK A4: DEBUGGING AND PROFILING
DATA_FILE = Path("TASK A2/cleaned_readings.csv")# ---------------------------------------

# Set True to activate an interactive debugger breakpoint
ENABLE_DEBUGGER = False
# ---------------------------------------
# LOGGING CONFIGURATION
# ---------------------------------------
logging.basicConfig(
    filename="air_quality_debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# ---------------------------------------
# FUNCTION 1: LOAD DATA
# ---------------------------------------
def load_data():
    if not DATA_FILE.exists():
        logging.error("Input file not found: %s", DATA_FILE)
        raise FileNotFoundError(DATA_FILE)
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    logging.info("Loaded %d records", len(data))
    return data
# ---------------------------------------
# FUNCTION 2: CLEAN AND VALIDATE DATA
# ---------------------------------------
def clean_data(data):
    cleaned = []
    rejected = []
    seen_keys = set()
    for row_number, row in enumerate(data, start=2):
        try:
            station = row["station"].strip()
            date = row["date"].strip()
            hour = row["hour"].strip()
            pm25_value = row["pm25"].strip()
            pm25 = float(pm25_value) if pm25_value else None
            assert station, "Station cannot be empty"
            assert date, "Date cannot be empty"
            assert hour, "Hour cannot be empty"
            assert pm25 is None or pm25 >= 0, "Negative PM2.5 value"
            key = (station, date, hour)
            assert key not in seen_keys, "Duplicate composite key"
            seen_keys.add(key)
            cleaned.append({
                "station": station,
                "date": date,
                "hour": hour,
                "pm25": pm25
            })
        except (ValueError, AssertionError, KeyError) as error:
            rejected.append(row)
            logging.warning(
                "Rejected row %d: %s",
                row_number,
                error
            )
    logging.info("Cleaned records: %d", len(cleaned))
    logging.warning("Rejected records: %d", len(rejected))
    return cleaned, rejected
# ---------------------------------------
# FUNCTION 3: ANALYSE DATA
# ---------------------------------------
def analyse_data(data):
    station_totals = defaultdict(float)
    station_counts = defaultdict(int)
    for row in data:
        if row["pm25"] is not None:
            station = row["station"]
            station_totals[station] += row["pm25"]
            station_counts[station] += 1
    averages = {}
    for station in station_totals:
        averages[station] = (
            station_totals[station] / station_counts[station]
        )
    logging.info("Analysis completed successfully")
    return averages
# ---------------------------------------
# A4.1: DEBUGGING USING PRINT AND ASSERT
# ---------------------------------------
print("\n========== DEBUGGING OUTPUT ==========")
data = load_data()
print("\nSample records:")
for row in data[:5]:
    print(row)
if data:
    print("\nPython data type:", type(data[0]))
    print("PM2.5 data type:", type(data[0]["pm25"]))
cleaned_data, rejected_data = clean_data(data)
# Development invariant checks
assert isinstance(cleaned_data, list)
assert len(cleaned_data) + len(rejected_data) == len(data)
print("\nAssertions passed successfully.")
print("Total records:", len(data))
print("Valid records:", len(cleaned_data))
print("Rejected records:", len(rejected_data))
# ---------------------------------------
# A4.1: PDB DEBUGGER
# ---------------------------------------
if ENABLE_DEBUGGER:
    print("\nStarting PDB debugger...")
    set_trace()
# ---------------------------------------
# A4.2: PROFILING USING PERF_COUNTER
# ---------------------------------------
print("\n========== TIME PROFILING ==========")
start_time = time.perf_counter()
data = load_data()
load_time = time.perf_counter() - start_time
start_time = time.perf_counter()
cleaned_data, rejected_data = clean_data(data)
clean_time = time.perf_counter() - start_time
start_time = time.perf_counter()
averages = analyse_data(cleaned_data)
analysis_time = time.perf_counter() - start_time
print(f"Data loading time: {load_time:.6f} seconds")
print(f"Data cleaning time: {clean_time:.6f} seconds")
print(f"Data analysis time: {analysis_time:.6f} seconds")
# ---------------------------------------
# A4.2: PROFILING USING TIMEIT
# ---------------------------------------
print("\n========== TIMEIT PROFILING ==========")
sample_values = [10, 20, 30, 40, 50]
def calculate_average():
    return sum(sample_values) / len(sample_values)
execution_time = timeit.timeit(
    calculate_average,
    number=10000
)
print("Operation: Calculate average")
print("Number of repetitions: 10000")
print(f"Total execution time: {execution_time:.6f} seconds")
print(
    f"Average execution time: "
    f"{execution_time / 10000:.10f} seconds"
)
# ---------------------------------------
# A4.2: PROFILING USING CPROFILE
# ---------------------------------------
print("\n========== CPROFILE OUTPUT ==========")
profiler = cProfile.Profile()
profiler.enable()
data = load_data()
cleaned_data, rejected_data = clean_data(data)
averages = analyse_data(cleaned_data)
profiler.disable()
profiler.dump_stats("air_quality_profile.prof")
stats = pstats.Stats(profiler)
stats.strip_dirs()
stats.sort_stats("cumulative")
stats.print_stats(10)
# ---------------------------------------
# DISPLAY ANALYSIS RESULTS
# ---------------------------------------
print("\n========== ANALYSIS RESULTS ==========")
for station, average in averages.items():
    print(f"{station}: {average:.2f}")
# ---------------------------------------
# SAVE PROFILING RESULTS
# ---------------------------------------
with open("profiling_results.txt", "w", encoding="utf-8") as file:
    file.write("AIR QUALITY - DEBUGGING AND PROFILING RESULTS\n")
    file.write("==============================================\n")
    file.write(f"Total records: {len(data)}\n")
    file.write(f"Valid records: {len(cleaned_data)}\n")
    file.write(f"Rejected records: {len(rejected_data)}\n")
    file.write(f"Data loading time: {load_time:.6f} seconds\n")
    file.write(f"Data cleaning time: {clean_time:.6f} seconds\n")
    file.write(f"Data analysis time: {analysis_time:.6f} seconds\n")
    file.write(f"Timeit total: {execution_time:.6f} seconds\n")
    file.write(
        f"Timeit average: {execution_time / 10000:.10f} seconds\n"
    )
print("\nTask A4 completed successfully!")
print("\nGenerated files:")
print("1. air_quality_debug.log")
print("2. air_quality_profile.prof")
print("3. profiling_results.txt")
