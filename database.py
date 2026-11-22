import sqlite3
from config import DATABASE

def connect():
    return sqlite3.connect(DATABASE)

def initialize():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS actual_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            observed_at TEXT NOT NULL UNIQUE,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            wind_speed REAL,
            source TEXT
        )""")
        con.execute("""
        CREATE TABLE IF NOT EXISTS forecast_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issued_at TEXT NOT NULL,
            valid_time TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            wind_speed REAL,
            UNIQUE(issued_at, valid_time)
        )""")
        con.execute("""
        CREATE TABLE IF NOT EXISTS collection_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collected_at TEXT NOT NULL,
            status TEXT NOT NULL,
            message TEXT
        )""")

def save_collection(actual, forecasts):
    with connect() as con:
        con.execute("""
        INSERT OR IGNORE INTO actual_weather
        (observed_at, temperature, humidity, rainfall, wind_speed, source)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (actual["observed_at"], actual["temperature"], actual["humidity"],
              actual["rainfall"], actual["wind_speed"], actual["source"]))
        con.executemany("""
        INSERT OR IGNORE INTO forecast_weather
        (issued_at, valid_time, temperature, humidity, rainfall, wind_speed)
        VALUES (:issued_at, :valid_time, :temperature, :humidity, :rainfall, :wind_speed)
        """, forecasts)

def log_event(status, message):
    from datetime import datetime, timezone
    with connect() as con:
        con.execute(
            "INSERT INTO collection_log (collected_at, status, message) VALUES (?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), status, message)
        )
