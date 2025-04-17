from flask import Flask, render_template, request, flash
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"  



def load_symbols():
    df = pd.read_csv("stocks.csv")
    return df["Symbol"].dropna().tolist()

def get_chart(symbol, chart_type, time_series, start_date, end_date):
    function_map = {
        "daily": "TIME_SERIES_DAILY_ADJUSTED",
        "weekly": "TIME_SERIES_WEEKLY",
        "monthly": "TIME_SERIES_MONTHLY"
    }

    url = f"https://www.alphavantage.co/query?function={function_map[time_series]}&symbol={symbol}&apikey={API_KEY}&outputsize=full"
    r = requests.get(url)
    data = r.json()

    key = next(k for k in data if "Time Series" in k)
    df = pd.DataFrame.from_dict(data[key], orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.loc[start_date:end_date]
    df = df.astype(float)

    if df.empty:
        raise ValueError("No data available for the selected date range.")


    plt.figure(figsize=(12, 5))
    if chart_type == "bar":
        df_subset = df[["1. open", "2. high", "3. low", "4. close"]]
        df_subset.plot(kind="bar", color=["red", "blue", "green", "gold"])
        plt.legend(["Open", "High", "Low", "Close"])
    else:
        plt.plot(df["4. close"], label="Close", color="blue")
        plt.legend()

    plt.title(f"Stock Data for {symbol}: {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Price")


    plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))

    plt.tight_layout()

    chart_path = os.path.join("static", "chart.png")
    plt.savefig(chart_path)
    plt.close()
    return "static/chart.png"


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

        if end_date < start_date:
            flash("End date must be after start date.")
            return render_template("index.html", symbols=symbols)

        try:
            chart_path = get_chart(symbol, chart_type, time_series, start_date, end_date)
            return render_template(
                "result.html",
                chart=chart_path,
                symbols=symbols,
                selected_symbol=symbol,
                selected_chart=chart_type,
                selected_series=time_series,
                selected_start=start_date,
                selected_end=end_date
            )
        except Exception as e:
            flash(f"Error generating chart: {e}")
            return render_template("index.html", symbols=symbols)

    return render_template("index.html", symbols=symbols)


if __name__ == '__main__':
    app.run(debug=True, port=5019)