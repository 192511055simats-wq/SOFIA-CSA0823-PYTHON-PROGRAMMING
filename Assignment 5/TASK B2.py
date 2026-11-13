
import csv
import sqlite3
import logging
from pathlib import Path
from io import StringIO

# -------------------------------
# LOGGING SETUP
# -------------------------------

logging.basicConfig(
    filename="B2_adversarial.log",
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    force=True
)

# -------------------------------
# B2.1 ADVERSARIAL FILE TESTS
# -------------------------------

required_columns = {"station", "day", "pm25"}

def test_file(filename, content, encoding="utf-8"):
    print(f"\nTesting: {filename}")

    try:
        data = content.encode(encoding)

        if len(data) == 0:
            raise ValueError("Empty file: no data or header")

        decoded = data.decode("utf-8")

        sample = decoded[:2048]
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = ","

        reader = csv.DictReader(StringIO(decoded), delimiter=delimiter)

        if not reader.fieldnames:
            raise ValueError("Missing header")

        columns = set(reader.fieldnames)

        if not required_columns.issubset(columns):
            raise ValueError(
                f"Schema error or wrong delimiter. Found columns: {reader.fieldnames}"
            )

        rows = list(reader)
        print(f"PASS: {len(rows)} records loaded")
        logging.info("%s: accepted (%d records)", filename, len(rows))

    except UnicodeDecodeError:
        message = "Encoding error: unable to decode as UTF-8"
        print("REJECTED:", message)
        logging.error("%s: %s; quarantined", filename, message)

    except Exception as error:
        print("REJECTED:", error)
        logging.error("%s: %s; quarantined", filename, error)


print("========== B2.1 ADVERSARIAL FILE TESTS ==========")

test_file(
    "missing_column.csv",
    "station,day\nAdyar,2026-10-01"
)

test_file(
    "wrong_delimiter.csv",
    "station;day;pm25\nAdyar;2026-10-01;48"
)

test_file(
    "different_encoding.csv",
    "station,day,pm25\nAdyar,2026-10-01,48",
    encoding="utf-16"
)

test_file(
    "empty_file.csv",
    ""
)

# -------------------------------
# B2.2 SQL INJECTION TEST
# -------------------------------

print("\n========== B2.2 SQL INJECTION TEST ==========")

readings = [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0),
    ("Guindy", "2026-10-03", 121.0),
    ("Adyar", "2026-10-04", 60.0)
]

con = sqlite3.connect(":memory:")

con.execute(
    "CREATE TABLE aq(station TEXT, day TEXT, pm25 REAL)"
)

con.executemany(
    "INSERT INTO aq VALUES(?,?,?)",
    readings
)

con.commit()


def station_average(name):
    row = con.execute(
        "SELECT AVG(pm25) FROM aq WHERE station=?",
        (name,)
    ).fetchone()

    return row[0]


print("Adyar average:", station_average("Adyar"))
print("Guindy average:", station_average("Guindy"))

injection = "Adyar' OR '1'='1"

print("Injection attempt:", injection)
print("Injection result:", station_average(injection))

# Demonstrate unsafe SQL construction without executing it
unsafe_query = (
    "SELECT AVG(pm25) FROM aq WHERE station='"
    + injection + "'"
)

print("\nUnsafe SQL construction:")
print(unsafe_query)

logging.info("Parameterized SQL injection test completed safely")

# -------------------------------
# B2.3 EXECUTEMANY VS EXECUTE LOOP
# -------------------------------

print("\n========== B2.3 INSERT COMPARISON ==========")

con.execute(
    "CREATE TABLE test_batch(station TEXT, pm25 REAL)"
)

# executemany()
con.executemany(
    "INSERT INTO test_batch VALUES(?,?)",
    readings_for_batch := [
        ("Adyar", 48.0),
        ("Guindy", 95.0),
        ("Adyar", 60.0)
    ]
)

print("executemany() inserted:", len(readings_for_batch), "records")

# execute() in a loop
con.execute(
    "CREATE TABLE test_loop(station TEXT, pm25 REAL)"
)

for record in readings_for_batch:
    con.execute(
        "INSERT INTO test_loop VALUES(?,?)",
        record
    )

print("execute() loop inserted:", len(readings_for_batch), "records")

batch_count = con.execute(
    "SELECT COUNT(*) FROM test_batch"
).fetchone()[0]

loop_count = con.execute(
    "SELECT COUNT(*) FROM test_loop"
).fetchone()[0]

print("Batch table records:", batch_count)
print("Loop table records:", loop_count)

con.close()

print("\n========== B2 TESTING COMPLETED ==========")
print("Check B2_adversarial.log for error details.")
