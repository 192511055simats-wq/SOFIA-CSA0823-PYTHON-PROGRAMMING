import sqlite3
import re
import statistics
import time
import csv
from pathlib import Path
from collections import Counter
# =====================================================
# B4.1 - SENTIMENT ANALYSIS ON 50 COMPLAINTS
# =====================================================
print("\n========== B4.1 SENTIMENT ANALYSIS ==========")
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}
# 50 complaints with manually assigned labels
complaints = [
    ("The roads are clean and the bus was fast.", "positive"),
    ("The factory smoke makes the air bad.", "negative"),
    ("The staff were not helpful.", "negative"),
    ("Not bad, the service improved.", "positive"),
    ("The streets are dirty and the air is polluted.", "negative"),
    ("The bus service is good today.", "positive"),
    ("The roads are broken and dirty.", "negative"),
    ("The staff are helpful and the service is good.", "positive"),
    ("The factory releases smoke every morning.", "negative"),
    ("The transport service is slow.", "negative"),
    ("The air quality has improved.", "positive"),
    ("The roads are clean.", "positive"),
    ("The bus was not fast.", "negative"),
    ("The workers were rude.", "negative"),
    ("The service is not bad.", "positive"),
    ("There is heavy smoke near the school.", "negative"),
    ("The public transport is good.", "positive"),
    ("The road is broken and dirty.", "negative"),
    ("The staff were never helpful.", "negative"),
    ("The environment is clean and healthy.", "positive"),
    ("The bus service is slow and bad.", "negative"),
    ("The complaint was recorded yesterday.", "neutral"),
    ("The meeting will happen tomorrow.", "neutral"),
    ("The station is located near the market.", "neutral"),
    ("The report contains daily pollution readings.", "neutral"),
    ("The factory operates during the daytime.", "neutral"),
    ("The road connects two residential areas.", "neutral"),
    ("The survey was conducted last week.", "neutral"),
    ("The station recorded several readings.", "neutral"),
    ("The department received a new report.", "neutral"),
    ("The air is not clean.", "negative"),
    ("The service is not slow.", "positive"),
    ("The factory smoke is terrible.", "negative"),
    ("The roads are good and clean.", "positive"),
    ("The staff are rude and unhelpful.", "negative"),
    ("The air quality is bad near the factory.", "negative"),
    ("The bus service improved this month.", "positive"),
    ("The water supply is normal today.", "neutral"),
    ("The pollution report was submitted.", "neutral"),
    ("The traffic department held a meeting.", "neutral"),
    ("The bus was fast but the road was dirty.", "negative"),
    ("The service was not helpful yesterday.", "negative"),
    ("The air quality is good near the park.", "positive"),
    ("The factory has a new operating schedule.", "neutral"),
    ("The smoke problem has not improved.", "negative"),
    ("The roads are clean but the bus is slow.", "negative"),
    ("The staff were helpful during registration.", "positive"),
    ("The pollution readings were recorded hourly.", "neutral"),
    ("The bus was not bad today.", "positive"),
    ("The complaint concerns the factory location.", "neutral")
]
def score(text):
    words = re.findall(r"[a-z]+", text.lower())
    total = 0
    for index, word in enumerate(words):
        value = (
            1 if word in POSITIVE
            else -1 if word in NEGATIVE
            else 0
        )
        if index > 0 and words[index - 1] in NEGATORS:
            value = -value
        total += value
    return total
def predict_label(text):
    value = score(text)
    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    else:
        return "neutral"
# Evaluate all 50 complaints
correct = 0
mismatches = 0
labels = ["positive", "negative", "neutral"]
confusion = {
    actual: {predicted: 0 for predicted in labels}
    for actual in labels
}
results = []
for text, manual_label in complaints:
    predicted = predict_label(text)
    if predicted == manual_label:
        correct += 1
    else:
        mismatches += 1
    confusion[manual_label][predicted] += 1
    results.append({
        "Complaint": text,
        "Manual Label": manual_label,
        "Predicted Label": predicted,
        "Correct": predicted == manual_label
    })
agreement = (correct / len(complaints)) * 100
print("Total complaints:", len(complaints))
print("Correct predictions:", correct)
print("Mismatches:", mismatches)
print("Agreement:", round(agreement, 2), "%")
print("\nCONFUSION MATRIX")
print("Rows = Manual labels; Columns = Predicted labels")
print(f"{'Actual':<12}", end="")
for label in labels:
    print(f"{label:<12}", end="")
print()
for actual in labels:
    print(f"{actual:<12}", end="")

    for predicted in labels:
        print(f"{confusion[actual][predicted]:<12}", end="")

    print()
# Save individual complaint results
with open("B4_sentiment_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "Complaint",
            "Manual Label",
            "Predicted Label",
            "Correct"
        ]
    )
    writer.writeheader()
    writer.writerows(results)
# Display incorrectly classified complaints
print("\nMISCLASSIFIED COMPLAINTS")
for item in results:
    if not item["Correct"]:
        print("Complaint:", item["Complaint"])
        print("Manual label:", item["Manual Label"])
        print("Predicted label:", item["Predicted Label"])
        print()
# =====================================================
# B4.1 - COMPLAINT SUMMARISATION
# =====================================================
print("\n========== SUMMARISATION ==========")
def first_k_summary(texts, k=5):
    return texts[:k]
def frequency_summary(texts, k=5):
    word_frequency = Counter()
    stop_words = {
        "the", "is", "are", "was", "were", "and",
        "a", "an", "to", "of", "in", "on", "for",
        "near", "this", "that", "has", "have", "had"
    }
    for sentence in texts:
        words = re.findall(r"[a-z]+", sentence.lower())
        for word in words:
            if word not in stop_words:
                word_frequency[word] += 1
    sentence_scores = []
    for position, sentence in enumerate(texts):
        words = re.findall(r"[a-z]+", sentence.lower())
        sentence_score = sum(
            word_frequency[word]
            for word in words
        )
        sentence_scores.append(
            (sentence_score, position, sentence)
        )
    selected = sorted(
        sentence_scores,
        key=lambda item: item[0],
        reverse=True
    )[:k]
    selected.sort(key=lambda item: item[1])
    return [item[2] for item in selected]
complaint_texts = [item[0] for item in complaints]
first_summary = first_k_summary(complaint_texts)
frequency_based_summary = frequency_summary(complaint_texts)

print("\nFirst-K Summary:")

for sentence in first_summary:
    print("-", sentence)

print("\nFrequency-Based Summary:")

for sentence in frequency_based_summary:
    print("-", sentence)


# =====================================================
# B4.2 - SQLITE COMPOSITE INDEX BENCHMARK
# =====================================================

print("\n========== B4.2 DATABASE INDEX TEST ==========")

DB_FILE = Path("TASK A1/air_quality.db")
INDEX_NAME = "idx_readings_station_day"


def median_query_time(connection, query, parameters, trials=9):

    # Warm-up query
    connection.execute(query, parameters).fetchone()

    timings = []

    for _ in range(trials):

        start = time.perf_counter()

        connection.execute(
            query, parameters
        ).fetchone()

        elapsed = time.perf_counter() - start

        timings.append(elapsed * 1000)

    return statistics.median(timings)


if not DB_FILE.exists():

    print("Database not found:", DB_FILE)
    print("Complete Task A1 before running the index test.")

else:

    db = sqlite3.connect(str(DB_FILE))

    # Inspect actual readings table
    columns = {
        row[1]
        for row in db.execute("PRAGMA table_info(readings)")
    }

    required = {"station_id", "reading_date", "pm25"}

    if not required.issubset(columns):

        print("Required readings columns are missing.")
        print("Found columns:", columns)

    else:

        # Select a station and date range from actual database data
        sample = db.execute("""
            SELECT
                station_id,
                MIN(reading_date),
                MAX(reading_date)
            FROM readings
            WHERE pm25 IS NOT NULL
            GROUP BY station_id
            LIMIT 1
        """).fetchone()
        if sample is None:
            print("No readings available for index testing.")
        else:
            station_id, first_date, last_date = sample
            # Make upper date bound exclusive
            from datetime import datetime, timedelta
            last_date_exclusive = (
                datetime.strptime(last_date, "%Y-%m-%d")
                + timedelta(days=1)
            ).strftime("%Y-%m-%d")
            query = """
                SELECT AVG(pm25)
                FROM readings
                WHERE station_id = ?
                AND reading_date >= ?
                AND reading_date < ?
            """

            parameters = (
                station_id,
                first_date,
                last_date_exclusive
            )
            # Remove the target index for baseline measurement
            db.execute(
                f"DROP INDEX IF EXISTS {INDEX_NAME}"
            )
            db.commit()
            before_time = median_query_time(
                db, query, parameters
            )
            before_plan = db.execute(
                "EXPLAIN QUERY PLAN " + query,
                parameters
            ).fetchall()
            print("\nQuery:", "Station/date PM2.5 average")
            print("Station ID:", station_id)
            print("Date range:", first_date, "to", last_date)
            print("\nBefore index:")
            print("Median time:", round(before_time, 4), "ms")
            for row in before_plan:
                print(row)
            # Create composite index
            db.execute("""
                CREATE INDEX IF NOT EXISTS idx_readings_station_day
                ON readings(station_id, reading_date)
            """)
            db.commit()
            after_time = median_query_time(
                db, query, parameters
            )
            after_plan = db.execute(
                "EXPLAIN QUERY PLAN " + query,
                parameters
            ).fetchall()
            print("\nAfter index:")
            print("Median time:", round(after_time, 4), "ms")
            for row in after_plan:
                print(row)
            # Calculate percentage change
            if before_time > 0:
                change = (
                    (before_time - after_time) / before_time
                ) * 100
            else:
                change = 0
            print("\nINDEX PERFORMANCE SUMMARY")
            print("Before index:", round(before_time, 4), "ms")
            print("After index:", round(after_time, 4), "ms")
            print("Performance change:", round(change, 2), "%")
            plan_text = " ".join(
                str(row).upper()
                for row in after_plan
            )
            index_used = INDEX_NAME.upper() in plan_text
            print("Target index used:", "YES" if index_used else "NO")
            db.close()
# =====================================================
# B4.3 - PRODUCTION ENGINEERING DECISION
# =====================================================
print("\n========== B4.3 PRODUCTION DECISION ==========")
daily_readings = 100 * 96
yearly_readings = daily_readings * 365
print("Additional stations:", 100)
print("Readings per station per day:", 96)
print("Additional readings per day:", f"{daily_readings:,}")
print("Additional readings per year:", f"{yearly_readings:,}")
print("""
STORAGE:
Use SQLite for a single-user prototype.
Use PostgreSQL for multi-user production workloads.
CLEANING:
Validate incoming schemas, units and ranges.
Quarantine invalid records.
Convert temperatures to Celsius.
Deduplicate using station and timestamp.
Preserve raw values and cleaning flags.
ANALYSIS:
Use SQL aggregation for recurring daily reports.
Use Pandas for exploratory analysis.
Use Python loops for streaming and low-dependency processing.
AI:
Lexicon sentiment is transparent but has limitations.
Train and evaluate a contextual classifier using labelled data.
Compare precision, recall and F1-score.
Use human review for ambiguous complaints.
FINAL DECISION:
Choose based on measured performance, scalability,
data quality, maintainability and operational requirements.
""")
print("\n========== B4 TESTING COMPLETED ==========")
print("Sentiment results saved to B4_sentiment_results.csv")
