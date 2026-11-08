from collections import defaultdict
import time
import sys
# Railway timetable using nested dictionaries, lists, tuples and sets
timetable = {
    "12601": {
        "name": "Chennai Express",
        "stops": [
            ("Chennai", "06:00", "06:10"),
            ("Katpadi", "08:00", "08:05"),
            ("Bengaluru", "10:30", "10:40")
        ],
        "days": {"Mon", "Wed", "Fri"}
    },
    "12602": {
        "name": "Kaveri Express",
        "stops": [
            ("Chennai", "07:00", "07:15"),
            ("Salem", "11:00", "11:05"),
            ("Mysuru", "14:00", "14:10")
        ],
        "days": {"Tue", "Thu", "Sat"}
    },
    "12603": {
        "name": "Vaigai Express",
        "stops": [
            ("Chennai", "13:00", "13:10"),
            ("Madurai", "20:00", "20:05")
        ],
        "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}
    },
    "12604": {
        "name": "West Coast Express",
        "stops": [
            ("Chennai", "15:00", "15:10"),
            ("Katpadi", "17:00", "17:05"),
            ("Coimbatore", "21:00", "21:10")
        ],
        "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
    },
    "12605": {
        "name": "Pandian Express",
        "stops": [
            ("Chennai", "21:00", "21:10"),
            ("Tiruchirappalli", "04:00", "04:05"),
            ("Madurai", "06:00", "06:10")
        ],
        "days": {"Sun", "Mon", "Wed", "Fri"}
    }
}
# Build station index
def build_index(data):
    index = defaultdict(list)

    for train, record in data.items():
        for station, arrival, departure in record["stops"]:
            index[station].append((train, arrival, departure))

    return index
# Query using full timetable scan
def query_scan(data, station, day):
    found = []
    for train, record in data.items():
        if day in record["days"]:
            for stop, arrival, departure in record["stops"]:
                if stop == station:
                    found.append(
                        (departure, train, record["name"], arrival)
                    )
    return sorted(found, key=lambda x: x[0])
# Query using station index
def query_index(data, index, station, day):
    found = []
    for train, arrival, departure in index.get(station, []):
        if day in data[train]["days"]:
            found.append(
                (departure, train, data[train]["name"], arrival)
            )
    return sorted(found, key=lambda x: x[0])
# Display timetable and test queries
idx = build_index(timetable)
print("FULL SCAN:")
print(query_scan(timetable, "Chennai", "Mon"))
print("\nINDEXED QUERY:")
print(query_index(timetable, idx, "Chennai", "Mon"))
print("\nUNKNOWN STATION:")
print(query_index(timetable, idx, "Unknown", "Mon"))
print("\nTRAIN NOT RUNNING ON TUESDAY:")
print(query_index(timetable, idx, "Madurai", "Tue"))
print("\nCOMPLETE TIMETABLE:")
for train, record in timetable.items():
    print(train, record["name"])

    for station, arrival, departure in record["stops"]:
        print(station, arrival, departure)
# Generate synthetic timetable data
def synthetic(n):
    stations = [
        "Chennai", "Katpadi", "Salem",
        "Madurai", "Coimbatore"
    ]
    return {
        str(i): {
            "name": "Train " + str(i),
            "stops": [
                (station, "08:00", "08:05")
                for station in stations
            ],
            "days": {"Mon", "Wed", "Fri"}
        }
        for i in range(n)
    }
# Measure approximate index container memory
def index_memory_bytes(index):
    total = sys.getsizeof(index)
    for train_list in index.values():
        total += sys.getsizeof(train_list)
        for record in train_list:
            total += sys.getsizeof(record)
    return total
# Scaling benchmark
print("\nSCALING BENCHMARK")
print(
    "Trains | Full scan | Index build | Indexed query | Index memory (bytes)"
)
for n in (100, 1000, 10000):
    data = synthetic(n)
    start = time.perf_counter()
    query_scan(data, "Chennai", "Mon")
    scan = time.perf_counter() - start
    start = time.perf_counter()
    ix = build_index(data)
    build = time.perf_counter() - start
    start = time.perf_counter()
    query_index(data, ix, "Chennai", "Mon")
    indexed = time.perf_counter() - start
    memory = index_memory_bytes(ix)
    print(
        n,
        round(scan, 8),
        round(build, 8),
        round(indexed, 8),
        memory
    )
