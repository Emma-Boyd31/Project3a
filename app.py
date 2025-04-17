from flask import Flask, render_template, request, flash
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import os

matplotlib.use('Agg')  
app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_KEY = "YOUR_ALPHA_VANTAGE_KEY"  # Replace this with your real key

def load_symbols():
    df = pd.read_csv("stocks.csv")  # Put your CSV in the project root
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

    plt.figure(figsize=(10, 4))
    if chart_type == "line":
        plt.plot(df["4. close"], label="Close Price")
    else:
        df["4. close"].plot(kind="bar")
    plt.title(f"{symbol} Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
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

        if end_date < start_date:
            flash("End date must be after start date.")
            return render_template("index.html", symbols=symbols)

        try:
            chart_path = get_chart(symbol, chart_type, time_series, start_date, end_date)
            return render_template("result.html", chart=chart_path)
        except Exception as e:
            flash(f"Error: {e}")
            return render_template("index.html", symbols=symbols)

    return render_template("index.html", symbols=symbols)

if __name__ == '__main__':
    app.run(debug=True, port=5019)