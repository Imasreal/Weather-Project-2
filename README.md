# Seri Iskandar Weather Monitoring IoT Project

This starter implementation retrieves weather data from Open-Meteo, stores current-condition snapshots and forecast snapshots in SQLite, and displays them in a Streamlit dashboard.

## 1. Requirements
- Python 3.10 or newer
- Internet connection
- Keep the computer running during the 72-hour collection period

## 2. Install
Open a terminal in this folder and run:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Start the 3-day collector
```bash
python collector.py
```
The default interval is 60 minutes and duration is 3 days. Edit `config.py` to change the interval. Do not close the terminal or shut down the computer during collection. For a real deployment, run it on a reliable always-on computer/server and add restart monitoring.

## 4. Start the dashboard
Open a second terminal in the same folder, activate the environment, then run:

```bash
streamlit run dashboard.py
```

Streamlit will display a local URL. The dashboard reads the same `weather.db` file created by the collector.

## 5. Database tables
- `actual_weather`: current-condition snapshots with timestamps.
- `forecast_weather`: forecast values, forecast issue time and valid time.
- `collection_log`: successful and failed collection attempts.

## 6. Important interpretation / limitation
The Open-Meteo `current` endpoint returns current weather conditions from a numerical weather model; it is not a physical weather-station sensor reading. Therefore, call these values "current model-based conditions" in the report. The assignment asks for observed-versus-forecast comparison. Explain this data-source limitation honestly. For independent ground-truth observations, connect a physical weather station or a suitable verified observation source. Do not describe model-based values as sensor measurements.

This starter app stores each forecast snapshot with its issue time so forecast history is preserved. The simple dashboard comparison matches records by hour; inspect the matching logic and dataset before reporting results. Forecast accuracy is more meaningful when comparing forecasts made before the valid time against an independent observation at that valid time.

## 7. Before submission
- Run for at least 72 continuous hours.
- Check that the database contains records from the full period.
- Export screenshots of the dashboard.
- Verify forecast/actual matching and calculate MAE (and optionally RMSE).
- Replace all illustrative report text with your actual results.
- Add citations in IEEE style.
- Remove the virtual environment and unnecessary generated files before zipping source code.
