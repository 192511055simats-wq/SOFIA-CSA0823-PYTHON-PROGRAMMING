import time
import io
# Method 1: Repeated +=
def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text
# Method 2: Using join()
def build_join(parts):
    return ";".join(parts) + ";"
# Method 3: Using f-string
def build_fstring(parts):
    return "".join(f"{p};" for p in parts)
# Benchmark function
def measure(function, items):
    total_time = 0

    for i in range(3):
        start = time.perf_counter()
        result = function(items)
        end = time.perf_counter()

        total_time += end - start

    return result, total_time / 3
# Test different input sizes
for size in [1000, 10000, 200000]:

    items = [f"Item{i}:Rs{i % 50}" for i in range(size)]

    print("\nNumber of lines:", size)

    a, t1 = measure(build_plus, items)
    b, t2 = measure(build_join, items)
    c, t3 = measure(build_fstring, items)

    print("All methods produce same text:", a == b == c)

    print(f"Plus time:    {t1:.6f} seconds")
    print(f"Join time:    {t2:.6f} seconds")
    print(f"F-string time:{t3:.6f} seconds")