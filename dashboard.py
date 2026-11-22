import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from config import DATABASE

st.set_page_config(page_title="Seri Iskandar Weather", page_icon="🌦️", layout="wide")
st.title("🌦️ Seri Iskandar Weather Monitoring")
st.caption("Weather data acquisition, history and forecast analysis | Seri Iskandar, Perak")

@st.cache_data(ttl=60)
def load_data():
    con = sqlite3.connect(DATABASE)
    try:
        actual = pd.read_sql_query("SELECT * FROM actual_weather ORDER BY observed_at", con)
        forecast = pd.read_sql_query("SELECT * FROM forecast_weather ORDER BY valid_time", con)
        logs = pd.read_sql_query("SELECT * FROM collection_log ORDER BY collected_at DESC", con)
    finally:
        con.close()
    return actual, forecast, logs

actual, forecast, logs = load_data()
if actual.empty:
    st.warning("No data collected yet. Start the collector with: python collector.py")
    st.stop()

actual["observed_at"] = pd.to_datetime(actual["observed_at"])
for col in ["temperature", "humidity", "rainfall", "wind_speed"]:
    actual[col] = pd.to_numeric(actual[col], errors="coerce")

latest = actual.iloc[-1]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Temperature", f'{latest["temperature"]:.1f} °C' if pd.notna(latest["temperature"]) else "N/A")
c2.metric("Humidity", f'{latest["humidity"]:.0f} %' if pd.notna(latest["humidity"]) else "N/A")
c3.metric("Precipitation", f'{latest["rainfall"]:.1f} mm' if pd.notna(latest["rainfall"]) else "N/A")
c4.metric("Wind speed", f'{latest["wind_speed"]:.1f} km/h' if pd.notna(latest["wind_speed"]) else "N/A")

st.subheader("Historical weather")
parameter = st.selectbox("Choose a parameter", ["temperature", "humidity", "rainfall", "wind_speed"])
labels = {"temperature":"Temperature (°C)", "humidity":"Relative humidity (%)",
          "rainfall":"Precipitation (mm)", "wind_speed":"Wind speed (km/h)"}
fig = px.line(actual, x="observed_at", y=parameter, markers=True,
              labels={"observed_at":"Time", parameter:labels[parameter]},
              title=labels[parameter] + " over time")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Forecast records")
if not forecast.empty:
    forecast["valid_time"] = pd.to_datetime(forecast["valid_time"])
    forecast["issued_at"] = pd.to_datetime(forecast["issued_at"], utc=True)
    fc_param = st.selectbox("Forecast parameter", ["temperature", "humidity", "rainfall", "wind_speed"])
    ffig = px.line(forecast.sort_values("valid_time"), x="valid_time", y=fc_param,
                   color=forecast["issued_at"].astype(str),
                   labels={"valid_time":"Forecast valid time", fc_param:labels[fc_param],
                           "color":"Forecast issue time"},
                   title="Stored forecast snapshots")
    st.plotly_chart(ffig, use_container_width=True)
else:
    st.info("Forecast records will appear after collection.")

st.subheader("Forecast versus actual evaluation")
st.caption("The comparison below matches the latest stored forecast for each valid hour to the nearest available current-condition record in that same hour.")
if not forecast.empty:
    # Use the latest forecast snapshot per valid hour, then match actual values by hourly timestamp.
    f = forecast.copy()
    f["valid_hour"] = f["valid_time"].dt.floor("h")
    f = f.sort_values("issued_at").drop_duplicates("valid_hour", keep="last")
    a = actual.copy()
    a["valid_hour"] = a["observed_at"].dt.floor("h")
    merged = pd.merge(f, a, on="valid_hour", suffixes=("_forecast", "_actual"))
    if not merged.empty:
        metric = st.selectbox("Metric for error calculation",
                              ["temperature", "humidity", "rainfall", "wind_speed"],
                              key="error_metric")
        merged["absolute_error"] = (merged[f"{metric}_forecast"] - merged[f"{metric}_actual"]).abs()
        merged = merged.dropna(subset=["absolute_error"])
        if not merged.empty:
            mae = merged["absolute_error"].mean()
            st.metric("Mean Absolute Error (MAE)", f"{mae:.2f}")
            st.dataframe(merged[["valid_hour", f"{metric}_forecast", f"{metric}_actual", "absolute_error"]],
                         use_container_width=True)
        else:
            st.info("Not enough matched, non-missing records to calculate error yet.")
    else:
        st.info("No matching forecast and actual hourly records yet. Continue collecting data.")
else:
    st.info("Forecast data is not available yet.")

st.subheader("Collection status")
st.write(f"Stored current-condition records: **{len(actual)}**")
st.write(f"Stored forecast records: **{len(forecast)}**")
if not logs.empty:
    st.dataframe(logs.head(10), use_container_width=True)
st.caption("Important: Open-Meteo's current conditions are model-based estimates, not measurements from a physical weather station. State this limitation in your report.")
