# Hotel Booking Data Analysis Dashboard

An interactive Streamlit dashboard analyzing 119,207 hotel bookings (2015–2017) across two properties — City Hotel and Resort Hotel — covering cancellation drivers, revenue patterns, guest behavior, and operations.

## Live App

Open the dashboard: *(add your Streamlit Cloud URL here)*

## What's Inside

- **Overview** — cancellation by hotel, customer types, top guest countries, length of stay, monthly bookings
- **Cancellation Drivers** — cancellation by month, deposit type vs. market segment, lead-time risk, booking changes, correlation heatmap
- **Revenue** — average daily rate trends, price vs. cancellation risk by segment
- **Guest Profile** — repeat vs. first-time guests, meal plan preferences, top clients per hotel
- **Operations** — booking outcomes, distribution channels, room-type mismatch, yearly booking volume

Every chart is filterable by hotel and arrival year using the sidebar.

## Data Pipeline

1. Raw CSV (119,390 rows) imported into MySQL via `LOAD DATA LOCAL INFILE`
2. Cleaned in SQL: removed 1 exact duplicate, 1 negative-price row, 180 zero-guest bookings, and 1 extreme price outlier — 119,207 clean rows remain
3. Connected live to Python (Jupyter) via `mysql-connector-python` for analysis
4. Exported to `hotel_booking.csv` and rebuilt as this Streamlit app

## Key Findings

- Cancellation tracks guest commitment (lead time, special requests, booking changes) far more than price
- "Non Refund" deposit bookings cancel at 99.4% — concentrated in Group bookings via travel agents
- City Hotel drives more volume; Resort Hotel converts a higher share of bookings into completed stays
- 82% of all bookings come through the TA/TO (travel agent) channel
- Repeat guests are only 3.1% of bookings but cancel at less than half the rate of first-timers

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack

Python, Streamlit, pandas, matplotlib, seaborn, MySQL
