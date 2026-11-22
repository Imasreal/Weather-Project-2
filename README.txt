# Seri Iskandar Weather Dashboard

A responsive static website built with plain HTML, CSS and JavaScript. It does not require Python packages, Streamlit, Plotly or Pandas.

## Run locally
1. Extract the ZIP.
2. Open `index.html` in Chrome or Edge.
3. Select start and end dates.
4. Click **Generate API URL**, then **Load data**.
   - Alternatively, upload `historical_weather.csv` created by your Python data collection script.
5. The page displays summary metrics, four charts and an hourly records table.

## Publish it and get a URL with GitHub Pages
1. Sign in to GitHub and create a new public repository, e.g. `seri-iskandar-weather`.
2. Upload `index.html` to the repository root.
3. Open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select branch `main` and folder `/ (root)`, then click **Save**.
6. Wait for deployment. GitHub will show a public website URL in the Pages section.

## Notes
- The page queries the Open-Meteo Historical Weather API from the browser. If the browser/network blocks the request, use the CSV upload option.
- Data are Open-Meteo historical/reanalysis estimates, not direct measurements from a local weather station.
- The website currently displays historical weather, not archived forecast accuracy.
