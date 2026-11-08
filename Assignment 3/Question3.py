import re
import random
import time
from collections import Counter
# Sample complaints
calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received"
]
# Words to ignore
STOP = {"not", "high"}
# Convert text into lowercase words
def words(text):
    return re.findall(r"[a-z]+", text.lower())
# Count word frequencies using dictionary
def frequencies(texts, stop):
    counts = {}

    for text in texts:
        for word in words(text):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1

    return counts
# Group complaints by district
def group_district(records):
    grouped = {}
    for district, complaint in records:
        grouped.setdefault(district, []).append(complaint)
    return grouped
# Find top k words
def top(counts, k):
    return sorted(
        counts.items(),
        key=lambda x: (-x[1], x[0])
    )[:k]
# Count words using list.count()
def list_count(texts, stop):
    all_words = [
        word
        for text in texts
        for word in words(text)
        if word not in stop
    ]
    return {
        word: all_words.count(word)
        for word in set(all_words)
    }
# Display results
print("Top 3 words:", top(frequencies(calls, STOP), 3))
print(
    "District complaints:",
    group_district([
        ("Chennai", "seed delay"),
        ("Madurai", "water issue")
    ])
)
print("Empty input:", frequencies([""], STOP))
print(
    "Case and punctuation:",
    frequencies(["SEEDS, seeds! Price."], STOP)
)
# Performance comparison
vocab = [
    "seeds", "fertiliser", "price",
    "subsidy", "water", "pest", "delayed"
]

for n in (1000, 10000, 100000):

    data = [
        " ".join(random.choices(vocab, k=8))
        for _ in range(n)
    ]

    methods = [
        ("Dictionary", lambda: frequencies(data, STOP)),

        ("Counter", lambda: dict(
            Counter(
                word
                for text in data
                for word in words(text)
                if word not in STOP
            )
        )),

        ("List Count", lambda: list_count(data, STOP))
    ]

    print("\nNumber of complaints:", n)

    for name, fn in methods:
        start = time.perf_counter()

        fn()

        elapsed = time.perf_counter() - start

        print(name, "Time:", round(elapsed, 6), "seconds")