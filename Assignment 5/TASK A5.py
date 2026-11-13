import sqlite3
import re
from pathlib import Path
from datetime import date
from collections import Counter
# ---------------------------------------
# TASK A5: AI APPLICATION FOR CITIZEN COMPLAINTS
# ---------------------------------------
DB_FILE = Path("TASK A1/air_quality.db")
# ---------------------------------------
# A5.1: SENTIMENT ANALYSIS
# ---------------------------------------
POSITIVE_WORDS = {
    "good", "excellent", "clean", "improved", "better",
    "safe", "helpful", "resolved", "satisfied", "happy",
    "efficient", "thankful", "wonderful"
}
NEGATIVE_WORDS = {
    "bad", "poor", "dirty", "polluted", "unhealthy",
    "dangerous", "problem", "issue", "delay", "worst",
    "unresolved", "complaint", "unacceptable", "harmful",
    "smoke", "dust", "toxic"
}
NEGATORS = {"not", "never", "no"}
STOP_WORDS = {
    "the", "is", "a", "an", "and", "or", "but", "to",
    "of", "in", "on", "at", "for", "with", "this",
    "that", "it", "was", "were", "are", "am", "i",
    "we", "they", "he", "she", "my", "our", "their",
    "has", "have", "had", "be", "been", "being",
    "from", "as", "by", "very", "too", "there",
    "here", "after", "before", "because"
}
def tokenize(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())
def analyse_sentiment(complaint):
    words = tokenize(complaint)
    score = 0
    for i, word in enumerate(words):
        if word in POSITIVE_WORDS:
            word_score = 1
        elif word in NEGATIVE_WORDS:
            word_score = -1
        else:
            continue
        if i > 0 and words[i - 1] in NEGATORS:
            word_score *= -1
        score += word_score
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return score, sentiment
# ---------------------------------------
# A5.1: EXTRACTIVE TEXT SUMMARISATION
# ---------------------------------------
def summarise_complaints(complaints, top_k=3):
    sentences = []
    for complaint in complaints:
        parts = re.split(r"(?<=[.!?])\s+", complaint.strip())
        for sentence in parts:
            if sentence.strip():
                sentences.append(sentence.strip())
    if not sentences:
        return []
    words = []
    for sentence in sentences:
        tokens = tokenize(sentence)
        important_words = [
            word for word in tokens
            if word not in STOP_WORDS
        ]
        words.extend(important_words)
    frequency = Counter(words)
    sentence_scores = []
    for index, sentence in enumerate(sentences):
        tokens = tokenize(sentence)
        score = sum(
            frequency[word]
            for word in tokens
            if word not in STOP_WORDS
        )
        sentence_scores.append((index, score, sentence))
    top_sentences = sorted(
        sentence_scores,
        key=lambda item: item[1],
        reverse=True
    )[:top_k]
    # Preserve original sentence order
    top_sentences.sort(key=lambda item: item[0])
    return [item[2] for item in top_sentences]
# ---------------------------------------
# A5.2: RULE-BASED CITIZEN CHATBOT
# ---------------------------------------
def get_pm25(station_name):
    if not DB_FILE.exists():
        return "Database not found. Run Task A1 first."
    today = date.today().isoformat()
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AVG(r.pm25), COUNT(r.pm25)
                FROM readings AS r
                JOIN stations AS s
                ON r.station_id = s.station_id
                WHERE LOWER(s.station_name) = LOWER(?)
                AND r.reading_date = ?
            """, (station_name, today))
            result = cursor.fetchone()
            average_pm25, reading_count = result
            if reading_count == 0:
                return (
                    f"No PM2.5 readings are available for "
                    f"{station_name} today ({today})."
                )
            return (
                f"Station: {station_name}\n"
                f"Date: {today}\n"
                f"Average PM2.5: {average_pm25:.2f} µg/m³\n"
                f"Valid readings: {reading_count}"
            )
    except sqlite3.Error as error:
        return f"Database error: {error}"
def chatbot(question):
    question = question.lower().strip()
    # Detect PM2.5 intent
    if "pm2.5" not in question and "pm25" not in question:
        return (
            "Sorry, I can currently answer questions "
            "about PM2.5 levels only."
        )
    # Detect station name
    station_names = ["adyar"]
    station_found = None
    for station in station_names:
        if station in question:
            station_found = station
            break
    if station_found is None:
        return "Please specify a supported station, such as Adyar."
    # Resolve today
    if "today" not in question:
        return "Please specify the date. Currently, I support today's readings."
    return get_pm25(station_found.title())
# ---------------------------------------
# MAIN PROGRAM
# ---------------------------------------
print("\n==========================================")
print(" CITIZEN COMPLAINT ANALYSIS SYSTEM")
print("==========================================")
# ---------------------------------------
# COLLECT CITIZEN COMPLAINTS
# ---------------------------------------
complaints = []
print("\nEnter citizen complaints.")
print("Press Enter on an empty line to finish.")
while True:
    complaint = input("\nEnter complaint: ").strip()
    if complaint == "":
        break
    complaints.append(complaint)
# ---------------------------------------
# DISPLAY SENTIMENT RESULTS
# ---------------------------------------
print("\n========== SENTIMENT ANALYSIS ==========")
for index, complaint in enumerate(complaints, start=1):
    score, sentiment = analyse_sentiment(complaint)
    print(f"\nComplaint {index}: {complaint}")
    print(f"Sentiment Score: {score}")
    print(f"Sentiment: {sentiment}")
# ---------------------------------------
# DISPLAY EXTRACTIVE SUMMARY
# ---------------------------------------
print("\n========== COMPLAINT SUMMARY ==========")
summary = summarise_complaints(complaints, top_k=3)
if summary:
    for index, sentence in enumerate(summary, start=1):
        print(f"{index}. {sentence}")
else:
    print("No complaints available for summarisation.")
# ---------------------------------------
# CHATBOT INTERACTION
# ---------------------------------------
print("\n========== CITIZEN CHATBOT ==========")
print("Example: What is the PM2.5 in Adyar today?")
print("Type 'exit' to stop the chatbot.")
while True:
    question = input("\nYou: ").strip()
    if question.lower() == "exit":
        print("Chatbot: Thank you for using the service.")
        break
    response = chatbot(question)
    print("\nChatbot:", response)
# ---------------------------------------
# COMPLETION
# ---------------------------------------
print("\n==========================================")
print("TASK A5 COMPLETED SUCCESSFULLY!")
print("==========================================")
