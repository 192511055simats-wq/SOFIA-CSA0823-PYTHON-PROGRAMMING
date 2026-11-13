import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
# ---------------------------------------
# READ CLEANED DATA FROM TASK A2
# ---------------------------------------
INPUT_FILE = Path("../TASK A2/cleaned_readings.csv")
if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "Cleaned data not found. Run air_quality_cleaning.py first."
    )
df = pd.read_csv(INPUT_FILE)
# Validate required columns
required = {
    "station", "date", "hour", "pm25", "temperature_c"
}
if not required.issubset(df.columns):
    raise ValueError("Required columns are missing.")
# Convert columns into correct data types
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["hour"] = pd.to_datetime(
    df["hour"], format="%H:%M", errors="coerce"
).dt.hour
df["pm25"] = pd.to_numeric(
    df["pm25"], errors="coerce"
)
df["temperature_c"] = pd.to_numeric(
    df["temperature_c"], errors="coerce"
)
df = df.dropna(subset=["station", "date", "hour"])
# ---------------------------------------
# A3.2: DAILY SUMMARY FOR EACH STATION
# ---------------------------------------
df["reading_date"] = df["date"].dt.strftime("%Y-%m-%d")
daily_summary = (
    df.dropna(subset=["pm25"])
    .groupby(["station", "reading_date"])["pm25"]
    .agg(
        pm25_min="min",
        pm25_max="max",
        pm25_mean="mean",
        valid_reading_count="count"
    )
    .reset_index()
)
daily_summary["pm25_mean"] = daily_summary["pm25_mean"].round(2)
# Save daily summary as CSV
daily_summary.to_csv("daily_summary.csv", index=False)
# ---------------------------------------
# STORE DAILY SUMMARY IN SQLITE DATABASE
# ---------------------------------------
with sqlite3.connect("../TASK A1/air_quality.db") as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            station_name TEXT NOT NULL,
            reading_date TEXT NOT NULL,
            pm25_min REAL,
            pm25_max REAL,
            pm25_mean REAL,
            valid_reading_count INTEGER,
            PRIMARY KEY (station_name, reading_date)
        )
    """)
    conn.executemany("""
        INSERT OR REPLACE INTO daily_summary
        (station_name, reading_date, pm25_min, pm25_max,
         pm25_mean, valid_reading_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, daily_summary[
        ["station", "reading_date", "pm25_min", "pm25_max",
         "pm25_mean", "valid_reading_count"]
    ].itertuples(index=False, name=None))
# ---------------------------------------
# CHART 1: MONTHLY PM2.5 TREND
# Line chart
# ---------------------------------------
monthly_trend = (
    df.dropna(subset=["pm25"])
    .groupby(df["date"].dt.to_period("M"))["pm25"]
    .mean()
)
plt.figure(figsize=(9, 5))
plt.plot(
    monthly_trend.index.astype(str),
    monthly_trend.values,
    marker="o"
)
plt.title("Monthly Average PM2.5 Trend")
plt.xlabel("Month")
plt.ylabel("Average PM2.5")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart1_pm25_trend.png")
plt.show()
# ---------------------------------------
# CHART 2: STATION COMPARISON
# Bar chart
# ---------------------------------------
station_average = (
    df.dropna(subset=["pm25"])
    .groupby("station")["pm25"]
    .mean()
    .sort_values()
)
plt.figure(figsize=(8, 5))
station_average.plot(kind="bar")
plt.title("Average PM2.5 by Station")
plt.xlabel("Station")
plt.ylabel("Average PM2.5")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart2_station_comparison.png")
plt.show()
# ---------------------------------------
# CHART 3: TEMPERATURE VS PM2.5
# Scatter plot
# ---------------------------------------
scatter_data = df.dropna(
    subset=["temperature_c", "pm25"]
)
plt.figure(figsize=(8, 5))
plt.scatter(
    scatter_data["temperature_c"],
    scatter_data["pm25"]
)
plt.title("Temperature vs PM2.5")
plt.xlabel("Temperature (Celsius)")
plt.ylabel("PM2.5")
plt.tight_layout()
plt.savefig("chart3_temperature_pm25.png")
plt.show()
# ---------------------------------------
# CHART 4: WORST HOURS
# Bar chart
# ---------------------------------------
hour_average = (
    df.dropna(subset=["pm25"])
    .groupby("hour")["pm25"]
    .mean()
    .sort_values(ascending=False)
)
plt.figure(figsize=(8, 5))
hour_average.plot(kind="bar")
plt.title("Average PM2.5 by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Average PM2.5")
plt.tight_layout()
plt.savefig("chart4_worst_hours.png")
plt.show()
# ---------------------------------------
# DISPLAY RESULTS
# ---------------------------------------
print("\nDAILY SUMMARY")
print(daily_summary.to_string(index=False))
print("\nAVERAGE PM2.5 BY STATION")
print(station_average.round(2))
print("\nWORST HOURS")
print(hour_average.round(2))
print("\nTask A3 completed successfully!")
print("\nGenerated files:")
print("1. daily_summary.csv")
print("2. chart1_pm25_trend.png")
print("3. chart2_station_comparison.png")
print("4. chart3_temperature_pm25.png")
print("5. chart4_worst_hours.png")
print("6. daily_summary table in air_quality.db")
