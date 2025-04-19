from flask import Flask, render_template, request, flash
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_KEY = "DQS7RLXP4BNSGO70"

def load_symbols():
    df = pd.read_csv("stocks.csv")
    return sorted(df["Symbol"].dropna().unique().tolist())

def get_chart(symbol, chart_type, time_series, start_date, end_date):
    function_map = {
        "daily": "TIME_SERIES_DAILY",
        "weekly": "TIME_SERIES_WEEKLY",
        "monthly": "TIME_SERIES_MONTHLY"
    }

    function = function_map.get(time_series, "TIME_SERIES_DAILY")
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}&datatype=json&outputsize=full"
    
    response = requests.get(url)
    print("Alpha Vantage URL:", url)
    print("Raw response preview:", response.text[:500])

    data = response.json()

    key_map = {
        "TIME_SERIES_DAILY": "Time Series (Daily)",
        "TIME_SERIES_WEEKLY": "Weekly Time Series",
        "TIME_SERIES_MONTHLY": "Monthly Time Series"
    }

    series_key = key_map.get(function)
    if series_key not in data:
        raise ValueError("API returned unexpected data — check symbol, date, or API limit.")

    raw_df = pd.DataFrame.from_dict(data[series_key], orient="index")
    raw_df.index = pd.to_datetime(raw_df.index)
    df = raw_df.rename(columns=lambda col: col.split(". ")[1] if ". " in col else col)
    df = df.sort_index()
    df = df.loc[start_date:end_date]

    if df.empty:
        raise ValueError("No data available for the selected date range.")

    plt.figure(figsize=(12, 5))

    if chart_type == "bar":
        df_subset = df[["open", "high", "low", "close"]].astype(float)
        df_subset.plot(kind="bar")
        plt.legend(["Open", "High", "Low", "Close"])
    else:
        plt.plot(df["close"].astype(float), label="Close", color="blue")
        plt.legend()

    plt.title(f"{symbol} Stock Data ({time_series.title()})\n{start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.tight_layout()

    chart_path = os.path.join("static", "chart.png")
    plt.savefig(chart_path)
    plt.close()

    return chart_path

@app.route('/', methods=['GET', 'POST'])
def index():
    symbols = load_symbols()
    if request.method == 'POST':
        symbol = request.form.get("symbol")
        chart_type = request.form.get("chart_type")
        time_series = request.form.get("time_series")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if not all([symbol, chart_type, time_series, start_date, end_date]):
            flash("All fields are required.")
            return render_template("index.html", symbols=symbols)

        if symbol not in symbols:
            flash("Invalid stock symbol selected.")
            return render_template("index.html", symbols=symbols)

        if chart_type not in ['line', 'bar']:
            flash("Invalid chart type selected.")
            return render_template("index.html", symbols=symbols)

        if time_series not in ['daily', 'weekly', 'monthly']:
            flash("Invalid time series selected.")
            return render_template("index.html", symbols=symbols)

        try:
            start = pd.to_datetime(start_date)
        except:
            flash("Invalid start date.")
            return render_template("index.html", symbols=symbols)

        try:
            end = pd.to_datetime(end_date)
        except:
            flash("Invalid end date.")
            return render_template("index.html", symbols=symbols)

        if end < start:
            flash("End date must be after start date.")
            return render_template("index.html", symbols=symbols)

        try:
            chart_path = get_chart(symbol, chart_type, time_series, start_date, end_date)
            return render_template(
                "index.html",
                symbols=symbols,
                chart=chart_path,
                selected_symbol=symbol,
                selected_chart=chart_type,
                selected_series=time_series,
                selected_start=start_date,
                selected_end=end_date
            )
        except Exception as e:
            flash(f"Error generating chart: {e}")
            return render_template(
                "index.html",
                symbols=symbols,
                selected_symbol=symbol,
                selected_chart=chart_type,
                selected_series=time_series,
                selected_start=start_date,
                selected_end=end_date
            )

    return render_template("index.html", symbols=symbols)

if __name__ == '__main__':
    app.run(host="0.0.0.0")