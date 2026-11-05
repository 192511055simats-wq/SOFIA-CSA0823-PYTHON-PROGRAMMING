import time

# Original method: repeated concatenation
def build_original(items):
    text = ""

    for item in items:
        text += item + ";"

    return text


# Redesigned method: list and join
def build_redesigned(items):
    parts = []

    for item in items:
        parts.append(item + ";")

    return "".join(parts)


# Function to measure average execution time
def measure(function, items):
    total_time = 0

    for i in range(3):
        start = time.perf_counter()
        result = function(items)
        end = time.perf_counter()

        total_time += end - start

    average = total_time / 3

    return result, average


# Test with different input sizes
sizes = [1000, 10000, 200000]

for size in sizes:

    items = [f"Item{i}:Rs{i % 50}" for i in range(size)]

    print("\nNumber of lines:", size)

    # Original method
    original_result, original_time = measure(
        build_original, items
    )

    # Redesigned method
    new_result, new_time = measure(
        build_redesigned, items
    )

    # Validate results
    print("Same output:", original_result == new_result)

    print("Original time:   {:.6f} seconds".format(original_time))
    print("Redesigned time: {:.6f} seconds".format(new_time))

    if new_time > 0:
        improvement = original_time / new_time
        print("Speed improvement: {:.2f} times".format(improvement))