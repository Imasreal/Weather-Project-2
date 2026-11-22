import time
from datetime import datetime, timedelta, timezone
from database import initialize, save_collection, log_event
from weather_api import get_weather
from config import COLLECTION_INTERVAL_MINUTES, COLLECTION_DAYS

def main():
    initialize()
    end_time = datetime.now(timezone.utc) + timedelta(days=COLLECTION_DAYS)
    interval = COLLECTION_INTERVAL_MINUTES * 60
    print(f"Starting collection for {COLLECTION_DAYS} days. Keep this program running.")
    while datetime.now(timezone.utc) < end_time:
        started = time.monotonic()
        try:
            actual, forecasts, lat, lon = get_weather()
            save_collection(actual, forecasts)
            msg = f"Saved current conditions and {len(forecasts)} forecast hours; location={lat},{lon}"
            log_event("SUCCESS", msg)
            print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}")
        except Exception as exc:
            log_event("ERROR", str(exc))
            print(f"Collection error: {exc}")
        elapsed = time.monotonic() - started
        time.sleep(max(0, interval - elapsed))
    print("Three-day collection window finished.")

if __name__ == "__main__":
    main()
