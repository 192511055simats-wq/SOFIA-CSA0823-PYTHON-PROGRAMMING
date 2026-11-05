from functools import lru_cache
import sys
calls = 0
# Method 1: Normal recursion
def ways_naive(n):
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_naive(n - 1) + ways_naive(n - 2)
# Method 2: Memoisation
@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_memo(n - 1) + ways_memo(n - 2)
# Method 3: Iteration
def ways_loop(n):
    if n <= 1:
        return 1

    a = 1
    b = 1

    for i in range(2, n + 1):
        a, b = b, a + b

    return b
# User input
n = int(input("Enter number of temple steps: "))
if n < 0:
    print("Please enter a non-negative number.")
else:
    print("\n--- Normal Recursion ---")
    if n <= 30:
        calls = 0
        result = ways_naive(n)
        print("Number of ways:", result)
        print("Function calls:", calls)
    else:
        print("Skipped for large input because it is very slow.")
    print("\n--- Memoisation ---")
    ways_memo.cache_clear()
    calls = 0
    try:
        result = ways_memo(n)
        print("Number of ways:", result)
        print("Function calls:", calls)
    except RecursionError:
        print("RecursionError: Maximum recursion depth exceeded.")

    print("\n--- Iteration ---")

    result = ways_loop(n)
    print("Number of ways:", result)